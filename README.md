# LinkedIn Data Cleaning Project

Data cleaning pipeline for LinkedIn scrape datasets.

## Project Structure

```
cleaningScripts/
  datacleaning.py    # Main cleaning pipeline
  try.r              # R experiments

data/
  raw/               # Raw scraped datasets
  processed/         # Cleaned, processed datasets
```

## Datasets

### 500 Dataset
- `LinkedIn_Scrape_500_Experiences_Wide_Full_List.csv` - Full experience history (27 positions)
- `LinkedIn_Scrape_500_Experiences_Wide_Current_List.csv` - Current position only
- `LinkedIn_Scrape_500_Skills_List.csv` - Skills list

### 5K Dataset
- `LinkedIn_Scrape_full_5865.xlsx` - 5865 profiles with URLs and timestamps
- `LinkedIn_Scrape_full_5865_Skills_List.csv` - Skills for 5865 profiles

## Cleaning Pipeline

The `datacleaning.py` script:
1. Reads raw datasets (CSV and Excel formats)
2. Consolidates wide-format columns (jobDescription_1, jobDescription_2, etc.) into single columns
3. Cleans company website data
4. Saves cleaned results to CSV

### Output Files
- `cleaned_500_experiences.csv`
- `cleaned_500_current_experiences.csv`
- `cleaned_500_skills.csv`
- `cleaned_5k_experiences.csv`
- `cleaned_5k_skills.csv`

## Usage

```bash
python cleaningScripts/datacleaning.py
```

This runs both 500 and 5K cleaning pipelines and displays sample output from each dataset.

## Requirements

- pandas
- openpyxl (for Excel file support)
