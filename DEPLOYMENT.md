# 🚀 Deployment Guide

## Streamlit Cloud Deployment

### Step 1: Prepare Your Repository

1. Push your code to GitHub
2. Ensure all files are committed:
   - `app.py`
   - `summarizer.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
   - `README.md`

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub account
4. Select your repository
5. Configure deployment:
   - **Repository**: `your-username/meeting-notes-summarizer`
   - **Branch**: `main`
   - **Main file**: `app.py`
6. Click "Deploy"

### Step 3: Add API Key Secret

1. Go to your app settings on Streamlit Cloud
2. Navigate to "Secrets"
3. Add a new secret:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your actual OpenAI API key
4. Save and redeploy

### Step 4: Verify Deployment

- Your app will be available at: `https://your-app-name.streamlit.app`
- Test the single summary mode
- Test batch processing
- Verify token tracking is working

## Hugging Face Spaces Deployment

### Step 1: Create a Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose:
   - **SDK**: Streamlit
   - **Space name**: `meeting-notes-summarizer`
   - **Visibility**: Public or Private

### Step 2: Upload Files

1. Clone your Space:
```bash
git clone https://huggingface.co/spaces/your-username/meeting-notes-summarizer
```

2. Copy all project files to the Space directory

3. Commit and push:
```bash
git add .
git commit -m "Initial deployment"
git push
```

### Step 3: Add Secrets

1. Go to your Space settings
2. Navigate to "Repository Secrets"
3. Add:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key

### Step 4: Deploy

- The Space will automatically build and deploy
- Your app will be available at: `https://huggingface.co/spaces/your-username/meeting-notes-summarizer`

## Environment Variables

For local development, set your API key:

### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

### Windows (Command Prompt)
```cmd
set OPENAI_API_KEY=your-api-key-here
```

### Linux/Mac
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Troubleshooting Deployment

### Streamlit Cloud Issues

**Issue**: Build fails
- **Solution**: Check that `requirements.txt` has correct versions
- **Solution**: Ensure all dependencies are compatible

**Issue**: API key errors
- **Solution**: Verify secret is set correctly in app settings
- **Solution**: Redeploy after adding secrets

**Issue**: App not loading
- **Solution**: Check logs in Streamlit Cloud dashboard
- **Solution**: Verify `app.py` is the main file

### Hugging Face Spaces Issues

**Issue**: Build timeout
- **Solution**: Optimize dependencies in requirements.txt
- **Solution**: Use specific version numbers

**Issue**: Runtime errors
- **Solution**: Check Space logs for detailed error messages
- **Solution**: Verify all files are uploaded correctly

## Performance Optimization

For production deployment:

1. **Caching**: Enable Streamlit caching for repeated operations
2. **Rate Limiting**: Implement rate limiting for API calls
3. **Database**: Add database for persistent summary storage
4. **Monitoring**: Set up error tracking (e.g., Sentry)
5. **CDN**: Use CDN for static assets if needed

## Security Best Practices

1. Never commit API keys to repository
2. Use environment variables or secrets management
3. Implement rate limiting
4. Add user authentication for production
5. Regularly update dependencies
6. Monitor usage for unusual patterns

## Custom Domain (Optional)

### Streamlit Cloud

1. Go to app settings
2. Navigate to "Domains"
3. Add your custom domain
4. Update DNS records as instructed

### Hugging Face Spaces

1. Go to Space settings
2. Navigate to "Domains"
3. Configure custom domain
4. Update DNS settings

## Monitoring and Analytics

### Streamlit Cloud

- Built-in usage metrics
- Error logs in dashboard
- Resource utilization tracking

### Hugging Face Spaces

- Space analytics dashboard
- Community engagement metrics
- Download statistics

## Backup and Recovery

### Regular Backups

- Export token usage logs regularly
- Backup important summaries
- Keep copy of requirements.txt

### Disaster Recovery

- Maintain GitHub repository with all code
- Document deployment process
- Keep API keys secure and backed up
