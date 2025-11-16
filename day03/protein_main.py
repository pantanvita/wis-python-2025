# main.py
import pandas as pd
from protein_utils import (
    digest_trypsin,
    digest_chymotrypsin,
    calculate_mass,
    calculate_mz
)

def main():
    print("\n*** Protein Digestion & m/z Calculator ***\n")

    # Step 1: Get user input
    protein = input("Enter protein sequence (single-letter code): ").strip().upper()
    enzyme = input("Enter enzyme (trypsin / chymotrypsin): ").strip().lower()

    if not protein or enzyme not in ["trypsin", "chymotrypsin"]:
        print("\nInvalid input. Please provide a valid sequence and enzyme.")
        return

    # Step 2: Digest based on enzyme
    if enzyme == "trypsin":
        peptides = digest_trypsin(protein)
    else:
        peptides = digest_chymotrypsin(protein)

    # Step 3: Compute peptide masses and m/z
    data = []
    for pep in peptides:
        mass = calculate_mass(pep)
        mz_values = [calculate_mz(mass, z) for z in (1, 2, 3)]
        data.append([pep, len(pep), round(mass, 4), *[round(mz, 4) for mz in mz_values]])

    # Step 4: Display results
    df = pd.DataFrame(
        data,
        columns=["Peptide", "Length", "Mass (Da)", "m/z (+1)", "m/z (+2)", "m/z (+3)"]
    )

    print("\n=== Cleaved Peptides and m/z Values ===\n")
    print(df.to_string(index=False))
    print(f"\nDigestion complete — {len(peptides)} peptides generated.\n")


if __name__ == "__main__":
    main()
