I have written codes for 2 tools that take input in three formats- input(), GUI and Command Line.

**TOOL 1: PCR PRIMER TOOL**
* Polymerase Chain Reaction (PCR) is a technique commonly used in Molecular Biology for DNA amplification. The technique has several steps- the most important one is the intial primer designing. Along with this, we need to perform concentration and volume calculations for the reagents frequently.
* I have personally felt the need of a tool for designing the primers and computing these calculations on a daily basis and displaying the results in a tabular format. 
* Therefore, I designed the PCR Primer Tool which has two parts- a) for primer designing and b) for reagent calculations (using C1V1= C2V2)
* There are 3 .py files for this tool as pcr-primer-tool-input, -gui, -cmdline
* For the code: **pcr-primer-tool-input**, I wrote the skeleton of the code myself.
* To proofread and smoothen the code, I used **Chat GPT-5.0**
* Significant prompts used that helped in writing this code-
1) What to write in python if I want to scan different positions along the DNA to find new potential candidate primers?
   Reply: for start in range(0, len(forward_strand) - primer_length * 2):
2) Is there a python function that can read a string in reverse?
3) There are two ways to enter a DNA sequence- in uppercase and lowercase. How to write a code that accepts both and does not give an error? Is there a better way to make DNA bases library (A=T, T=A, G=C, C=G)?
   Reply: complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
          return ''.join(complement[base] for base in reversed(seq.upper()))
4) Explain the above lines in the code
5) Suggest how to improve this code. Have I covered all possibilities?
   Reply: AI suggested to add the following to prevent any error-
    if len(forward_strand) < primer_length * 2:
    raise ValueError("Sequence too short for primer design.")
This is done to check the primer length does not exceed DNA sequence entered.
6) Write a code to enter multiple strings from the suer and terminate it when done inputting
7) Calculate if reagent volume exceeds total volume
8) How to display results in a tabular format
9) How to install pandas using --user command as I am getting error
10) Re-write the code using pandas
11) **The GUI application and command line code was created entirely using AI Chat GPT-5.0**



**TOOL 2: PROTEIN M/Z CALCULATION TOOL**
* In bottom-up proteomics, protein sequences are regularly cleaved into peptides using enzymes- trypsin and chymotrypsin (routinely used in lab) and then analyzed in mass spectrometers producing charged ions: +1, +2 and/or +3
* I have created a tool that calculates which peptide sequences can be hypothetically generated when a protein (sequence input by user) is cleaved using trypsin and/or chymotrypsin.
* There are 3 .py files for this tool as protein-mz-tool-input, -gui, -cmdline
* To proofread and smoothen the code, I used **Chat GPT-5.0**
* Significant prompts used that helped in writing this code-
1) Create a library of amino acid masses
2) Write a for-loop that scans protein sequence entered and checks when Trypsin cleaves after K or R (except when followed by P) and for Chymotrypsin cleaves after F, W, or Y (except when followed by P)
   Reply- for i, aa in enumerate(sequence):
        current += aa
        if aa in ['K', 'R'] and not (i + 1 < len(sequence) and sequence[i + 1] == 'P'):
            peptides.append(current)
            current = ""
    if current:
        peptides.append(current)
    return peptides
3) What is .strip() in the code?
4) How to write the code for multiple charges +1, +2 and +3?
5) Add mass of H2O
6) Count for total number of peptides generated
7) **The GUI application and command line code was created entirely using AI Chat GPT-5.0**


Additonally, while thinking of ideas for these tools, I took inspiration from my classmates who designed interesting tools such as "DNA Sequence Validator" during the class.
