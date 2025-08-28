import openai
from openai import OpenAI
from supabase import create_client
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI"))
supabase = create_client(os.environ.get("SUPABASE_URL"),
                         os.environ.get("SUPABASE_KEY"))
# OpenAI embedding model client initialization

chunkSize = 300


def engineer_prompt(relevent_chunks, parse_description):
    context = "Context:\n"
    for i, chunk in enumerate(relevent_chunks):
        context += f"{i+1}. \"{chunk['content']}\"\n"

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
    try:
        result = supabase.table("documents").insert({
            "content": chunk,
            "embedding": embedding
        }).execute()
        print("Supabase insert result:", result)
    except Exception as e:
        print("Supabase insert error:", e)


def parse_file(pdf, chunksize=chunkSize):
    reader = PdfReader(pdf)
    curr_chunk = []

    for page in reader.pages:
        page_text = page.extract_text()

        words = page_text.split()

        for word in words:
            curr_chunk.append(word)

            # check for end of sentence and over chunksize limit
            if len(curr_chunk) >= chunksize and word.endswith((".", "?", "!")):
                embed(" ".join(curr_chunk))
                curr_chunk = []
                continue

    if curr_chunk:
        embed(" ".join(curr_chunk))


def retrieve_relevent_chunks(query, top_k):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    # gets the vector representation of the embedding in floats
    query_emb = response.data[0].embedding

    # retireves the top_k similar embeddings based on function in supabase
    response = supabase.rpc(
        "match_documents",
        {"query_embedding": query_emb, "match_count": top_k}
    ).execute()

    # returns the embeddings(text)
    return response.data


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
