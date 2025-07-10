import os
from openai import OpenAI
import pandas as pd
import time 
from dotenv import load_dotenv
from prompt import build_prompt, CATEGORIES_DATA


load_dotenv()

MODEL_ID = "gpt-4.1-nano-2025-04-14"  # Or "gpt-4o-mini"



# --- OpenAI API Interaction ---

try:
    client = OpenAI()
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    print("Please ensure your OPENAI_API_KEY environment variable is set correctly.")
    exit()

def get_formatted_response_from_api(citation_context_for_analysis):
    """
    Sends the constructed prompt to the OpenAI model and gets a formatted response.

    Args:
        citation_context_for_analysis (str): The full citation context string from the CSV.

    Returns:
        str: The model's response, ideally in the "Answer 1: ... Answer 2: ..." format,
             or an error message.
    """
    full_prompt = build_prompt(citation_context_for_analysis)


    try:
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "You are an expert scientometrician following instructions precisely."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.1,  
            max_tokens=500    
        )
        response_content = completion.choices[0].message.content
        return response_content.strip()

    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return f"API_Error: {e}" # Return a distinguishable error message

def parse_model_response(response_text):
    """
    Parses the model's response to extract category and justification.
    """
    category = "Error: Parsing failed - No Answer 1"
    justification = "Error: Parsing failed - No Answer 2"

    if response_text.startswith("API_Error:"):
        return response_text, response_text # Propagate API error

    lines = response_text.split('\n')
    for line in lines:
        if line.startswith("Answer 1:"):
            category = line.replace("Answer 1:", "").strip()
        elif line.startswith("Answer 2:"):
            justification = line.replace("Answer 2:", "").strip()
    return category, justification

if __name__ == "__main__":
    input_csv_path = r"C:\Users\Zaina\Desktop\TU Braunschweig\Semester 6\MasterArbeit\Task2\Data\Annotation-MU.csv"
    output_csv_path = r"C:\Users\Zaina\Desktop\TU Braunschweig\Semester 6\MasterArbeit\Task2\Data\Annotation-MU_{}.csv".format(MODEL_ID.replace(".", "_"))
    citation_column_name = "CitationContext"

    try:
        df = pd.read_csv(input_csv_path)
        df = df[df['Class'] == 'Dependent']
        print(f"Successfully loaded data from '{input_csv_path}'. Found {len(df)} rows.")
    except FileNotFoundError:
        print(f"Error: Input CSV file not found at '{input_csv_path}'. Exiting.")
        exit()
    except Exception as e:
        print(f"An error occurred while loading the CSV: {e}. Exiting.")
        exit()

    if citation_column_name not in df.columns:
        print(f"Error: Column '{citation_column_name}' not found in the CSV file. Available columns: {df.columns.tolist()}. Exiting.")
        exit()

    ai_categories = []
    ai_justifications = []

    print(f"\nStarting analysis using OpenAI model: {MODEL_ID}")
    print("Processing rows (a '.' will be printed for each processed row):")

    for index, row in df.iterrows():
        print(index)
        # break
        
        citation_text = row[citation_column_name]

        if pd.isna(citation_text) or not isinstance(citation_text, str) or not citation_text.strip():
            print(f"Skipping row {index + 2} due to empty or invalid citation text.")
            ai_categories.append("Skipped: Empty Input")
            ai_justifications.append("Skipped: Empty Input")
            continue

        model_raw_response = get_formatted_response_from_api(str(citation_text)) 
        category, justification = parse_model_response(model_raw_response)

        ai_categories.append(category)
        ai_justifications.append(justification)

        print(f"  Category: {category}")
        print(f"  Justification: {justification}")
        print(".", end="", flush=True) # Progress indicator

    print("\nAnalysis complete.")

    df['Category_openai'] = ai_categories
    df['Justification_openai'] = ai_justifications

    try:
        df.to_csv(output_csv_path, index=False)
        print(f"\nSuccessfully saved results to '{output_csv_path}'.")
    except Exception as e:
        print(f"\nAn error occurred while saving the output CSV: {e}")