import os
import re

def clean_text(text):
    # Remove XML tags
    cleaned_text = re.sub(r'<[^>]+>', '', text)

    # Remove other markup (e.g., {{...}}, [http://...], [[:...]], [[...]], <!--...-->, {{*}}...{{/*}})
    cleaned_text = re.sub(r'\{\{[^}]*\}\}', '', cleaned_text)
    cleaned_text = re.sub(r'\[[:\]?[^\]]+\]', '', cleaned_text)
    cleaned_text = re.sub(r'<!--[^>]+-->', '', cleaned_text)
    cleaned_text = re.sub(r'\{\{[/*]?[^}]+\}\}', '', cleaned_text)

    # Remove extra whitespace
    cleaned_text = ' '.join(cleaned_text.split())

    return cleaned_text

def clean_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                cleaned_text = clean_text(text)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_text)

if __name__ == '__main__':
    directory = 'articles'
    clean_files(directory)