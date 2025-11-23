**About Day04 assignment**

While working in the field of Proteomics, I deal with hundreds of proteins at a time and often need to refer to the protein-protein interactions in biological pathways to gain an understanding of the larger picture. 

**REACTOME [https://reactome.org/]**

REACTOME is an open-source, open access, manually curated and peer-reviewed pathway database.
The goal of the databse is to provide the user a graphical map of known biological processes and pathways along with intuitive bioinformatics tools for the visualization, interpretation and analysis of biological pathway knowledge.

!(reactome-logo)[reactome-logo.png]

I have written a program that downloads data files (e.g., pathway data, reactions, or protein interactions) from the Reactome database and saves them locally as .json files, separating the business logic from the UI (CLI). 
The user can also store their email in a separate config file for API calls.
The user specifies a pathway ID and the code downloads pathway/reaction data in JSON or BioPAX format from the Reactome Content Service (Reactome’s REST API) or directly from their FTP/data download server, saving them on the user’s Desktop.

**Project Structure**

reactome_downloader/

│

├── main.py              # User Interface (CLI)

├── reactome_service.py  # Business logic

├── config.json          # User email / API key

├── .gitignore


**How It Works**
1. User provides Reactome pathway ID (e.g., R-HSA-199420).
2. User chooses format: JSON or BioPAX.
3. Program fetches the file from Reactome’s Content Service API or download server.
4. Files are saved as .json in:
   Desktop/Reactome_Downloads/<PATHWAY_ID>/

**Significant prompts given to the AI (Used ChatGPT-5.0)**

* Write a python based project that can be done using Reactome. The program will download the files from the reactome database and save it on the user's desktop in a file or in multiple files. Separate the "business logic" and the UI (User Interface). 
* How to provide the email addresss if you need to use some API secrets
* What to do with the json file?
