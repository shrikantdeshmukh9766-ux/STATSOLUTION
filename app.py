import streamlit as st
import pandas as pd
import tempfile
import rpy2.robjects as ro

from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import default_converter


st.title("GTSummary Table Generator")

# Upload dataset
file = st.file_uploader("Upload Excel or CSV", type=["xlsx","csv"])

if file:

    # read file
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.subheader("Data Preview")
    st.dataframe(df.head())

    # select variables
    variables = st.multiselect("Select Variables", df.columns)

    datatype = {}

    if variables:

        st.subheader("Select Variable Type")

        for v in variables:

            datatype[v] = st.selectbox(
                f"{v}",
                ["continuous","categorical"],
                key=v
            )

    if st.button("Generate Table"):

        # convert pandas → R dataframe
        with localconverter(default_converter + pandas2ri.converter):
            r_df = ro.conversion.py2rpy(df)

        ro.globalenv["data_py"] = r_df
        ro.globalenv["var_list"] = ro.StrVector(variables)

        types = [datatype[v] for v in variables]
        ro.globalenv["type_list"] = ro.StrVector(types)

        # temp file for word output
        temp_doc = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        ro.globalenv["outfile"] = temp_doc.name

        # R code
        ro.r('''
        library(gtsummary)
        library(flextable)
        library(dplyr)
        library(officer)

        data <- data_py

        vars <- var_list
        types <- type_list

        data2 <- data %>% select(all_of(vars))

        type_formula <- list()

        for(i in seq_along(vars)){
            if(types[i] == "continuous"){
                type_formula[[vars[i]]] <- "continuous"
            } else {
                type_formula[[vars[i]]] <- "categorical"
            }
        }

        tbl <- data2 %>%
        tbl_summary(type = type_formula)

        ft <- as_flex_table(tbl)

        ft <- fontsize(ft, size = 11)
        ft <- font(ft, fontname = "Calibri")

        save_as_docx(ft, path = outfile)
        ''')

        st.success("Table Created Successfully")

        with open(temp_doc.name, "rb") as f:

            st.download_button(
                "Download Table (Word)",
                f,
                file_name="gtsummary_table.docx"
            )
