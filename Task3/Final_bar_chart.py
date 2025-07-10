import pandas as pd
import matplotlib.pyplot as plt

def plot_unique_values_pie_chart(csv_file_path, column_name):

    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Filter rows where alignment is True
        # df = df[df['alignment'] == True]
        
        # Check if column exists
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in CSV file")
        
        # Count unique values
        value_counts = df[column_name].value_counts()
        
        # Create pie chart with actual counts
        plt.figure(figsize=(8, 8))
        plt.pie(value_counts.values, 
                labels=value_counts.index,
                autopct=lambda p: f'{int(p * sum(value_counts.values) / 100)}',
                labeldistance=1.15,  # Move labels further out to avoid overlap
                textprops={'fontsize': 10})  # Control text size
        plt.title('Category by Gemini', y=1.1)  # Move title upward
        
        # Ensure the pie chart is circular
        plt.axis('equal')
        
        # Adjust layout with padding to prevent text cutoff
        plt.tight_layout(pad=2.0)
        
        # Show the plot
        plt.show()
        
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

input_csv_path = r"C:\Users\Zaina\Desktop\TU Braunschweig\Semester 6\MasterArbeit\Task3\Data\Task_3_Annotation-MU-dependent_gpt_gemini.csv"

# Example usage:
plot_unique_values_pie_chart(input_csv_path, 'category_gemini')