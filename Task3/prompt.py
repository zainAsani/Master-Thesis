# --- Prompt Definitions ---
def build_prompt(citation_context_text):
    """
    Builds the full prompt for the OpenAI API.
    The BASE_CONTEXT describes the task and classification categories.
    The citation_context_text is the specific text from your CSV to be analyzed.
    """
    BASE_CONTEXT_TEMPLATE = """You are an expert scientometrician specializing in the analysis of scholarly citations. Your task is to determine how a citing paper uses a **retracted article**, denoted as retracted/cited text, based on some, but not all, Example Phrases provided.

        Please classify the citation's function into one of the following categories. The Example Phrases are some words and phrases used to :

        1.  **Uses_Data**: The citing paper explicitly states it is using, re-analyzing, or referring to specific datasets or raw data originating from the retracted article retracted/cited text.
            *Example Phrases:* data, dataset, experimental data, data from retracted/cited text, using the dataset of retracted/cited text, figures from retracted/cited text, tables from retracted/cited text, raw data provided by retracted/cited text, background information from retracted/cited text
            *Example Classification:* Uses_Data
            *Example Justification:* The citing paper states it performed a "secondary analysis on the data from retracted/cited text".

        2.  **Uses_Results**: The citing paper explicitly states it is using, building upon, comparing its own results directly to, or attempting to replicate specific findings or conclusions reported in the retracted article retracted/cited text.
            *Example Phrases:* as shown in retracted/cited text, the results of retracted/cited text indicate, findings from retracted/cited text suggest, according to retracted/cited text, the outcome was similar/ same, the study by retracted/cited text demonstrated, result extension from retracted/cited text
            *Example Classification:* Uses_Results
            *Example Justification:* The citing paper is re-examining an "initial finding" from the retracted retracted/cited text.

        3.  **Uses_Methods**: The citing paper explicitly states it is employing, adapting, following, or referencing a specific methodology, experimental procedure, protocol, algorithm, or theoretical approach described in the retracted article retracted/cited text.
            *Example Phrases:* following the method described in retracted/cited text, using the technique from retracted/cited text, adopting the approach of retracted/cited text, based on the protocol outlined in retracted/cited text, employing the procedure from retracted/cited text, method from retracted/cited text
            *Example Classification:* Uses_Methods
            *Example Justification:* The citing paper "initially adapted" the "protocol" from retracted/cited text.

        4.  **Shows_Consistency**: The citing paper states its findings, arguments, theoretical stance, or observations are generally consistent with, or in alignment with, the broader claims or framework of the retracted article retracted/cited text, without necessarily detailing use of specific data, results, or methods.
            *Example Phrases:*  consistent with the findings of retracted/cited text, in agreement with retracted/cited text, similar results were obtained as in retracted/cited text, confirms the observations of retracted/cited text, supports the conclusions drawn in retracted/cited text, result extension from retracted/cited text
            *Example Classification:* Shows_Consistency
            *Example Justification:* The citing paper states its "general trend is consistent with" the work of retracted/cited text.

        5.  **Other**: The citation's function within the context does not clearly or primarily fall into any of the above categories, or the context is insufficient to make a determination.

        Now, please analyze the following citation context:
        {context_to_analyze}
        """
    QUESTIONS_AND_FORMATTING_INSTRUCTIONS = """
        Questions:
        1.  Which category best describes how the citing paper uses the retracted article retracted/cited text in this context?
        2.  Provide a brief justification for your choice, referencing specific phrases or ideas from the provided sentences.

        Please format your response *exactly* as follows, with no other text or explanations:
        Answer 1: [Category Name]
        Answer 2: [Your justification]
        """
    # The user's add_context function inserts the dynamic context here.
    # We are making it more explicit that the prompt expects the context here.
    # The initial part of the prompt still mentions "three-sentence context" as a general guideline
    # for the *type* of analysis, even if the input is a single block.
    full_user_prompt = BASE_CONTEXT_TEMPLATE.format(context_to_analyze=citation_context_text) + \
                       QUESTIONS_AND_FORMATTING_INSTRUCTIONS
    return full_user_prompt


# --- Prompt Definitions ---
def build_prompt_pdf(citation_context_text):
    """
    Builds the full prompt for the OpenAI API.
    The BASE_CONTEXT describes the task and classification categories.
    The citation_context_text is the research paper to be analyzed.
    """
    BASE_CONTEXT_TEMPLATE = """You are an expert scientometrician specializing in the analysis of scholarly citations. Your task is to determine how a citing paper uses a **retracted article**, denoted as retracted/cited text, based on some, but not all, Example Phrases provided.

        Please classify the citation's function into one of the following categories. The Example Phrases are some words and phrases used to :

        1.  **Uses_Data**: The citing paper explicitly states it is using, re-analyzing, or referring to specific datasets or raw data originating from the retracted/cited text.
            *Example Phrases:* data, dataset, experimental data, data from retracted/cited text, using the dataset of retracted/cited text, figures from retracted/cited text, tables from retracted/cited text, raw data provided by retracted/cited text, background information from retracted/cited text
            *Example Classification:* Uses_Data
            *Example Justification:* The citing paper states it performed a "secondary analysis on the data from retracted/cited text".

        2.  **Uses_Results**: The citing paper explicitly states it is using, building upon, comparing its own results directly to, or attempting to replicate specific findings or conclusions reported in the retracted/cited text.
            *Example Phrases:* as shown in retracted/cited text, the results of retracted/cited text indicate, findings from retracted/cited text suggest, according to retracted/cited text, the outcome was similar/ same, the study by retracted/cited text demonstrated, result extension from retracted/cited text
            *Example Classification:* Uses_Results
            *Example Justification:* The citing paper is re-examining an "initial finding" from the retracted retracted/cited text.

        3.  **Uses_Methods**: The citing paper explicitly states it is employing, adapting, following, or referencing a specific methodology, experimental procedure, protocol, algorithm, or theoretical approach described in the retracted/cited text.
            *Example Phrases:* following the method described in retracted/cited text, using the technique from retracted/cited text, adopting the approach of retracted/cited text, based on the protocol outlined in retracted/cited text, employing the procedure from retracted/cited text, method from retracted/cited text
            *Example Classification:* Uses_Methods
            *Example Justification:* The citing paper "initially adapted" the "protocol" from retracted/cited text.

        4.  **Shows_Consistency**: The citing paper states its findings, arguments, theoretical stance, or observations are generally consistent with, or in alignment with, the broader claims or framework of the retracted article retracted/cited text, without necessarily detailing use of specific data, results, or methods.
            *Example Phrases:*  consistent with the findings of retracted/cited text, in agreement with retracted/cited text, similar results were obtained as in retracted/cited text, confirms the observations of retracted/cited text, supports the conclusions drawn in retracted/cited text, result extension from retracted/cited text
            *Example Classification:* Shows_Consistency
            *Example Justification:* The citing paper states its "general trend is consistent with" the work of retracted/cited text.

        5.  **Other**: The citation's function within the context does not clearly or primarily fall into any of the above categories, or the context is insufficient to make a determination.

        Now, please analyze the following citing and cited text:
        {context_to_analyze}
        """
    QUESTIONS_AND_FORMATTING_INSTRUCTIONS = """
        Questions:
        1.  Which category best describes how the citing paper uses the retracted article retracted/cited text in this context?
        2.  Provide a brief justification for your choice (in your own words in maximum 4 sentences)
        3.  Provide referencing specific phrases from the text, data or other informtion to back the justification

        Please format your response *exactly* as follows, with no other text or explanations:
        Answer 1: [Category Name]
        Answer 2: [Your justification]
        Answer 3: [Your Reference]
        """
    # The user's add_context function inserts the dynamic context here.
    # We are making it more explicit that the prompt expects the context here.
    # The initial part of the prompt still mentions "three-sentence context" as a general guideline
    # for the *type* of analysis, even if the input is a single block.
    full_user_prompt = BASE_CONTEXT_TEMPLATE.format(context_to_analyze=citation_context_text) + \
                       QUESTIONS_AND_FORMATTING_INSTRUCTIONS
    return full_user_prompt



CATEGORIES_DATA = {
    "Uses_Data": "The citing paper explicitly states it is using, re-analyzing, or referring to specific datasets or raw data originating from the retracted article.",
    "Uses_Results": "The citing paper explicitly states it is using, building upon, comparing its own results directly to, or attempting to replicate specific findings or conclusions reported in the retracted article.",
    "Uses_Methods": "The citing paper explicitly states it is employing, adapting, following, or referencing a specific methodology, experimental procedure, protocol, algorithm, or theoretical approach described in the retracted article.",
    "Shows_Consistency": "The citing paper states its findings, arguments, theoretical stance, or observations are generally consistent with, or in alignment with, the broader claims or framework of the retracted article, without necessarily detailing use of specific data, results, or methods.",
    "Other": "The citation's function within the context does not clearly or primarily fall into any of the above categories, or the context is insufficient to make a determination."
}

def build_prompt_pdf_new(citation_context_text):
    """
    
    The BASE_CONTEXT describes the task and classification categories.
    The citation_context_text is the cited/retracted article and citing article to be analyzed.
    """
    BASE_CONTEXT_TEMPLATE = """You are an expert scientometrician specializing in the analysis of scholarly citations. Your task is to determine how a citing paper uses a **retracted article**..

        Please classify the citation's function into one of the following categories:

        1.  **Uses_Data**: 

        2.  **Uses_Results**: 

        3.  **Uses_Methods**: 

        4.  **Shows_Consistency**: 

        5.  **Other**: 

        Now, please analyze the following citing and cited text:
        {context_to_analyze}
        """
    QUESTIONS_AND_FORMATTING_INSTRUCTIONS = """
        Questions:
        1.  Which category best describes how the citing paper uses the retracted article retracted/cited text in this context?
        2.  Provide a brief justification for your choice (in your own words in maximum 4 sentences)
        3.  Provide referencing specific phrases from the text, data or other informtion to back the justification

        Please format your response *exactly* as follows, with no other text or explanations:
        Answer 1: [Category Name]
        Answer 2: [Your justification]
        Answer 3: [Your Reference]
        """

    full_user_prompt = BASE_CONTEXT_TEMPLATE.format(context_to_analyze=citation_context_text) + \
                       QUESTIONS_AND_FORMATTING_INSTRUCTIONS
    return full_user_prompt

def build_prompt_pdf_gemini(citation_context_text):
    """
    Constructs a detailed prompt for an LLM to analyze the use of a retracted paper
    by a citing paper.

    The BASE_CONTEXT_TEMPLATE provides a clear persona, a step-by-step analysis guide,
    and detailed definitions for each classification category.

    The QUESTIONS_AND_FORMATTING_INSTRUCTIONS directs the model to provide its answer
    in a structured, easily parsable format.
    """
    
    # This template is heavily revised to provide clarity, context, and a structured
    # reasoning process for the LLM.
    BASE_CONTEXT_TEMPLATE = """You are an expert scientometrician specializing in the analysis of scholarly citations. Your primary task is to analyze how a **citing paper** makes use of a **cited paper that has been retracted**. Your analysis must be precise and based *only* on the text provided.

**Analysis Steps:**

First, carefully examine the **"Cited Paper (Retracted) Text"** to identify the following core components.:
* **Data:** The specific datasets, observations, or evidence the paper generated or used.
* **Methods:** The key techniques, procedures, or experimental protocols described.
* **Results:** The main findings, conclusions, or claims presented by the authors.

Second, analyze the **"Citing Paper Text"** to determine if it uses any of the core components you identified from the retracted paper.

**Classification Task:**

Based on your analysis, classify the citation's function into **one** of the following categories. Please adhere strictly to these definitions:

1.  **Uses_Data**: The citing paper uses or re-analyzes the *specific data* (e.g., datasets, figures, tables) originally presented in the retracted paper. The citing paper's work is directly dependent on this data.
2.  **Uses_Results**: The citing paper explicitly states, builds upon, or treats as established fact the *specific results or conclusions* from the retracted paper. This goes beyond a general background mention and indicates reliance on the retracted findings.
3.  **Uses_Methods**: The citing paper adopts or replicates a *specific method, technique, or experimental protocol* that was detailed in the retracted paper. The citing paper explicitly credits the retracted paper for the methodology.
4.  **Shows_Consistency**: The citing paper does not directly use the data, results, or methods, but instead claims its *own, independently derived findings* are consistent with, or supported by, the results of the retracted paper. This is a weaker form of reliance than `Uses_Results`.
5.  **Other**: The citing paper's use of the retracted article does not fit any of the above categories. This may include:
    * Mentioning the paper as general background reading.
    * Discussing or criticizing the paper's ideas without using its data/results/methods or showing consistency.
    * Explicitly acknowledging the paper's retraction.
    * Any other peripheral mention.

Now, please analyze the following texts:
{context_to_analyze}
"""

    # This section is slightly tweaked for clarity and to elicit more precise evidence.
    QUESTIONS_AND_FORMATTING_INSTRUCTIONS = """
Questions:
1.  Which category from the definitions above best describes how the citing paper uses the retracted paper?
2.  Provide a brief justification for your choice, explaining your reasoning in no more than four sentences.
3.  Provide direct quotes from the texts that serve as evidence for your justification. If possible, provide a quote from the citing paper and the corresponding part of the cited (retracted) paper it refers to.

Please format your response *exactly* as follows, with no other text or explanations. In Answer 3, the quote should be 3 sentences and in Answer 2 the Justification should be based on Answer 3:
Answer 1: [Category Name]
Answer 2: [Your justification]
Answer 3: [Evidence from Citing Paper: "quote"] \n [Evidence from Cited Paper: "quote"]
"""

    full_user_prompt = BASE_CONTEXT_TEMPLATE.format(context_to_analyze=citation_context_text) + \
                       QUESTIONS_AND_FORMATTING_INSTRUCTIONS
    
    return full_user_prompt

def build_prompt_pdf_grok(citation_context_text):
    """
    The BASE_CONTEXT describes the task and classification categories.
    The citation_context_text is the cited/retracted article and citing article to be analyzed.
    """
    BASE_CONTEXT_TEMPLATE = """You are an expert scientometrician specializing in the analysis of scholarly citations. Your task is to analyze a retracted article (cited paper) and determine how a citing paper uses it. First, extract the following from the cited (retracted) paper: (1) key results (e.g., findings, conclusions), (2) data used (e.g., datasets, sources), (3) methods (e.g., experimental or analytical techniques), and (4) other relevant information (e.g., hypotheses, theoretical frameworks). Then, evaluate the citing paper to determine if it uses the cited paper’s data, results, methods, or shows consistency with its findings (e.g., replicating or supporting its conclusions).

Please classify the citation’s function into one of the following categories:

1. **Uses_Data**: The citing paper directly uses or references the same dataset(s) or data sources as the retracted paper.
2. **Uses_Results**: The citing paper relies on or references specific findings or conclusions from the retracted paper.
3. **Uses_Methods**: The citing paper adopts or references the same methodology or analytical techniques as the retracted paper.
4. **Shows_Consistency**: The citing paper’s findings align with or support the retracted paper’s results or conclusions, without directly using its data, results, or methods.
5. **Other**: The citing paper references the retracted paper in a way that does not fit the above categories (e.g., background, literature review, or critique).

When analyzing, prioritize key sections (e.g., abstract, methods, results, discussion) in both papers, especially if the text is lengthy or truncated. If critical sections are missing, note this in your justification.

Now, please analyze the following citing and cited text:

{context_to_analyze}
"""

    QUESTIONS_AND_FORMATTING_INSTRUCTIONS = """
    Questions:
    1. Which category best describes how the citing paper uses the retracted article retracted/cited text in this context?
    2. Provide a brief justification for your choice (in your own words in maximum 4 sentences)
    3. Provide referencing specific phrases from the text, data or other information to back the justification

    Please format your response *exactly* as follows, with no other text or explanations:

    Answer 1: [Category Name]
    Answer 2: [Your justification]
    Answer 3: [Evidence from Citing Paper: "quote"] [Evidence from Cited Paper: "quote"]
    """

    full_user_prompt = BASE_CONTEXT_TEMPLATE.format(context_to_analyze=citation_context_text) + \
                       QUESTIONS_AND_FORMATTING_INSTRUCTIONS

    return full_user_prompt