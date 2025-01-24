from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st


template = (
    "You are an AI assistant tasked with helping users extract specific information from a PDF document. "
    "You have been given a chunk of the document, and the user is asking about a specific event or detail. the chunk is as follows: {allContent}"
    "Please follow these instructions carefully:\n\n"
    "1. **Context:** This is a portion of a larger document, and the user is asking about something specific: {parse_description}. "
    "You must provide an answer only if the information is present in this chunk.\n"
    "2. **Search for Relevant Information:** Focus on the most relevant parts of the text, and only extract the information that directly matches the user's question. "
    "3. **No Extra Content:** Do not include any extra explanations, and return only the extracted information. "
    "4. **Empty Response:** If you do not find any relevant information in this chunk that answers the prompt, return an empty string."
    "5. **Chunk Consideration:** Each chunk represents part of a larger document. If the information is not in this chunk, return an empty string. If it is, answer succinctly."
)


model = OllamaLLM(model="llama3.2")


def splitChunks(text, chunksize=8000):
    # st.write(f"text length before splitting: {len(text)}")
    splitText = text.split()
    # st.write(f"Total number of words in document: {len(splitText)}")
    chunks = [splitText[i:i+chunksize]
              for i in range(0, len(splitText), chunksize)]
    # st.write(f"total number of chunks: {len(chunks)}")
    return [" ".join(chunk) for chunk in chunks]


def parseText(allChunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
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
