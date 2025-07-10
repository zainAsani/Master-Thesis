import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus.reader import wordnet
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer, util
import io # For using the sample data
from  hierarchy_list import categories

# --- NLTK Setup ---
def download_nltk_resource_if_missing(resource_path, download_name):
    """Checks if an NLTK resource exists, and downloads it if not."""
    try:
        nltk.data.find(resource_path)
        print(f"NLTK resource '{resource_path}' found.")
    except LookupError:
        print(f"NLTK resource '{resource_path}' not found. Downloading '{download_name}'...")
        nltk.download(download_name, quiet=True) # quiet=True suppresses the interactive downloader GUI
        # Verify after download
        try:
            nltk.data.find(resource_path)
            print(f"NLTK resource '{download_name}' downloaded successfully.")
        except LookupError:
            print(f"Failed to download NLTK resource '{download_name}'. Please try manually: import nltk; nltk.download('{download_name}')")

print("Checking and downloading NLTK resources if necessary...")
# download_nltk_resource_if_missing('tokenizers/punkt', 'punkt')
# download_nltk_resource_if_missing('corpora/stopwords', 'stopwords')
# download_nltk_resource_if_missing('corpora/reader/wordnet', 'wordnet')
# download_nltk_resource_if_missing('corpora/omw-1.4', 'omw-1.4') # Often needed for WordNet
print("NLTK resource check complete.")

lemmatizer = WordNetLemmatizer()
stop_words_set = set(stopwords.words('english'))

def preprocess_text_simple(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s/]', '', text) # Keep '/' for phrases like "Falsification/ Fabrication"
    text = re.sub(r'\s+', ' ', text).strip() # Normalize whitespace
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words_set and word.isalpha()]
    return " ".join(tokens)

# --- Approach 1: Normal NLP (Keyword-based) ---
def find_category_simple(text_to_analyze, local_categories_dict):
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return None, None

    text_lower = text_to_analyze.lower()
    # Keep original punctuation for exact phrase matching, but be mindful of its impact
    # For keyword matching, use processed text
    processed_text_tokens = set(preprocess_text_simple(text_lower).split())
    if not processed_text_tokens and not any(sub.lower() in text_lower for cat_list in local_categories_dict.values() for sub in cat_list): # check if any subphrase is in text_lower
         return None, None


    matches = []

    for category_name, sub_category_list in local_categories_dict.items():
        for sub_cat_phrase in sub_category_list:
            sub_cat_phrase_lower = sub_cat_phrase.lower()
            processed_sub_cat_phrase_original_case = preprocess_text_simple(sub_cat_phrase) # for keyword matching
            processed_sub_cat_tokens = set(processed_sub_cat_phrase_original_case.lower().split())


            # 1. Exact phrase match (high priority)
            # Allows for partial exact matches e.g. "manipulation of images" in a longer text
            if sub_cat_phrase_lower in text_lower:
                # Score by length of phrase to prefer more specific matches
                # and add a high base score to prioritize exact matches
                matches.append({
                    'category': category_name,
                    'sub_category': sub_cat_phrase,
                    'score': 1000 + len(sub_cat_phrase_lower), # Base score + length
                    'type': 'exact_phrase_match'
                })
                continue # Found an exact match for this sub_cat_phrase, move to the next one

            # 2. All keywords match (medium priority)
            if not processed_sub_cat_tokens: # Skip if sub_cat_phrase is only stopwords/punctuation
                continue
            
            # Check if all keywords from the PREPROCESSED sub_cat_phrase are in the PREPROCESSED text
            if processed_sub_cat_tokens.issubset(processed_text_tokens):
                matches.append({
                    'category': category_name,
                    'sub_category': sub_cat_phrase,
                    'score': 500 + len(processed_sub_cat_tokens), # Base score + number of keywords
                    'type': 'all_keywords_match'
                })
                continue

            # 3. Partial keyword match (Jaccard index, lower priority)
            # Check for common keywords between PREPROCESSED text and PREPROCESSED sub_cat_phrase
            common_keywords = processed_sub_cat_tokens.intersection(processed_text_tokens)
            if common_keywords:
                # Jaccard: intersection / union
                union_keywords = processed_sub_cat_tokens.union(processed_text_tokens)
                if union_keywords: # Avoid division by zero
                    jaccard_score = len(common_keywords) / len(union_keywords)
                    # Consider a threshold for Jaccard score
                    if jaccard_score > 0.3: # Example threshold, can be tuned
                        matches.append({
                            'category': category_name,
                            'sub_category': sub_cat_phrase,
                            'score': jaccard_score * 100, # Score 0-100
                            'type': 'partial_keywords_match (Jaccard)'
                        })
    
    if not matches:
        return None, None

    # Sort matches by score (descending). If scores are equal, longer sub_category might be more specific.
    # The scoring already prefers exact and then all_keywords.
    best_match = sorted(matches, key=lambda m: (-m['score'], -len(m['sub_category'])))[0]
    return best_match['category'], best_match['sub_category']


# --- Approach 2: Semantic Information ---
semantic_model = None
precomputed_subcat_embeddings = {}

def initialize_semantic_model(model_name='all-MiniLM-L6-v2'):
    global semantic_model
    print(f"Loading semantic model '{model_name}'...")
    semantic_model = SentenceTransformer(model_name)
    print("Semantic model loaded.")

def precompute_subcategory_embeddings(local_categories_dict):
    global precomputed_subcat_embeddings
    if not semantic_model:
        raise ValueError("Semantic model not initialized. Call initialize_semantic_model() first.")
    print("Pre-computing subcategory embeddings...")
    all_phrases_map = [] # list of tuples (category, sub_category_phrase)
    all_phrases_for_encoding = []

    for category_name, sub_category_list in local_categories_dict.items():
        for sub_cat_phrase in sub_category_list:
            all_phrases_map.append((category_name, sub_cat_phrase))
            # For semantic matching, using the original phrase (not preprocessed heavily) might be better
            # as models are often trained on natural language.
            all_phrases_for_encoding.append(sub_cat_phrase)

    if not all_phrases_for_encoding:
        print("No subcategories found to precompute embeddings.")
        return

    embeddings = semantic_model.encode(all_phrases_for_encoding, convert_to_tensor=True, show_progress_bar=True)
    
    for i, (cat_name, sub_cat) in enumerate(all_phrases_map):
        precomputed_subcat_embeddings[(cat_name, sub_cat)] = embeddings[i]
    print(f"Pre-computed {len(precomputed_subcat_embeddings)} subcategory embeddings.")


def find_category_semantic(text_to_analyze, similarity_threshold=0.45):
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return None, None, 0.0  # CORRECTED: Ensure three values are returned
    if not semantic_model:
        raise ValueError("Semantic model not initialized. Call initialize_semantic_model() first.")
    if not precomputed_subcat_embeddings:
        # Handle case where there are no subcategories to match against
        print("Warning: Subcategory embeddings not precomputed or empty. Semantic matching will find no results.")
        return None, None, 0.0

    text_embedding = semantic_model.encode(text_to_analyze, convert_to_tensor=True)

    best_match_score = -1.0  # Initialize with a float, lower than any possible similarity score
    best_match_category = None
    best_match_sub_category = None

    # Iterate through all precomputed embeddings to find the one with the highest similarity
    for (category_name, sub_cat_phrase), sub_cat_embedding in precomputed_subcat_embeddings.items():
        similarity = util.pytorch_cos_sim(text_embedding, sub_cat_embedding).item()

        if similarity > best_match_score:
            best_match_score = similarity
            best_match_category = category_name
            best_match_sub_category = sub_cat_phrase

    # After checking all subcategories, if the best score found is above the threshold, return the match
    if best_match_category is not None and best_match_score >= similarity_threshold:
        return best_match_category, best_match_sub_category, best_match_score
    else:
        # If no match met the threshold, or no subcategories existed (best_match_category would be None)
        return None, None, 0.0


# --- Main Processing ---
if __name__ == "__main__":
    # Initialize semantic model and precompute embeddings
    initialize_semantic_model()
    precompute_subcategory_embeddings(categories)

    # --- Load Data ---
    # Replace this with your actual CSV file path:
    input_csv = r"C:\Users\Zaina\Desktop\TU Braunschweig\Semester 6\MasterArbeit\Work\Task_1_Dataset.csv"  # Replace with your input CSV path
    output_csv = r"C:\Users\Zaina\Desktop\TU Braunschweig\Semester 6\MasterArbeit\Work\Task_1_Dataset_resullt_01.csv"  # Replace with your output CSV path
    df = pd.read_csv(input_csv)


    results = []

    for index, row in df.iterrows():
        pmid = row.get('pmid', 'N/A')
        text_rw = row.get('Retraction_Watch', '')
        text_rn = row.get('Retraction_Notice', '')

        # Simple NLP Matching
        cat_rw_simple, subcat_rw_simple = find_category_simple(text_rw, categories)
        cat_rn_simple, subcat_rn_simple = find_category_simple(text_rn, categories)

        # Semantic Matching
        cat_rw_semantic, subcat_rw_semantic, score_rw_sem = find_category_semantic(text_rw)
        cat_rn_semantic, subcat_rn_semantic, score_rn_sem = find_category_semantic(text_rn)
        
        results.append({
            'PMID': pmid,
            'Retraction_Watch_Text': text_rw[:100] + "..." if isinstance(text_rw, str) and len(text_rw) > 100 else text_rw, # Show snippet
            'RW_Simple_Category': cat_rw_simple,
            'RW_Simple_SubCategory': subcat_rw_simple,
            'RW_Semantic_Category': cat_rw_semantic,
            'RW_Semantic_SubCategory': subcat_rw_semantic,
            'RW_Semantic_Score': f"{score_rw_sem:.2f}" if score_rw_sem else "N/A",
            'Retraction_Notice_Text': text_rn[:100] + "..." if isinstance(text_rn, str) and len(text_rn) > 100 else text_rn, # Show snippet
            'RN_Simple_Category': cat_rn_simple,
            'RN_Simple_SubCategory': subcat_rn_simple,
            'RN_Semantic_Category': cat_rn_semantic,
            'RN_Semantic_SubCategory': subcat_rn_semantic,
            'RN_Semantic_Score': f"{score_rn_sem:.2f}" if score_rn_sem else "N/A",
        })

    results_df = pd.DataFrame(results)
    
    # Display results
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000) # Adjust width for better console display
    pd.set_option('display.max_colwidth', 200) # Show more text in columns
    print("\n--- Categorization Results ---")
    print(results_df)

    # You can save the results to a new CSV file if needed:
    results_df.to_csv(output_csv, index=False)