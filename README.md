# 📝 Meeting Notes Summarizer

A user-friendly web application for summarizing meeting notes using AI-powered analysis. Built with Streamlit, this application provides robust input handling, token tracking, cost estimation, and batch processing capabilities.

## ✨ Features

- **Single Summary Mode**: Paste meeting notes and get instant AI-powered summaries
- **Batch Processing**: Process multiple meeting notes at once with progress tracking
- **Robust Input Handling**: Never crashes - comprehensive error handling for all edge cases
- **Token & Cost Tracking**: Real-time monitoring of API usage with detailed statistics
- **Cost Estimation**: Monthly cost projections based on usage patterns
- **History View**: Track all your summaries in one place
- **Download Support**: Export summaries as text files or batch results as JSON
- **User-Friendly Interface**: Clean, modern UI designed for non-technical users

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (get one at https://platform.openai.com/api-keys)

### Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or enter it directly in the app sidebar.

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 💰 Cost Analysis

### API Pricing (GPT-3.5-turbo)

- **Input**: $0.0005 per 1,000 tokens
- **Output**: $0.0015 per 1,000 tokens

### Cost Estimates

#### Single Meeting Summary
- **Average meeting notes**: 2,000 tokens (~1,500 words)
- **Average summary**: 300 tokens
- **Cost per summary**: ~$0.0014

#### Monthly Usage Scenarios

| Daily Summaries | Monthly Cost | Annual Cost |
|----------------|-------------|-------------|
| 10 summaries | $0.42 | $5.04 |
| 50 summaries | $2.10 | $25.20 |
| 100 summaries | $4.20 | $50.40 |
| 500 summaries | $21.00 | $252.00 |

#### Batch Processing
- Processing 100 meetings in batch: ~$0.14
- Processing 1,000 meetings in batch: ~$1.40

### Token Tracking

The application automatically tracks:
- Input tokens per request
- Output tokens per request
- Total session tokens
- Running cost total
- Historical usage (last 100 requests)

All usage data is saved to `token_usage.json` for analysis.

## 📖 Usage Guide

### Single Summary Mode

1. Navigate to the "Single Summary" tab
2. Paste your meeting notes in the text area
3. Select summary length (short/medium/long)
4. Click "Generate Summary"
5. View the summary and download if needed

### Batch Processing Mode

1. Navigate to the "Batch Processing" tab
2. Either upload a text file or paste multiple meeting notes
3. Separate each meeting note with `---` on its own line
4. Select summary length
5. Click "Process Batch"
6. Monitor progress and view individual results
7. Download all results as JSON

### History View

- View all previously generated summaries
- See timestamps, previews, and costs
- Track your usage over time

## 🔧 Configuration

### API Key Setup

You can provide your OpenAI API key in two ways:

1. **Environment Variable** (Recommended):
```bash
export OPENAI_API_KEY="your-api-key-here"
```

2. **In-App Input**:
- Enter your API key in the sidebar
- Key is stored only for the current session

### Summary Length Options

- **Short**: ~3 sentences, key points only
- **Medium**: ~5 sentences, balanced detail
- **Long**: ~8 sentences, comprehensive summary

## 🌐 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Click "New app"
4. Connect your GitHub repository
5. Configure:
   - **Repository**: Your repo name
   - **Branch**: main
   - **Main file**: app.py
6. Add your OpenAI API key in the app secrets
7. Click "Deploy"

### Hugging Face Spaces

1. Create a new Space at [Hugging Face Spaces](https://huggingface.co/spaces)
2. Choose "Streamlit" as the SDK
3. Upload your files
4. Add `OPENAI_API_KEY` as a secret in the Space settings
5. The app will automatically deploy

## 🛡️ Error Handling

The application includes comprehensive error handling:

- **Empty input**: Validates that text is not empty
- **Minimum length**: Requires at least 50 characters
- **Maximum length**: Limits input to 100,000 characters
- **API errors**: Gracefully handles API failures
- **Network issues**: Provides clear error messages
- **Invalid inputs**: Validates all user inputs before processing

The application will never crash due to user input - all errors are caught and displayed clearly.

## 📁 Project Structure

```
meeting-notes-summarizer/
├── app.py                 # Streamlit web application
├── summarizer.py          # Core summarization logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── token_usage.json      # Token usage log (auto-generated)
```

## 🔒 Security

- API keys are never stored permanently
- Session-only storage for API keys
- No data is sent to third parties except OpenAI API
- All processing happens server-side

## 🤝 Contributing

This is a demonstration project. For production use, consider:

- Adding user authentication
- Implementing database storage for summaries
- Adding more summary customization options
- Supporting multiple AI models
- Adding export to multiple formats (PDF, DOCX)

## 📝 License

This project is provided as-is for educational and demonstration purposes.

## 🆘 Troubleshooting

**Issue**: "API key not found"
- **Solution**: Set OPENAI_API_KEY environment variable or enter in sidebar

**Issue**: "Input text too short"
- **Solution**: Provide at least 50 characters of meeting notes

**Issue**: High costs
- **Solution**: Monitor usage in sidebar, use shorter summaries, batch process efficiently

**Issue**: Deployment fails
- **Solution**: Ensure all dependencies are in requirements.txt, check API key is set as secret

## 📞 Support

For issues or questions, please check the error messages displayed in the application - they provide detailed guidance for resolving common problems.

---

**Built with ❤️ using Streamlit and OpenAI GPT-3.5-turbo**
