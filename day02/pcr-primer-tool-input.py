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

def main():
    print("*** This is a DNA primers designing tool and PCR reagents calculator ***\n")
    print("*** Tool to calculate DNA primers from a given DNA sequence ***\n")
    dna_seq = input("Enter the forward DNA strand (5' → 3'): ").strip()

    try:
        result = design_primers(dna_seq, primer_length=20)
        print("\n*** Primer Design Results ***")
        print(f"Forward Primer (5'→3'): {result['forward_primer']}")
        print(f"  GC%: {result['f_gc']:.2f}%  |  Tm: {result['f_tm']:.2f}°C")
        print(f"Reverse Primer (5'→3'): {result['reverse_primer']}")
        print(f"  GC%: {result['r_gc']:.2f}%  |  Tm: {result['r_tm']:.2f}°C")
    except ValueError as e:
        print(f"\nError {e}")

if __name__ == "__main__":
    main()


# Part B: Compute PCR calculations
# This part of the code deals with computing PCR reagent calculations

import pandas as pd

# To calculate volumes of reagents needed for PCR master mix
def calculate_volume(C1, C2, V2):
    """Calculate volume (V1) needed using C1V1 = C2V2."""
    return (C2 * V2) / C1

# To calculate theoretical yield after n cycles
def theoretical_yield(N0, cycles):
    """Calculate theoretical PCR yield: N = N0 × 2^n"""
    return N0 * (2 ** cycles)

def main():
    print("*** PCR Reagents Calculator ***\n")

    # 1st part: User inputs
    Vfinal = float(input("Enter final reaction volume per tube (µL): "))
    n_reactions = int(input("Enter number of reactions: "))

    reagents = []
    total_reagent_vol = 0

    # 2nd part: Allow user to enter reagents and conc and volumes
    print("\nEnter reagent details one by one. Type 'done' when finished.\n")
    print("\nCAUTION: This tool is designed for calculations based on same units. Enter the same units for intial and final concentrations.\n")

    while True:
        name = input("Reagent name (or type 'done' to finish): ").strip()
        if name.lower() == "done":
            break
        try:
            C1 = float(input(f"Enter stock concentration of {name} (accepted units: X, mM, µM): "))
            C2 = float(input(f"Enter desired final concentration of {name} (accepted units: X, mM, µM): "))
            V1 = calculate_volume(C1, C2, Vfinal)
            reagents.append({
                "Reagent": name,
                "Stock Conc. (C1)": C1,
                "Final Conc. (C2)": C2,
                "Vol/Reaction (µL)": V1
            })
            total_reagent_vol += V1
        except ValueError:
            print("Invalid entry. Please enter numeric values for concentrations.")
            continue

    # 3rd part: Calculate nuclease-free water volume
    water_vol = Vfinal - total_reagent_vol
    if water_vol < 0:
        print("\nERROR: Total reagent volume exceeds final reaction volume. Please check inputs.")
        return
    reagents.append({
        "Reagent": "Nuclease-free Water",
        "Stock Conc. (C1)": "—",
        "Final Conc. (C2)": "—",
        "Vol/Reaction (µL)": water_vol
    })

    # 4th part: Calculate total volumes for all reactions
    for r in reagents:
        if isinstance(r["Vol/Reaction (µL)"], (int, float)):
            r["Total Vol (µL)"] = r["Vol/Reaction (µL)"] * n_reactions
        else:
            r["Total Vol (µL)"] = "—"

    # 5th part: Display the pandas table
    df = pd.DataFrame(reagents, columns=[
        "Reagent", "Stock Conc. (C1)", "Final Conc. (C2)",
        "Vol/Reaction (µL)", "Total Vol (µL)"
    ])

    print("\n*** PCR Reaction Setup Summary ***\n")
    print(df.to_string(index=False))

    print("\n*** Summary ***")
    print(f"Total per reaction: {Vfinal:.2f} µL")
    total_master_mix = Vfinal * n_reactions
    print(f"Total master mix volume (with % loss): {total_master_mix:.2f} µL")

    # 6th part: Theoretical PCR yield
    print("\n*** Theoretical PCR Yield ***")
    try:
        N0 = float(input("Enter initial number of template copies (N₀): "))
        cycles = int(input("Enter number of PCR cycles (n): "))
        N = theoretical_yield(N0, cycles)
        print(f"Theoretical product copies after {cycles} cycles: {N:.3e}")
    except ValueError:
        print("Skipped theoretical yield calculation (invalid input).")

    print("\nCalculation complete.")

if __name__ == "__main__":
    main()
