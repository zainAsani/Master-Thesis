DATA = [
    "Original Data Not Provided",
    "Falsification/ Fabrication of Data",
    "Error in Data",
    "Unreliable Data",
    "Duplication of Data",
    "Concerns/Issues About Data",
	"Plagiarism of Data"
]

METHOD = [
    "Error in Methods",
    "Error in Analyses",
    "Error in Materials",
    "Contamination of Materials",
    "Error in Cell Lines/Tissues",
    "Contamination of Cell Lines/Tissues",
    "IRB/IACUC Approval",
    "Lack of Approval From Company/Institution",
    "Informed Consent - Patient None-Withdrawn",
    "Concerns/Issues About Human Subject Welfare",
    "Sabotage of Materials",
    "Sabotage of Methods"
]

RESULT = [
    "Falsification/Fabrication of Results",
    "Manipulation of Results",
    "Error in Results and/or Conclusion",
    "Unreliable Results",
    "Results Not Reproducible",
    "Concerns/Issues About Results"
]

TEXT = [
    "Plagiarism of Text",
    "Plagiarism of Article",
    "Error in Text",
    "Duplication of Text",
    "Duplication of Article",
    "Randomly Generated Content",
    "Paper Mill",
    "Concerns/Issues About Referencing/Attributions",
    "Cites Retracted Work",
    "Taken From Dissertation/Thesis"
    ]

IMAGE = [
    "Concerns/Issues About Image",
    "Duplication of Image",
    "Falsification/Fabrication of Image",
    "Manipulation of Images",
    "Plagiarism of Image",
    "Unreliable Image",
    "Error in Image"
    ]

AUTHORSHIP = [
    "False/Forged Authorship",
    "False Affiliation",
    "Ethical Violations by Author",
    "Misconduct by Author",
    "Conflict of Interest",
    "Miscommunication by Author",
    "Author Unresponsive",
    "Complaints About Author",
    "Lack of Approval From Author",
    "Concerns/Issues About Authorship/ Affiliation",
    "Objections by Author",
    "Breach of Policy by Author",
    "Forged Authorship"
    ]

PEER_REVIEW_AND_PUBLISHING_PROCESS = [
    "Fake Peer Review",
    "Taken via Peer Review",
    "Concerns/Issues with Peer Review",
    "Error by Journal/Publisher",
    "Duplicate Publication through Error by Journal/ Publisher",
    "Misconduct by Company/Institution",
    "Misconduct by Third Party",
    "Investigation by Company/ Institution",
    "Investigation by Third Party",
    "Investigation by Journal/Publisher",
    "Investigation by ORI",
    "Misconduct - Official Investigation/Finding",
    "Date of Retraction/Other Unknown",
    "Updated to Retraction",
    "Updated to Correction",
    "Upgrade/Update of Prior Notice",
    "Notice - Lack of",
    "Notice - Limited or No Information",
    "Objections by Third Party",
    "Concerns/Issues about Third Party Involvement",
    "Legal Reasons/Legal Threats",
    "Copyright Claims",
    "Nonpayment of Fees/Refusal to Pay",
    "Doing the Right Thing",
    "Removed",
    "Bias Issues or Lack of Balance",
    "Civil Proceedings",
    "Complaints about Company/Institution",
    "Complaints about Third Party",
    "Concerns/Issues about Animal Welfare",
    "Concern/Issues about Article",
    "EOC Lifted",
    "Error by Third Party",
    "Error in Materials (General)",
    "Ethical Violations by Third Party",
    "Hoax Paper",
    "Informed/Patient Consent - None/Withdrawn",
    "Miscommunication by Journal/Publisher",
    "Miscommunication by Third Party",
    "Misconduct - Official Investigation/Finding",
    "No Further Action",
    "Withdrawn to Publish in Different Journal",
    "Notice - Limited or No Information",
    "Notice - Unable to Access via current resources",
    "Objections by Author(s)",
    "Objections by Company/Institution",
    "Publishing Ban",
    "Retract and Replace",
    "Rogue Editor",
    "Salami Slicing",
    "Temporary Removal",
    "Transfer of Copyright/Ownership",
    "Withdrawn (out of date)"
    
]

# Create the dictionary
categories = {
  'Data': DATA,
  'Methods': METHOD,
  'Results': RESULT,
  'Text': TEXT,
  'Images': IMAGE,
  'Authorship': AUTHORSHIP,
  'Peer_Review_and_Publishing_Process': PEER_REVIEW_AND_PUBLISHING_PROCESS
}

# print("Data:", data)
# print("Methods:", methods)
# print("Results:", results)
# print("Text:", text)
# print("Images:", images)
# print("Authorship:", authorship)
# print("Peer Review and Publishing Process:", peer_review_and_publishing_process)