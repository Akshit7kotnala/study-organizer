# 🤖 AI Study Assistant Chatbot - Feature Documentation

## Overview
The AI Study Assistant is a powerful chatbot integrated into your Study Organizer that helps you:
- 💬 Chat with your documents using Google Gemini AI
- ❓ Ask questions about uploaded study materials
- 📝 Generate practice quizzes automatically
- 📅 Create personalized study plans

---

## 🚀 Features

### 1. **Document-Aware Conversations**
- Start a chat about any uploaded document
- AI understands the context from your PDFs, DOCX files, and images
- Get instant answers to questions about your study materials
- References document summaries and extracted text

### 2. **Quiz Generation**
- Auto-generate multiple-choice questions from any document
- Choose difficulty level (Easy, Medium, Hard)
- Specify number of questions (1-20)
- Get explanations for correct answers

### 3. **Study Plan Generator**
- AI creates personalized study schedules
- Set your goals and available time
- Get daily task breakdowns
- Includes study tips and recommendations

### 4. **Smart Features**
- Conversation history saved for each session
- Quick action buttons (Summarize, Quiz Me, Explain, Topics)
- Typing indicators for natural chat feel
- Beautiful, responsive UI

---

## 📖 How to Use

### Starting a Chat

1. **Navigate to AI Chat**
   - Click "AI Chat" in the main navigation bar
   - Or go to: http://127.0.0.1:5000/chat

2. **Choose Chat Type**
   - **General Study Chat**: Ask general questions or discuss study strategies
   - **Document Chat**: Select a specific document to chat about
   - **Generate Quiz**: Create practice questions from a document
   - **Study Plan**: Get a personalized study schedule

### Chatting with Documents

```
1. Click "Chat About Document"
2. Select a document from the dropdown
3. Start asking questions like:
   - "What are the main topics in this document?"
   - "Can you explain [specific concept]?"
   - "Create 5 quiz questions about this"
   - "Summarize the key points"
```

### Quick Actions

Use the quick action buttons for common tasks:
- **Summarize**: Get a quick summary of the document
- **Quiz Me**: Generate practice questions
- **Explain**: Ask for simplified explanations
- **Topics**: List main topics covered

### Generating Quizzes

```python
1. Click "Generate Quiz" button
2. Select document
3. Choose:
   - Number of questions (1-20)
   - Difficulty (Easy/Medium/Hard)
4. Click "Generate Quiz"
5. Quiz appears in JSON format (can be displayed in a dedicated quiz page)
```

### Creating Study Plans

```python
1. Click "Create Study Plan" button
2. Enter:
   - Study Goal (e.g., "Prepare for final exams")
   - Duration in days (1-30)
   - Hours per day (1-12)
3. Click "Create Plan"
4. Get a detailed day-by-day schedule
```

---

## 🎯 Use Cases

### For Students
- **Before Exams**: Generate quizzes to test knowledge
- **Study Sessions**: Ask questions while studying
- **Planning**: Create study schedules for upcoming tests
- **Understanding**: Get explanations of difficult concepts

### For Educators
- **Content Review**: Check if study materials cover all topics
- **Quiz Creation**: Generate practice questions quickly
- **Student Help**: Provide 24/7 AI tutor for students

---

## 🔧 Technical Details

### Database Models

**ChatSession**
```python
- id: Primary key
- user_id: Owner of the chat
- document_id: Optional linked document
- title: Chat title
- created_at, updated_at: Timestamps
```

**ChatMessage**
```python
- id: Primary key
- session_id: Parent chat session
- role: 'user' or 'assistant'
- content: Message text
- created_at: Timestamp
```

### API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/chat` | GET | List all chat sessions |
| `/chat/new` | POST | Create new chat session |
| `/chat/<id>` | GET | View chat session |
| `/chat/<id>/message` | POST | Send message and get AI response |
| `/chat/<id>/delete` | POST | Delete chat session |
| `/chat/quiz/generate` | POST | Generate quiz from document |
| `/chat/study-plan/generate` | POST | Create study plan |

### AI Integration

**Powered by Google Gemini AI**
- Model: `gemini-2.0-flash`
- Context window: Up to 3000 characters from document
- Conversation history: Last 10 messages
- Response includes full document context

---

## 💡 Tips & Best Practices

### Getting Better Responses
1. **Be Specific**: "Explain photosynthesis in simple terms" > "Tell me about biology"
2. **Reference Context**: "What does the document say about X?" works better with document chats
3. **Use Quick Actions**: Fast way to get common tasks done
4. **Ask Follow-ups**: AI remembers conversation history

### Quiz Generation Tips
- Start with medium difficulty
- Use documents with clear, factual content
- 5-10 questions per document works best
- Review AI-generated answers for accuracy

### Study Plan Tips
- Set realistic goals (2-3 hours per day)
- Allow at least 3-7 days duration
- Be specific about your goal
- Review plan and adjust as needed

---

## 🎨 UI Features

### Chat Interface
- **Modern Design**: Clean, professional chat bubbles
- **User Messages**: Blue bubbles on the right
- **AI Responses**: White bubbles on the left with border
- **Timestamps**: Each message shows send time
- **Typing Indicator**: Animated dots while AI is thinking

### Document Context Card
- Shows linked document info
- Expandable summary view
- Color-coded by subject

### Responsive Design
- Works on desktop, tablet, and mobile
- Sidebar collapses on small screens
- Touch-friendly interface

---

## 🚀 Future Enhancements

### Planned Features
1. **Voice Input**: Speak your questions
2. **Image Upload**: Send images in chat
3. **Code Highlighting**: For programming documents
4. **Export Chats**: Download conversations as PDF
5. **Shared Chats**: Collaborate with study groups
6. **Quiz Interface**: Dedicated page for taking quizzes
7. **Study Plan Tracker**: Check off completed tasks
8. **Multi-language**: Support for different languages

---

## 🐛 Troubleshooting

### Common Issues

**"AI not configured" error**
- Ensure `GEMINI_API_KEY` is set in `.env` file
- Restart Flask server after adding API key

**Empty responses**
- Check if document has extracted text
- Run "Analyze Document" first if needed

**Quiz not generating properly**
- Ensure document has sufficient content (at least 500 characters)
- Try adjusting difficulty level

**Chat not loading**
- Clear browser cache
- Check browser console for JavaScript errors
- Ensure Flask server is running

---

## 📊 Performance

### Optimization Tips
- **First 3000 characters** of documents used for context (fast responses)
- **Last 10 messages** included in conversation history
- **Async loading** for chat history
- **Auto-scroll** to latest message

### Response Times
- Simple questions: 2-5 seconds
- Quiz generation: 10-20 seconds (5-10 questions)
- Study plan: 15-30 seconds (7-day plan)

---

## 🔐 Security & Privacy

- Chats are private to each user
- No cross-user access to chat sessions
- API keys stored securely in environment variables
- Messages stored in database (can be deleted anytime)

---

## 📝 Examples

### Example Chat Conversation

**User**: "What are the main topics in this CDS syllabus document?"

**AI**: "Based on the CDS 1 2024 exam syllabus, the main topics covered are:
1. English Language - grammar, vocabulary, comprehension
2. General Knowledge - current affairs, history, geography
3. Elementary Mathematics - arithmetic, algebra, geometry
4. Logical Reasoning and Numerical Ability
..."

**User**: "Create 3 quiz questions about the math topics"

**AI**: "Here are 3 multiple-choice questions about the math topics:
1. What is the formula for calculating simple interest?
   A) P × R × T / 100
   B) P × R × T
   C) P + R + T
   D) P / R / T
   Correct: A
..."

---

## 🎓 Educational Value

### Learning Benefits
- **Self-paced learning**: Study at your own speed
- **Instant feedback**: Get answers immediately
- **Active recall**: Quiz generation helps retention
- **Personalization**: Plans tailored to your needs
- **24/7 availability**: Study anytime, anywhere

---

## 📞 Support

For issues or feature requests:
1. Check this documentation
2. Review troubleshooting section
3. Contact: akshitkotnala@gmail.com
4. GitHub: https://github.com/Akshit7kotnala/study-organizer

---

## 🎉 Success Metrics

Track your learning:
- Number of chats created
- Questions asked
- Quizzes generated
- Study plans completed
- Documents analyzed

---

**Built with ❤️ by Akshit Kotnala**
*Powered by Google Gemini AI*
