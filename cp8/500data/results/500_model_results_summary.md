# 500 Dataset Model Results Summary

This file summarizes the test-set performance for the 500-profile modeling
pipeline.

| Model | Split | Precision Micro | Recall Micro | F1 Micro | Macro F1 | Subset Accuracy |
|---|---|---:|---:|---:|---:|---:|
| GLMNET | Test | 0.000 | 0.000 | 0.000 | 0.000 | 0.206 |
| Logistic Regression | Test | 0.000 | 0.000 | 0.000 | 0.000 | 0.206 |
| KNN | Test | 0.269 | 0.036 | 0.064 | 0.034 | 0.206 |
| XGBoost | Test | 0.292 | 0.072 | 0.116 | 0.063 | 0.118 |

## Best Model

The best model on the 500-profile dataset is **XGBoost** based on test micro F1.

XGBoost has the strongest balance of precision and recall among the tested
models, with a test micro F1 score of **0.116**.

## Notes

- GLMNET and Logistic Regression predicted no positive skill labels at the
  default 0.50 threshold.
- KNN predicted some positive labels but had low recall.
- XGBoost performed best, but the 500 dataset is small, so performance is limited
  compared with the 5k dataset.

The CSV version of this table is saved as:

```text
cp8/500data/results/500_model_results_summary.csv
```
