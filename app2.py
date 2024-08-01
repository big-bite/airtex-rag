import streamlit as st 
import pandas as pd
from openai import OpenAI
from utils import *

st.set_page_config(page_title="Airtex Streamlit POC", page_icon="🎴", layout="wide")

client = OpenAI()

st.title("🎴 Airtex Streamlit POC ")
st.write("It is a tool to search for the item code in the document and provide the explaination related to it. ")
st.write('---')
df = pd.read_csv('aritex_task_updated.csv', header=0)

def gpt_response(history):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=history,
        # stream=True
    )
    # for chunk in response:
    #     if chunk.choices[0].delta.content is not None:
    #         yield chunk.choices[0].delta.content
    return response.choices[0].message.content


page_divide = st.columns(2, gap="medium")

with page_divide[0]:

    input_cols = st.columns(2)
    # with input_cols[0]:
    # doc = st.file_uploader("Upload a file", type=["pdf", "txt", "csv", "xlsx"])

    folder_path = 'pdf_files'

    pdf_files = list_pdf_files(folder_path)
    # docs = df[df['imagen/documento'].str.lower() == 'doc']['Document name']
    # pdf_files = [doc for doc in pdf_files if doc in docs.values]

    doc_selected = st.selectbox("Select from the following documents in the folder", pdf_files)
    filter_df = df[df['Document name'].str.contains(doc_selected)]
    if filter_df.empty:
        st.error("No data found for the selected document")
        st.stop()
    code_value = filter_df['Code to search'].values[0]
    # is_doc = filter_df['imagen/documento'].str.lower().values[0] == 'doc'
    
    

    code_input = st.text_input("Enter some code", code_value)
    if doc_selected:
        # selected_path = os.path.join(folder_path, doc_selected+'.pdf')
        # if is_doc:
        #     pdf_text = get_pdf_text(selected_path)
        # else:
        #     pdf_text = get_text_from_pdf_image(selected_path)
        pdf_text = filter_df['Extracted Text'].values[0]

        st.text_area("Extracted Text", pdf_text, height=240)

    go = st.button("Run")


init_prompt = f"""You are given a item code and a document. You need to find if the item code or anything similar to it is present in the document. 
If you find the item code or any similar code, you need to provide the explaination related to it. Include information from the document, but dont 
write the exact content from the document. We need only refined information. 

An ideal example if direct similarity under same category is present: 
<just an example>
"The material code ""S355JR"" was not found in the document. However, a similar material code ""S355J2H"" was found. The difference between ""S355JR"" and ""S355J2H"" lies in their impact test requirements and specific applications:

S355JR: This grade has a minimum yield strength of 355 MPa and is suitable for general structural applications. It requires a Charpy V-notch impact test at room temperature (20°C) with a minimum energy of 27 Joules.

S355J2H: This grade also has a minimum yield strength of 355 MPa but is used for hollow sections and requires a Charpy V-notch impact test at a lower temperature (-20°C) with a minimum energy of 27 Joules.

Here is the relevant excerpt from the document:

Steel grade S355J2H Z3
</just an example>


If you do not find the item code or any similar code, you need to provide a response saying that the code is not present in the document. The code should also match some character then is declared as similar.

Here is the document which you need to search for the item code:

<Document Text>
{pdf_text}
</Document Text>

# Language: English
# Format: At the last line of the resoponse, write the answer in square brackets. [Accurate] or [Similar] or  [Not Found] 
(Return Similar if it is related to the same class or category of elements)
- Give the clear and short 4-5 points of importance if word is similar or found. 
- Dont give the context if the code is not found.
- Do not provide extra information if word is completely different.
""" 

item_detail: f"""
Search for it...

Item Code: {code_input}

"""

history = [
    {"role": "system", "content": init_prompt},
    {"role": "assistant", "content": "Enter the item code you want to search for"},
    {"role": "user", "content": code_input}
]
    

with page_divide[1]:
    st.subheader("The data preview")
    st.dataframe(df)



if True:
    response = gpt_response(history)
    full_response = response
    st.write("#### Response")
    with st.container(border=True):
        st.info(full_response,)
    
    # Extract final response as last line [Accurate] or [Similar] or [Not Found], removing []
    # final_response = full_response.split('\n')[-1]
    final_response = full_response.split('[')[-1].replace(']', '')
    st.write(final_response)

