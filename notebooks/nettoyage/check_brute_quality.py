import pandas as pd
from pathlib import Path

BRUTE_DIR = Path(r"C:\Users\Amin\Desktop\TEK-UP\football-match-prediction\data\brute")

FILES = [
    BRUTE_DIR / "seriea_rich_modern.csv",
    BRUTE_DIR / "seriea_core_all_seasons.csv",
]

def report(path: Path, subset_keys=None, top_cols=25):
    print("=" * 100)
    print("FILE:", path)
    print("=" * 100)

    df = pd.read_csv(path)
    print("Shape:", df.shape)

    # NA
    na_count = df.isna().sum()
    na_pct = (df.isna().mean() * 100).round(2)

    print("\n🕳️ Missing values (top columns):")
    tmp = pd.DataFrame({"na_count": na_count, "na_%": na_pct}).sort_values("na_count", ascending=False)
    print(tmp.head(top_cols).to_string())

    # Duplicates
    dup_all = df.duplicated().sum()
    print(f"\n🧬 Duplicate rows (all columns): {dup_all}")

    if subset_keys:
        dup_keys = df.duplicated(subset=subset_keys).sum()
        print(f"🧬 Duplicate rows (subset={subset_keys}): {dup_keys}")

        if dup_keys > 0:
            print("\n👀 Exemple de doublons (subset):")
            dups = df[df.duplicated(subset=subset_keys, keep=False)].sort_values(subset_keys)
            print(dups.head(10).to_string(index=False))

    # Petit aperçu
    print("\n👀 Head(3):")
    print(df.head(3).to_string(index=False))


if __name__ == "__main__":
    report(FILES[0], subset_keys=["Date", "HomeTeam", "AwayTeam", "Season"])  # rich
    report(FILES[1], subset_keys=["Date", "HomeTeam", "AwayTeam", "Season"])  # core
