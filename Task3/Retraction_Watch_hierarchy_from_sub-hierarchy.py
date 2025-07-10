from hierarchy_list import categories
import pandas as pd
import os
import re

# Function to normalize text: convert to lowercase and remove special characters
def normalize_text(text):
    # Convert to lowercase and remove special characters, keeping only alphanumeric and spaces
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

# Create a reverse mapping from normalized sub-hierarchy to hierarchy
sub_to_hierarchy = {}
for hierarchy, sub_hierarchies in categories.items():
    for sub_hierarchy in sub_hierarchies:
        normalized_sub = normalize_text(sub_hierarchy)
        sub_to_hierarchy[normalized_sub] = hierarchy

# Input and output file paths
input_file = "C:/Users/Zaina/Desktop/TU Braunschweig/Semester 6/MasterArbeit/Task3/Data/Task_3_Annotation-MU-dependent_gpt_gemini.csv"
output_file = "C:/Users/Zaina/Desktop/TU Braunschweig/Semester 6/MasterArbeit/Task3/Data/Task_3_Annotation-MU-dependent_gpt_gemini.csv"

# Read the CSV file
df = pd.read_csv(input_file)

# Function to map sub-hierarchies to hierarchies
def map_to_hierarchies(retraction_text):
    if pd.isna(retraction_text):
        return set()
    # Split the retraction text by newlines and clean up
    sub_hierarchies = [s.strip().lstrip('+') for s in retraction_text.split('\n') if s.strip()]
    # Map each sub-hierarchy to its top-level hierarchy
    hierarchies = set()
    for sub_hierarchy in sub_hierarchies:
        normalized_sub = normalize_text(sub_hierarchy)
        hierarchy = sub_to_hierarchy.get(normalized_sub, 'Other')
        hierarchies.add(hierarchy)
    return hierarchies

# Apply the mapping function to the Retraction_Watch column
df['Retraction_Watch_citing_hierarchy'] = df['Retraction_Watch_citing'].apply(map_to_hierarchies)

# Save the updated DataFrame to a new CSV file
df.to_csv(output_file, index=False)