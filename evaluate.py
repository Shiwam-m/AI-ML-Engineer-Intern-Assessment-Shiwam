import pandas as pd
import os
import time
from backend import get_vectorstore, generate_assistant_response

def run_evaluation():
    print("\n--- Starting Assessment Evaluation (25 Queries) ---")
    vstore = get_vectorstore()
    
    if vstore is None:
        print("Error: Please put PDFs in 'data' folder first.")
        return

    queries = [
        # Prerequisite 
        "What are the prerequisites for 6.1210?",
        "Can I take 6.1020 if I finished 6.1010?",
        "Is 6.1200 a prerequisite for 6.1220?",
        "Does 6.1800 require 6.1210?",
        "What do I need before taking 6.1910?",
        "What are the prerequisites for 6.1400?",
        "Can I take 6.100B without 6.100A?",
        "Is Linear Algebra (18.06) required for Computer Science?",
        "What is required for Software Construction?",
        "Can I take 6.1810 Operating Systems directly?",

        # Prerequisite 
        "I want to take Database Systems (6.5831). List all courses I must take in order.",
        "What is the full math sequence for Course 6-3?",
        "Explain the path from 6.100A to Computer Systems Engineering.",
        "List all prerequisites needed to eventually take Computability and Complexity.",
        "What subjects must be completed before entering Advanced Undergraduate Subjects?",

        # Program 
        "How many total units are required beyond GIRs for SB in 6-3?",
        "What are the Science GIR requirements?",
        "Tell me about the Communication Requirement (CI-M) for EECS.",
        "How many EECS track subjects are required?",
        "Are 6.1910 and 6.1200 REST requirements?",

        # Not in Catalog / Trick
        "What is the phone number for MIT admissions?",
        "Who is the professor for 6.1010 next year?",
        "Where is the cheapest place to buy a laptop at MIT?",
        "How can I apply for a parking permit?",
        "What is the dining hall menu for today?"
    ]

    results = []
    start_time = time.time()

    for i, q in enumerate(queries):
        print(f"Processing Query {i+1}/25: {q}")
        try:
            ans = generate_assistant_response(vstore, q, "History: New student, no credits.")
            results.append({"Question": q, "Assistant_Response": ans})
        except Exception as e:
            print(f"Failed on query {i+1}: {e}")
            results.append({"Question": q, "Assistant_Response": f"Error: {str(e)}"})

    df = pd.DataFrame(results)
    df.to_csv("evaluation_results.csv", index=False)
    
    end_time = time.time()
    print(f"\nSUCCESS: 'evaluation_results.csv' created.")
    print(f"Total Time Taken: {round((end_time - start_time)/60, 2)} minutes.")

if __name__ == "__main__":
    run_evaluation()