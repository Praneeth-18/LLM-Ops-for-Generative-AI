# LLM-Ops-for-Generative-AI

[YouTube Demo](https://youtu.be/pvVsIh6wS8I)

--- 

# Smart Document Analyzer - LLMOps GenAI Application

## Overview
Smart Document Analyzer is an end-to-end AI application that leverages OpenAI's GPT-3.5 model to analyze documents and provide natural language interaction capabilities. The application demonstrates key LLMOps principles including configuration management, error handling, logging, and scalable architecture.

## Features
- Document upload and analysis
- Natural language querying of document contents
- Real-time processing feedback
- Vector-based document storage for efficient retrieval
- Comprehensive error handling and logging
- Clean, intuitive web interface

## Technology Stack
- Backend:
  - FastAPI (Python web framework)
  - LangChain (AI orchestration)
  - FAISS (Vector store)
  - OpenAI GPT-3.5
  - PyYAML (Configuration management)

- Frontend:
  - React
  - TailwindCSS
  - esbuild (Frontend bundling)

## Prerequisites
- Python 3.8+
- Node.js 14+
- OpenAI API key
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart-document-analyzer.git
cd smart-document-analyzer
```

2. Create and activate Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Node.js dependencies:
```bash
npm install
```

5. Configure the application:
   - Copy `config/config.yaml.example` to `config/config.yaml`
   - Add your OpenAI API key to `config.yaml`

6. Build the frontend:
```bash
npm run build
```

## Project Structure
```
smart-document-analyzer/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── static/
│       └── js/
│           ├── app.jsx
│           └── app.js
├── config/
│   └── config.yaml
├── package.json
├── requirements.txt
└── README.md
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

2. Access the application:
   - Open http://localhost:8000 in your web browser
   - Use the Swagger documentation at http://localhost:8000/docs

## Usage Guide

1. Document Upload:
   - Click the upload area or drag and drop a document
   - Supported formats: .txt, .doc, .docx, .pdf
   - Maximum file size: 10MB

2. Document Analysis:
   - After upload, the system provides an initial analysis
   - Review the key points and topics identified

3. Asking Questions:
   - Type your question in the query box
   - Click "Ask" or press Enter
   - View the AI-generated response

## Configuration

The `config.yaml` file contains important settings:
```yaml
openai_api_key: "your-api-key-here"
model_settings:
  temperature: 0.3
  max_tokens: 500
vector_store:
  chunk_size: 1000
  chunk_overlap: 200
logging:
  level: DEBUG
  file: app.log
```

## Error Handling and Logging

- All errors are logged to `app.log`
- User-friendly error messages are displayed in the UI
- Comprehensive error tracking for debugging

## Development Notes

1. Frontend Development:
   - Edit files in `app/static/js/`
   - Run `npm run build` after changes

2. Backend Development:
   - Modify `app/main.py` for API changes
   - Server auto-reloads with code changes

## Testing
```bash
# Run Python tests
pytest

# Run frontend tests
npm test
```

## Deployment

1. Production Configuration:
   - Update `config.yaml` with production settings
   - Set appropriate logging levels
   - Configure security settings

2. Build for Production:
```bash
npm run build:prod
```

3. Start Production Server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Security Considerations

- API keys are managed through configuration files
- Input validation on all user inputs
- Secure error handling prevents information leakage
- Rate limiting on API endpoints

