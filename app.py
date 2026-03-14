import streamlit as st
import pandas as pd
import subprocess
import tempfile
import json
import os

st.title("GTSummary Table Generator")

file = st.file_uploader("Upload Excel or CSV", type=["xlsx","csv"])

if file:

    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.subheader("Preview")
    st.dataframe(df.head())

    variables = st.multiselect("Select variables", df.columns)

    datatype = {}

    if variables:

        st.subheader("Select variable type")

        for v in variables:

            datatype[v] = st.selectbox(
                f"{v}",
                ["continuous","categorical"],
                key=v
            )

    if st.button("Generate Table"):

        temp_dir = tempfile.mkdtemp()

        data_path = os.path.join(temp_dir,"data.csv")
        json_path = os.path.join(temp_dir,"vars.json")
        output_doc = os.path.join(temp_dir,"table.docx")

        df.to_csv(data_path,index=False)

        config = {
            "variables":variables,
            "types":[datatype[v] for v in variables]
        }

        with open(json_path,"w") as f:
            json.dump(config,f)

        cmd = [
            "Rscript",
            "gtsummary_script.R",
            data_path,
            json_path,
            output_doc
        ]

        subprocess.run(cmd)

        st.success("Table Created")

        with open(output_doc,"rb") as f:

            st.download_button(
                "Download Word Table",
                f,
                "gtsummary_table.docx"
            )
