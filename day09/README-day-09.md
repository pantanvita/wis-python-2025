# **About Day 09 assignment**

Given file- subjects.txt

## Initial analysis performed-
* Added the deadline of each assignment (subjects.txt)
* Normalized the .txt file, extracted the individual headers, parsed the submission records and arranged in clean Pandas DataFrame
  (subjects_reordered.ipynb)
* Output .xlsx file- assignment_submission_report.xlsx
* This file was used for further analysis

## **Assignments submission data analysis**
1. Open vs Closed Assignments
2. Students with atleast 1 and 2 missing assignments
3. Average & Mode Submission Time per Student and,
4. Weekend vs Weekday Submissions (Friday and Saturday as weekends)
   <img width="350" height="400" alt="image" src="https://github.com/user-attachments/assets/5ca9b251-7f91-4e70-8ecf-76a1d71895bb" />
   
5. The final analysis was exported to an excel file with multiple tabs- assignment_analysis_report.xlsx


## Files required
1. subjects.txt
2. assignment_submission_report.xlsx

## File details
1. **subjects.txt**: contains the original .txt file provided along with added assignment deadlines
2. **subjects_reordered.ipynb**: code for parsing and arranging the submission data in clean Pandas DataFrame
3. **assignment_submission_report.xlsx**: final output from subjects_reordered.ipynb
4. **assignment_analysis.ipynb**: code for carrying out final analysis using the .xlsx file
5. **assignment_analysis_report.xlsx**: the final analysis report

## Installations
1. Anaconda
2. Jupyter Notebook
3. Python v3.13+
4. numpy
5. pandas
6. matplotlib.pyplot
7. datetime, time
