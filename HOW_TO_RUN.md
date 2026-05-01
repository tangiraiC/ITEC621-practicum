# How to Run the Skills Extraction Pipeline

This guide shows the simple run order for the KSB621 Skills Extraction project:

```text
data -> preparation -> preprocessing -> model encoding -> modeling -> external validation -> Shiny app
```

## 1. Open the Project

Open this folder in RStudio:

```text
practictum/
```

Set the working directory to the project root. In RStudio, this is usually:

```r
setwd("/Users/fibonacci/Documents/practictum")
```

## 2. Install Required Packages

Run this once:

```r
install.packages(c(
  "readr",
  "readxl",
  "dplyr",
  "tidyr",
  "stringr",
  "purrr",
  "tibble",
  "ggplot2",
  "tidytext",
  "text2vec",
  "Matrix",
  "caret",
  "glmnet",
  "xgboost",
  "class",
  "scales",
  "forcats",
  "shiny"
))
```

## 3. Check the Input Files

Make sure these files exist:

```text
data/raw/LinkedIn_Scrape_full_5865.xlsx
data/raw/LinkedIn_Scrape_full_5865_Skills_List.csv
data/externalvalidation/alumnivalidation.xlsx
```

## 4. Run the Pipeline

Run these commands in RStudio, in this order:

```r
rmarkdown::render("cleaningScripts/join_external_validation.Rmd")
rmarkdown::render("cp8/datapreparation.rmd")
rmarkdown::render("cp8/datapreprocessing.rmd")
rmarkdown::render("cp8/model_input_encoding.rmd")
rmarkdown::render("cp8/modeling.rmd")
rmarkdown::render("cp8/external_validation_modeling.rmd")
rmarkdown::render("cp8/skills_extraction_eda.rmd")
```

## 5. Check the Main Outputs

The important output files are:

```text
cp8/modeling.html
cp8/external_validation_modeling.html
cp8/skills_extraction_eda.html
data/processed/5k_model_outputs/
data/processed/external_validation_model_outputs/
```

## 6. Run the Shiny App

The Shiny app uses the saved model files in:

```text
shiny_demo/models/
```

Run:

```r
shiny::runApp("shiny_demo")
```

The app lets a user paste profile/job text and returns predicted skills with confidence percentages.

## Simple Rerun Rule

If you change the data, rerun the whole pipeline.

If you only want to demo the final app and the model files already exist, just run:

```r
shiny::runApp("shiny_demo")
```
