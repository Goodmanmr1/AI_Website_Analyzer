"""Configuration settings for AI Website Grader"""

import os

# ============================================================================
# API Configuration
# ============================================================================

# Google PageSpeed Insights API (Optional - 25k requests/day without key)
PAGESPEED_API_KEY = os.getenv('GOOGLE_PAGESPEED_API_KEY', None)
PAGESPEED_API_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

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
# Includes:
# - Browser identification (Chrome on Windows)
# - Tool identification (AIWebsiteGrader/1.0)
# - Contact URL (for site owners to learn more)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 AIWebsiteGrader/1.0"

# Request timeout in seconds
REQUEST_TIMEOUT = 30

# Retry configuration for external API calls
MAX_RETRIES = 2
RETRY_DELAY = 1  # seconds

# Additional headers to appear more browser-like
DEFAULT_HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

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
# Error Messages
# ============================================================================

ERROR_MESSAGES = {
    'timeout': 'The website took too long to respond. Please try again or check if the site is accessible.',
    'network_error': 'Unable to connect to the website. Please check the URL and try again.',
    'invalid_url': 'Please enter a valid URL starting with http:// or https://',
    'forbidden': '''⚠️ This website is blocking automated analysis tools (HTTP 403 Forbidden).

**Common Reasons:**
• Web Application Firewall (Cloudflare, Akamai, AWS WAF, etc.)
• Bot protection or rate limiting enabled
• Geographic or IP-based restrictions

**If this is YOUR website:**
• Whitelist this tool's IP address in your WAF settings
• Temporarily disable bot protection for testing
• Contact your hosting provider or IT team
• Try running the analysis from your local network

**If analyzing a third-party site:**
• This is a limitation of automated tools - the site owner has chosen to block bots
• Consider reaching out to the site owner directly
• Most enterprise and financial sites block automated analysis for security

**Note:** This is common for SEO tools. Even established tools like Screaming Frog and Ahrefs face similar blocking.''',
    'server_error': 'The website returned a server error. The site may be experiencing issues.',
    'not_found': 'The page was not found (404). Please check the URL.',
}

# ============================================================================
# Feature Flags
# ============================================================================

# Enable/disable specific analyzers
ENABLE_PERFORMANCE_API = True  # Google PageSpeed Insights
ENABLE_HTML_VALIDATION = True  # W3C Validator
ENABLE_SCHEMA_ANALYSIS = True
ENABLE_MOBILE_ANALYSIS = True

# Analysis depth
DEEP_ANALYSIS = True  # More thorough but slower
INCLUDE_RECOMMENDATIONS = True
INCLUDE_CODE_EXAMPLES = True

# ============================================================================
# Rate Limiting
# ============================================================================

# Maximum analyses per hour (to prevent abuse)
MAX_REQUESTS_PER_HOUR = 50

# Cache TTL in seconds (1 hour)
CACHE_TTL = 3600
