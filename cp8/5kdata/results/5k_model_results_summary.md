# 5k Dataset Model Results Summary

This file summarizes the test-set performance for the 5k-profile modeling
pipeline.

| Model | Split | Precision Micro | Recall Micro | F1 Micro | Precision Macro | Recall Macro | F1 Macro |
|---|---|---:|---:|---:|---:|---:|---:|
| Baseline Frequency Prior | Test | 0.114 | 1.000 | 0.204 | 0.114 | 1.000 | 0.201 |
| Logistic Regression | Test | 0.115 | 0.971 | 0.206 | 0.122 | 0.966 | 0.203 |
| KNN | Test | 0.150 | 0.283 | 0.196 | 0.131 | 0.249 | 0.171 |
| XGBoost | Test | 0.196 | 0.525 | 0.285 | 0.209 | 0.477 | 0.273 |

## Best Model

The best model on the 5k-profile dataset is **XGBoost** based on test micro F1.

XGBoost has the strongest balance of precision and recall among the tested
models, with a test micro F1 score of **0.285**.

## Notes

- The baseline frequency prior and logistic regression models had very high
  recall, but much lower precision.
- KNN was more conservative than the baseline and logistic regression models,
  but had lower test micro F1.
- XGBoost had the highest test micro F1 and macro F1 among the available 5k
  model outputs.

The CSV version of this table is saved as:

```text
cp8/5kdata/results/5k_model_results_summary.csv
```
