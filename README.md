# AI PDF Reader

This is a Streamlit-based application that allows users to upload PDF files, extract their content into manageable chunks, and interact with an AI model to answer questions about the content. The project leverages OpenAI's GPT-3.5-turbo for natural language processing and SentenceTransformers for embedding and similarity matching.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-pdf-reader.git
   cd ai-pdf-reader
   ```
2. Set up a Python virtual environment (optional but recommended):
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # Linux/Mac
   myenv\Scripts\activate    # Windows
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Add your OpenAI API key in a file named apiKeys.py in the following format:
   ```python
   OpenAi = "your_openai_api_key"
   ```
   
   ---

## Usage
1. Run the application:
  ```bash
  streamlit run main.py
  ```
2. Upload a PDF file using the provided file uploader in the Streamlit interface.
3. Ask a question or provide a description of the information you are looking for.
4. Click the "Search File" button to get answers based on the content of the PDF.

## My File Structure
```
.
├── main.py               # Main Streamlit app file
├── parse.py              # File containing utility functions for text extraction and AI interaction
├── requirements.txt      # List of dependencies
├── apiKeys.py            # File to store OpenAI API key (excluded from version control)

```
