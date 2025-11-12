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

# User Agent
USER_AGENT = "Mozilla/5.0 (compatible; AIWebsiteGrader/1.0)"

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
}
