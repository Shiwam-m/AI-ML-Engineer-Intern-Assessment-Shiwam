
## This is a Local AI Chatbot that helps students plan their terms at MIT. It reads official MIT Course Catalog PDFs and answers questions about prerequisites and subjects.


## Features
- PDF Reading: It reads all PDF files from the /data folder.
- Smart Planning: It looks at "Student History" (grades and past courses) to give better advice.
- Local AI: Uses Ollama (Llama 3), so don't need an expensive API key.
- Clean UI: A simple and professional chat interface built with Streamlit.


## How to Setup

1. Requirements
    - Llama 3 
    - Open terminal and run: ollama pull llama3:8b

2. Install Dependencies
    - pip install -r requirements.txt

## Run
    - streamlit run frontend.py

## GitHub Repository Link: https://github.com/Shiwam-m/AI-ML-Engineer-Intern-Assessment-Shiwam
