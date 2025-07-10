
def build_prompt(citation_context_text):
    """
    Builds the full prompt for the OpenAI API.
    The BASE_CONTEXT describes the task and classification categories.
    The citation_context_text is the specific text from the CSV to be analyzed.
    """
    BASE_CONTEXT_TEMPLATE = """You are an expert scientometrician specializing in the analysis of scholarly citations. Your task is to determine how a citing paper uses a **retracted article**, denoted as <RA>, based on some, but not all, Example Phrases provided.

        Please classify the citation's function into one of the following categories. The Example Phrases are some words and phrases used to :

        1.  **Uses_Data**: The citing paper explicitly states it is using, re-analyzing, or referring to specific datasets or raw data originating from the retracted article <RA>.
            *Example Phrases:* data, dataset, experimental data, data from <RA>, using the dataset of <RA>, figures from <RA>, tables from <RA>, raw data provided by <RA>, background information from <RA>
            *Example Classification:* Uses_Data
            *Example Justification:* The citing paper states it performed a "secondary analysis on the data from <RA>".

        2.  **Uses_Results**: The citing paper explicitly states it is using, building upon, comparing its own results directly to, or attempting to replicate specific findings or conclusions reported in the retracted article <RA>.
            *Example Phrases:* as shown in <RA>, the results of <RA> indicate, findings from <RA> suggest, according to <RA>, the outcome was similar/ same, the study by <RA> demonstrated, result extension from <RA>
            *Example Classification:* Uses_Results
            *Example Justification:* The citing paper is re-examining an "initial finding" from the retracted <RA>.

        3.  **Uses_Methods**: The citing paper explicitly states it is employing, adapting, following, or referencing a specific methodology, experimental procedure, protocol, algorithm, or theoretical approach described in the retracted article <RA>.
            *Example Phrases:* following the method described in <RA>, using the technique from <RA>, adopting the approach of <RA>, based on the protocol outlined in <RA>, employing the procedure from <RA>, method from <RA>
            *Example Classification:* Uses_Methods
            *Example Justification:* The citing paper "initially adapted" the "protocol" from <RA>.

        4.  **Shows_Consistency**: The citing paper states its findings, arguments, theoretical stance, or observations are generally consistent with, or in alignment with, the broader claims or framework of the retracted article <RA>, without necessarily detailing use of specific data, results, or methods.
            *Example Phrases:*  consistent with the findings of <RA>, in agreement with <RA>, similar results were obtained as in <RA>, confirms the observations of <RA>, supports the conclusions drawn in <RA>, result extension from <RA>
            *Example Classification:* Shows_Consistency
            *Example Justification:* The citing paper states its "general trend is consistent with" the work of <RA>.

        5.  **Other**: The citation's function within the context does not clearly or primarily fall into any of the above categories, or the context is insufficient to make a determination.

        Now, please analyze the following citation context:
        {context_to_analyze}
        """
    QUESTIONS_AND_FORMATTING_INSTRUCTIONS = """
        Questions:
        1.  Which category best describes how the citing paper uses the retracted article <RA> in this context?
        2.  Provide a brief justification for your choice, referencing specific phrases or ideas from the provided sentences.

        Please format your response *exactly* as follows, with no other text or explanations:
        Answer 1: [Category Name]
        Answer 2: [Your justification]
        """
    full_user_prompt = BASE_CONTEXT_TEMPLATE.format(context_to_analyze=citation_context_text) + \
                       QUESTIONS_AND_FORMATTING_INSTRUCTIONS
    return full_user_prompt



CATEGORIES_DATA = {
    "Uses_Data": "The text explicitly states it is using, re-analyzing, or referring to specific datasets or raw data originating from the retracted article.",
    "Uses_Results": "The citing paper explicitly states it is using, building upon, comparing its own results directly to, or attempting to replicate specific findings or conclusions reported in the retracted article.",
    "Uses_Methods": "The citing paper explicitly states it is employing, adapting, following, or referencing a specific methodology, experimental procedure, protocol, algorithm, or theoretical approach described in the retracted article.",
    "Shows_Consistency": "The citing paper states its findings, arguments, theoretical stance, or observations are generally consistent with, or in alignment with, the broader claims or framework of the retracted article, without necessarily detailing use of specific data, results, or methods.",
    "Other": "The citation's function within the context does not clearly or primarily fall into any of the above categories, or the context is insufficient to make a determination."
}