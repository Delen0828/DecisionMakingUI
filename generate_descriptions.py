import json
import os
from openai import OpenAI
from typing import Dict, List
import time

def load_json_file(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_source_description(source_name: str, sources_data: List[Dict]) -> str:
    for source in sources_data:
        if source["name"] == source_name:
            return f"Source Type: {source['type']}\nTrust Level: {source['trust_level']}\nDescription: {source['description']}"
    return "Source information not found"

def generate_ai_description(target: Dict, source_info: str, client: OpenAI) -> str:
    prompt = f"""
Given the following target information and source characteristics, generate a 100-word description in the tone and style matching the source's nature:

Target Information:
- Name: {target['Target Name']}
- Category: {target['Target Category']}
- Cluster Damage: {target['Cluster Damage']}
- Certainty: {target['Certainty']}
- Suggested Strike Method: {target['Suggested Strike Method']}

Source Information:
{source_info}

Generate a detailed 100-word intelligence description of the target that matches the source's tone, reliability level, and characteristics.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an intelligence analyst writing target descriptions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating description for {target['Target Name']}: {str(e)}")
        return "Description generation failed"

def main():
    # Initialize OpenAI client
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")
    
    client = OpenAI(api_key=api_key)

    # Load data files
    targets_data = load_json_file('processed_data.json')
    sources_data = load_json_file('source.json')

    # Process each target
    for target in targets_data:
        source_info = get_source_description(target['Source'], sources_data)
        
        # Add delay to respect API rate limits
        time.sleep(1)
        
        # Generate and add AI description
        target['AI Description'] = generate_ai_description(target, source_info, client)
        print(f"Generated description for {target['Target Name']}")

    # Save updated data
    with open('processed_data_with_descriptions.json', 'w', encoding='utf-8') as file:
        json.dump(targets_data, file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main() 