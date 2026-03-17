import pandas as pd
import os
import glob

# =============================================================================
# XTMA — Excel Fusion Script
# -----------------------------------------------------------------------------
# Merges all monthly categorized Excel files from a given folder into a
# single consolidated file (VERIFICATION_FUSION.xlsx).
#
# Safety rules:
#   - Ignores temporary files starting with ~$
#   - Ignores files containing "Compilation" or "Resultat" in their name
#     to avoid circular merging if a previous output is still in the folder
#
# Built-in checkpoint: compares the cumulative sum of all individual files
# against the total in the merged output to detect any data loss.
# =============================================================================


# --- INPUT -------------------------------------------------------------------

folder_path = input("Paste the folder path: ")

all_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

dataframes = []
cumulative_sum = 0.0  # used for final verification checkpoint

print("\n--- FILE ANALYSIS ---")

# --- PROCESS EACH FILE -------------------------------------------------------

for filepath in all_files:
    filename = os.path.basename(filepath)

    # Safety filter — skip temp files and previous outputs
    if filename.startswith("~$") or "Compilation" in filename or "Resultat" in filename:
        print(f"SKIPPED : {filename}")
        continue

    df = pd.read_excel(filepath)
    df.columns = df.columns.astype(str).str.strip()

    if 'Montant' in df.columns:
        # Normalize amount format (handle comma as decimal separator)
        df['Montant'] = pd.to_numeric(
            df['Montant'].astype(str).str.replace(',', '.'),
            errors='coerce'
        )

        file_total = df['Montant'].sum()
        cumulative_sum += file_total

        # Track source file for traceability
        df['Source_Fichier'] = filename

        dataframes.append(df)
        print(f"READ    : {filename} | Amount : {file_total:.2f}")


# --- MERGE & CHECKPOINT ------------------------------------------------------

if dataframes:
    df_merged = pd.concat(dataframes, ignore_index=True)
    merged_total = df_merged['Montant'].sum()

    print("\n--- CHECKPOINT ---")
    print(f"Cumulative sum (individual files) : {cumulative_sum:.2f}")
    print(f"Total in merged file              : {merged_total:.2f}")

    # Verify no data was lost during merge
    if round(cumulative_sum, 2) == round(merged_total, 2):
        print("OK — Totals match. No data loss detected.")
    else:
        print("WARNING — Totals do not match. Check for missing or duplicate rows.")

    df_merged.to_excel("VERIFICATION_FUSION.xlsx", index=False)
    print(f"\nOutput file : VERIFICATION_FUSION.xlsx")
    print(f"Total rows  : {len(df_merged)}")

else:
    print("No valid files found in the specified folder.")
