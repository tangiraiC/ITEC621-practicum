# Model Variables Explained

This file explains the main variables used when running the CP8 modeling files,
especially the 5k model notebooks in `cp8/5k_model_notebooks/`.

## Input Data Objects

### `split_objects`

`split_objects` is the main saved R object loaded from:

```text
data/processed/train_validation_test_split.rds
```

It contains the train, validation, and test data needed by the model notebooks.
The object is a list with feature matrices, target matrices, profile metadata,
and skill labels.

### `X_train`

`X_train` is the training feature matrix.

Each row is one LinkedIn profile. Each column is a TF-IDF text feature created
from the profile text. The model learns from this matrix.

### `X_validation`

`X_validation` is the validation feature matrix.

It has the same columns as `X_train`, but contains profiles held out from
training. It is used to tune thresholds and compare model performance before the
final test check.

### `X_test`

`X_test` is the final test feature matrix.

It is used after training and validation to estimate how well the model performs
on unseen data.

## Target Variables

### `y_train`

`y_train` is the training target matrix.

Each row matches one profile in `X_train`. Each column is one skill label. A
value of `1` means the profile has that skill, and `0` means it does not.

### `y_validation`

`y_validation` is the validation target matrix.

It is used to evaluate validation predictions and tune model thresholds.

### `y_test`

`y_test` is the final test target matrix.

It is used to evaluate final model performance.

### `retained_skills`

`retained_skills` is the list of skill names kept for modeling.

The full dataset contains many skill labels, so the modeling workflow keeps the
most common labels. In the 5k workflow, the model notebooks use the top 25
skills by training-set prevalence.

### `max_model_labels`

`max_model_labels` controls how many skill labels are modeled.

In the 5k model notebooks:

```r
max_model_labels <- 25
```

This keeps the model runs practical while still comparing the most common skill
labels.

## Model-Specific Variables

### Baseline Frequency Prior

### `skill_prevalence`

`skill_prevalence` stores the proportion of training profiles that have each
skill.

The baseline model uses this value as the predicted probability for every
profile.

### `baseline_probs_validation`

`baseline_probs_validation` contains baseline predicted probabilities for the
validation set.

Each skill gets the same probability for every profile, based only on training
prevalence.

### `baseline_probs_test`

`baseline_probs_test` contains baseline predicted probabilities for the test
set.

### Logistic Regression

### `logit_models`

`logit_models` is a list of one-vs-rest logistic regression models.

There is one model per skill label. Each model predicts whether a profile has
one specific skill.

### `logit_validation_probs`

`logit_validation_probs` contains predicted skill probabilities for the
validation set from the logistic regression models.

### `logit_test_probs`

`logit_test_probs` contains predicted skill probabilities for the test set from
the logistic regression models.

### KNN

### `knn_feature_count`

`knn_feature_count` controls how many TF-IDF features are kept for KNN.

KNN is memory-intensive, so the notebook keeps the most useful 500 features
rather than converting the full sparse matrix to dense format.

### `top_feature_indices`

`top_feature_indices` stores the selected TF-IDF feature column positions used
by KNN.

### `X_train_dense`

`X_train_dense` is the dense, scaled training matrix used by KNN.

KNN requires dense numeric inputs, so the sparse TF-IDF matrix is reduced and
converted.

### `X_validation_dense`

`X_validation_dense` is the dense, scaled validation matrix used by KNN.

It is scaled using the training-set center and scale values.

### `X_test_dense`

`X_test_dense` is the dense, scaled test matrix used by KNN.

### `k_value`

`k_value` is the number of nearest neighbors used by KNN.

In the notebook:

```r
k_value <- 5
```

### `knn_validation_probs`

`knn_validation_probs` contains KNN predicted probabilities for the validation
set.

### `knn_test_probs`

`knn_test_probs` contains KNN predicted probabilities for the test set.

### XGBoost

### `xgb_models`

`xgb_models` is a list of one-vs-rest XGBoost models.

There is one boosted-tree model per skill label.

### `dtrain`

`dtrain` is the XGBoost training matrix for one skill label.

XGBoost uses its own `xgb.DMatrix` format for efficient training.

### `dvalidation`

`dvalidation` is the XGBoost validation matrix for one skill label.

It is used during training for early stopping.

### `dtest`

`dtest` is the XGBoost test matrix for one skill label.

### `scale_pos_weight`

`scale_pos_weight` helps XGBoost handle class imbalance.

Many skills are rare, so positive examples can be much less common than negative
examples. This weight gives more importance to positive examples during
training.

### `xgb_validation_probs`

`xgb_validation_probs` contains XGBoost predicted probabilities for the
validation set.

### `xgb_test_probs`

`xgb_test_probs` contains XGBoost predicted probabilities for the test set.

## Prediction Variables

### Probability Matrices

Variables ending in `_probs` store predicted probabilities.

Examples:

```r
logit_test_probs
knn_test_probs
xgb_test_probs
```

A value closer to `1` means the model is more confident the profile has that
skill.

### Threshold Variables

Variables ending in `_thresholds` store the probability cutoff used to convert
probabilities into `0` or `1` predictions.

Examples:

```r
logit_thresholds
knn_thresholds
xgb_thresholds
```

The threshold is tuned on the validation set for each skill.

### Binary Prediction Matrices

Variables ending in `_pred_validation` or `_pred_test` store final binary
predictions.

Examples:

```r
logit_pred_test
knn_pred_test
xgb_pred_test
```

Each value is:

- `1` if the model predicts the profile has the skill
- `0` if the model predicts the profile does not have the skill

## Evaluation Variables

### `validation_metrics`

Validation metrics show how a model performs on the validation set.

The validation set is mainly used for model selection and threshold tuning.

### `test_metrics`

Test metrics show how a model performs on the final held-out test set.

The test set is the best estimate of performance on unseen profiles.

### `precision_micro`

`precision_micro` answers:

Of all predicted skills, how many were correct?

Higher precision means fewer false positives.

### `recall_micro`

`recall_micro` answers:

Of all true skills, how many did the model find?

Higher recall means fewer missed skills.

### `f1_micro`

`f1_micro` balances micro precision and micro recall.

This is one of the main metrics used to compare the models.

### `precision_macro`

`precision_macro` calculates precision separately for each skill, then averages
across skills.

### `recall_macro`

`recall_macro` calculates recall separately for each skill, then averages across
skills.

### `f1_macro`

`f1_macro` calculates F1 separately for each skill, then averages across skills.

Macro F1 gives more equal weight to rare and common skills.

## Saved Output Locations

Each separate 5k model notebook saves results under:

```text
data/processed/5k_model_outputs/
```

The model-specific folders are:

```text
data/processed/5k_model_outputs/baseline_frequency_prior/
data/processed/5k_model_outputs/logistic_regression/
data/processed/5k_model_outputs/knn/
data/processed/5k_model_outputs/xgboost/
```

Each folder includes:

- an `.rds` file with the full model results object
- `validation_metrics.csv`
- `test_metrics.csv`

## How the Model Files Work Overall

Each model notebook follows the same process:

1. Load the encoded 5k train, validation, and test data.
2. Keep the top 25 skill labels.
3. Train one model per skill label.
4. Predict probabilities for validation and test profiles.
5. Tune skill-specific thresholds using validation data.
6. Convert probabilities into binary predictions.
7. Calculate validation and test metrics.
8. Save the model outputs.

