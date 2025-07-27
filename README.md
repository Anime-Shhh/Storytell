# Storytell - Your Personal Book Companion

A modern web application that lets you chat with your books without spoilers. Upload your book PDF and have spoiler-free conversations about the story, characters, and plot points you've read so far.

## ✨ Features

- **🛡️ Spoiler-Free Zone**: Ask questions about your current reading progress without fear of spoilers from future chapters
- **📚 Book Conversations**: Have natural conversations about characters, plot points, and themes
- **🧠 Smart Analysis**: AI-powered analysis that understands context and story progression
- **🔒 Privacy First**: Your books are processed in memory only and never stored permanently
- **🎨 Beautiful UI**: Persona 5-inspired design with dynamic animations and purple theme
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anime-Shhh/Storytell.git
   cd Storytell
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key**
   Create or update `apiKeys.py` with your OpenAI API key:
   ```python
   OpenAi = "your_openai_api_key_here"
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎯 How to Use

### Landing Page
- Learn about Storytell's spoiler-free features
- Click "Start Reading" to begin

### Chatbot Interface
1. **Upload Book**: Drag and drop or click to select your book PDF
2. **Wait for Analysis**: The AI will analyze your book (usually takes 10-30 seconds)
3. **Start Chatting**: Ask questions about characters, plot, themes, and more
4. **Get Spoiler-Free Insights**: Receive answers based only on what you've read so far

### Example Questions
- "What is the main character's motivation?"
- "Can you summarize what happened so far?"
- "What are the main themes in this book?"
- "Who are the key characters introduced so far?"
- "What's the current conflict in the story?"

## 🛠️ Technical Stack

### Backend
- **Flask**: Web framework for API endpoints
- **OpenAI GPT-3.5**: Natural language processing
- **Sentence Transformers**: Semantic search and embeddings
- **PyPDF2**: PDF text extraction

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript (ES6+)**: Interactive functionality
- **Persona 5 Design**: Dynamic UI with geometric animations
- **Responsive Design**: Mobile-first approach

### Key Technologies
- **Semantic Search**: Uses `all-mpnet-base-v2` model for book understanding
- **RAG Architecture**: Retrieval-Augmented Generation for accurate responses
- **Session Management**: Secure book processing with unique session IDs

## 📁 Project Structure

```
Storytell/
├── app.py                 # Main Flask application
├── parse.py              # Book processing and AI functions
├── apiKeys.py            # API key configuration (not in version control)
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/           # HTML templates
│   ├── landing.html     # Landing page
│   └── chatbot.html     # Chat interface
└── static/              # Static assets
    ├── css/
    │   ├── landing.css  # Landing page styles
    │   └── chatbot.css  # Chat interface styles
    └── js/
        ├── landing.js   # Landing page interactions
        └── chatbot.js   # Chat functionality
```

## 🎨 Design Features

### Persona 5 Inspiration
- **Geometric Shapes**: Floating background elements with smooth animations
- **Purple Color Palette**: Modern gradients with dark backgrounds
- **Typography**: Orbitron for headings, Rajdhani for body text
- **Dynamic Elements**: Hover effects, 3D transforms, and particle systems

### Interactive Elements
- **Floating Cards**: 3D hover effects with perspective transforms
- **Animated Buttons**: Pulse effects and gradient transitions
- **Chat Bubbles**: Distinct user and book assistant message styles
- **Loading Animations**: Multi-ring spinners and typing indicators

## 🔒 Privacy & Data Security

### What We Store
- **Temporary Memory**: Book content is processed in RAM only during your session
- **Session Data**: Text chunks and embeddings are stored temporarily in memory
- **No Permanent Storage**: Nothing is saved to disk or databases

### What We Don't Store
- **Book Files**: Your PDF is never saved to our servers
- **Chat History**: Conversations are not logged or stored
- **Personal Data**: We don't collect or store any personal information

### Data Lifecycle
- **Upload**: Book is processed and converted to text chunks
- **Session**: Chunks and embeddings stay in memory while you chat
- **Cleanup**: All data is automatically deleted after 24 hours of inactivity
- **Manual Clear**: You can clear your session anytime using the "New Book" button

### OpenAI Usage
- **Questions Only**: Your questions and relevant book passages are sent to OpenAI
- **No Full Upload**: Your complete book is never uploaded to OpenAI
- **Temporary Processing**: OpenAI processes your request and returns a response

## 🔧 Configuration

### Environment Variables
Create a `.env` file for additional configuration:
```env
FLASK_ENV=development
FLASK_DEBUG=True
OPENAI_API_KEY=your_api_key_here
```

### Customization
- **Colors**: Modify CSS variables in `:root` selectors
- **Animations**: Adjust timing and easing in CSS keyframes
- **Models**: Change embedding model in `app.py`
- **Chunk Size**: Modify `chunkSize` in `parse.py`

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. **Set environment variables**
   ```bash
   export FLASK_ENV=production
   export OPENAI_API_KEY=your_api_key
   ```

2. **Use a production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **For Docker deployment**
   ```bash
   docker build -t storytell .
   docker run -p 5000:5000 storytell
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Persona 5**: Inspiration for the UI design aesthetic
- **OpenAI**: For providing the GPT-3.5 API
- **Sentence Transformers**: For semantic search capabilities
- **Flask**: For the web framework foundation

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section below
- Review the error logs in the browser console

## 🔧 Troubleshooting

### Common Issues

1. **Book Upload Fails**
   - Ensure file is a valid PDF
   - Check file size (recommended < 50MB)
   - Verify internet connection

2. **Chat Not Working**
   - Verify OpenAI API key is valid
   - Check browser console for errors
   - Ensure all dependencies are installed

3. **Slow Performance**
   - Large books may take longer to process
   - Consider splitting very large books
   - Check server resources

4. **Styling Issues**
   - Clear browser cache
   - Ensure all CSS files are loading
   - Check for JavaScript errors

### Performance Tips

- **Book Size**: Keep books under 50MB for optimal performance
- **Chunk Size**: Adjust `chunkSize` in `parse.py` for different book types
- **Session Management**: Sessions are automatically cleaned up after 24 hours
- **Memory Usage**: Large books will use more RAM during processing

## 🎯 Use Cases

### Perfect For
- **Series Readers**: Avoid spoilers while reading multi-book series
- **Complex Plots**: Get help understanding intricate storylines
- **Character Analysis**: Deep dive into character motivations and development
- **Theme Exploration**: Discover underlying themes and symbolism
- **Book Clubs**: Discuss books without revealing plot twists

### Example Scenarios
- Reading "Game of Thrones" and want to understand character relationships without spoilers
- Analyzing "The Great Gatsby" themes without reading ahead
- Discussing "Harry Potter" plot points without revealing future events
- Understanding complex fantasy world-building in current book only

---

**Made with ❤️ for book lovers everywhere**
