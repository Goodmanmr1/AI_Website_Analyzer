# 🚀 AI Website Grader with Firecrawl Integration

A comprehensive web application that evaluates websites for AI-powered search engine optimization, mobile experience, and technical SEO performance. Now with **Firecrawl integration** for enhanced JavaScript site analysis!

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 🔥 New: Firecrawl Integration

This version includes optional **Firecrawl** integration for superior content extraction from:
- JavaScript-heavy websites
- Single Page Applications (SPAs)
- React, Vue, Angular sites
- Dynamic content that loads after page load
- Sites that standard scrapers struggle with

## 📋 Overview

AI Website Grader analyzes websites across seven weighted categories to assess how effectively they can be understood and utilized by AI-powered search systems, chatbots, and intelligent assistants.

### Key Features

- **🤖 AI Readiness Analysis** - Evaluates content structure for AI comprehension
- **📱 Mobile Experience** - Assesses responsive design and mobile optimization
- **🔍 Search Visibility** - Reviews technical SEO and crawlability
- **📊 Structured Data** - Checks schema markup implementation
- **✅ Performance Metrics** - Integrates with Google PageSpeed Insights
- **🔥 Firecrawl Mode** - Enhanced extraction for JavaScript sites
- **📄 Downloadable Reports** - Export results in Markdown format

## 🎯 Analysis Categories

| Category | Weight | Description |
|----------|--------|-------------|
| **AI Readiness & Optimization** | 25% | Content structure, chunkability, semantic clarity |
| **Mobile Experience** | 20% | Responsive design, viewport configuration |
| **Crawlability & Indexing** | 16% | Bot access, robots.txt, technical accessibility |
| **Structured Data** | 12% | Schema markup, JSON-LD implementation |
| **Technical SEO** | 10% | Meta tags, headings, image optimization |
| **Content Quality** | 10% | Depth, comprehensiveness, readability |
| **Trust Signals** | 7% | Expertise, authority, credibility indicators |

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Streamlit account (for cloud deployment)
- Optional: Firecrawl API key for enhanced scraping

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-website-grader.git
cd ai-website-grader

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional)
export FIRECRAWL_API_KEY="your-firecrawl-api-key"  # Get from firecrawl.dev
export GOOGLE_PAGESPEED_API_KEY="your-pagespeed-key"  # Optional

# Run the app
streamlit run app.py
```

## 🔥 Firecrawl Setup

### Getting a Firecrawl API Key

1. Visit [firecrawl.dev](https://firecrawl.dev)
2. Sign up for a free account (500 credits/month)
3. Copy your API key from the dashboard

### Configuration Options

#### Option 1: Environment Variable
```bash
export FIRECRAWL_API_KEY="fc-your-api-key"
```

#### Option 2: Streamlit Secrets (for cloud deployment)
Add to `.streamlit/secrets.toml`:
```toml
FIRECRAWL_API_KEY = "fc-your-api-key"
```

#### Option 3: User-Provided Key
Users can enter their own API key directly in the app's Advanced Options

### When to Use Firecrawl

Enable Firecrawl mode when analyzing:
- React, Vue, Angular applications
- Sites showing < 200 words in standard mode
- E-commerce sites with dynamic content
- Modern web apps with client-side rendering
- Sites behind Cloudflare (better success rate)

## 📁 Project Structure

```
ai-website-grader/
├── app.py                      # Main Streamlit application with Firecrawl toggle
├── config.py                   # Configuration with Firecrawl settings
├── requirements.txt            # Dependencies including firecrawl-py
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── utils/
│   ├── __init__.py
│   ├── fetcher.py             # Standard website fetcher
│   ├── fetcher_firecrawl.py  # Firecrawl-enhanced fetcher
│   ├── scoring.py             # Score calculation logic
│   └── export.py              # Report generation
├── analyzers/
│   ├── __init__.py
│   ├── ai_optimization.py     # AI readiness analyzer
│   ├── content_quality.py     # Content analysis
│   ├── eeat_signals.py        # Trust signals analyzer
│   ├── mobile_optimization.py # Mobile experience checker
│   ├── performance.py         # Performance metrics
│   ├── schema_analysis.py     # Structured data checker
│   └── technical_seo.py       # Technical SEO analyzer
└── README.md                   # This file
```

## 🔧 Configuration

### API Keys

The app works without API keys but is enhanced with:

- **Firecrawl API**: JavaScript rendering and enhanced extraction
- **Google PageSpeed Insights API**: Performance metrics
- **W3C HTML Validator**: Uses public endpoint (no key needed)

### Firecrawl vs Standard Mode

| Feature | Standard Mode | Firecrawl Mode |
|---------|--------------|----------------|
| JavaScript Rendering | ❌ | ✅ |
| SPA Support | Limited | Full |
| Content Extraction | HTML only | HTML + Markdown |
| Dynamic Content | ❌ | ✅ |
| Clean Markdown | ❌ | ✅ |
| LLM Insights | ❌ | ✅ |
| API Key Required | No | Yes |
| Cost | Free | Free tier available |

## 🎨 Usage Examples

### Basic Analysis (Standard Mode)
1. Enter website URL
2. Click "START ANALYSIS"
3. View results and download report

### Enhanced Analysis (Firecrawl Mode)
1. Enter website URL
2. Expand "Advanced Options"
3. Check "Use Firecrawl"
4. Click "START ANALYSIS"
5. Get enhanced insights including:
   - Better content extraction
   - Questions the content answers
   - Key facts and statistics
   - Expertise indicators

### Batch Analysis (Coming Soon)
Future feature for analyzing multiple URLs

## 📊 Scoring System

Scores are calculated on a 0-100 scale:

- **90-100 (Excellent)**: Highly optimized for AI-powered systems
- **80-89 (Good)**: Strong foundation with minor improvements needed
- **70-79 (Fair)**: Adequate but would benefit from optimization
- **Below 70 (Needs Work)**: Significant optimization opportunities

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add more LLM extraction schemas
- [ ] Implement batch URL processing
- [ ] Add competitor comparison features
- [ ] Create API endpoint version
- [ ] Add more export formats (PDF, JSON)

## 📈 Deployment

### Deploy to Streamlit Cloud

1. Fork this repository
2. Add secrets in Streamlit Cloud dashboard:
   ```toml
   FIRECRAWL_API_KEY = "your-key"
   GOOGLE_PAGESPEED_API_KEY = "your-key"  # optional
   ```
3. Deploy from GitHub repository

### Deploy with Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FIRECRAWL_API_KEY="your-key"
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 🔒 Security

- API keys are never logged or exposed
- Firecrawl requests are server-side only
- User-provided keys are session-specific
- No data is permanently stored

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Enhanced with [Firecrawl](https://firecrawl.dev/)
- Uses [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- Integrates [Google PageSpeed Insights](https://developers.google.com/speed/pagespeed/insights/)

## 📧 Support

- Open an [Issue](https://github.com/yourusername/ai-website-grader/issues)
- Check [Discussions](https://github.com/yourusername/ai-website-grader/discussions)
- Firecrawl docs: [docs.firecrawl.dev](https://docs.firecrawl.dev)

## 🚀 Roadmap

- [x] Firecrawl integration for JS sites
- [ ] Full site crawling mode
- [ ] Competitor analysis features
- [ ] Historical tracking
- [ ] API endpoint version
- [ ] Chrome extension
- [ ] WordPress plugin

---

**Made with ❤️ for the AI-powered web**
