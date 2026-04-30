required_packages <- c(
  "shiny",
  "tibble",
  "dplyr",
  "text2vec",
  "Matrix",
  "xgboost"
)

missing_packages <- required_packages[
  !vapply(required_packages, requireNamespace, logical(1), quietly = TRUE)
]

if (!requireNamespace("shiny", quietly = TRUE)) {
  stop(
    "The shiny package is required to run this demo. Install it with: ",
    "install.packages('shiny')",
    call. = FALSE
  )
}

library(shiny)

model_dir <- file.path("models")
model_paths <- list(
  final_model = file.path(model_dir, "final_model.rds"),
  tfidf_vectorizer = file.path(model_dir, "tfidf_vectorizer.rds"),
  retained_skills = file.path(model_dir, "retained_skills.rds")
)

missing_model_files <- names(model_paths)[!file.exists(unlist(model_paths))]

clean_profile_text <- function(x) {
  x <- ifelse(is.na(x), "", as.character(x))
  x <- tolower(x)
  x <- gsub("[[:punct:]]+", " ", x)
  x <- gsub("[[:space:]]+", " ", x)
  trimws(x)
}

combine_profile_fields <- function(
  headline,
  current_job_title,
  current_job_description,
  previous_job_title,
  previous_job_description
) {
  fields <- c(
    headline,
    current_job_title,
    current_job_description,
    previous_job_title,
    previous_job_description
  )

  fields <- fields[!is.na(fields) & trimws(fields) != ""]
  clean_profile_text(paste(fields, collapse = " "))
}

load_demo_artifacts <- function() {
  if (length(missing_model_files) > 0) {
    return(NULL)
  }

  list(
    final_model = readRDS(model_paths$final_model),
    tfidf_vectorizer = readRDS(model_paths$tfidf_vectorizer),
    retained_skills = readRDS(model_paths$retained_skills)
  )
}

align_sparse_columns <- function(matrix_in, feature_names) {
  existing_features <- colnames(matrix_in)
  matched_features <- intersect(feature_names, existing_features)

  aligned <- Matrix::Matrix(
    0,
    nrow = nrow(matrix_in),
    ncol = length(feature_names),
    sparse = TRUE
  )
  colnames(aligned) <- feature_names

  if (length(matched_features) > 0) {
    aligned[, matched_features] <- matrix_in[, matched_features, drop = FALSE]
  }

  aligned
}

make_tfidf_features <- function(cleaned_text, tfidf_bundle) {
  tokens_iterator <- text2vec::itoken(
    cleaned_text,
    tokenizer = text2vec::word_tokenizer,
    progressbar = FALSE
  )

  dtm <- text2vec::create_dtm(tokens_iterator, tfidf_bundle$vectorizer)
  tfidf_matrix <- tfidf_bundle$tfidf_transformer$transform(dtm)
  align_sparse_columns(tfidf_matrix, tfidf_bundle$feature_names)
}

predict_skills <- function(cleaned_text, artifacts, threshold) {
  final_model <- artifacts$final_model
  retained_skills <- artifacts$retained_skills

  tfidf_matrix <- make_tfidf_features(cleaned_text, artifacts$tfidf_vectorizer)
  xgb_matrix <- xgboost::xgb.DMatrix(data = tfidf_matrix)

  probabilities <- vapply(
    seq_along(retained_skills),
    function(i) {
      as.numeric(predict(final_model$models[[i]], newdata = xgb_matrix))
    },
    numeric(1)
  )

  results <- tibble::tibble(
    skill = retained_skills,
    probability = probabilities,
    confidence = probabilities * 100,
    confidence_label = sprintf("%.1f%%", confidence),
    predicted = probability >= threshold
  ) |>
    dplyr::arrange(dplyr::desc(probability))

  list(
    predicted_skills = results |> dplyr::filter(predicted),
    top_skills = results |> dplyr::slice_head(n = 10)
  )
}

artifacts <- load_demo_artifacts()

ui <- fluidPage(
  tags$head(
    tags$title("KSB621 Skills Extraction Demo"),
    tags$style(HTML("
      body {
        background: #f6f7f9;
        color: #1f2933;
      }
      .app-shell {
        max-width: 1180px;
        margin: 0 auto;
        padding: 24px 16px 40px;
      }
      .app-header {
        border-bottom: 1px solid #d9dee7;
        margin-bottom: 22px;
        padding-bottom: 14px;
      }
      .app-title {
        font-size: 28px;
        font-weight: 700;
        margin: 0 0 6px;
      }
      .app-subtitle {
        max-width: 920px;
        color: #52606d;
        font-size: 15px;
        line-height: 1.45;
      }
      .panel {
        background: #ffffff;
        border: 1px solid #d9dee7;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 18px;
      }
      .panel h3 {
        margin-top: 0;
        font-size: 18px;
        font-weight: 700;
      }
      .btn-primary {
        background-color: #174ea6;
        border-color: #174ea6;
        font-weight: 600;
      }
      .skill-chip {
        display: inline-block;
        background: #e8f0fe;
        border: 1px solid #adc7ff;
        color: #173f8a;
        border-radius: 999px;
        padding: 7px 11px;
        margin: 4px 6px 4px 0;
        font-weight: 600;
      }
      .muted-note {
        color: #66788a;
        font-size: 14px;
      }
      .warning-box {
        border: 1px solid #f0b429;
        background: #fffbea;
        color: #7c5e10;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 18px;
      }
      table {
        background: white;
      }
    "))
  ),
  div(
    class = "app-shell",
    div(
      class = "app-header",
      div(class = "app-title", "KSB621 Skills Extraction Demo"),
      div(
        class = "app-subtitle",
        "The app reads profile text, converts it into model-ready features, ",
        "and predicts which skills are most likely present."
      )
    ),
    uiOutput("setup_warning"),
    fluidRow(
      column(
        width = 6,
        div(
          class = "panel",
          h3("Profile Input"),
          textInput("headline", "Headline", placeholder = "Example: Data Analyst | MBA Candidate"),
          textInput("current_job_title", "Current Job Title", placeholder = "Example: Senior Business Analyst"),
          textAreaInput(
            "current_job_description",
            "Current Job Description",
            placeholder = "Paste current role responsibilities here...",
            height = "110px"
          ),
          textInput("previous_job_title", "Previous Job Title", placeholder = "Example: Operations Analyst"),
          textAreaInput(
            "previous_job_description",
            "Previous Job Description",
            placeholder = "Paste previous role responsibilities here...",
            height = "110px"
          ),
          sliderInput(
            "threshold",
            "Prediction Threshold",
            min = 0,
            max = 1,
            value = 0.50,
            step = 0.05
          ),
          actionButton("extract", "Extract Skills", class = "btn-primary")
        )
      ),
      column(
        width = 6,
        div(
          class = "panel",
          h3("Predicted Skills"),
          uiOutput("predicted_skills"),
          tags$hr(),
          h3("Top 10 Skill Probabilities"),
          tableOutput("top_skill_table")
        )
      )
    )
  )
)

server <- function(input, output, session) {
  output$setup_warning <- renderUI({
    messages <- character(0)

    if (length(missing_packages) > 0) {
      messages <- c(
        messages,
        paste(
          "Missing R packages:",
          paste(missing_packages, collapse = ", "),
          ". Install them before running predictions."
        )
      )
    }

    if (length(missing_model_files) > 0) {
      messages <- c(
        messages,
        paste(
          "Missing model files:",
          paste(unlist(model_paths[missing_model_files]), collapse = ", ")
        )
      )
    }

    if (length(messages) == 0) {
      return(NULL)
    }

    div(
      class = "warning-box",
      tags$strong("Setup check"),
      tags$ul(lapply(messages, tags$li))
    )
  })

  prediction_result <- eventReactive(input$extract, {
    validate(
      need(length(missing_packages) == 0, "Install the missing R packages before running predictions."),
      need(length(missing_model_files) == 0, "Add the missing model files before running predictions."),
      need(!is.null(artifacts), "Model artifacts could not be loaded.")
    )

    combined_text <- combine_profile_fields(
      headline = input$headline,
      current_job_title = input$current_job_title,
      current_job_description = input$current_job_description,
      previous_job_title = input$previous_job_title,
      previous_job_description = input$previous_job_description
    )

    validate(
      need(nchar(combined_text) > 0, "Fill in at least one profile field before extracting skills.")
    )

    predict_skills(
      cleaned_text = combined_text,
      artifacts = artifacts,
      threshold = input$threshold
    )
  })

  output$predicted_skills <- renderUI({
    result <- prediction_result()
    predicted <- result$predicted_skills

    if (nrow(predicted) == 0) {
      return(div(class = "muted-note", "No strong skills detected."))
    }

    tagList(
      lapply(
        seq_len(nrow(predicted)),
        function(i) {
          div(
            class = "skill-chip",
            paste0(predicted$skill[i], " (", predicted$confidence_label[i], ")")
          )
        }
      )
    )
  })

  output$top_skill_table <- renderTable({
    result <- prediction_result()

    result$top_skills |>
      dplyr::transmute(
        Skill = skill,
        `Confidence` = confidence_label,
        `Above Threshold` = ifelse(predicted, "Yes", "No")
      )
  })
}

shinyApp(ui = ui, server = server)
