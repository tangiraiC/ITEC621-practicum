# CP8 500-Profile Pipeline

This folder contains the 500-profile workflow grouped by pipeline stage.

## Folder Structure

- `data_preparation/`
  - `datapreparation_500.rmd`
  - `datapreparation_500.html`
- `data_preprocessing/`
  - `datapreprocessing_500.rmd`
  - `datapreprocessing_500.html`
- `feature_encoding/`
  - `model_input_encoding_500.rmd`
  - `model_input_encoding_500.html`
- `models/`
  - `modeling_500.rmd`
  - `modeling_500.html`
  - `glmnet/`
  - `logistic_regression/`
  - `knn/`
  - `xgboost/`
- `evaluation/`
  - `KSB621_CP8_Model_Evaluation_500.rmd`
  - `KSB621_CP8_Model_Evaluation_500.html`
- `results/`
  - `500_model_results_summary.csv`
  - `500_model_results_summary.md`

## Run Order

1. `data_preparation/datapreparation_500.rmd`
2. `data_preprocessing/datapreprocessing_500.rmd`
3. `feature_encoding/model_input_encoding_500.rmd`
4. `models/modeling_500.rmd` or the individual notebooks under `models/`
5. `evaluation/KSB621_CP8_Model_Evaluation_500.rmd`

## Notes

- The notebooks now live under `cp8/500data`, but they still read from `data/raw/` and write shared outputs to `data/processed/`, `models/`, and `results/`.
- The individual model notebooks save outputs under `data/processed/500_model_outputs/`.
- The comparison notebook `cp8/dataset_comparison_5k_vs_500.rmd` stays outside this folder because it compares both datasets.
