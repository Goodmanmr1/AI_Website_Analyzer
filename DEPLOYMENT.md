# 🚀 Deployment Guide

## Streamlit Cloud Deployment (Recommended)

Streamlit Cloud is the easiest way to deploy this app. It's free for public repositories.

### Prerequisites

- GitHub account
- This repository forked or uploaded to your GitHub

### Step-by-Step Deployment

#### 1. Prepare Your Repository

Make sure your repository has these files:
- ✅ `app.py` (main application)
- ✅ `requirements.txt` (dependencies)
- ✅ `.streamlit/config.toml` (configuration)
- ✅ All folders: `utils/`, `analyzers/`

#### 2. Sign Up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Authorize Streamlit to access your repositories

#### 3. Deploy Your App

1. Click **"New app"** button
2. Fill in the deployment form:
   - **Repository**: Select `yourusername/ai-website-grader`
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `app.py`
3. Click **"Deploy!"**

#### 4. Wait for Deployment

- Initial deployment takes 2-5 minutes
- Streamlit Cloud will:
  - Clone your repository
  - Install dependencies from `requirements.txt`
  - Start the app
  - Provide you with a public URL

#### 5. Access Your App

Your app will be available at:
```
https://[your-app-name]-[random-string].streamlit.app
```

You can customize the URL in the app settings.

### Configuration

#### Custom Domain (Optional)

Streamlit Cloud supports custom domains on paid plans:
1. Go to app settings
2. Click "Domains"
3. Add your custom domain
4. Update DNS records as instructed

#### Secrets Management

If you want to add API keys:

1. Go to your app dashboard
2. Click on your app
3. Click "Settings" → "Secrets"
4. Add secrets in TOML format:

```toml
# .streamlit/secrets.toml format
GOOGLE_PAGESPEED_API_KEY = "your-api-key-here"
```

5. Access in code:
```python
import streamlit as st
api_key = st.secrets["GOOGLE_PAGESPEED_API_KEY"]
```

## Alternative Deployment Options

### Option 1: Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Create setup.sh
cat > setup.sh << 'EOF'
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
EOF

# Deploy
heroku create your-app-name
git push heroku main
```

### Option 2: Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Build and run
docker build -t ai-website-grader .
docker run -p 8501:8501 ai-website-grader
```

### Option 3: AWS EC2

```bash
# On EC2 instance
sudo apt update
sudo apt install python3-pip
git clone https://github.com/yourusername/ai-website-grader.git
cd ai-website-grader
pip3 install -r requirements.txt

# Run with nohup
nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
```

### Option 4: Google Cloud Run

```bash
# Create Dockerfile (see Docker option above)

# Deploy to Cloud Run
gcloud run deploy ai-website-grader \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError"

**Problem**: Missing dependencies

**Solution**: 
- Check `requirements.txt` includes all packages
- Redeploy the app

#### 2. "App is taking too long to load"

**Problem**: Cold start or heavy processing

**Solution**:
- Add `@st.cache_data` decorators to expensive functions
- Optimize imports
- Use Streamlit Cloud's always-on feature (paid)

#### 3. "External API calls failing"

**Problem**: Network restrictions or rate limits

**Solution**:
- Add retry logic
- Implement caching
- Use API keys if available

#### 4. "Memory limit exceeded"

**Problem**: Processing large websites

**Solution**:
- Add content size limits
- Implement pagination
- Upgrade to larger instance (paid plans)

### Performance Optimization

1. **Enable Caching**
```python
@st.cache_data(ttl=3600)
def fetch_website(url):
    # Your code here
```

2. **Lazy Loading**
```python
# Load analyzers only when needed
if st.button("Analyze"):
    from analyzers.ai_optimization import AIOptimizationAnalyzer
```

3. **Async Processing**
```python
import asyncio
# Use async for API calls
```

## Monitoring

### Streamlit Cloud

- View logs in the app dashboard
- Check resource usage
- Monitor uptime

### Custom Monitoring

Add analytics:
```python
# Google Analytics
st.components.v1.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
""")
```

## Updating Your App

### Automatic Updates (Streamlit Cloud)

Streamlit Cloud automatically redeploys when you push to GitHub:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

### Manual Reboot

In Streamlit Cloud dashboard:
1. Click on your app
2. Click "Reboot app"

## Security Best Practices

1. **Never commit secrets** to GitHub
2. **Use environment variables** for sensitive data
3. **Implement rate limiting** to prevent abuse
4. **Validate user input** before processing
5. **Keep dependencies updated**

## Support

- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [GitHub Issues](https://github.com/yourusername/ai-website-grader/issues)

---

**Ready to deploy? Start with Streamlit Cloud - it's the easiest option!**
