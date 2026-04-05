# How to Run

## Prerequisites
- Python 3.7+ with pandas, openpyxl
- R 4.0+ with readr, readxl, dplyr, tidyr, stringr (for Quarto)
- Git

## Setup
1. Clone repo: `git clone https://github.com/tangiraiC/ITEC621-practicum.git`
2. Place data files in `data/raw/` folder
3. Ensure filenames match: `LinkedIn_Scrape_500_*.csv`, `LinkedIn_Scrape_full_5865.*`

## Run Python Pipeline
```bash
cd ITEC621-practicum
python cleaningScripts/datacleaning.py
```

## Run Quarto Pipeline
1. Open `cleaningScripts/datacleaning.qmd` in RStudio/VS Code
2. Render document or run chunks

## Output
- Cleaned CSVs generated in `data/processed/`
- Console shows sample data previews
- 5 output files: `cleaned_500_*.csv`, `cleaned_5k_*.csv`

## Notes
- `data/raw/` files are ignored by git (place manually)
- Re-running overwrites `data/processed/` files
- Check README.md for detailed instructions