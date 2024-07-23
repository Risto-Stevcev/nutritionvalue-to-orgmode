import pandas as pd

# Define the list of key nutrients
key_nutrients = [
    'Calories', 'Iron', 'Zinc', 'Calcium', 'Vitamin A, RAE', 'Thiamin [Vitamin B1]',
    'Riboflavin [Vitamin B2]', 'Niacin [Vitamin B3]', 'Pantothenic acid [Vitamin B5]',
    'Vitamin B6', 'Vitamin B12 [Cobalamin]', 'Folate, DFE [Vitamin B9]', 
    'Vitamin C [Ascorbic acid]', 'Protein', 'Carbohydrate', 'Sugars',
    'Fat', 'Saturated fatty acids', 'Monounsaturated fatty acids', 
    'Polyunsaturated fatty acids', 'Cholesterol'
]

# Read the entire CSV file
csv_file = 'meal.csv'  # Path to your CSV file
with open(csv_file, 'r') as file:
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
from io import StringIO
ingredient_data = StringIO('\n'.join(ingredient_lines))
nutrient_data = StringIO('\n'.join(nutrient_lines))

# Create DataFrames
ingredient_df = pd.read_csv(ingredient_data)
nutrient_df = pd.read_csv(nutrient_data)

# Filter the nutrient DataFrame to only include key nutrients
nutrient_df = nutrient_df[nutrient_df['Nutrient'].isin(key_nutrients)]

# Convert DataFrames to org-mode table format
def df_to_org_table(df):
    org_table = "| " + " | ".join(df.columns) + " |\n"
    org_table += "|-" + "-|-".join(['-' * len(col) for col in df.columns]) + "-|\n"
    for _, row in df.iterrows():
        org_table += "| " + " | ".join(row.astype(str)) + " |\n"
    return org_table

# Create org-mode tables
ingredients_table = df_to_org_table(ingredient_df)
nutrients_table = df_to_org_table(nutrient_df)

# Print the org-mode tables
print("Ingredients Table:\n", ingredients_table)
print("Nutrients Table:\n", nutrients_table)
