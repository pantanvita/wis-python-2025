# This is a DNA primer design tool and PCR reagents calculator

import argparse
import pandas as pd

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
    """Design primers ensuring GC%, Tm, and Tm difference constraints."""
    forward_strand = forward_strand.upper().replace(" ", "").replace("\n", "")

    if len(forward_strand) < primer_length * 2:
        raise ValueError("Sequence too short for primer design.")

    for start in range(0, len(forward_strand) - primer_length * 2):
        forward_primer = forward_strand[start:start + primer_length]
        reverse_primer = reverse_complement(forward_strand[-(start + primer_length):-start if start != 0 else None])

        f_gc = gc_content(forward_primer)
        r_gc = gc_content(reverse_primer)
        f_tm = calculate_tm(forward_primer)
        r_tm = calculate_tm(reverse_primer)

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
    """Calculate volume (V1) using C1V1 = C2V2."""
    return (C2 * V2) / C1

# To calculate theoretical yield after n cycles
def theoretical_yield(N0, cycles):
    """Calculate theoretical PCR yield: N = N0 × 2^n"""
    return N0 * (2 ** cycles)

def main():
    parser = argparse.ArgumentParser(
        description="DNA Primer Design Tool and PCR Reagent Calculator"
    )

    # Primer Design arguments
    parser.add_argument(
        "--sequence",
        help="DNA sequence (5'→3') for primer design"
    )
    parser.add_argument(
        "--primer_length",
        type=int,
        default=20,
        help="Primer length (default: 20)"
    )

    # PCR Calculator arguments
    parser.add_argument(
        "--final_volume",
        type=float,
        help="Final reaction volume per tube (µL)"
    )
    parser.add_argument(
        "--num_reactions",
        type=int,
        default=1,
        help="Number of reactions (default: 1)"
    )
    parser.add_argument(
        "--reagents",
        nargs="+",
        help="List of reagents in the format name:C1:C2 (example: Buffer:10:1 MgCl2:25:1.5)"
    )
    parser.add_argument(
        "--N0",
        type=float,
        help="Initial number of DNA template copies (for theoretical yield)"
    )
    parser.add_argument(
        "--cycles",
        type=int,
        help="Number of PCR cycles"
    )

    args = parser.parse_args()

    # Part A: Primer Design
    if args.sequence:
        print("\n*** DNA Primer Design Results ***")
        try:
            result = design_primers(args.sequence, args.primer_length)
            print(f"Forward Primer (5'→3'): {result['forward_primer']}")
            print(f"  GC%: {result['f_gc']:.2f}%  |  Tm: {result['f_tm']:.2f}°C")
            print(f"Reverse Primer (5'→3'): {result['reverse_primer']}")
            print(f"  GC%: {result['r_gc']:.2f}%  |  Tm: {result['r_tm']:.2f}°C")
        except ValueError as e:
            print(f"Error {e}")

    # Part B: PCR Reagents Calculator
    if args.final_volume and args.reagents:
        print("\n*** PCR Reagents Calculator ***\n")

        reagents = []
        total_reagent_vol = 0

        for item in args.reagents:
            try:
                name, C1, C2 = item.split(":")
                C1, C2 = float(C1), float(C2)
                V1 = calculate_volume(C1, C2, args.final_volume)
                reagents.append({
                    "Reagent": name,
                    "Stock Conc. (C1)": C1,
                    "Final Conc. (C2)": C2,
                    "Vol/Reaction (µL)": V1
                })
                total_reagent_vol += V1
            except Exception:
                print(f"Skipping invalid reagent format: {item}")
                continue

        water_vol = args.final_volume - total_reagent_vol
        reagents.append({
            "Reagent": "Nuclease-free Water",
            "Stock Conc. (C1)": "—",
            "Final Conc. (C2)": "—",
            "Vol/Reaction (µL)": water_vol
        })

        for r in reagents:
            if isinstance(r["Vol/Reaction (µL)"], (int, float)):
                r["Total Vol (µL)"] = r["Vol/Reaction (µL)"] * args.num_reactions
            else:
                r["Total Vol (µL)"] = "—"

        df = pd.DataFrame(reagents, columns=[
            "Reagent", "Stock Conc. (C1)", "Final Conc. (C2)",
            "Vol/Reaction (µL)", "Total Vol (µL)"
        ])

        print("\n*** PCR Reaction Setup Summary ***\n")
        print(df.to_string(index=False))

        total_master_mix = args.final_volume * args.num_reactions
        print(f"\nTotal per reaction: {args.final_volume:.2f} µL")
        print(f"Total master mix volume: {total_master_mix:.2f} µL")

        if args.N0 and args.cycles:
            yield_val = theoretical_yield(args.N0, args.cycles)
            print(f"\n*** Theoretical PCR Yield ***")
            print(f"Initial copies (N₀): {args.N0:.2e}")
            print(f"After {args.cycles} cycles: {yield_val:.3e} copies")

    print("\nCalculation complete.")


if __name__ == "__main__":
    main()