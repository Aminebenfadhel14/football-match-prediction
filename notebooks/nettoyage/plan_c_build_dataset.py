from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # adapte si besoin
DATASET_DIR = PROJECT_ROOT / "data" / "Scrapping" / "football-datasets-main" / "football-datasets-main" / "datasets" / "serie-a"
OUT_DIR = PROJECT_ROOT / "data" / "brute"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# on prend uniquement les fichiers de saison
files = sorted(DATASET_DIR.glob("season-*.csv"))

print("DATASET_DIR =", DATASET_DIR)
print("Nb fichiers trouvés =", len(files))
print("Exemples =", [f.name for f in files[:5]])
assert len(files) > 0, "❌ Aucun fichier trouvé. Vérifie le chemin."

def season_from_filename(p: Path) -> str:
    # season-1617.csv -> 2016-2017
    s = p.stem.replace("season-", "")
    if len(s) == 4 and s.isdigit():
        return f"20{s[:2]}-20{s[2:]}"
    return s

dfs = []
for f in files:
    df = pd.read_csv(f)
    df.columns = [c.strip() for c in df.columns]
    df["Season"] = season_from_filename(f)

    # parsing date robuste
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%y", errors="coerce")
    mask = df["Date"].isna()
    if mask.any():
        df.loc[mask, "Date"] = pd.to_datetime(df.loc[mask, "Date"], format="%d/%m/%Y", errors="coerce")

    before = len(df)
    df = df.dropna(subset=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"])
    print(f"{f.name}: {before} -> {len(df)} lignes après nettoyage")

    dfs.append(df)

df_all = pd.concat(dfs, ignore_index=True)
print("TOTAL =", df_all.shape)

# CORE
core_cols = ["Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","Season"]
df_core = df_all[core_cols].copy()

# RICH (modern only = saisons où stats existent bien)
rich_cols = core_cols + ["HS","AS","HST","AST","HF","AF","HC","AC","HY","AY","HR","AR"]
df_rich = df_all.dropna(subset=["HS","AS","HST","AST","HF","AF","HC","AC","HY","AY","HR","AR"])[rich_cols].copy()

core_path = OUT_DIR / "seriea_core_all_seasons.csv"
rich_path = OUT_DIR / "seriea_rich_modern.csv"

df_core.to_csv(core_path, index=False)
df_rich.to_csv(rich_path, index=False)

print("✅ CORE saved:", core_path, "rows=", len(df_core))
print("✅ RICH saved:", rich_path, "rows=", len(df_rich))
