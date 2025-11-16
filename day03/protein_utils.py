# protein_mass_utils.py
"""
Protein digestion and m/z computation utilities.
"""

# Monoisotopic amino acid masses (in Daltons)
aa_masses = {
    'A': 71.03711, 'R': 156.10111, 'N': 114.04293, 'D': 115.02694,
    'C': 103.00919, 'E': 129.04259, 'Q': 128.05858, 'G': 57.02146,
    'H': 137.05891, 'I': 113.08406, 'L': 113.08406, 'K': 128.09496,
    'M': 131.04049, 'F': 147.06841, 'P': 97.05276, 'S': 87.03203,
    'T': 101.04768, 'W': 186.07931, 'Y': 163.06333, 'V': 99.06841
}


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


def calculate_mass(sequence):
    """Calculate monoisotopic mass of a peptide sequence (Da)."""
    mass = 18.01056  # Add mass of H2O
    for aa in sequence:
        if aa not in aa_masses:
            raise ValueError(f"Unknown amino acid: {aa}")
        mass += aa_masses[aa]
    return mass


def calculate_mz(mass, charge):
    """Calculate m/z ratio for a given charge state."""
    return (mass + (charge * 1.007276)) / charge
