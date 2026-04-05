# LinkedIn Data Cleaning Project

A comprehensive data cleaning pipeline for LinkedIn profile scrape datasets. This project processes raw scraped data from LinkedIn profiles, consolidates wide-format columns, removes unnecessary fields, and produces clean CSV files for analysis.

## Project Structure

```
practictum/
├── cleaningScripts/
│   ├── datacleaning.py       # Main Python cleaning pipeline
│   ├── datacleaning.qmd      # Quarto equivalent with same functionality
│   └── try.r                 # R experiments
├── data/
│   ├── raw/                  # Raw scraped datasets (place your files here)
│   │   ├── LinkedIn_Scrape_500_Experiences_Wide_Full_List.csv
│   │   ├── LinkedIn_Scrape_500_Experiences_Wide_Current_List.csv
│   │   ├── LinkedIn_Scrape_500_Skills_List.csv
│   │   ├── LinkedIn_Scrape_full_5865.xlsx
│   │   └── LinkedIn_Scrape_full_5865_Skills_List.csv
│   └── processed/            # Cleaned datasets (auto-generated)
│       ├── cleaned_500_experiences.csv
│       ├── cleaned_500_current_experiences.csv
│       ├── cleaned_500_skills.csv
│       ├── cleaned_5k_experiences.csv
│       └── cleaned_5k_skills.csv
├── .gitignore
└── README.md
```

## Datasets

### 500 Dataset (Small Sample)
- **Full Experiences**: `LinkedIn_Scrape_500_Experiences_Wide_Full_List.csv`
  - Wide-format CSV with up to 27 job positions per profile
  - Columns: linkedinUrl, companyId_1..27, companyName_1..27, companySize_1..27, etc.
- **Current Experiences**: `LinkedIn_Scrape_500_Experiences_Wide_Current_List.csv`
  - Current position data (1 position per profile)
- **Skills**: `LinkedIn_Scrape_500_Skills_List.csv`
  - Skills data with linkedinUrl and skill columns

### 5K Dataset (Large Scale)
- **Experiences**: `LinkedIn_Scrape_full_5865.xlsx`
  - Excel file with "Scraped data" sheet containing 5,865 profiles
  - Columns: linkedin_url, headline, field_of_study, current_job_title, etc.
- **Skills**: `LinkedIn_Scrape_full_5865_Skills_List.csv`
  - Skills for the 5K profiles

## Data Cleaning Process

The cleaning pipeline performs the following transformations:

### 500 Dataset Cleaning

1. **Column Consolidation**:
   - `jobDescription_1` to `jobDescription_27` → single `jobDescription` column
   - `title_1` to `title_27` → single `jobTitle` column
   - `companyName_1` to `companyName_27` → single `companyName` column

2. **Column Removal**:
   - All `companyId_*` columns (27 columns)
   - All `companySize_*` columns (27 columns)
   - All `companyIndustry_*` columns (27 columns)
   - All `companyWebsite_*` columns (27 columns)
   - All `employmentType_*` columns (27 columns)
   - All `jobLocation_*` columns (27 columns)
   - All `jobLocationCountry_*` columns (27 columns)
   - All `jobStillWorking_*` columns (27 columns)

3. **Final Selection**:
   - Keeps: `linkedinUrl`, `jobDescription`, `jobTitle`, `companyName`, `jobStartedOn_1..27`, `jobEndedOn_1..27`
   - Result: 58 columns for full experiences, 6 columns for current experiences

### 5K Dataset Cleaning

1. **Sheet Selection**:
   - Reads "Scraped data" sheet from Excel file

2. **Column Removal**:
   - Removes 19 specific columns: `current_company_url`, `Company_size`, `last_scraped_date`, `previous_job_start_date`, `previous_job_location`, `previous_job_country`, `previous_company_size`, `employment_type`, `is_currently_employed`, `current_job_country`, `current_job_location`, `current_job_start_date`, `email`, `full_name`, `education_start_year`, `education_end_year`, `previous_job_end_date`, `total_experience_years`, `current_job_duration_years`

3. **Result**: 13 columns retained for experiences data

### Raw File Modifications

Additionally, the raw 500 experiences file (`LinkedIn_Scrape_500_Experiences_Wide_Full_List.csv`) has been pre-processed to remove:
- All `companyId_*` columns (27)
- All `companySize_*` columns (27)
- All `companyWebsite_*` columns (27)
- All `employmentType_*` columns (27)
- All `jobStillWorking_*` columns (27)
- All `jobEndedOn_*` columns (27)
- All `jobLocation_*` columns (27)

Resulting in 163 columns from original 352.

## Generated Files

After running the cleaning pipeline, the following files are created in `data/processed/`:

### 500 Dataset Outputs
- `cleaned_500_experiences.csv`: Full experience history (58 columns, ~500 rows)
- `cleaned_500_current_experiences.csv`: Current positions only (6 columns, ~500 rows)
- `cleaned_500_skills.csv`: Skills data (unchanged, ~500 rows)

### 5K Dataset Outputs
- `cleaned_5k_experiences.csv`: Cleaned experiences (13 columns, 5,865 rows)
- `cleaned_5k_skills.csv`: Skills data (unchanged, 5,865 rows)

## How to Run

### Prerequisites

**For Python Pipeline**:
- Python 3.7+
- pandas
- openpyxl (for Excel reading)

**For Quarto Pipeline**:
- R 4.0+
- RStudio or Quarto CLI
- Required R packages: `readr`, `readxl`, `dplyr`, `tidyr`, `stringr`

### Setup

1. **Place Raw Data Files**:
   - Copy your scraped LinkedIn data files to `data/raw/` folder
   - Ensure filenames match exactly as listed above

2. **Directory Structure**:
   - The `data/processed/` folder will be created automatically
   - All output files will be generated there

### Running the Python Pipeline

```bash
# Navigate to project root
cd /path/to/practictum

# Run the cleaning script
python cleaningScripts/datacleaning.py
```

This will:
- Process both 500 and 5K datasets
- Display sample output from each cleaned dataset
- Save all cleaned files to `data/processed/`

### Running the Quarto Pipeline

1. **Open in RStudio or VS Code**:
   - Open `cleaningScripts/datacleaning.qmd`

2. **Install Dependencies** (if needed):
   ```r
   install.packages(c("readr", "readxl", "dplyr", "tidyr", "stringr"))
   ```

3. **Run the Document**:
   - In RStudio: Click "Render" to generate HTML report
   - Or run chunks individually in the console
   - With Quarto CLI: `quarto render cleaningScripts/datacleaning.qmd`

The Quarto file performs identical cleaning and produces the same output files.

### Expected Output

After successful run, you should see:
- Console output showing sample rows from each dataset
- 5 new CSV files in `data/processed/`
- Confirmation messages for file saves

## Usage Notes

- **Raw Files**: Place your data files in `data/raw/` - do not modify filenames
- **Processed Files**: Automatically created in `data/processed/` - will be overwritten on re-run
- **Error Handling**: Script checks for file existence and column presence
- **Performance**: 5K dataset processing may take a few minutes due to Excel reading
- **Memory**: Ensure sufficient RAM for large datasets (5K profiles)

## Troubleshooting

- **Missing Files**: Ensure all raw data files are in `data/raw/` with correct names
- **Import Errors**: Install required packages for your chosen pipeline
- **Column Mismatches**: Raw data structure must match expected format
- **Permission Issues**: Ensure write access to `data/processed/` directory

## Contributing

To modify the cleaning logic:
- Edit `cleaningScripts/datacleaning.py` for Python changes
- Edit `cleaningScripts/datacleaning.qmd` for R changes
- Update this README if file structures change

## License

This project is for educational/data analysis purposes. Ensure compliance with LinkedIn's terms of service and data privacy regulations.
