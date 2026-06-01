FROM rocker/r-ver:4.5.1

RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libgomp1 \
  && rm -rf /var/lib/apt/lists/*

RUN install2.r --error --skipinstalled \
    shiny \
    tibble \
    dplyr \
    text2vec \
    xgboost

WORKDIR /app
COPY . /app

EXPOSE 3838

CMD ["R", "-e", "shiny::runApp('/app', host = '0.0.0.0', port = as.numeric(Sys.getenv('PORT', '3838')))"]
