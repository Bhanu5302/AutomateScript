import pandas as pd
import json


#-----------------File names with path ---------------------------------
nodered_file = 'flow.json'  # Replace with your file path
excel_file = 'variables_mapping.xlsx'  # Replace with your file path
#-----------------------------------------------------------------

df = pd.read_excel(excel_file)

mapping = dict(zip(df['old_variable'], df['new_variable']))

# Load the Node-RED flow

with open(nodered_file, 'r', encoding='utf-8') as file:
    data = json.load(file)


def replace_values(data, mapping):
    if isinstance(data, dict):
        # Apply the replacement to both keys and values in the dictionary
        return {replace_values(key, mapping): replace_values(value, mapping) for key, value in data.items()}
    elif isinstance(data, list):
        # Apply the replacement to each item in the list
        return [replace_values(item, mapping) for item in data]
    elif isinstance(data, str):
        # Replace any occurrences of old variables with new ones in the string
        for old, new in mapping.items():
            data = data.replace(old, new)
        return data
    else:
        # Return data as-is if it's neither a dict, list, nor string
        return data

# Replace old variables with new variables in the Node-RED flow
updated_data = replace_values(data, mapping)

# Save the updated Node-RED flow JSON file
updated_nodered_file = 'updated_nodered_flow.json'  # Replace with your desired output file path
with open(updated_nodered_file, 'w', encoding='utf-8') as file:
    json.dump(updated_data, file, indent=4)

print(f'Updated Node-RED flow has been saved to {updated_nodered_file}')
