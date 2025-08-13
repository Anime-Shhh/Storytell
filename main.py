import os
import openai
import streamlit as st
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv
from parse import (
    extract_text_to_chunks,
    engineer_prompt,
    promptLLM
)

# load embedding mode
embedding_model = SentenceTransformer(
    'sentence-transformers/all-mpnet-base-v2')

# load api
# load_dotenv()
openai.api_key = os.environ.get("OpenAi")

st.title("AI PDF Reader")

# ask the user to upload their file and ensure its a pdf
userFile = st.file_uploader("Upload your PDF file", type=["pdf"])

# ensure that a file was uploaded
if userFile is not None:
    # read file and convert to chunks
    split_text_chunks = extract_text_to_chunks(userFile)

    st.write(f"""PDF read successfuly and was split into {len(split_text_chunks)} chunk(s)
             for the AI's readibility""")

    # embed the split chunks
    chunk_embeddings = embedding_model.encode(
        split_text_chunks, convert_to_tensor=True)

    # get the prompt from the user
    parse_description = st.text_area(
        "What question do you have regarding this file?")

    # embed the question
    question_embedding = embedding_model.encode(
        parse_description, convert_to_tensor=True)

    # find relevent chunks
    similarities = util.cos_sim(question_embedding, chunk_embeddings)
    top_k = 5  # change value for how many similar chunks you want
    top_chunk_indicies = similarities.argsort(descending=True)[0][:top_k]

    # get the relevent chunks
    relevent_chunks = [split_text_chunks[i] for i in top_chunk_indicies]

    if st.button("Search File"):
        if parse_description.strip():
            response = promptLLM(relevent_chunks, parse_description)
            st.write(response)

            # st.write("Cleaned content")
            # st.write(recheckText(parsedContent))
        else:
            # in case nothing is passed
            st.warning("Enter a valid question or description")
