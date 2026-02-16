# eda/data_comprehension.py
import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def load_csv(path: Path) -> pd.DataFrame:
    # Essayes UTF-8 puis Latin-1 (souvent utile pour les datasets football)
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")


def summarize_df(df: pd.DataFrame, name: str = "data") -> None:
    print("\n" + "=" * 90)
    print(f"📄 FILE: {name}")
    print("=" * 90)

    print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")

    # Colonnes / types
    print("🧱 Columns & dtypes:")
    dtypes = df.dtypes.astype(str)
    print(pd.DataFrame({"dtype": dtypes}).T.to_string(index=True))
    print()

    # Valeurs manquantes
    na_count = df.isna().sum().sort_values(ascending=False)
    na_pct = (df.isna().mean() * 100).sort_values(ascending=False)
    missing = pd.DataFrame({"na_count": na_count, "na_%": na_pct}).query("na_count > 0")

    print("🕳️ Missing values (NA):")
    if missing.empty:
        print("✅ No missing values detected.\n")
    else:
        print(missing.to_string())
        print()

    # Doublons
    dup_rows = df.duplicated().sum()
    print(f"🧬 Duplicate rows: {dup_rows}\n")

    # Aperçu
    print("👀 Head(5):")
    print(df.head(5).to_string(index=False))
    print()

    # Statistiques numériques
    num_cols = df.select_dtypes(include="number").columns.tolist()
    if num_cols:
        print("📊 Numeric describe():")
        print(df[num_cols].describe().T.to_string())
        print()
    else:
        print("📊 Numeric describe(): (no numeric columns)\n")

    # Quelques checks utiles si colonnes classiques football-data existent
    classic_cols = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]
    existing = [c for c in classic_cols if c in df.columns]
    if existing:
        print("⚽ Classic columns present:", existing)
        # Exemple: distribution de FTR si existe
        if "FTR" in df.columns:
            print("\n🏁 Result distribution (FTR):")
            print(df["FTR"].value_counts(dropna=False).to_string())
        print()


def plot_missingness(df: pd.DataFrame, outpath: Path | None = None, title: str = "") -> None:
    na_pct = (df.isna().mean() * 100).sort_values(ascending=False)
    na_pct = na_pct[na_pct > 0]

    if na_pct.empty:
        print("✅ No missingness plot: no missing values.")
        return

    plt.figure()
    na_pct.plot(kind="bar")
    plt.ylabel("Missing %")
    plt.title(title or "Missingness by column (%)")
    plt.xticks(rotation=70, ha="right")
    plt.tight_layout()

    if outpath:
        outpath.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(outpath, dpi=150)
        print(f"🖼️ Saved missingness plot: {outpath}")
    else:
        plt.show()
    plt.close()


def iter_csv_files(target: Path) -> list[Path]:
    if target.is_file() and target.suffix.lower() == ".csv":
        return [target]
    if target.is_dir():
        return sorted(target.rglob("*.csv"))
    raise FileNotFoundError(f"Target not found: {target}")


def main():
    parser = argparse.ArgumentParser(
        description="Data comprehension (nulls, stats, duplicates) for football CSV datasets."
    )
    parser.add_argument(
        "target",
        type=str,
        help="CSV file path OR folder containing CSVs (e.g., datasets/premier-league)",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=10,
        help="Max number of CSV files to analyze (when target is a folder).",
    )
    parser.add_argument(
        "--plots",
        action="store_true",
        help="Generate missingness plots (saved into ./eda_outputs/).",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    files = iter_csv_files(target)
    if target.is_dir():
        files = files[: args.max_files]

    print(f"🔎 Found {len(files)} CSV file(s).")

    out_dir = Path("eda_outputs").resolve()

    for f in files:
        df = load_csv(f)
        summarize_df(df, name=str(f))

        if args.plots:
            safe_name = f.name.replace(".csv", "")
            plot_missingness(
                df,
                outpath=out_dir / f"missingness_{safe_name}.png",
                title=f"Missingness - {f.name}",
            )


if __name__ == "__main__":
    main()
