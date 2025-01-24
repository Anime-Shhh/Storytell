import streamlit as st
from PyPDF2 import PdfReader
from parse import (
    splitChunks,
    parseText
)

st.title("AI PDF Reader")

# ask the user to upload their file and ensure its a pdf
userFile = st.file_uploader("Upload your PDF file", type=["pdf"])

# ensure that a file was uploaded
if userFile is not None:
    # setup for processing the file uploaded
    processor = PdfReader(userFile)
    text = ""

    # process every page
    for page in processor.pages:
        text += page.extract_text() or ""

    # for debugging, show extracted text length and first 500 words
    st.write(f"Extracted text length is {len(text)} characters")
    # st.write(f"the first 500 words are: \n{text[:500]}")

    splitText = splitChunks(text)
    st.write(f"""PDF read successfuly and was split into {len(splitText)} chunk(s)
             for the AI's readibility""")

    # get the prompt from the user
    parse_description = st.text_area(
        "What question do you have regarding this file?")
    if st.button("Search File"):
        if parse_description.strip():
            parsedContent = parseText(splitText, parse_description)
            st.write(parsedContent)

            # st.write("Cleaned content")
            # st.write(recheckText(parsedContent))
        else:
            st.warning("Enter a valid question or description")
