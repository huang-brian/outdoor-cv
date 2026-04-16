# generates body html text from a csv
# https://gemini.google.com/app/80d1178c8166a432
# example usage: python html_gen.py outdoorcv.csv bodytext.html
import pandas as pd
import sys
import os

def generate_cv_body(csv_filename):
    if not os.path.exists(csv_filename):
        return f"Error: The file '{csv_filename}' was not found."

    df = pd.read_csv(csv_filename)
    df = df.fillna('')
    
    body_html = ["<h1>Outdoor Experience</h1>"]
    
    for _, row in df.iterrows():
        date = row['date']
        date_sub = row['date subheader (grey)']
        title = row['title']
        title_sub = row['title subheader (grey)']
        desc = row['description']
        
        entry = [
            '    <div class="cv-entry">',
            '        <div class="left-col">',
            f'            <div>{date}</div>'
        ]
        if date_sub:
            entry.append(f'            <div class="grey">{date_sub}</div>')
        
        entry.append('        </div>')
        entry.append('        <div class="right-col">')
        entry.append(f'            <div class="bold">{title}</div>')
        
        if title_sub:
            entry.append(f'            <div class="grey">{title_sub}</div>')
        if desc:
            desc_formatted = desc.replace('\n', '<br>\n                ')
            entry.append(f'            <div class="description">\n                {desc_formatted}\n            </div>')
            
        entry.append('        </div>')
        entry.append('    </div>')
        body_html.append('\n'.join(entry))
        
    return '\n'.join(body_html)

if __name__ == "__main__":
    # Check if both parameters are provided
    if len(sys.argv) != 3:
        print("Usage: python generate_cv.py <input_csv_path> <output_filename>")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        
        html_content = generate_cv_body(input_path)
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        print(f"Success! HTML body code saved to {output_path}")