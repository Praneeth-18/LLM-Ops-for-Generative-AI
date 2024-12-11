import React, { useState } from 'react';
import ReactDOM from 'react-dom';

function DocumentAnalyzer() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileUpload = async (e) => {
    const uploadedFile = e.target.files[0];
    if (!uploadedFile) return;
    
    setFile(uploadedFile);
    setError('');
    setLoading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);
      
      const response = await fetch('/analyze', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Error processing document');
      }
      
      setAnalysis(data);
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.message || 'Error uploading document');
      setAnalysis(null);
    } finally {
      setLoading(false);
    }
  };

  const handleQuery = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`/query?question=${encodeURIComponent(question)}`);
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Error querying document');
      }
      
      setAnswer(data.answer);
    } catch (err) {
      console.error('Query error:', err);
      setError(err.message || 'Error querying document');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8 text-center">Document Analyzer</h1>
      
      {/* File Upload Section */}
      <div className="mb-8">
        <div className="border-2 border-dashed rounded-lg p-6 text-center hover:border-blue-500 transition-colors">
          <input
            type="file"
            onChange={handleFileUpload}
            className="hidden"
            id="file-upload"
            accept=".txt,.doc,.docx,.pdf"
          />
          <label
            htmlFor="file-upload"
            className="flex flex-col items-center cursor-pointer"
          >
            <span className="text-4xl mb-2">📄</span>
            <span className="text-sm text-gray-500">
              {file ? file.name : 'Click to upload or drag and drop'}
            </span>
            <span className="text-xs text-gray-400 mt-1">
              Supports txt, doc, docx, pdf
            </span>
          </label>
        </div>
      </div>

      {/* Analysis Results */}
      {analysis && (
        <div className="mb-8 p-4 bg-gray-50 rounded-lg shadow-sm">
          <h2 className="text-xl font-semibold mb-2">Analysis Results</h2>
          <p className="text-gray-700 whitespace-pre-wrap">{analysis.analysis}</p>
        </div>
      )}

      {/* Query Section */}
      <div className="mb-8">
        <form onSubmit={handleQuery} className="flex gap-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about the document..."
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg disabled:opacity-50 hover:bg-blue-600 transition-colors"
          >
            {loading ? '⏳' : '🔍'} Ask
          </button>
        </form>
      </div>

      {/* Answer Section */}
      {answer && (
        <div className="p-4 bg-gray-50 rounded-lg shadow-sm">
          <h2 className="text-xl font-semibold mb-2">Answer</h2>
          <p className="text-gray-700 whitespace-pre-wrap">{answer}</p>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg">
          ⚠️ {error}
        </div>
      )}

      {/* Loading Indicator */}
      {loading && (
        <div className="fixed top-0 left-0 w-full h-1">
          <div className="h-full bg-blue-500 animate-pulse"></div>
        </div>
      )}
    </div>
  );
}

// Render the app
const root = document.getElementById('root');
ReactDOM.render(<DocumentAnalyzer />, root);