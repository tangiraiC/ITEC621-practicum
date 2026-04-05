"""
LinkedIn Data Cleaning Pipeline

This script cleans and processes LinkedIn scrape datasets:
- 500 dataset: Wide-format CSV files with experience data
- 5K dataset: Excel file with scraped data and skills

The pipeline consolidates wide columns, removes unnecessary data, and saves cleaned CSVs.
"""

from pathlib import Path
import pandas as pd

# File paths for datasets
DATA_500_EXPERIENCE_FULL_PATH = Path("./data/raw/LinkedIn_Scrape_500_Experiences_Wide_Full_List.csv")
DATA_500_EXPERIENCE_CURRENT_PATH = Path("./data/raw/LinkedIn_Scrape_500_Experiences_Wide_Current_List.csv")
DATA_500_SKILLS_PATH = Path("./data/raw/LinkedIn_Scrape_500_Skills_List.csv")

DATA_5K_EXPERIENCE_PATH = Path("./data/raw/LinkedIn_Scrape_full_5865.xlsx")
DATA_5K_SKILLS_PATH = Path("./data/raw/LinkedIn_Scrape_full_5865_Skills_List.csv")

PROCESSED_DIR = Path("./data/processed")


def join_columns(df: pd.DataFrame, columns: list[str], output_column: str) -> pd.DataFrame:
    """
    Join multiple columns into a single column by concatenating non-null values.

    Args:
        df: Input DataFrame
        columns: List of column names to join
        output_column: Name of the new combined column

    Returns:
        DataFrame with the new column and original columns dropped
    """
    existing_columns = [col for col in columns if col in df.columns]
    if not existing_columns:
        return df

    # Concatenate values from existing columns, ignoring NaN
    df[output_column] = df[existing_columns].apply(
        lambda row: " ".join(row.dropna().astype(str)).strip(),
        axis=1,
    )
    # Remove the original columns
    df.drop(columns=existing_columns, inplace=True)
    return df


def drop_prefixed_columns(df: pd.DataFrame, prefix: str, max_index: int) -> pd.DataFrame:
    """
    Drop columns that match a numbered prefix pattern (e.g., prefix_1, prefix_2, ...).

    Args:
        df: Input DataFrame
        prefix: Column prefix to match
        max_index: Maximum index to check (e.g., 27 for 1-27)

    Returns:
        DataFrame with matching columns removed
    """
    columns_to_drop = [f"{prefix}_{i}" for i in range(1, max_index + 1) if f"{prefix}_{i}" in df.columns]
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)
    return df


def select_500_columns(df: pd.DataFrame, max_index: int = 27) -> pd.DataFrame:
    """
    Select only the desired columns for the cleaned 500 dataset output.

    Args:
        df: Input DataFrame
        max_index: Maximum job index (default 27)

    Returns:
        DataFrame with only allowed columns
    """
    allowed_columns = ["linkedinUrl", "jobDescription", "jobTitle", "companyName"]
    # Add job start and end dates
    allowed_columns += [f"jobStartedOn_{i}" for i in range(1, max_index + 1)]
    allowed_columns += [f"jobEndedOn_{i}" for i in range(1, max_index + 1)]
    # Keep only columns that exist in the DataFrame
    return df[[col for col in allowed_columns if col in df.columns]]


def clean_full_experience_df(df: pd.DataFrame, max_index: int = 27) -> pd.DataFrame:
    """
    Clean the wide-format experience DataFrame by consolidating columns and removing unwanted ones.

    Args:
        df: Raw experience DataFrame
        max_index: Maximum job index (default 27)

    Returns:
        Cleaned DataFrame with consolidated and selected columns
    """
    df = df.copy()

    # Define column groups to consolidate
    job_description_columns = [f"jobDescription_{i}" for i in range(1, max_index + 1)]
    title_columns = [f"title_{i}" for i in range(1, max_index + 1)]
    company_name_columns = [f"companyName_{i}" for i in range(1, max_index + 1)]

    # Consolidate wide columns into single columns
    df = join_columns(df, job_description_columns, "jobDescription")
    df = join_columns(df, title_columns, "jobTitle")
    df = join_columns(df, company_name_columns, "companyName")

    # Remove unwanted prefixed columns
    df = drop_prefixed_columns(df, "companyId", max_index)
    df = drop_prefixed_columns(df, "companySize", max_index)
    df = drop_prefixed_columns(df, "companyIndustry", max_index)
    df = drop_prefixed_columns(df, "companyWebsite", max_index)
    df = drop_prefixed_columns(df, "employmentType", max_index)
    df = drop_prefixed_columns(df, "jobLocation", max_index)
    df = drop_prefixed_columns(df, "jobLocationCountry", max_index)
    df = drop_prefixed_columns(df, "jobStillWorking", max_index)

    # Select final columns for output
    df = select_500_columns(df, max_index)
    return df


def clean_500_dataset():
    """
    Load and clean the 500 dataset files.

    Returns:
        Tuple of (full_experiences_df, current_experiences_df, skills_df)
    """
    df_experiences = pd.read_csv(DATA_500_EXPERIENCE_FULL_PATH)
    df_current_experiences = pd.read_csv(DATA_500_EXPERIENCE_CURRENT_PATH)
    df_skills = pd.read_csv(DATA_500_SKILLS_PATH)

    # Clean the experience dataframes
    df_experiences = clean_full_experience_df(df_experiences)
    df_current_experiences = clean_full_experience_df(df_current_experiences, max_index=1)

    return df_experiences, df_current_experiences, df_skills


def clean_5k_dataset():
    """
    Load and clean the 5K dataset files.

    Returns:
        Tuple of (experiences_df, skills_df)
    """
    # Read the "Scraped data" sheet from the Excel file
    df_experiences = pd.read_excel(DATA_5K_EXPERIENCE_PATH, sheet_name="Scraped data")
    df_skills = pd.read_csv(DATA_5K_SKILLS_PATH)

    # List of columns to remove from 5K dataset
    columns_to_drop = [
        "current_company_url",
        "Company_size",
        "last_scraped_date",
        "previous_job_start_date",
        "previous_job_location",
        "previous_job_country",
        "previous_company_size",
        "employment_type",
        "is_currently_employed",
        "current_job_country",
        "current_job_location",
        "current_job_start_date",
        "email",
        "full_name",
        "education_start_year",
        "education_end_year",
        "previous_job_end_date",
        "total_experience_years",
        "current_job_duration_years",
    ]

    # Drop the specified columns if they exist
    df_experiences = df_experiences.drop(
        columns=[col for col in columns_to_drop if col in df_experiences.columns]
    )

    return df_experiences, df_skills


def save_cleaned_data(df_experiences, df_current_experiences, df_skills):
    """
    Save the cleaned 500 dataset DataFrames to CSV files.

    Args:
        df_experiences: Full experiences DataFrame
        df_current_experiences: Current experiences DataFrame
        df_skills: Skills DataFrame
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df_experiences.to_csv(PROCESSED_DIR / "cleaned_500_experiences.csv", index=False)
    df_current_experiences.to_csv(PROCESSED_DIR / "cleaned_500_current_experiences.csv", index=False)
    df_skills.to_csv(PROCESSED_DIR / "cleaned_500_skills.csv", index=False)


def save_cleaned_5k_data(df_experiences, df_skills):
    """
    Save the cleaned 5K dataset DataFrames to CSV files.

    Args:
        df_experiences: Experiences DataFrame
        df_skills: Skills DataFrame
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df_experiences.to_csv(PROCESSED_DIR / "cleaned_5k_experiences.csv", index=False)
    df_skills.to_csv(PROCESSED_DIR / "cleaned_5k_skills.csv", index=False)


def showheads(df_experiences, df_current_experiences, df_skills):
    """
    Print the first 5 rows of each 500 dataset DataFrame.
    """
    print("Experiences DataFrame:")
    print(df_experiences.head())
    print("\nCurrent Experiences DataFrame:")
    print(df_current_experiences.head())
    print("\nSkills DataFrame:")
    print(df_skills.head())


def showheads_5k(df_experiences, df_skills):
    """
    Print the first 5 rows of each 5K dataset DataFrame.
    """
    print("5K Experiences DataFrame:")
    print(df_experiences.head())
    print("\n5K Skills DataFrame:")
    print(df_skills.head())


def main():
    """
    Main function to run the full cleaning pipeline for both datasets.
    """
    # Process 500 dataset
    df_experiences, df_current_experiences, df_skills = clean_500_dataset()
    save_cleaned_data(df_experiences, df_current_experiences, df_skills)
    showheads(df_experiences, df_current_experiences, df_skills)

    # Process 5K dataset
    df_5k_experiences, df_5k_skills = clean_5k_dataset()
    save_cleaned_5k_data(df_5k_experiences, df_5k_skills)
    showheads_5k(df_5k_experiences, df_5k_skills)


if __name__ == "__main__":
    main()
