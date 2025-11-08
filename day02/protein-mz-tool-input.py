# Protein Digestion and m/z Calculator
# This tool digests a protein sequence using specified enzymes and calculates the m/z values of resulting peptides.

import pandas as pd

# Monoisotopic amino acid masses library (in Daltons)
aa_masses = {
    'A': 71.03711, 'R': 156.10111, 'N': 114.04293, 'D': 115.02694,
    'C': 103.00919, 'E': 129.04259, 'Q': 128.05858, 'G': 57.02146,
    'H': 137.05891, 'I': 113.08406, 'L': 113.08406, 'K': 128.09496,
    'M': 131.04049, 'F': 147.06841, 'P': 97.05276, 'S': 87.03203,
    'T': 101.04768, 'W': 186.07931, 'Y': 163.06333, 'V': 99.06841
}

# Enzyme digestion functions
def digest_trypsin(sequence):
    """Trypsin cleaves after K or R (except when followed by P)."""
    peptides, current = [], ""
    for i, aa in enumerate(sequence):
        current += aa
        if aa in ['K', 'R'] and not (i + 1 < len(sequence) and sequence[i + 1] == 'P'):
            peptides.append(current)
            current = ""
    if current:
        peptides.append(current)
    return peptides

def digest_chymotrypsin(sequence):
    """Chymotrypsin cleaves after F, W, or Y (except when followed by P)."""
    peptides, current = [], ""
    for i, aa in enumerate(sequence):
        current += aa
        if aa in ['F', 'W', 'Y'] and not (i + 1 < len(sequence) and sequence[i + 1] == 'P'):
            peptides.append(current)
            current = ""
    if current:
        peptides.append(current)
    return peptides

# Mass and m/z calculations
def calculate_mass(sequence):
    """Calculate monoisotopic mass of a peptide sequence (Da)."""
     # 1.007276 Da = proton mass
    mass = 18.01056  # + H2O
    for aa in sequence:
        if aa not in aa_masses:
            raise ValueError(f"Unknown amino acid: {aa}")
        mass += aa_masses[aa]
    return mass

def calculate_mz(mass, charge):
    """Calculate m/z ratio for a given charge state."""
    return (mass + (charge * 1.007276)) / charge

def main():
    print("\n*** Protein Digestion & m/z Calculator ***\n")

    # Step 1: Get user input
    protein = input("Enter protein sequence (single-letter code): ").strip().upper()
    enzyme = input("Enter enzyme (trypsin / chymotrypsin): ").strip().lower()

    if not protein or enzyme not in ["trypsin", "chymotrypsin"]:
        print("\nInvalid input. Please provide a valid sequence and enzyme.")
        return

    # Step 2: Digest sequence based on enzyme choice
    if enzyme == "trypsin":
        peptides = digest_trypsin(protein)
    else:
        peptides = digest_chymotrypsin(protein)

    # Step 3: Compute properties for charges 1+, 2+, 3+
    data = []
    for pep in peptides:
        mass = calculate_mass(pep)
        mz_values = [calculate_mz(mass, z) for z in (1, 2, 3)]
        data.append([pep, len(pep), round(mass, 4), *[round(mz, 4) for mz in mz_values]])

    # Step 4: Display peptides and m/z values
    df = pd.DataFrame(
        data,
        columns=["Peptide", "Length", "Mass (Da)", "m/z (+1)", "m/z (+2)", "m/z (+3)"]
    )

    print("\n=== Cleaved Peptides and m/z Values ===\n")
    print(df.to_string(index=False))
    print(f"\nDigestion complete — {len(peptides)} peptides generated.\n")

# Run
if __name__ == "__main__":
    main()