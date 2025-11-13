"""Configuration settings for AI Website Grader"""

import os

# Try to import streamlit for secrets support
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

# ============================================================================
# API Configuration
# ============================================================================

# Google PageSpeed Insights API (Optional - 25k requests/day without key)
# Tries Streamlit secrets first, then falls back to environment variable
if HAS_STREAMLIT:
    try:
        PAGESPEED_API_KEY = st.secrets.get("GOOGLE_PAGESPEED_API_KEY", None)
    except:
        PAGESPEED_API_KEY = os.getenv('GOOGLE_PAGESPEED_API_KEY', None)
else:
    PAGESPEED_API_KEY = os.getenv('GOOGLE_PAGESPEED_API_KEY', None)
PAGESPEED_API_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

# Firecrawl API Configuration (Enhanced scraping for JS-heavy sites)
# Tries Streamlit secrets first, then falls back to environment variable
if HAS_STREAMLIT:
    try:
        FIRECRAWL_API_KEY = st.secrets.get("FIRECRAWL_API_KEY", None)
    except:
        FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY', None)
else:
    FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY', None)

# Firecrawl settings
USE_FIRECRAWL_DEFAULT = False  # Default to regular fetcher unless specified
FIRECRAWL_WAIT_TIME = 3000  # Milliseconds to wait for JS rendering
FIRECRAWL_TIMEOUT = 60  # Seconds timeout for Firecrawl operations

# W3C HTML Validator (Public endpoint - no key needed)
W3C_VALIDATOR_URL = "https://validator.w3.org/nu/"

# ============================================================================
# Scoring Weights (must sum to 1.0)
# ============================================================================

CATEGORY_WEIGHTS = {
    'ai_optimization': 0.25,
    'mobile_optimization': 0.20,
    'technical_crawlability': 0.16,
    'schema_analysis': 0.12,
    'technical_seo': 0.10,
    'content_quality': 0.10,
    'eeat_signals': 0.07
}

# ============================================================================
# Score Thresholds
# ============================================================================

EXCELLENT_THRESHOLD = 90
GOOD_THRESHOLD = 80
NEEDS_IMPROVEMENT_THRESHOLD = 70

# ============================================================================
# Content Analysis Parameters
# ============================================================================

MIN_WORD_COUNT = 300
IDEAL_WORD_COUNT = 1500
IDEAL_TITLE_LENGTH = (30, 60)
IDEAL_META_DESC_LENGTH = (150, 160)
MAX_H1_COUNT = 1

# ============================================================================
# Network Configuration
# ============================================================================

# Improved User Agent - More browser-like but still honest
# Includes browser identification + tool identification
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 AIWebsiteGrader/1.0"

# Additional headers to appear more browser-like
DEFAULT_HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0',
}

# Request timeout in seconds
REQUEST_TIMEOUT = 30

# Retry configuration for external API calls
MAX_RETRIES = 2
RETRY_DELAY = 1  # seconds

# ============================================================================
# UI Configuration
# ============================================================================

# Color scheme
COLORS = {
    'primary': '#3d4f5d',
    'accent': '#ff8c42',
    'success': '#4caf50',
    'warning': '#ffc107',
    'critical': '#f44336',
    'background': '#f5f5f5'
}

# Status label ranges
STATUS_LABELS = {
    'excellent': (90, 100),
    'good': (80, 89),
    'needs-improvement': (70, 79),
    'critical': (0, 69)
}

# ============================================================================
# Performance & Caching
# ============================================================================

# Enable caching to reduce API calls and improve performance
ENABLE_CACHING = True
CACHE_TTL = 3600  # 1 hour in seconds

# Rate limiting to prevent excessive API usage
RATE_LIMIT_ENABLED = True
MAX_REQUESTS_PER_HOUR = 50

# ============================================================================
# Feature Flags
# ============================================================================

FEATURES = {
    'pagespeed_api': True,      # Enable Google PageSpeed Insights
    'w3c_validator': True,       # Enable W3C HTML Validator
    'export_markdown': True,     # Enable Markdown export
    'export_pdf': False,         # PDF export (future feature)
    'batch_analysis': False,     # Batch URL analysis (future feature)
    'firecrawl': True,          # Enable Firecrawl for JS-heavy sites
}

# ============================================================================
# Error Handling
# ============================================================================

# Graceful degradation: If external APIs fail, continue with available data
GRACEFUL_DEGRADATION = True

# Error messages
ERROR_MESSAGES = {
    'network_error': 'Unable to connect to the website. Please check the URL and try again.',
    'timeout_error': 'Request timed out. The website may be slow or unavailable.',
    'invalid_url': 'Invalid URL provided. Please enter a valid website URL.',
    'rate_limit': 'Rate limit exceeded. Please wait before analyzing another URL.',
    'api_error': 'External API error. Analysis will continue with available data.',
    'firecrawl_api_missing': 'Firecrawl API key not configured. Please add FIRECRAWL_API_KEY to use enhanced scraping.',
    'firecrawl_error': 'Firecrawl enhanced scraping failed. Falling back to standard scraper.',
    'forbidden': '''⚠️ This website is blocking automated analysis (HTTP 403 Forbidden).

**Common Reasons:**
• Web Application Firewall (Cloudflare, Akamai, AWS WAF, etc.)
• Bot protection or rate limiting enabled
• Geographic or IP-based restrictions

**If this is YOUR website:**
• Whitelist this tool's IP address in your WAF settings
• Temporarily disable bot protection for testing
• Contact your hosting provider or IT team
• Try running from your local network

**If analyzing a third-party site:**
• This is a limitation of automated tools
• The site owner has chosen to block bots for security
• Even major SEO tools (Ahrefs, SEMrush) face similar blocking
• Consider reaching out to the site owner directly''',
    'not_found': 'Page not found (404). Please check the URL and try again.',
    'server_error': 'The website returned a server error (5xx). The site may be experiencing issues.',
}
