import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Amin\Desktop\TEK-UP\football-match-prediction")
BRUTE_DIR = PROJECT_ROOT / "data" / "brute"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

RICH_IN = BRUTE_DIR / "seriea_rich_modern.csv"
CORE_IN = BRUTE_DIR / "seriea_core_all_seasons.csv"

def standardize_common(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # clean strings
    for c in ["HomeTeam", "AwayTeam", "FTR", "HTR", "Season"]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()

    # parse date
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # remove invalid essentials
    essential = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "Season"]
    for col in essential:
        if col not in df.columns:
            raise ValueError(f"Colonne manquante: {col}")

    df = df.dropna(subset=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "Season"])

    # numeric safety (no negative)
    for c in ["FTHG", "FTAG"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["FTHG", "FTAG"])
    df = df[(df["FTHG"] >= 0) & (df["FTAG"] >= 0)]

    # normalize date format (ISO) by keeping datetime then formatting at save
    df = df.sort_values(["Date", "HomeTeam", "AwayTeam"]).reset_index(drop=True)

    # drop exact duplicates if any (safety)
    df = df.drop_duplicates()

    return df

def clean_rich():
    df = pd.read_csv(RICH_IN)
    df = standardize_common(df)

    # columns expected for rich
    rich_cols = ["HS","AS","HST","AST","HF","AF","HC","AC","HY","AY","HR","AR","HTHG","HTAG","HTR"]
    for c in rich_cols:
        if c not in df.columns:
            raise ValueError(f"RICH: colonne manquante: {c}")

    # convert numerics
    numeric_cols = ["HS","AS","HST","AST","HF","AF","HC","AC","HY","AY","HR","AR","HTHG","HTAG"]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # remove the very rare HT missing rows (you have only 1)
    before = len(df)
    df = df.dropna(subset=["HTHG","HTAG","HTR"])
    removed = before - len(df)

    # format date string ISO for CSV
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    out = PROCESSED_DIR / "seriea_rich_modern_clean.csv"
    df.to_csv(out, index=False)
    print("✅ RICH cleaned saved:", out)
    print("   rows:", len(df), "| removed_rows_due_to_missing_HT:", removed)

def clean_core():
    df = pd.read_csv(CORE_IN)
    df = standardize_common(df)

    # HT columns exist but may be missing
    for c in ["HTHG","HTAG","HTR"]:
        if c not in df.columns:
            raise ValueError(f"CORE: colonne manquante: {c}")

    # numeric conversion for HT goals (can be NaN)
    df["HTHG"] = pd.to_numeric(df["HTHG"], errors="coerce")
    df["HTAG"] = pd.to_numeric(df["HTAG"], errors="coerce")

    # flag availability
    df["HT_available"] = (~df["HTHG"].isna()) & (~df["HTAG"].isna()) & (df["HTR"].astype(str).str.lower() != "nan")
    df["HT_available"] = df["HT_available"].astype(int)

    # Save 3 versions
    df_full = df.copy()
    df_full["Date"] = pd.to_datetime(df_full["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
    out_full = PROCESSED_DIR / "seriea_core_all_seasons_clean.csv"
    df_full.to_csv(out_full, index=False)

    df_no_ht = df_full.drop(columns=["HTHG","HTAG","HTR"])
    out_no_ht = PROCESSED_DIR / "seriea_core_all_seasons_noHT.csv"
    df_no_ht.to_csv(out_no_ht, index=False)

    df_ht_only = df_full[df_full["HT_available"] == 1].drop(columns=["HT_available"])
    out_ht_only = PROCESSED_DIR / "seriea_core_all_seasons_HTcomplete.csv"
    df_ht_only.to_csv(out_ht_only, index=False)

    print("✅ CORE cleaned saved:", out_full)
    print("✅ CORE noHT saved:", out_no_ht)
    print("✅ CORE HTcomplete saved:", out_ht_only)
    print("   rows_full:", len(df_full), "| rows_HTcomplete:", len(df_ht_only), "| HT_missing_rows:", (df_full['HT_available']==0).sum())

if __name__ == "__main__":
    clean_rich()
    clean_core()
    print("✅ Terminé (processed).")
