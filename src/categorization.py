import pandas as pd
import os

# =============================================================================
# XTMA — Categorization Script
# -----------------------------------------------------------------------------
# Reads a monthly transaction file (Excel) and categorizes each transaction
# based on a keyword reference file (Référentiel.xlsx).
#
# Special rule: keywords flagged as duplicates across categories are resolved
# by amount threshold — above THRESHOLD → Transport, below → Food & Dining.
#
# Note on amounts: in US bank statements, negative = Entrée (inflow),
# positive = Sortie (outflow).
# =============================================================================


# --- CONFIGURATION -----------------------------------------------------------

CAT_TRANSPORT = "Travel_Expenses_Transport"
CAT_FOOD      = "Travel_Expenses_Food&Dining"
THRESHOLD     = 100.0  # USD — amount above which a duplicate keyword → Transport


# --- LOAD REFERENCE FILE -----------------------------------------------------
# The reference file (Référentiel.xlsx) maps keywords to categories.
# Each column header = one category.
# Each value in a column = a keyword to match in transaction descriptions.

df_ref = pd.read_excel("Référentiel.xlsx")
df_ref.columns = df_ref.columns.astype(str).str.strip()

categories_dict = {}        # { category_name: [keyword1, keyword2, ...] }
duplicate_keywords = set()  # keywords appearing in more than one category
all_keywords = {}           # { keyword: first_category_found } — duplicate detection

for col in df_ref.columns:
    if "Unnamed" not in col:
        keywords = df_ref[col].dropna().astype(str).str.upper().tolist()
        categories_dict[col] = keywords
        for kw in keywords:
            if kw in all_keywords:
                duplicate_keywords.add(kw)
            all_keywords[kw] = col

print(f"Duplicate keywords detected (resolved by amount rule): {duplicate_keywords}")


# --- CATEGORIZATION FUNCTION -------------------------------------------------

def categorize(description, amount):
    """
    Categorizes a single transaction.

    Step A: If the description contains a duplicate keyword, apply the
            amount threshold rule to resolve the ambiguity.
    Step B: Otherwise, match against the reference file left-to-right.
            Column order in Référentiel.xlsx defines priority.

    Amount convention (US bank statements):
        negative amount = Entrée (inflow — money coming into the account)
        positive amount = Sortie (outflow — money leaving the account)

    Returns:
        category (str): matched category name or 'NON_CLASSE'
        keyword_source (str): keyword that triggered the match or 'AUCUN'
    """
    desc  = str(description).upper()
    value = abs(float(amount))

    # Step A — Duplicate keyword resolution
    for kw in duplicate_keywords:
        if kw in desc:
            if value > THRESHOLD:
                return CAT_TRANSPORT, f"{kw} (> {THRESHOLD}$)"
            else:
                return CAT_FOOD, f"{kw} (<= {THRESHOLD}$)"

    # Step B — Standard reference file lookup
    for cat, keywords in categories_dict.items():
        for kw in keywords:
            if kw in desc:
                return cat, kw

    return "NON_CLASSE", "AUCUN"


# --- PROCESSING --------------------------------------------------------------

filename = input("Transaction file to process (.xlsx): ")

if not os.path.exists(filename):
    print(f"File not found: {filename}")
else:
    df = pd.read_excel(filename)
    df.columns = df.columns.astype(str).str.strip()

    # Apply categorization to each row
    results = df.apply(lambda row: categorize(row['Description'], row['Montant']), axis=1)
    df[['Categorie', 'Mot_Cle_Source']] = pd.DataFrame(results.tolist(), index=df.index)

    # Add In/Out column
    # Note: in US bank statements, negative amounts = Entrée (inflow)
    # and positive amounts = Sortie (outflow)
    df['Type'] = df['Montant'].apply(lambda x: "Entrée" if x < 0 else "Sortie")

    # --- CHECKPOINTS ---------------------------------------------------------
    total_rows   = len(df)
    unclassified = len(df[df['Categorie'] == 'NON_CLASSE'])
    total_amount = df['Montant'].sum()

    output_filename = "Auto_Regle_" + os.path.basename(filename)
    df.to_excel(output_filename, index=False)

    print("-" * 50)
    print(f"File processed : {output_filename}")
    print(f"Total rows     : {total_rows}")
    print(f"Unclassified   : {unclassified} ({round(unclassified/total_rows*100, 1)}%)")
    print(f"Total amount   : {total_amount:.2f}")
    print(f"Threshold rule : duplicates resolved at {THRESHOLD}$")
    print("-" * 50)
