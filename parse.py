import openai
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_core.prompts import ChatPromptTemplate


openai.api_key = os.environ.get("OpenAi")


chunkSize = 300


def engineer_prompt(relevent_chunks, parse_description):
    context = "Context:\n"
    for i, chunk in enumerate(relevent_chunks):
        context += f"{i+1}. \"{chunk}\"\n"

    prompt = f"""
    {context}
    Instruction: Using ONLY the information provided in the context above,
    answer the following question in DETAIL. If the context does not provide enough
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


def promptLLM(relevent_chunks, parse_description):
    prompt = engineer_prompt(relevent_chunks, parse_description)

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a assistant answering questions based only on the provided context"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
