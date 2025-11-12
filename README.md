# 🚀 AI Website Grader

A comprehensive web application that evaluates websites for AI-powered search engine optimization, mobile experience, and technical SEO performance.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 📋 Overview

AI Website Grader analyzes websites across seven weighted categories to assess how effectively they can be understood and utilized by AI-powered search systems, chatbots, and intelligent assistants.

### Key Features

- **🤖 AI Readiness Analysis** - Evaluates content structure for AI comprehension
- **📱 Mobile Experience** - Assesses responsive design and mobile optimization
- **🔍 Search Visibility** - Reviews technical SEO and crawlability
- **📊 Structured Data** - Checks schema markup implementation
- **✅ Performance Metrics** - Integrates with Google PageSpeed Insights
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

### Deploy to Streamlit Cloud

1. **Fork this repository** to your GitHub account

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Click "New app"**

4. **Select your forked repository**
   - Main file path: `app.py`
   - Python version: 3.9+

5. **Click "Deploy"**

That's it! Your app will be live in a few minutes.

### Run Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-website-grader.git
cd ai-website-grader

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
ai-website-grader/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── utils/
│   ├── __init__.py
│   ├── fetcher.py             # Website fetching utilities
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
├── README.md                   # This file
└── LICENSE                     # MIT License
```

## 🔧 Configuration

### API Keys (Optional)

The app works without API keys, but you can enhance it with:

- **Google PageSpeed Insights API**: Add to Streamlit secrets for performance analysis
- **W3C HTML Validator**: Uses public endpoint (no key needed)

To add API keys in Streamlit Cloud:
1. Go to your app settings
2. Click "Secrets"
3. Add:
```toml
GOOGLE_PAGESPEED_API_KEY = "your-api-key-here"
```

### Customization

Edit `config.py` to customize:
- Category weights
- Scoring thresholds
- Timeout values
- User agent string

## 📊 How It Works

1. **Fetch**: Retrieves HTML content from the provided URL
2. **Parse**: Extracts metadata, content, and structural elements
3. **Analyze**: Runs 35+ individual checks across 7 categories
4. **Score**: Calculates weighted scores based on findings
5. **Report**: Generates detailed recommendations

## 🛠️ Technology Stack

- **Framework**: Streamlit
- **Web Scraping**: BeautifulSoup4, Requests
- **Content Analysis**: textstat
- **APIs**: Google PageSpeed Insights, W3C Validator

## 📈 Scoring System

Scores are calculated on a 0-100 scale:

- **90-100 (Excellent)**: Highly optimized for AI-powered systems
- **80-89 (Good)**: Strong foundation with minor improvements needed
- **70-79 (Fair)**: Adequate but would benefit from optimization
- **Below 70 (Needs Work)**: Significant optimization opportunities

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Inspired by the evolving landscape of AI-powered search
- Uses free and open-source libraries

## 📧 Support

For questions or issues:
- Open an [Issue](https://github.com/yourusername/ai-website-grader/issues)
- Check the [Discussions](https://github.com/yourusername/ai-website-grader/discussions)

## 🔗 Links

- [Live Demo](https://your-app-url.streamlit.app)
- [Documentation](https://github.com/yourusername/ai-website-grader/wiki)
- [Changelog](https://github.com/yourusername/ai-website-grader/releases)

---

**Made with ❤️ for the AI-powered web**
