# CP8 5k-Profile Pipeline

This folder contains the 5k-profile workflow grouped by pipeline stage.

## Folder Structure

- `data_preparation/`
  - `datapreparation_5k.rmd`
  - `datapreparation_5k.html`
- `data_preprocessing/`
  - `datapreprocessing_5k.rmd`
  - `datapreprocessing_5k.html`
- `feature_encoding/`
  - `model_input_encoding_5k.rmd`
  - `model_input_encoding_5k.html`
- `models/`
  - `modeling_5k.rmd`
  - `modeling_5k.html`
  - `baseline_frequency_prior/`
  - `logistic_regression/`
  - `knn/`
  - `xgboost/`
- `evaluation/`
  - `KSB621_CP8_Model_Evaluation_5k.docx`
- `results/`
  - `5k_model_results_summary.csv`
  - `5k_model_results_summary.md`
  - `model_outputs/`

## Run Order

1. `data_preparation/datapreparation_5k.rmd`
2. `data_preprocessing/datapreprocessing_5k.rmd`
3. `feature_encoding/model_input_encoding_5k.rmd`
4. `models/modeling_5k.rmd` or the individual notebooks under `models/`
5. Review `results/5k_model_results_summary.md`

## Notes

- The notebooks now live under `cp8/5kdata`, but they still read from `data/raw/` and write shared outputs to `data/processed/`, `models/`, and `results/`.
- The individual model notebooks save outputs under `data/processed/5k_model_outputs/`.
- Copies of the current 5k model outputs are included under `results/model_outputs/`.
- The comparison notebook `cp8/dataset_comparison_5k_vs_500.rmd` stays outside this folder because it compares both datasets.
