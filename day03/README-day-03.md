**FOR DAY 03 ASSIGNMENT-**
* I had created 2 tools for Day 02 assignment- pcr-primer-tool and protein-mz-tool
* I moved the "business logic" (the computation) from both STDIN files of pcr-primer and protein-mz-tool (Day 02 assignment) to a separate file and made the main program use it.
* Replaced the code with 3rd party library-
  1. For pcr-primer-tool: Biopython 1.83 (only primer designing). Concentration and volume calculator does not have a 3rd party library subsitute.
  2. For protein-mz-tool: Pyteomics 4.6
* Added tests for both the tools.


**File names explanation**
1. For pcr-primer-tool: dna_utils.py, dna_main.py, test_dna_utils.py and requirements_dna.txt
2. For protein-mz-tool: protein_utils.py, protein_main.py, test_protein_utils.py and requirements_dna.txt


**Tests used**
* For test_dna_utils.py- Pytest
* test_protein_utils.py- Unittest


**Installation instructions**
1. To install Biopython: pip install biopython
2. To install Pyteomics: pip install pyteomics
3. For pytest: pip install pytest
4. For unittest: pip install unittest
5. Similar command if numpy and pandas are not installed previously
6. If unable to, add --user after each command


**ISSUES FACED**
* No error encountered in test_protein_utils.py using Unittest. All 7 tests passed in 0.001s.
* 1 test always failing in test_dna_utils.py using Pytest. Unable to resolve it despite multiple attempts (including taking help from AI)
* ![pcr-test-failure-msg](day03/test-failure.PNG)


**List of installed versions**
* biopython==1.83
* pandas==2.2.2
* pyteomics==4.6
* pytest==8.0.0
* numpy==1.26.4


**Used ChatGPT-5. Significant prompts-**
1. Write a code for pcr-primer-tool-input.py that moves the "business logic" (the computation) to a separate file and make the main program use it. Add some tests, especially to check the "business logic". Make sure you can run the tests. Look at the tests and make sure they test the code properly. Replace the code with some 3rd-party library when possible, try pytest.
2. Write a code for protein-mz-tool-input.py that moves the "business logic" (the computation) to a separate file and make the main program use it. Add some tests, especially to check the "business logic". Make sure you can run the tests. Look at the tests and make sure they test the code properly. Replace the code with some 3rd-party library when possible.
3. I am getting this error for the test (pasted image). How to resolve it?
4. Getting similar error for the test.
