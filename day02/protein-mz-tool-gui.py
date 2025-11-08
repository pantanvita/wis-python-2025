# Protein Digestion and m/z Calculator
# This tool digests a protein sequence using specified enzymes and calculates the m/z values of resulting peptides.

# Monoisotopic amino acid masses library (in Daltons)
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# === Monoisotopic amino acid masses (in Daltons) ===
aa_masses = {
    'A': 71.03711, 'R': 156.10111, 'N': 114.04293, 'D': 115.02694,
    'C': 103.00919, 'E': 129.04259, 'Q': 128.05858, 'G': 57.02146,
    'H': 137.05891, 'I': 113.08406, 'L': 113.08406, 'K': 128.09496,
    'M': 131.04049, 'F': 147.06841, 'P': 97.05276, 'S': 87.03203,
    'T': 101.04768, 'W': 186.07931, 'Y': 163.06333, 'V': 99.06841
}

# Enzyme digestion functions
def digest_trypsin(sequence):
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
    mass = 18.01056  # + H2O
    for aa in sequence:
        if aa not in aa_masses:
            raise ValueError(f"Unknown amino acid: {aa}")
        mass += aa_masses[aa]
    return mass

def calculate_mz(mass, charge):
    return (mass + (charge * 1.007276)) / charge

# GUI Application
class ProteinDigestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Protein Digestion & m/z Calculator")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Input frame
        input_frame = ttk.LabelFrame(root, text="Input Protein & Enzyme", padding=10)
        input_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(input_frame, text="Protein Sequence (single-letter code):").grid(row=0, column=0, sticky='w')
        self.seq_entry = tk.Text(input_frame, width=80, height=4)
        self.seq_entry.grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Label(input_frame, text="Select Enzyme:").grid(row=2, column=0, sticky='w')
        self.enzyme_var = tk.StringVar(value="trypsin")
        ttk.Combobox(input_frame, textvariable=self.enzyme_var, values=["trypsin", "chymotrypsin"], state="readonly").grid(row=2, column=1, sticky='w')

        ttk.Button(input_frame, text="Digest Protein & Calculate m/z", command=self.digest_protein).grid(row=3, column=0, columnspan=2, pady=10)

        # Output frame
        self.output_frame = ttk.LabelFrame(root, text="Cleaved Peptides and m/z", padding=10)
        self.output_frame.pack(padx=10, pady=10, fill='both', expand=True)

        columns = ["Peptide", "Length", "Mass (Da)", "m/z (+1)", "m/z (+2)", "m/z (+3)"]
        self.tree = ttk.Treeview(self.output_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='center')
        self.tree.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(self.output_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

    def digest_protein(self):
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)

        sequence = self.seq_entry.get("1.0", tk.END).strip().upper()
        enzyme = self.enzyme_var.get().lower()

        if not sequence:
            messagebox.showwarning("Input Error", "Please enter a protein sequence.")
            return

        try:
            if enzyme == "trypsin":
                peptides = digest_trypsin(sequence)
            else:
                peptides = digest_chymotrypsin(sequence)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        data = []
        for pep in peptides:
            try:
                mass = calculate_mass(pep)
                mz_values = [calculate_mz(mass, z) for z in (1, 2, 3)]
                data.append([pep, len(pep), round(mass,4), round(mz_values[0],4), round(mz_values[1],4), round(mz_values[2],4)])
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
                return

        # Insert data into treeview
        for row in data:
            self.tree.insert("", "end", values=row)

        messagebox.showinfo("Done", f"Digestion complete — {len(peptides)} peptides generated.")

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ProteinDigestGUI(root)
    root.mainloop()