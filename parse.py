import openai
from openai import OpenAI
from supabase import create_client
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_core.prompts import ChatPromptTemplate


openai.api_key = os.environ.get("OpenAi")
supabase = create_client(os.environ.get("SUPABASE_URL"),
                         os.environ.get("SUPABASE_KEY"))
# OpenAI embedding model client initialization
client = OpenAI()

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


# create embeddings in supabase
def embed(chunk):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk
    )
    # gets the first embedding from the list of embeddings generated
    embedding = response.data[0].embedding

    # move to supabase
    supabase.table("documents").insert({
        "content": chunk,
        "embedding": embedding
    }).execute()


def parse_file(pdf, chunksize=chunkSize):
    reader = PdfReader(pdf)
    curr_chunk = []
    chunk_count = 0

    for page in reader.pages:
        page_text = page.extractText()

        words = page_text.split()

        for word in words:
            curr_chunk.append(word)

            # check for end of sentence and over chunksize limit
            if len(curr_chunk) >= chunksize and word.endswith((".", "?", "!")):
                embed(" ".join(curr_chunk))
                curr_chunk = []
                chunk_count += 1
                continue

    if curr_chunk:
        embed(" ".join(curr_chunk))
        chunk_count += 1
    return chunk_count


def retrieve_relevent_chunks(query)


def promptLLM(relevent_chunks, parse_description):
    prompt = engineer_prompt(relevent_chunks, parse_description)

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are a assistant answering questions based only on the provided context"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
