import pandas as pd
import argparse
from io import StringIO

# Define the list of key nutrients
key_nutrients = [
    'Calories', 'Iron', 'Zinc', 'Calcium', 'Vitamin A, RAE', 'Thiamin [Vitamin B1]',
    'Riboflavin [Vitamin B2]', 'Niacin [Vitamin B3]', 'Pantothenic acid [Vitamin B5]',
    'Vitamin B6', 'Vitamin B12 [Cobalamin]', 'Folate, DFE [Vitamin B9]', 
    'Vitamin C [Ascorbic acid]', 'Protein', 'Carbohydrate', 'Sugars',
    'Fat', 'Saturated fatty acids', 'Monounsaturated fatty acids', 
    'Polyunsaturated fatty acids', 'Cholesterol'
]

# Setup argument parser
parser = argparse.ArgumentParser(description='Process meal and DRI CSV files.')
parser.add_argument('meal_csv', help='Path to the meal CSV file')
parser.add_argument('dris_csv', help='Path to the DRIs CSV file')
args = parser.parse_args()

# Read the meal CSV file
with open(args.meal_csv, 'r') as file:
    lines = file.readlines()

# Initialize lists to hold the lines for each section
ingredient_lines = []
nutrient_lines = []

# Loop through the lines to collect ingredients
for line in lines:
    if line.startswith('Ingredient,Amount,Unit,Description'):
        ingredient_lines.append(line.strip())
        continue
    if ingredient_lines and line.strip() == '':
        break
    if ingredient_lines:
        ingredient_lines.append(line.strip())

# Loop through the lines to collect nutrients
for line in lines:
    if line.startswith('Nutrient,Amount,Unit,DV'):
        nutrient_lines.append(line.strip())
        continue
    if nutrient_lines and line.strip() == '':
        break
    if nutrient_lines:
        nutrient_lines.append(line.strip())

# Convert lines to StringIO objects to use with pandas read_csv
ingredient_data = StringIO('\n'.join(ingredient_lines))
nutrient_data = StringIO('\n'.join(nutrient_lines))

# Create DataFrames
ingredient_df = pd.read_csv(ingredient_data)
nutrient_df = pd.read_csv(nutrient_data)

# Filter the nutrient DataFrame to only include key nutrients
nutrient_df = nutrient_df[nutrient_df['Nutrient'].isin(key_nutrients)]

# Read the DRIs CSV file
dris_df = pd.read_csv(args.dris_csv)

# Merge nutrient_df with dris_df on the 'Nutrient' column
merged_df = pd.merge(nutrient_df, dris_df, how='left', left_on='Nutrient', right_on='Nutrient')

# Calculate %EAR, %RDA, and %UL, truncated to one decimal place and appended with '%'
merged_df['% EAR'] = merged_df.apply(lambda row: f"{(float(row['Amount']) / float(row['Highest EAR']) * 100):.1f}%" if row['Highest EAR'] != 'NE' and pd.notnull(row['Highest EAR']) else 'N/A', axis=1)
merged_df['% RDA/AI'] = merged_df.apply(lambda row: f"{(float(row['Amount']) / float(row['Highest RDA/AI Males']) * 100):.1f}%" if pd.notnull(row['Highest RDA/AI Males']) else 'N/A', axis=1)
merged_df['% UL'] = merged_df.apply(lambda row: f"{(float(row['Amount']) / float(row['Lowest UL']) * 100):.1f}%" if row['Lowest UL'] != 'ND' and pd.notnull(row['Lowest UL']) else 'N/A', axis=1)

# Select relevant columns
nutrient_final_df = merged_df[['Nutrient', 'Amount', 'Unit_x', '% EAR', '% RDA/AI', '% UL']]
nutrient_final_df.columns = ['Nutrient', 'Amount', 'Unit', '% EAR', '% RDA/AI', '% UL']

# Convert DataFrames to org-mode table format
def df_to_org_table(df):
    org_table = "| " + " | ".join(df.columns) + " |\n"
    org_table += "|-" + "-|-".join(['-' * len(col) for col in df.columns]) + "-|\n"
    for _, row in df.iterrows():
        org_table += "| " + " | ".join(row.astype(str)) + " |\n"
    return org_table

# Create org-mode tables
ingredients_table = df_to_org_table(ingredient_df)
nutrients_table = df_to_org_table(nutrient_final_df)

# Print the org-mode tables
print("Ingredients Table:\n", ingredients_table)
print("Nutrients Table:\n", nutrients_table)
