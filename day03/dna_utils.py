# dna_utils.py
from Bio.Seq import Seq
from Bio.SeqUtils import MeltingTemp as mt
from Bio.SeqUtils import gc_fraction

def reverse_complement(seq: str) -> str:
    """Return reverse complement using BioPython."""
    return str(Seq(seq).reverse_complement()).upper()

def gc_content(seq: str) -> float:
    """Return GC% using BioPython."""
    return gc_fraction(seq) * 100

def calculate_tm(seq: str) -> float:
    """Return melting temperature using BioPython's Wallace rule."""
    return mt.Tm_Wallace(seq)

def design_primers(forward_strand: str, primer_length: int = 20):
    """
    Design forward & reverse primers using real thermodynamic values.
    """
    seq = forward_strand.upper().replace(" ", "").replace("\n", "")
    L = len(seq)

    if L < primer_length * 2:
        raise ValueError("Sequence too short for primer design.")

    for i in range(0, L - 2 * primer_length):
        fwd = seq[i:i + primer_length]
        rev_region = seq[-(i + primer_length): L - i]
        rev = reverse_complement(rev_region)

        f_gc = gc_content(fwd)
        r_gc = gc_content(rev)
        f_tm = calculate_tm(fwd)
        r_tm = calculate_tm(rev)

        if (
            40 <= f_gc <= 60 and
            40 <= r_gc <= 60 and
            55 <= f_tm <= 65 and
            55 <= r_tm <= 65 and
            abs(f_tm - r_tm) <= 10
        ):
            return {
                "forward_primer": fwd,
                "reverse_primer": rev,
                "f_gc": f_gc,
                "r_gc": r_gc,
                "f_tm": f_tm,
                "r_tm": r_tm,
            }

    raise ValueError("No suitable primers found meeting all constraints.")


def calculate_volume(C1, C2, V2):
    """C1V1 = C2V2"""
    return (C2 * V2) / C1

def theoretical_yield(N0, cycles):
    """Theoretical PCR yield: N = N0 × 2^n"""
    return N0 * (2 ** cycles)
