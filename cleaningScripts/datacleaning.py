from pathlib import Path

import pandas as pd

# Paths to the datasets
DATA_500_EXPERIENCE_FULL_PATH = Path("./data/raw/LinkedIn_Scrape_500_Experiences_Wide_Full_List.csv")
DATA_500_EXPERIENCE_CURRENT_PATH = Path("./data/raw/LinkedIn_Scrape_500_Experiences_Wide_Current_List.csv")
DATA_500_SKILLS_PATH = Path("./data/raw/LinkedIn_Scrape_500_Skills_List.csv")

DATA_5K_EXPERIENCE_PATH = Path("./data/raw/LinkedIn_Scrape_full_5865.xlsx")
DATA_5K_SKILLS_PATH = Path("./data/raw/LinkedIn_Scrape_full_5865_Skills_List.csv")

PROCESSED_DIR = Path("./data/processed")


def join_columns(df: pd.DataFrame, columns: list[str], output_column: str) -> pd.DataFrame:
    existing_columns = [col for col in columns if col in df.columns]
    if not existing_columns:
        return df

    df[output_column] = df[existing_columns].apply(
        lambda row: " ".join(row.dropna().astype(str)).strip(),
        axis=1,
    )
    df.drop(columns=existing_columns, inplace=True)
    return df


def clean_company_websites(df: pd.DataFrame, max_index: int) -> pd.DataFrame:
    for i in range(1, max_index + 1):
        col = f"companyWebsite_{i}"
        if col in df.columns:
            df[col] = df[col].apply(
                lambda value: value if pd.isna(value) else str(value).split(",")[0].strip()
            )
    return df


def clean_full_experience_df(df: pd.DataFrame, max_index: int = 27) -> pd.DataFrame:
    df = df.copy()

    job_description_columns = [f"jobDescription_{i}" for i in range(1, max_index + 1)]
    title_columns = [f"title_{i}" for i in range(1, max_index + 1)]
    company_name_columns = [f"companyName_{i}" for i in range(1, max_index + 1)]

    df = join_columns(df, job_description_columns, "jobDescription")
    df = join_columns(df, title_columns, "jobTitle")
    df = join_columns(df, company_name_columns, "companyName")
    df = clean_company_websites(df, max_index)

    return df


def clean_500_dataset():
    df_experiences = pd.read_csv(DATA_500_EXPERIENCE_FULL_PATH)
    df_current_experiences = pd.read_csv(DATA_500_EXPERIENCE_CURRENT_PATH)
    df_skills = pd.read_csv(DATA_500_SKILLS_PATH)

    df_experiences = clean_full_experience_df(df_experiences)
    df_current_experiences = clean_full_experience_df(df_current_experiences, max_index=1)

    return df_experiences, df_current_experiences, df_skills


def clean_5k_dataset():
    df_experiences = pd.read_excel(DATA_5K_EXPERIENCE_PATH)
    df_skills = pd.read_csv(DATA_5K_SKILLS_PATH)

    # If this sheet uses the same wide experience format (jobDescription_N, title_N, ...), apply the same cleaning.
    if any(col.startswith("jobDescription_") for col in df_experiences.columns):
        df_experiences = clean_full_experience_df(df_experiences)

    return df_experiences, df_skills


def save_cleaned_data(df_experiences, df_current_experiences, df_skills):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df_experiences.to_csv(PROCESSED_DIR / "cleaned_500_experiences.csv", index=False)
    df_current_experiences.to_csv(PROCESSED_DIR / "cleaned_500_current_experiences.csv", index=False)
    df_skills.to_csv(PROCESSED_DIR / "cleaned_500_skills.csv", index=False)


def save_cleaned_5k_data(df_experiences, df_skills):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df_experiences.to_csv(PROCESSED_DIR / "cleaned_5k_experiences.csv", index=False)
    df_skills.to_csv(PROCESSED_DIR / "cleaned_5k_skills.csv", index=False)


def showheads(df_experiences, df_current_experiences, df_skills):
    print("Experiences DataFrame:")
    print(df_experiences.head())
    print("\nCurrent Experiences DataFrame:")
    print(df_current_experiences.head())
    print("\nSkills DataFrame:")
    print(df_skills.head())


def showheads_5k(df_experiences, df_skills):
    print("5K Experiences DataFrame:")
    print(df_experiences.head())
    print("\n5K Skills DataFrame:")
    print(df_skills.head())


def main():
    df_experiences, df_current_experiences, df_skills = clean_500_dataset()
    save_cleaned_data(df_experiences, df_current_experiences, df_skills)
    showheads(df_experiences, df_current_experiences, df_skills)

    df_5k_experiences, df_5k_skills = clean_5k_dataset()
    save_cleaned_5k_data(df_5k_experiences, df_5k_skills)
    showheads_5k(df_5k_experiences, df_5k_skills)


if __name__ == "__main__":
    main()
