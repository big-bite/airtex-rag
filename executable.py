from utils import *
import pandas as pd
from openai import OpenAI
from utils import *
# Executable file to add all pdf text to the csv file

# openai = OpenAI()

# def gpt_response(history):
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=history,
#         stream=True
#     )
#     for chunk in response:
#         if chunk.choices[0].delta.content is not None:
#             yield chunk.choices[0].delta.content

df = pd.read_csv('aritex_task.csv', header=1)

folder_path = 'pdf_files'

pdf_files = list_pdf_files(folder_path)

for doc_selected in pdf_files:
    print("Processing: ", doc_selected, end=' >>> ')
    filter_df = df[df['Document name'].str.contains(doc_selected)]
    if filter_df.empty:
        continue
    code_value = filter_df['Code to search'].values[0]
    is_doc = filter_df['imagen/documento'].str.lower().values[0] == 'doc'
    
    print("Code Value: ", code_value, end=' >>> ')
    if is_doc:
        pdf_text = get_pdf_text(os.path.join(folder_path, doc_selected+ '.pdf'))
    else:
        pdf_text = get_text_from_pdf_image(os.path.join(folder_path, doc_selected+ '.pdf'))
    
    print("Text Length: ", len(pdf_text), end=' >>> ')
    df.loc[filter_df.index, 'Extracted Text'] = pdf_text    
    print("Success")
df.to_csv('aritex_task_updated.csv', index=False)
    
