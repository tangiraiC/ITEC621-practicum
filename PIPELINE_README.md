# KSB621 Skills Extraction Pipeline

This README explains how to run the full KSB621 Skills Extraction pipeline from
raw/cleaned LinkedIn data through modeling, external validation, EDA, and the
local Shiny demo.

The project goal is:

```text
LinkedIn profile text -> TF-IDF features -> skill prediction models -> predicted skills
```

## Project Folders

```text
practictum/
  cleaningScripts/
    join_external_validation.Rmd
  cp8/
    datapreparation.rmd
    datapreprocessing.rmd
    model_input_encoding.rmd
    modeling.rmd
    external_validation_modeling.rmd
    skills_extraction_eda.rmd
  data/
    raw/
    externalvalidation/
    processed/
  results/
    skills_extraction_eda_5k_external/
  shiny_demo/
    app.R
    README.md
    models/
```

## Required R Packages

Install these packages once before running the pipeline:

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

## Required Input Files

Make sure these files exist before running the full pipeline:

```text
data/raw/LinkedIn_Scrape_full_5865.xlsx
data/raw/LinkedIn_Scrape_full_5865_Skills_List.csv
data/externalvalidation/alumnivalidation.xlsx
```

The external validation Excel file should contain the alumni and LinkedIn sheets
used by `cleaningScripts/join_external_validation.Rmd`.

## Recommended Run Order

Run the files in this exact order. Each step creates outputs needed by later
steps.

## 1. Join External Validation Sheets

Run:

```r
rmarkdown::render("cleaningScripts/join_external_validation.Rmd")
```

This joins the KSB alumni and LinkedIn external validation sheets using `Index`.

Main output:

```text
data/externalvalidation/ksb_alumni_linkedin_joined.csv
cleaningScripts/join_external_validation.html
```

## 2. Prepare Data

Run:

```r
rmarkdown::render("cp8/datapreparation.rmd")
```

This prepares the 5k LinkedIn training dataset and the joined KSB alumni
external validation dataset.

Important note: external validation rows with blank `Skills` are kept as
zero-skill examples.

Main outputs:

```text
data/processed/linkedin_full_5865_prepared.csv
data/processed/ksb_alumni_linkedin_prepared.csv
cp8/datapreparation.html
```

## 3. Preprocess Data

Run:

```r
rmarkdown::render("cp8/datapreprocessing.rmd")
```

This cleans text fields, standardizes categories, creates `profile_text`, parses
skills, and counts skills per profile.

Main outputs:

```text
data/processed/linkedin_full_5865_preprocessed.csv
data/processed/ksb_alumni_linkedin_preprocessed.csv
cp8/datapreprocessing.html
```

## 4. Encode Model Inputs

Run:

```r
rmarkdown::render("cp8/model_input_encoding.rmd")
```

This creates:

- TF-IDF text features from `profile_text`
- Multi-label skill target matrices
- Train/validation/test splits for the 5k dataset
- External validation TF-IDF inputs using the same vocabulary

Main outputs:

```text
data/processed/linkedin_full_5865_tfidf.rds
data/processed/linkedin_full_5865_multilabel_targets.csv
data/processed/train_validation_test_split.rds
data/processed/ksb_alumni_linkedin_tfidf.rds
data/processed/ksb_alumni_linkedin_multilabel_targets.csv
data/processed/ksb_alumni_linkedin_encoded_profiles.csv
cp8/model_input_encoding.html
```

## 5. Train and Evaluate 5k Models

Run:

```r
rmarkdown::render("cp8/modeling.rmd")
```

This trains and compares the main skill extraction models on the 5k dataset.

Models include:

- Baseline Frequency Prior
- Logistic Regression
- KNN
- XGBoost

Main outputs include:

```text
data/processed/5k_model_outputs/
data/processed/cp8_model_results.rds
cp8/modeling.html
```

If your current workflow uses the 5k model notebooks under `cp8/5kdata/`, run
those model files before external validation so the saved model outputs are
available in:

```text
data/processed/5k_model_outputs/
```

## 6. Run External Validation Models

Run:

```r
rmarkdown::render("cp8/external_validation_modeling.rmd")
```

This loads the saved 5k models and evaluates them on the KSB alumni external
validation dataset.

Main outputs:

```text
data/processed/external_validation_model_outputs/
data/processed/external_validation_model_outputs/external_validation_model_metrics.csv
data/processed/external_validation_model_outputs/external_validation_prediction_summary.csv
cp8/external_validation_modeling.html
```

## 7. Run EDA

Run:

```r
rmarkdown::render("cp8/skills_extraction_eda.rmd")
```

This creates a detailed EDA comparing:

- 5k training dataset
- KSB alumni external validation dataset

It summarizes:

- Dataset dimensions
- Total skill assignments
- Unique skills
- Skills per profile
- Zero-skill profiles
- Text availability
- Skill overlap
- TF-IDF sparsity
- Skill co-occurrence
- Train-vs-external drift
- Model-readiness risks

Main outputs:

```text
cp8/skills_extraction_eda.html
results/skills_extraction_eda_5k_external/
```

## 8. Run the Shiny Demo

Run:

```r
shiny::runApp("shiny_demo")
```

The app demonstrates:

```text
profile fields -> cleaned profile_text -> TF-IDF features -> XGBoost model -> predicted skills
```

The demo uses these files:

```text
shiny_demo/models/final_model.rds
shiny_demo/models/tfidf_vectorizer.rds
shiny_demo/models/retained_skills.rds
```

See the Shiny-specific README:

```text
shiny_demo/README.md
```

## One-Command Full Pipeline

From the project root, you can run the main pipeline with:

```r
rmarkdown::render("cleaningScripts/join_external_validation.Rmd")
rmarkdown::render("cp8/datapreparation.rmd")
rmarkdown::render("cp8/datapreprocessing.rmd")
rmarkdown::render("cp8/model_input_encoding.rmd")
rmarkdown::render("cp8/modeling.rmd")
rmarkdown::render("cp8/external_validation_modeling.rmd")
rmarkdown::render("cp8/skills_extraction_eda.rmd")
```

Run the Shiny demo separately:

```r
shiny::runApp("shiny_demo")
```

## When to Rerun Earlier Steps

Use this rule:

- If you change raw data or joined external validation data, rerun everything.
- If you change preparation, rerun preprocessing, encoding, modeling, external
  validation, and EDA.
- If you change preprocessing, rerun encoding, modeling, external validation,
  and EDA.
- If you change model encoding, rerun modeling, external validation, and EDA.
- If you change saved models, rerun external validation and update the Shiny
  model files if needed.

## Expected Final Outputs

After the full pipeline runs, the most important review files are:

```text
cp8/datapreparation.html
cp8/datapreprocessing.html
cp8/model_input_encoding.html
cp8/modeling.html
cp8/external_validation_modeling.html
cp8/skills_extraction_eda.html
data/processed/external_validation_model_outputs/external_validation_model_metrics.csv
shiny_demo/app.R
```

## Troubleshooting

If a package is missing, install it with:

```r
install.packages("package_name")
```

If a file is missing, check that the required raw data files exist in:

```text
data/raw/
data/externalvalidation/
```

If external validation fails, rerun:

```r
rmarkdown::render("cleaningScripts/join_external_validation.Rmd")
rmarkdown::render("cp8/datapreparation.rmd")
rmarkdown::render("cp8/datapreprocessing.rmd")
rmarkdown::render("cp8/model_input_encoding.rmd")
rmarkdown::render("cp8/external_validation_modeling.rmd")
```

If the Shiny app says model files are missing, confirm these files exist:

```text
shiny_demo/models/final_model.rds
shiny_demo/models/tfidf_vectorizer.rds
shiny_demo/models/retained_skills.rds
```
