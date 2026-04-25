# CP8: Easy Run Instructions

Run the CP8 files in this exact order. Each file creates the data needed by the next file.

## Before You Start

Make sure this file exists:

```text
data/raw/LinkedIn_Scrape_full_5865.xlsx
```

If R says a package is missing, install it once using:

```r
install.packages(c(
  "readr", "readxl", "dplyr", "stringr", "tidyr", "tibble",
  "purrr", "tidytext", "text2vec", "Matrix", "caret",
  "glmnet", "xgboost", "class"
))
```

## Step 1: Run Data Preparation

Open:

```text
cp8/datapreparation.rmd
```

Click **Knit** or **Run All**.

This creates:

```text
data/processed/linkedin_full_5865_prepared.csv
cp8/datapreparation.html
```

## Step 2: Run Data Preprocessing

Open:

```text
cp8/datapreprocessing.rmd
```

Click **Knit** or **Run All**.

This creates:

```text
data/processed/linkedin_full_5865_preprocessed.csv
cp8/datapreprocessing.html
```

## Step 3: Run Model Input Encoding

Open:

```text
cp8/model_input_encoding.rmd
```

Click **Knit** or **Run All**.

This creates:

```text
data/processed/linkedin_full_5865_tfidf.rds
data/processed/linkedin_full_5865_multilabel_targets.csv
data/processed/train_validation_test_split.rds
cp8/model_input_encoding.html
```

## Step 4: Run Modeling

Open:

```text
cp8/modeling.rmd
```

Click **Knit** or **Run All**.

This creates:

```text
data/processed/cp8_model_results.rds
cp8/modeling.html
```

## Important Notes

- Always run the files in order: preparation, preprocessing, encoding, modeling.
- If you change an earlier file, rerun all files after it.
- Running a file again will replace its old output files.
- `modeling.rmd` takes the longest because it trains several models.
- Open the `.html` files in `cp8/` to review the final reports.
