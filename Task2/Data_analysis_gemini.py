import os
import google.generativeai as genai
import pandas as pd
import time 
from dotenv import load_dotenv
from prompt import build_prompt, CATEGORIES_DATA

load_dotenv()

# Choose your model
MODEL_ID = "gemini-2.5-flash-lite-preview-06-17"  # Or "gemini-1.5-pro"


try:
    gemini_api_key = os.getenv("GOOGLE_API_KEY")
    if not gemini_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel(MODEL_ID)
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    exit()

def get_formatted_response_from_api(citation_context_for_analysis):
    """
    Sends the constructed prompt to the Gemini model and gets a formatted response.

    Args:
        citation_context_for_analysis (str): The full citation context string from the CSV.

    Returns:
        str: The model's response, ideally in the "Answer 1: ... Answer 2: ..." format,
             or an error message.
    """
    system_prompt = "You are an expert scientometrician following instructions precisely."
    full_user_prompt = build_prompt(citation_context_for_analysis)
    
    final_prompt = f"{system_prompt}\n\n{full_user_prompt}"

    try:
        generation_config = genai.types.GenerationConfig(
            temperature=0.1,
            max_output_tokens=500
        )
        
        response = model.generate_content(
            final_prompt,
            generation_config=generation_config
        )
        
        response_content = response.text
        return response_content.strip()

    except Exception as e:
        print(f"Error during Gemini API call: {e}")
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

    input_csv_path = r"Data\Annotation-MU.csv"
    output_csv_path = r"Data\Annotation-MU_{}.csv".format(MODEL_ID.replace(".", "_"))

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

    print(f"\nStarting analysis using Gemini model: {MODEL_ID}")
    print("Processing rows (a '.' will be printed for each processed row):")


    # for index, row in df_subset.iterrows():
    for index, row in df.iterrows():
        print(f"Processing row {index + 1}/{len(df)}")

        citation_text = row[citation_column_name]

        if pd.isna(citation_text) or not isinstance(citation_text, str) or not citation_text.strip():
            print(f"Skipping row {index + 1} due to empty or invalid citation text.")
            ai_categories.append("Skipped: Empty Input")
            ai_justifications.append("Skipped: Empty Input")
            continue

        model_raw_response = get_formatted_response_from_api(str(citation_text)) # Ensure it's a string
        category, justification = parse_model_response(model_raw_response)

        ai_categories.append(category)
        ai_justifications.append(justification)

        print(f"  Category: {category}")
        print(f"  Justification: {justification}")
        print(".", end="", flush=True)

    print("\nAnalysis complete.")

    df['Category_gemini'] = ai_categories
    df['Justification_gemini'] = ai_justifications

    try:
        df.to_csv(output_csv_path, index=False)
        print(f"\nSuccessfully saved results to '{output_csv_path}'.")
    except Exception as e:
        print(f"\nAn error occurred while saving the output CSV: {e}")