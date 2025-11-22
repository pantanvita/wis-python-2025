# This is a DNA primer design tool and PCR reagents calculator

# Part A: DNA Primer Design Tool
# This code designs forward and reverse primers from a given DNA sequence
# while ensuring they meet specific GC content and melting temperature (Tm) constraints

# 1st part: defines complement combinations (ATGC), converts lower case input seq to uppercase (in case user inputs lower case letters) and joins the sequence in reverse order
def reverse_complement(seq):
    """Return the reverse complement of a DNA sequence."""
    complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
    return ''.join(complement[base] for base in reversed(seq.upper()))

# 2nd part: defines GC% by counting G and C and then diving the sum by the length of the seq
def gc_content(seq):
    """Calculate GC% of a DNA sequence."""
    g = seq.count('G')
    c = seq.count('C')
    gc_percent = ((g + c) / len(seq)) * 100
    return gc_percent

# 3rd part: defines melting temp by applying Wallace rule
# Wallace rule: Tm = 2°C × (A+T) + 4°C × (G+C)
def calculate_tm(seq):
    """Calculate melting temperature (Tm) using the Wallace rule."""
    a = seq.count('A')
    t = seq.count('T')
    g = seq.count('G')
    c = seq.count('C')
    tm = 2 * (a + t) + 4 * (g + c)
    return tm

# 4th part: designs primers
def design_primers(forward_strand, primer_length=20):
    """
    Design forward and reverse primers ensuring:
    - Primer length = 20 bp
    - GC% between 40-60%
    - Tm between 55-65°C
    - Tm difference <= 5°C
    """
    forward_strand = forward_strand.upper().replace(" ", "").replace("\n", "")

# 5th part: To check if sequence length is long enough (not shorter than both fwd and rev primers themselves)
    if len(forward_strand) < primer_length * 2:
        raise ValueError("Sequence too short for primer design.")

    for start in range(0, len(forward_strand) - primer_length * 2):
        # Take possible forward and reverse primers
        forward_primer = forward_strand[start:start + primer_length]
        reverse_primer = reverse_complement(forward_strand[-(start + primer_length):-start if start != 0 else None])

        # Calculate GC% and Tm for both primers
        f_gc = gc_content(forward_primer)
        r_gc = gc_content(reverse_primer)
        f_tm = calculate_tm(forward_primer)
        r_tm = calculate_tm(reverse_primer)

        # Check constraints
        if (40 <= f_gc <= 60 and 40 <= r_gc <= 60 and
            55 <= f_tm <= 65 and 55 <= r_tm <= 65 and
            abs(f_tm - r_tm) <= 5):
            return {
                "forward_primer": forward_primer,
                "reverse_primer": reverse_primer,
                "f_gc": f_gc, "r_gc": r_gc,
                "f_tm": f_tm, "r_tm": r_tm
            }

    raise ValueError("No suitable primers found meeting all constraints.")

# Part B: Compute PCR calculations
# This part of the code deals with computing PCR reagent calculations

# To calculate volumes of reagents needed for PCR master mix
def calculate_volume(C1, C2, V2):
    """Calculate volume (V1) needed using C1V1 = C2V2."""
    return (C2 * V2) / C1

# To calculate theoretical yield after n cycles
def theoretical_yield(N0, cycles):
    """Calculate theoretical PCR yield: N = N0 × 2^n"""
    return N0 * (2 ** cycles)