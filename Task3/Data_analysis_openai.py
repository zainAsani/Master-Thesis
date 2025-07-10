import os
from openai import OpenAI
import pdfplumber # For reading PDF files
import time
from dotenv import load_dotenv
from prompt import  build_prompt_pdf_gemini
import pandas as pd
import re
import fitz


# OPENAI_API_KEY='sk-your_actual_openai_api_key'
load_dotenv()

try:
    client = OpenAI()
    if client:
        print("✅ OpenAI client initialized successfully.")
    else:
        print("⚠️ OpenAI client object is None after initialization. Please check your setup.")
        exit()
except Exception as e:
    print(f"❌ Error initializing OpenAI client: {e}")
    print("   Ensure your OPENAI_API_KEY is correctly set in your .env file or as an environment variable.")
    print("   The key should start with 'sk-...'")
    exit()

# --- Model Configuration ---
MODEL_ID = "gpt-4.1-nano-2025-04-14" 
# MODEL_ID = "gemini-2.5-flash-lite-preview-06-17"

def extract_text_from_pdf(pdf_path):
    print("inside extract_text_from_pdf")
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print("error extract_text_from_pdf")
        return f"Error extracting text from {pdf_path}: {str(e)}"

def analyze_papers(cited_pdf_path, citing_pdf_path):
    print("Inside analyze_papers")
    # Extract text from both PDFs
    cited_text = extract_text_from_pdf(cited_pdf_path)
    citing_text = extract_text_from_pdf(citing_pdf_path)
    
    if "Error" in cited_text or "Error" in citing_text:
        print(f"error: {cited_text} + |  + {citing_text}")
        return "", "", ""
    
    # Construct the citation context (combining both texts for analysis)
    citation_context_text = f"Cited Paper (Retracted) Text:\n{cited_text[:500000]}\n\nCiting Paper Text:\n{citing_text[:500000]}"
    
    # Build the prompt using the provided function
    prompt = build_prompt_pdf_gemini(citation_context_text)
    print("After prompt")
    
    try:
        # Call the OpenAI API
        print("Inside try for response")
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "You are a precise and analytical assistant for academic literature review."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.1, 
            timeout=20
        )

        print("before response_text")
        
        # Extract the response content
        response_text = response.choices[0].message.content
        category, justification, reference = "", "", ""

        print("After response_text")
        
        # Parse the response to extract category, justification, and reference
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
            print("analyze paper match else")
            return "", "", ""
        


    except Exception as e:
        print("Error in analyze paper")
        return "", "", ""
    
def sanitize_filename(title):
    return re.sub(r'[\\/*?:"<>|]', '_', title.replace(' ', '_'))


def main():

    cited_dir = "Data/MU_cited/"
    cited_dir_all_items = os.listdir(cited_dir)
    cited_dir_all_items = [int(item[:-4]) for item in cited_dir_all_items]

    citing_dir = "MU_citing/"
    citing_dir_all_items = os.listdir(citing_dir)
    citing_dir_all_items = [int(item[:-4]) for item in citing_dir_all_items]
    

    input_csv_path = r"Annotation-MU-dependent.csv"
    file_name_output = input_csv_path.split("\\")[-1].split(".")[0]
    output_csv_path = r"Data\Annotation-MU-dependent_{}.csv".format(MODEL_ID.replace(".", "_"))
    

    df = pd.read_csv(input_csv_path)
    df = df[df['Class'] == 'Dependent']
    category_list = []
    justification_list = []
    reference_list = []

    for index, row in df.iterrows():
        print(f"index: {index}")
        if pd.isna(row["CitingID"]):
            category_list.append("")
            justification_list.append("")
            reference_list.append("")
            continue

        
        CitedID = int(row['CitedID'])
        CitingID = int(row['CitingID'])
        print(f"CitedID: {CitedID} ----- CitingID: {CitingID}")

        cited_pdf_path = os.path.join(cited_dir, sanitize_filename(str(CitedID)) + ".pdf")

        citing_pdf_path = os.path.join(citing_dir, sanitize_filename(str(CitingID)) + ".pdf")

        print(f"cited_pdf_path: {cited_pdf_path} ------ citing_pdf_path: {citing_pdf_path}")

        if os.path.exists(cited_pdf_path) and os.path.exists(citing_pdf_path): 
            print("inside if")
            category, justification, reference = analyze_papers(cited_pdf_path, citing_pdf_path)
            category_list.append(category)
            justification_list.append(justification)
            reference_list.append(reference)
            # print(result)
        else:
            print("not in if")
            print(f"CitedID: {CitedID} -- cited_dir_all_items: {cited_dir_all_items}")
            print(f"CitingID: {CitingID} -- citing_pdf_path: {citing_pdf_path}")
            category_list.append("")
            justification_list.append("")
            reference_list.append("")


    df['category_gpt'] = category_list
    df['justification_gpt'] = justification_list
    df['reference_gpt'] = reference_list
    df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    main()