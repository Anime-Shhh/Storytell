from PyPDF2 import PdfReader
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st


template = (
    "You are an AI assistant tasked with helping users extract specific information from a PDF document. "
    "You have been given chunks of the document and can only use these chunks to answer. the chunks are as follows: {allContent}"
    "Please follow these instructions carefully:\n\n"
    "1. **Context:** This is a portion of a larger document, and the user is asking about something specific: {parse_description}. "
    "You must provide an answer only if the information is present in this chunk.\n"
    "2. **Search for Relevant Information:** Focus on the most relevant parts of the text, and only extract the information that directly matches the user's question. "
    "3. **No Extra Content:** Do not include any extra explanations, and return only the extracted information. "
    "4. **Empty Response:** If you do not find any relevant information in this chunk that answers the prompt, return an empty string."
    "5. **Chunk Consideration:** Each chunk represents part of a larger document. If the information is not in this chunk, return an empty string. If it is, answer succinctly."
)


model = OllamaLLM(model="llama3.2")

chunkSize = 1000


def engineer_prompt(relevent_chunks, parse_description):
    context = "Context:\n"
    for i, chunk in enumerate(relevent_chunks):
        context += f"{i+1}. \"{chunk}\"\n"

    prompt = f"""
    {context}
    Instruction: Using ONLY the information provided in the context above,
    answer the following question. If the context does not provide enough
    information to answer the question, respond with "I cannot answer this
    question based on the given context."

    Question: {parse_description}

    """
    return prompt


def extract_text_to_chunks(pdf, chunksize=chunkSize):
    reader = PdfReader(pdf)
    chunks = []
    curr_chunk = []
    curr_chunk_word_count = 0

    for page in reader.pages:
        page_text = page.extract_text()

        words = page_text.split()

        for word in words:
            curr_chunk.append(word)
            curr_chunk_word_count += 1

            if curr_chunk_word_count >= chunksize:
                chunks.append(" ".join(curr_chunk))
                curr_chunk_word_count = 0
                curr_chunk = []

    # possible case of leftovers in curr_chunk then add it as the last chunk
    if curr_chunk:
        chunks.append(" ".join(curr_chunk))

    return chunks


def parseText(allChunks, parse_description):

    prompt = ChatPromptTemplate.from_template(template)
    # prompt = engineer_prompt(allChunks, parse_description)
    chain = prompt | model

    allParsedResults = []

    for i, chunk in enumerate(allChunks, start=1):
        response = chain.invoke(
            {"allContent": chunk, "parse_description": parse_description})
        if "empty string" in response.lower():
            # to see where relevent info was found and where it doesnt exist
            st.write(f"Parsed chunk {i} of {len(allChunks)}: MISS")
            # allParsedResults.append(response)
        elif "no mention" in response.lower():
            st.write(f"Parsed chunk {i} of {len(allChunks)}: MISS")
        elif "not contain" in response.lower():
            st.write(f"Parsed chunk {i} of {len(allChunks)}: MISS")
        else:
            st.write(f"Parsed chunk {i} of {len(allChunks)}: HIT!")
            allParsedResults.append(response)

    return "\n".join(allParsedResults)


def promptLLM(relevent_chunks, parse_description):
    prompt = engineer_prompt(relevent_chunks, parse_description)

    prompt_template = ChatPromptTemplate.from_template("{input}")
    chain = prompt_template | model

    response = chain.invoke({"input": prompt})
    return response
