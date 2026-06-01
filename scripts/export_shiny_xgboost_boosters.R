required_packages <- c("xgboost")
missing_packages <- required_packages[
  !vapply(required_packages, requireNamespace, logical(1), quietly = TRUE)
]

if (length(missing_packages) > 0) {
  stop(
    "Install missing packages before exporting boosters: ",
    paste(missing_packages, collapse = ", "),
    call. = FALSE
  )
}

model_path <- file.path("shiny_demo", "models", "final_model.rds")
booster_dir <- file.path("shiny_demo", "models", "xgboost_boosters")

dir.create(booster_dir, recursive = TRUE, showWarnings = FALSE)

final_model <- readRDS(model_path)

for (i in seq_along(final_model$models)) {
  xgboost::xgb.save(
    final_model$models[[i]],
    file.path(booster_dir, sprintf("model_%03d.json", i))
  )
}

message(
  "Exported ",
  length(final_model$models),
  " XGBoost boosters to ",
  booster_dir
)
