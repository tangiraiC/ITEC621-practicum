# KSB621 Skills Extraction Shiny Demo

This folder contains a local R Shiny demo for the KSB621 Skills Extraction
project. The app lets a user enter LinkedIn profile fields, converts the text
into the same model-ready TF-IDF feature format used in the CP8 modeling
workflow, and returns predicted skills with confidence percentages.

## What the App Does

The demo supports the presentation flow:

`profile_text -> TF-IDF features -> trained model -> predicted skills -> confidence percentages`

Users can enter:

- Headline
- Current job title
- Current job description
- Previous job title
- Previous job description

The app combines those fields into one `profile_text` value, cleans the text,
generates skill probabilities, and displays:

- Predicted skills above the selected threshold
- Confidence percentage for each predicted skill
- Top 10 skill probabilities, sorted highest to lowest
- A clear message when no skill is above the threshold

## Required R Packages

Install the required packages in R or RStudio:

```r
install.packages(c(
  "shiny",
  "tibble",
  "dplyr",
  "text2vec",
  "Matrix",
  "xgboost"
))
```

## Model Files

The app expects these files inside `shiny_demo/models/`:

```text
shiny_demo/
  models/
    final_model.rds
    tfidf_vectorizer.rds
    retained_skills.rds
```

These files are included in this demo folder:

- `final_model.rds`: the saved one-vs-rest XGBoost skill extraction model
- `tfidf_vectorizer.rds`: the saved TF-IDF vectorizer/transformer bundle
- `retained_skills.rds`: the modeled skill labels

If any file is missing, the app shows a setup message naming the missing file.

## How to Run

From the practicum project root, run:

```r
shiny::runApp("shiny_demo")
```

In RStudio, you can also open `shiny_demo/app.R` and click **Run App**.

## Deploy to Render

Render does not provide a native R/Shiny runtime, so this Shiny app deploys on
Render with Docker. The app still runs as R Shiny; Docker only supplies the R
environment and package dependencies.

### Blueprint Deploy

1. Push this repository to GitHub.
2. In Render, click **New +** -> **Blueprint**.
3. Connect the GitHub repository.
4. Render will read `render.yaml` from the project root.
5. Create the service and wait for the build to finish.

### Manual Web Service Deploy

1. Push this repository to GitHub.
2. In Render, click **New +** -> **Web Service**.
3. Connect the GitHub repository.
4. Use these settings:

```text
Runtime: Docker
Root Directory: shiny_demo
Dockerfile Path: ./Dockerfile
Plan: Free is acceptable for the demo
```

Render provides the public port through the `PORT` environment variable. The
Dockerfile starts Shiny with `host = "0.0.0.0"` and that Render port, which is
required for Render to route traffic to the app.

### Deployment Notes

- Keep these model files committed in `shiny_demo/models/`:
  - `final_model.rds`
  - `tfidf_vectorizer.rds`
  - `retained_skills.rds`
- The first build can take several minutes because Render installs R packages,
  including `xgboost`.
- If the app deploys but predictions do not run, check the Render logs for
  missing R packages or missing files under `/app/models/`.

## How This Supports CP9/CP10

This is a presentation-ready local demo, not a production system. It shows the
project's core modeling idea in a way that non-technical users can understand:

1. Enter LinkedIn profile fields or job-description text.
2. Click **Extract Skills**.
3. See which skills the trained model thinks are present.
4. Review confidence percentages and adjust the prediction threshold.

The demo is useful for CP9/CP10 because it translates the modeling workflow into
a visible client/classroom experience: profile fields go in, predicted skills
come out.
