import os
import google.generativeai as genai
import time
from dotenv import load_dotenv
import pandas as pd
import re
import fitz # PyMuPDF

from prompt import build_prompt_pdf_gemini

load_dotenv()

try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file or environment variables.")
    genai.configure(api_key=api_key)
    print("✅ Google Gemini client configured successfully.")
except Exception as e:
    print(f"❌ Error configuring Google Gemini client: {e}")
    exit()

# --- Model Configuration ---
MODEL_ID = "gemini-2.5-flash-lite-preview-06-17"

def extract_text_from_pdf(pdf_path):
    print("Inside extract_text_from_pdf")
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return f"Error extracting text from {pdf_path}: {str(e)}"

def analyze_papers(cited_pdf_path, citing_pdf_path):
    print("Inside analyze_papers")
    # Extract text from both PDFs
    cited_text = extract_text_from_pdf(cited_pdf_path)
    citing_text = extract_text_from_pdf(citing_pdf_path)
    
    if "Error" in cited_text or "Error" in citing_text:
        print(f"Error during text extraction: {cited_text} | {citing_text}")
        return "", "", ""
    
    citation_context_text = f"Cited Paper (Retracted) Text:\n{cited_text[:500000]}\n\nCiting Paper Text:\n{citing_text[:500000]}"
    
    prompt = build_prompt_pdf_gemini(citation_context_text)
    print("After prompt")
    
    try:
        print("Inside try for Gemini response")
        model = genai.GenerativeModel(
            model_name=MODEL_ID,
            system_instruction="You are a precise and analytical assistant for academic literature review."
        )

        generation_config = genai.types.GenerationConfig(
            max_output_tokens=2000,
            temperature=0.1
        )

        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )

        print("before response_text")
        
        response_text = response.text
        category, justification, reference = "", "", ""

        print("After response_text")
        
        pattern = r"Answer 1: (.*?)\nAnswer 2: (.*?)\nAnswer 3: (.*)"
        match = re.search(pattern, response_text, re.DOTALL)
        
        if match:
            print("Inside match")
            category = match.group(1).strip()
            justification = match.group(2).strip()
            reference = match.group(3).strip()
            print(f"category: {category} ---- justification: {justification} ---- reference: {reference}")
            return category, justification, reference
        else:
            print("Analyze paper match failed. Full response was:\n", response_text)
            return "Parsing Failed", response_text, ""

    except Exception as e:
        print(f"Error in analyze_papers calling Gemini API: {e}")
        return "API Error", str(e), ""
    
def sanitize_filename(title):
    """Removes invalid characters from a string to be used as a filename."""
    return re.sub(r'[\\/*?:"<>|]', '_', title.replace(' ', '_'))

def main():
    """Main function to process the dataset."""
    cited_dir = "Data/cited/"
    citing_dir = "Data/citing/"
    
    input_csv_path = r"Data\Task_3_Dataset.csv"
    file_name_output = input_csv_path.split("\\")[-1].split(".")[0]
    output_csv_path = r"Data\Task_3_Dataset_{}.csv".format(MODEL_ID.replace(".", "_"))
    
    df = pd.read_csv(input_csv_path)
    
    # Initialize lists to store results
    results = []

    for index, row in df.iterrows():
        if pd.isna(row["pmid_citing"]):
            results.append(("", "", ""))
            continue
            
        CitedID = int(row['pmid'])
        CitingID = int(row['pmid_citing'])

        print(f"Processing Index {index}: CitedID: {CitedID} ----- CitingID: {CitingID}")

        cited_pdf_path = os.path.join(cited_dir, f"{CitedID}.pdf")
        citing_pdf_path = os.path.join(citing_dir, f"{CitingID}.pdf")

        print(f"Cited Path: {cited_pdf_path}\nCiting Path: {citing_pdf_path}")

        if os.path.exists(cited_pdf_path) and os.path.exists(citing_pdf_path): 
            print("PDFs found, starting analysis.")
            category, justification, reference = analyze_papers(cited_pdf_path, citing_pdf_path)
            results.append((category, justification, reference))
        else:
            print("PDF not found for one or both IDs.")
            if not os.path.exists(cited_pdf_path):
                print(f"Missing: {cited_pdf_path}")
            if not os.path.exists(citing_pdf_path):
                print(f"Missing: {citing_pdf_path}")
            results.append(("File Not Found", "", ""))
        
        print("-" * 50)

    df['category_gemini'] = [res[0] for res in results]
    df['justification_gemini'] = [res[1] for res in results]
    df['reference_gemini'] = [res[2] for res in results]
    
    # Save the updated DataFrame
    df.to_csv(output_csv_path, index=False)
    print(f"Processing complete. Results saved to {output_csv_path}")

if __name__ == "__main__":
    main()