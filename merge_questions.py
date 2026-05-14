import json

# Read the new 152 questions from the attachment
with open(r'c:\Users\User\Downloads\prev_year_2026.json', 'r', encoding='utf-8') as f:
    new_data = json.load(f)

# Extract the 152 questions
questions_2026 = new_data['previous_year_questions']

# Create the year object for 2026
year_2026 = {
    'year': '2026',
    'questions': questions_2026
}

# Read existing years (2024, 2023)
with open(r'c:\Users\User\Desktop\J\questions\prev.json', 'r', encoding='utf-8-sig') as f:
    existing = json.load(f)

# Keep 2024 and 2023 if they exist
other_years = [y for y in existing if y['year'] != '2026']

# Combine: new 2026 first, then 2024, 2023
combined = [year_2026] + other_years

# Write back to prev.json
with open(r'c:\Users\User\Desktop\J\questions\prev.json', 'w', encoding='utf-8') as f:
    json.dump(combined, f, indent=2, ensure_ascii=False)

print('✓ Successfully merged 152 questions for 2026')
print(f'Total years: {len(combined)}')
for y in combined:
    print(f'  {y["year"]}: {len(y["questions"])} questions')
