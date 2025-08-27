import openai
from openai import OpenAI
from supabase import create_client
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
from dotenv import load_dotenv
from parse import extract_text_to_chunks, engineer_prompt, promptLLM, embed, parse_file
import uuid
import json
import time

app = Flask(__name__)
app.secret_key = "storytell-secret-key-2024"  # Change this in production
CORS(app)

# SETUP
# Load OpenAI API key
openai.api_key = os.environ.get("OpenAi")
supabase = create_client(os.environ.get("SUPABASE_URL"),
                         os.environ.get("SUPABASE_KEY"))
# OpenAI embedding model client initialization
client = OpenAI()

# Store PDF data in memory with timestamps for cleanup
pdf_sessions = {}

# Session cleanup function


def cleanup_expired_sessions():
    """Remove sessions older than 24 hours"""
    current_time = time.time()
    expired_sessions = []

    for session_id, session_data in pdf_sessions.items():
        if current_time - session_data.get("created_at", 0) > 86400:  # 24 hours
            expired_sessions.append(session_id)

    for session_id in expired_sessions:
        del pdf_sessions[session_id]
        print(f"Cleaned up expired session: {session_id}")


# --------------------routes---------------------#


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


@app.route("/api/upload-pdf", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No book file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No book selected"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "File must be a PDF book"}), 400

    try:
        # Clean up expired sessions
        cleanup_expired_sessions()

        # Generate session ID
        session_id = str(uuid.uuid4())

        # embed the pdf in supabase
        chunks = parse_file(file)

        # Store in memory with timestamp
        pdf_sessions[session_id] = {
            "chunks": chunks,
            "filename": file.filename,
            "created_at": time.time(),
            "last_accessed": time.time(),
        }

        return jsonify(
            {
                "session_id": session_id,
                "filename": file.filename,
                "chunk_count": len(chunks),
                "message": f"Book uploaded successfully! Found {len(chunks)} text sections for analysis.",
            }
        )

    except Exception as e:
        return jsonify({"error": f"Error processing book: {str(e)}"}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    session_id = data.get("session_id")
    message = data.get("message")

    if not session_id or not message:
        return jsonify({"error": "Missing session_id or message"}), 400

    if session_id not in pdf_sessions:
        return jsonify(
            {"error": "Invalid session ID. Please upload your book again."}
        ), 400

    try:
        # Update last accessed time
        pdf_sessions[session_id]["last_accessed"] = time.time()

        # Get stored PDF data
        pdf_data = pdf_sessions[session_id]
        chunks = pdf_data["chunks"]

        # Embed the user's question
        question_embedding = client.embeddings.create(
            input=message, model="text-embedding-3-small", encoding_format="float"
        )

        # Find relevant chunks
        similarities = util.cos_sim(question_embedding, chunk_embeddings)
        top_k = 5
        top_chunk_indices = similarities.argsort(descending=True)[0][:top_k]

        # Get relevant chunks
        relevant_chunks = [chunks[i] for i in top_chunk_indices]

        # Get AI response
        response = promptLLM(relevant_chunks, message)

        return jsonify(
            {"response": response,
                "relevant_chunks_count": len(relevant_chunks)}
        )

    except Exception as e:
        return jsonify({"error": f"Error generating response: {str(e)}"}), 500


@app.route("/api/clear-session", methods=["POST"])
def clear_session():
    data = request.get_json()
    session_id = data.get("session_id")

    if session_id in pdf_sessions:
        del pdf_sessions[session_id]
        print(f"Session cleared by user: {session_id}")

    return jsonify({"message": "Book session cleared successfully"})


@app.route("/api/privacy-info")
def privacy_info():
    """Return information about data privacy"""
    return jsonify(
        {
            "privacy_policy": {
                "data_storage": "Books are processed in memory only and never saved to disk",
                "session_duration": "Sessions are automatically cleaned up after 24 hours of inactivity",
                "data_usage": "Book content is only used to answer your questions and is not shared with third parties",
                "embeddings": "Text embeddings are stored temporarily in memory and deleted when the session ends",
                "openai_usage": "Your questions and relevant book passages are sent to OpenAI for processing, but your full book is never uploaded",
            }
        }
    )


if __name__ == "__main__":
    print("📚 Starting server on http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
