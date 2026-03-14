args <- commandArgs(trailingOnly=TRUE)

data_path <- args[1]
json_path <- args[2]
output_doc <- args[3]

library(gtsummary)
library(flextable)
library(dplyr)
library(readr)
library(jsonlite)
library(officer)

data <- read_csv(data_path)

config <- fromJSON(json_path)

vars <- config$variables
types <- config$types

data2 <- data %>% select(all_of(vars))

type_list <- list()

for(i in seq_along(vars)){
  
  if(types[i]=="continuous"){
    type_list[[vars[i]]] <- "continuous"
  } else {
    type_list[[vars[i]]] <- "categorical"
  }
}

tbl <- data2 %>%
tbl_summary(type = type_list)

ft <- as_flex_table(tbl)

ft <- fontsize(ft,size=11)
ft <- font(ft,fontname="Calibri")

save_as_docx(ft,path=output_doc)