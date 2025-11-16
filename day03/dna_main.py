# dna_main.py
import pandas as pd
from dna_utils import (
    design_primers, calculate_volume, theoretical_yield
)

def main():
    print("\n*** DNA Primer Design Tool ***\n")
    seq = input("Enter forward DNA sequence (5'→3'): ").strip()

    try:
        res = design_primers(seq)
        print("\n--- Primer Design Results ---")
        print(f"Forward Primer: {res['forward_primer']}")
        print(f"GC%: {res['f_gc']:.2f}   Tm: {res['f_tm']:.2f}°C")
        print(f"Reverse Primer: {res['reverse_primer']}")
        print(f"GC%: {res['r_gc']:.2f}   Tm: {res['r_tm']:.2f}°C")
    except ValueError as e:
        print(f"Error: {e}")
        return

    print("\n*** PCR Calculator ***\n")
    Vfinal = float(input("Final volume per reaction (µL): "))
    n = int(input("Number of reactions: "))

    reagents = []
    total_reagent_vol = 0

    while True:
        name = input("Enter reagent (or 'done'): ")
        if name.lower() == "done":
            break

        C1 = float(input("Stock concentration: "))
        C2 = float(input("Final concentration: "))
        V1 = calculate_volume(C1, C2, Vfinal)

        reagents.append({
            "Reagent": name,
            "Vol/Reaction": V1
        })

        total_reagent_vol += V1

    water = Vfinal - total_reagent_vol
    reagents.append({"Reagent": "Water", "Vol/Reaction": water})

    df = pd.DataFrame(reagents)
    df["Total Volume"] = df["Vol/Reaction"] * n

    print("\n--- Reaction Mix ---\n")
    print(df.to_string(index=False))

    print("\n*** Theoretical PCR Yield ***")
    N0 = float(input("Initial template copies: "))
    cycles = int(input("PCR cycles: "))
    product = theoretical_yield(N0, cycles)
    print(f"Yield after {cycles} cycles: {product:.3e}")

if __name__ == "__main__":
    main()
