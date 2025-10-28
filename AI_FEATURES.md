# 🤖 AI Features Documentation

## Overview

The Study Organizer now includes advanced AI-powered features to enhance your learning experience. These features leverage cutting-edge technologies including OpenAI GPT-3.5, Tesseract OCR, NLTK, and scikit-learn to provide intelligent document analysis, summarization, tagging, search, and recommendations.

## Features

### 1. 📄 Document Summarization

**Technology**: OpenAI GPT-3.5 Turbo

**Description**: Automatically generate concise summaries of your documents using advanced AI.

**How it works**:

- Extracts text from PDFs, Word documents, and images
- Sends the text to OpenAI's GPT-3.5 model
- Generates a 500-character summary highlighting key points
- Stores the summary for quick access

**Usage**:

```python
# Via API
POST /document/<doc_id>/analyze

# Get summary
GET /document/<doc_id>/summary
```

**Benefits**:

- Quick overview without reading entire document
- Save time on document review
- Identify relevant documents faster

---

### 2. 🏷️ Smart Tagging

**Technology**: NLTK + OpenAI GPT-3.5

**Description**: Automatically extract relevant keywords and tags from document content.

**How it works**:

1. **NLP Analysis**: Uses NLTK to tokenize text and extract frequent meaningful words
2. **AI Enhancement**: OpenAI analyzes content and suggests context-aware tags
3. **Subject Context**: Takes into account the document's subject for better accuracy
4. **Deduplication**: Removes duplicate tags and limits to top 5

**Usage**:

```python
# Get AI tags
GET /document/<doc_id>/smart-tags

# Tags are automatically generated during analysis
POST /document/<doc_id>/analyze
```

**Example Tags**:

- For a Math document: "calculus", "derivatives", "integration", "limits", "functions"
- For a History document: "world war", "treaty", "imperialism", "nationalism", "alliance"

---

### 3. 👁️ OCR Text Extraction

**Technology**: Tesseract OCR + PyPDF2

**Description**: Extract text from images, scanned PDFs, and Word documents.

**Supported Formats**:

- PDF documents (native and scanned)
- Images (JPG, PNG, etc.)
- Word documents (DOCX)

**How it works**:

- **PDFs**: Uses PyPDF2 to extract native text
- **Images**: Uses Tesseract OCR for optical character recognition
- **Word Docs**: Uses python-docx to extract text
- Stores extracted text in database for search

**Configuration**:

```env
# Tesseract path (Windows)
TESSERACT_CMD=C:\\Program Files\\Tesseract-OCR\\tesseract.exe

# OCR language
OCR_LANGUAGE=eng
```

**Installation**:

1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to `C:\Program Files\Tesseract-OCR\`
3. Update `.env` with correct path if different

---

### 4. 🔍 Intelligent Content Search

**Technology**: SQLAlchemy Full-Text Search

**Description**: Search across all document content including:

- Document titles
- Subjects and tags
- AI-generated summaries
- Extracted text content

**Usage**:

```python
# Via web interface
GET /search?q=query

# Via API
GET /api/search?q=query
```

**Search Fields**:

- `original_filename`: Document names
- `subject`: Subject/course names
- `tags`: Manual tags
- `ai_tags`: AI-generated tags
- `summary`: AI summaries
- `extracted_text`: Full document text

**Features**:

- Case-insensitive search
- Partial matching
- Results limited to user's documents
- Configurable result limit (default: 50)

---

### 5. 💡 Study Recommendations

**Technology**: scikit-learn (TF-IDF + Cosine Similarity)

**Description**: Get personalized document recommendations based on content similarity.

**How it works**:

1. **TF-IDF Vectorization**: Converts document text to numerical vectors
2. **Similarity Calculation**: Computes cosine similarity between documents
3. **Ranking**: Returns top 5 most similar documents
4. **Filtering**: Only shows documents with >10% similarity

**Usage**:

```python
# Get recommendations for a document
GET /document/<doc_id>/recommendations
```

**Use Cases**:

- Find related study materials
- Discover documents on similar topics
- Group related content together
- Study preparation

**Example**:
If you're viewing a "Calculus 101" document, you might get recommendations for:

- "Advanced Calculus Notes"
- "Derivative Examples"
- "Integration Practice"

---

## Configuration

### Environment Variables

Add to `.env` file:

```env
# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-api-key-here

# Tesseract OCR Configuration (Windows)
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
TESSERACT_CMD=C:\\Program Files\\Tesseract-OCR\\tesseract.exe

# AI Features Configuration
AI_SUMMARY_MAX_LENGTH=500
AI_TAGS_COUNT=5
OCR_LANGUAGE=eng
SEARCH_RESULTS_LIMIT=50
RECOMMENDATIONS_COUNT=5
```

### Database Schema

New fields added to `Document` model:

```python
class Document(db.Model):
    # ... existing fields ...

    # AI-powered features
    summary = db.Column(db.Text, nullable=True)
    extracted_text = db.Column(db.Text, nullable=True)
    ai_tags = db.Column(db.String(512), nullable=True)
    content_vector = db.Column(db.Text, nullable=True)
    last_analyzed = db.Column(db.DateTime, nullable=True)
```

### Dependencies

Install via pip:

```bash
pip install openai>=1.0.0
pip install PyPDF2>=3.0.0
pip install pytesseract>=0.3.10
pip install python-docx>=0.8.11
pip install scikit-learn>=1.3.0
pip install nltk>=3.8.1
```

Download NLTK data:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')
```

---

## API Endpoints

### Document Analysis

**Trigger AI Analysis**

```http
POST /document/<doc_id>/analyze
```

Response:

```json
{
  "success": true,
  "summary": "Summary text...",
  "ai_tags": "tag1, tag2, tag3",
  "extracted_text_length": 5000
}
```

### Get Summary

```http
GET /document/<doc_id>/summary
```

Response:

```json
{
  "success": true,
  "summary": "This document covers..."
}
```

### Get Smart Tags

```http
GET /document/<doc_id>/smart-tags
```

Response:

```json
{
  "success": true,
  "tags": ["calculus", "derivatives", "limits"]
}
```

### Get Extracted Text

```http
GET /document/<doc_id>/extracted-text
```

Response:

```json
{
  "success": true,
  "text": "Full extracted text...",
  "length": 10000
}
```

### Search Documents

```http
GET /api/search?q=query
```

Response:

```json
{
  "success": true,
  "results": [
    {
      "id": 1,
      "original_filename": "Calculus Notes.pdf",
      "year": 2,
      "subject": "Mathematics",
      "summary": "Covers derivatives...",
      "upload_date": "2024-01-15"
    }
  ],
  "count": 1
}
```

### Get Recommendations

```http
GET /document/<doc_id>/recommendations
```

Response:

```json
{
  "success": true,
  "recommendations": [
    {
      "id": 2,
      "original_filename": "Advanced Calc.pdf",
      "year": 3,
      "subject": "Mathematics",
      "summary": "Advanced topics...",
      "thumbnail_url": "/thumbnails/..."
    }
  ]
}
```

---

## User Interface

### AI Features Page

Access via: **Collaborate → AI Features 🤖**

Features:

- Statistics dashboard
- Feature overview
- How it works timeline
- Quick access to all AI features

### Search Interface

Access via: **Search bar** or **/search**

Features:

- Full-text search across all documents
- Result highlighting
- Document cards with summaries
- Quick view links

### Document View Enhancements

On document detail pages:

- View AI-generated summary
- See smart tags
- Get recommendations
- Analyze button for documents without AI data

---

## Performance Considerations

### API Costs

**OpenAI API Pricing** (as of 2024):

- GPT-3.5 Turbo: ~$0.002 per 1K tokens
- Average document analysis: $0.01 - $0.05

**Recommendations**:

- Use free tier credits for development
- Analyze documents on-demand vs. automatic
- Cache summaries and tags
- Limit input text to 12,000 characters

### Processing Time

- **Summary Generation**: 2-5 seconds per document
- **Smart Tagging**: 1-3 seconds
- **OCR**: 3-10 seconds per page
- **Recommendations**: <1 second (after analysis)
- **Search**: <1 second

### Optimization Tips

1. **Batch Processing**: Analyze multiple documents in background
2. **Caching**: Store results in database
3. **Rate Limiting**: Respect OpenAI API limits
4. **Text Truncation**: Limit input to avoid token limits
5. **Async Processing**: Use Celery or background tasks

---

## Troubleshooting

### OpenAI API Issues

**Problem**: "AI features not configured"
**Solution**:

1. Get API key from https://platform.openai.com/api-keys
2. Add to `.env`: `OPENAI_API_KEY=sk-...`
3. Restart Flask app

**Problem**: "Rate limit exceeded"
**Solution**:

- Wait and retry
- Upgrade OpenAI plan
- Implement request queuing

### Tesseract OCR Issues

**Problem**: "Tesseract OCR not found"
**Solution**:

1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to `C:\Program Files\Tesseract-OCR\`
3. Update `TESSERACT_CMD` in `.env`

**Problem**: Poor OCR accuracy
**Solution**:

- Ensure high-quality scans
- Use correct language setting
- Preprocess images (contrast, brightness)

### Search Issues

**Problem**: No results found
**Solution**:

- Check if documents are analyzed
- Run analysis: `POST /document/<id>/analyze`
- Verify text extraction worked

---

## Future Enhancements

### Planned Features

1. **🎯 Question Answering**: Ask questions about document content
2. **🗣️ Text-to-Speech**: Listen to summaries
3. **🌐 Multi-language Support**: OCR and summaries in multiple languages
4. **📊 Analytics Dashboard**: Track AI usage and insights
5. **🔄 Auto-Analysis**: Automatic processing on upload
6. **💬 AI Chat**: Interactive document Q&A
7. **📝 Note Generation**: AI-generated study notes
8. **🎓 Quiz Creation**: Generate practice questions

### Integration Ideas

- Google Drive integration
- Notion sync
- Anki flashcard export
- Calendar integration for study scheduling

---

## Best Practices

### For Students

1. **Analyze Important Documents First**: Focus on key study materials
2. **Use Tags for Organization**: Leverage AI tags to organize content
3. **Explore Recommendations**: Discover related materials
4. **Search Before Uploading**: Check if similar content exists
5. **Review AI Summaries**: Verify accuracy for critical documents

### For Developers

1. **Handle API Errors Gracefully**: Implement retry logic
2. **Cache Aggressively**: Store AI results
3. **Monitor Costs**: Track OpenAI usage
4. **Test with Various Formats**: PDF, images, Word docs
5. **Implement Background Jobs**: For long-running tasks

---

## Security & Privacy

### Data Protection

- AI analysis runs server-side
- Document content sent to OpenAI API
- Results stored in your database
- No sharing with third parties (except OpenAI API)

### Recommendations

1. **Use Environment Variables**: Never commit API keys
2. **Limit API Access**: Restrict to authenticated users
3. **Rate Limiting**: Prevent abuse
4. **Data Encryption**: Use HTTPS in production
5. **Regular Backups**: Backup database regularly

---

## Support & Resources

### Documentation

- OpenAI API: https://platform.openai.com/docs
- Tesseract OCR: https://github.com/tesseract-ocr/tesseract
- NLTK: https://www.nltk.org/
- scikit-learn: https://scikit-learn.org/

### Getting Help

- Check error logs in Flask console
- Review API responses for error details
- Test with simple documents first
- Contact maintainer for issues

---

## Statistics

### Current Implementation

- **Libraries**: 6 AI/ML packages
- **Features**: 5 major AI features
- **API Endpoints**: 8 new routes
- **Database Fields**: 5 new AI fields
- **Lines of Code**: ~250 AI helper functions

### Capabilities

- PDF text extraction
- Image OCR (multi-language)
- Word document processing
- AI summarization (GPT-3.5)
- Smart tagging (NLP + AI)
- Full-text search
- Content recommendations (ML)

---

**Last Updated**: January 2024
**Version**: 1.0
**Author**: Study Organizer Team

---

## Quick Start

1. **Set up OpenAI API**:

   ```bash
   export OPENAI_API_KEY=sk-your-key
   ```

2. **Install Tesseract** (Windows):

   - Download from https://github.com/UB-Mannheim/tesseract/wiki
   - Install to default location

3. **Run the app**:

   ```bash
   python app.py
   ```

4. **Upload a document** and click **"Analyze"**

5. **View results**:
   - See summary in document view
   - Check smart tags
   - Get recommendations
   - Search across content

🎉 **You're all set to use AI-powered features!**
