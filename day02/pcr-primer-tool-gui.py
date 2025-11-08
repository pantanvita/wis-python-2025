# This is a DNA primer design tool and PCR reagents calculator

# Part A: DNA Primer Design Tool
# This code designs forward and reverse primers from a given DNA sequence
# while ensuring they meet specific GC content and melting temperature (Tm) constraints

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# 1st part: defines complement combinations (ATGC), converts lower case input seq to uppercase (in case user inputs lower case letters) and joins the sequence in reverse order
def reverse_complement(seq):
    complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
    return ''.join(complement[base] for base in reversed(seq.upper()))

# 2nd part: defines GC% by counting G and C and then diving the sum by the length of the seq
def gc_content(seq):
    g = seq.count('G')
    c = seq.count('C')
    return ((g + c) / len(seq)) * 100

# 3rd part: defines melting temp by applying Wallace rule
# Wallace rule: Tm = 2°C × (A+T) + 4°C × (G+C)
def calculate_tm(seq):
    a = seq.count('A')
    t = seq.count('T')
    g = seq.count('G')
    c = seq.count('C')
    return 2 * (a + t) + 4 * (g + c)

# 4th part: designs primers and check if sequence length is long enough (not shorter than both fwd and rev primers themselves)
def design_primers(forward_strand, primer_length=20):
    forward_strand = forward_strand.upper().replace(" ", "").replace("\n", "")
    if len(forward_strand) < primer_length * 2:
        raise ValueError("Sequence too short for primer design.")

    for start in range(0, len(forward_strand) - primer_length * 2):
        forward_primer = forward_strand[start:start + primer_length]
        reverse_primer = reverse_complement(forward_strand[-(start + primer_length):-start if start != 0 else None])
        f_gc, r_gc = gc_content(forward_primer), gc_content(reverse_primer)
        f_tm, r_tm = calculate_tm(forward_primer), calculate_tm(reverse_primer)
        if (40 <= f_gc <= 60 and 40 <= r_gc <= 60 and 55 <= f_tm <= 65 and 55 <= r_tm <= 65 and abs(f_tm - r_tm) <= 5):
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
    return (C2 * V2) / C1

# To calculate theoretical yield after n cycles
def theoretical_yield(N0, cycles):
    return N0 * (2 ** cycles)

# GUI Application
class PCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DNA Primer Design & PCR Calculator")
        self.root.geometry("950x750")
        self.root.resizable(False, False)

        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        self.primer_frame = ttk.Frame(notebook)
        self.pcr_frame = ttk.Frame(notebook)
        notebook.add(self.primer_frame, text="Primer Design Tool")
        notebook.add(self.pcr_frame, text="PCR Master Mix Calculator")

        self.create_primer_tab()
        self.create_pcr_tab()

    # Primer Design Tab
    def create_primer_tab(self):
        ttk.Label(self.primer_frame, text="Enter Forward DNA Strand (5'→3'):", font=('Arial', 12)).pack(pady=10)
        self.seq_entry = tk.Text(self.primer_frame, width=80, height=5)
        self.seq_entry.pack(pady=10)

        ttk.Button(self.primer_frame, text="Design Primers", command=self.run_primer_design).pack(pady=10)

        self.primer_output = tk.Text(self.primer_frame, width=90, height=12, state='disabled')
        self.primer_output.pack(pady=10)

    def run_primer_design(self):
        dna_seq = self.seq_entry.get("1.0", tk.END).strip()
        if not dna_seq:
            messagebox.showwarning("Input Error", "Please enter a DNA sequence.")
            return

        self.primer_output.config(state='normal')
        self.primer_output.delete("1.0", tk.END)

        try:
            result = design_primers(dna_seq)
            # Display results with color highlighting
            self.display_primer_result(result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

        self.primer_output.config(state='disabled')

    def display_primer_result(self, result):
        f_gc, r_gc = result["f_gc"], result["r_gc"]
        f_tm, r_tm = result["f_tm"], result["r_tm"]

        self.primer_output.insert(tk.END, "Forward Primer (5'→3'): ", 'bold')
        self.primer_output.insert(tk.END, f"{result['forward_primer']}\n")
        self.insert_validated_value(f"  GC%: {f_gc:.2f}%  |  Tm: {f_tm:.2f}°C\n", 40 <= f_gc <= 60, 55 <= f_tm <= 65)

        self.primer_output.insert(tk.END, "\nReverse Primer (5'→3'): ", 'bold')
        self.primer_output.insert(tk.END, f"{result['reverse_primer']}\n")
        self.insert_validated_value(f"  GC%: {r_gc:.2f}%  |  Tm: {r_tm:.2f}°C\n", 40 <= r_gc <= 60, 55 <= r_tm <= 65)

        # Warn if large Tm difference
        if abs(f_tm - r_tm) > 5:
            self.primer_output.insert(tk.END, "\n Warning: Tm difference between primers exceeds 5°C.\n", 'warn')

        # Style tags
        self.primer_output.tag_configure('bold', font=('Arial', 10, 'bold'))
        self.primer_output.tag_configure('ok', foreground='green')
        self.primer_output.tag_configure('bad', foreground='red')
        self.primer_output.tag_configure('warn', foreground='orange')

    def insert_validated_value(self, text, gc_ok, tm_ok):
        # If either GC% or Tm invalid, mark red
        if not gc_ok or not tm_ok:
            self.primer_output.insert(tk.END, text, 'bad')
        else:
            self.primer_output.insert(tk.END, text, 'ok')

    # PCR Calculator Tab
    def create_pcr_tab(self):
        ttk.Label(self.pcr_frame, text="PCR Reaction Setup", font=('Arial', 14, 'bold')).pack(pady=10)

        input_frame = ttk.Frame(self.pcr_frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Final Volume per Reaction (µL):").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text="Number of Reactions:").grid(row=1, column=0, padx=5, pady=5)

        self.vfinal_entry = ttk.Entry(input_frame)
        self.nreactions_entry = ttk.Entry(input_frame)
        self.vfinal_entry.grid(row=0, column=1, padx=5, pady=5)
        self.nreactions_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="Add Reagent", command=self.add_reagent_popup).grid(row=2, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.pcr_frame, columns=("C1", "C2", "Vol/Reaction", "Total Vol"), show='headings', height=10)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        ttk.Button(self.pcr_frame, text="Calculate", command=self.calculate_pcr).pack(pady=10)
        self.output_label = ttk.Label(self.pcr_frame, text="", font=('Arial', 11))
        self.output_label.pack(pady=10)

    def add_reagent_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add Reagent")

        labels = ["Reagent Name:", "Stock Conc. (C1)", "Final Conc. (C2)"]
        entries = []
        for i, text in enumerate(labels):
            ttk.Label(popup, text=text).grid(row=i, column=0, padx=5, pady=5)
            e = ttk.Entry(popup)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries.append(e)

        ttk.Button(popup, text="Add", command=lambda: self.add_reagent(entries, popup)).grid(row=3, column=0, columnspan=2, pady=10)

    def add_reagent(self, entries, popup):
        name = entries[0].get()
        try:
            C1 = float(entries[1].get())
            C2 = float(entries[2].get())
        except ValueError:
            messagebox.showerror("Error", "Concentrations must be numeric.")
            return

        # Check validity
        if C2 >= C1:
            messagebox.showwarning("Concentration Warning", f"⚠️ {name}: Final conc. ≥ Stock conc. — please verify.")
        elif C2 <= 0 or C1 <= 0:
            messagebox.showerror("Error", "Concentrations must be positive values.")
            return

        self.tree.insert("", "end", values=(name, C1, C2, "", ""))
        popup.destroy()

    def calculate_pcr(self):
        try:
            Vfinal = float(self.vfinal_entry.get())
            n_reactions = int(self.nreactions_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for volume and reactions.")
            return

        rows = self.tree.get_children()
        reagents = []
        total_reagent_vol = 0

        for r in rows:
            name, C1, C2, _, _ = self.tree.item(r)["values"]
            try:
                vol = calculate_volume(float(C1), float(C2), Vfinal)
            except:
                continue
            total_reagent_vol += vol
            reagents.append([name, C1, C2, f"{vol:.2f}", f"{vol * n_reactions:.2f}"])

        water_vol = Vfinal - total_reagent_vol
        reagents.append(["Nuclease-free Water", "—", "—", f"{water_vol:.2f}", f"{water_vol * n_reactions:.2f}"])

        df = pd.DataFrame(reagents, columns=["Reagent", "C1", "C2", "Vol/Reaction", "Total Vol"])
        messagebox.showinfo("PCR Summary", df.to_string(index=False))

        total_master_mix = Vfinal * n_reactions
        self.output_label.config(text=f"Total Master Mix Volume: {total_master_mix:.2f} µL\nWater Volume per Reaction: {water_vol:.2f} µL")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = PCRApp(root)
    root.mainloop()
