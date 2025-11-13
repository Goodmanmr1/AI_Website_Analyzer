"""AI Website Grader - Streamlit Application with Firecrawl Integration"""

import streamlit as st
from datetime import datetime
import time
import os
from urllib.parse import urlparse

# Import utilities and analyzers
from utils.fetcher import WebsiteFetcher
from utils.scoring import calculate_category_score, calculate_overall_score, get_status_label, get_status_color
from utils.export import generate_markdown_report, save_markdown_report

from analyzers.ai_optimization import AIOptimizationAnalyzer
from analyzers.eeat_signals import EEATAnalyzer
from analyzers.technical_seo import TechnicalSEOAnalyzer
from analyzers.content_quality import ContentQualityAnalyzer
from analyzers.mobile_optimization import MobileOptimizationAnalyzer
from analyzers.schema_analysis import SchemaAnalyzer, TechnicalCrawlabilityAnalyzer
from analyzers.performance import PerformanceAnalyzer

import config

# URL validation function (replaces validators package)
def is_valid_url(url):
    """Validate URL without external validators package"""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False

# Check if Firecrawl is available
def is_firecrawl_available():
    """Check if Firecrawl API key is configured"""
    return bool(config.FIRECRAWL_API_KEY)

# Page configuration
st.set_page_config(
    page_title="AI Website Grader",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.25rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        color: white;
    }
    .score-number {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    .category-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f3f4f6;
    }
    .firecrawl-badge {
        background: linear-gradient(135deg, #ff6b35, #f77737);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚀 AI Website Grader</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Evaluate your site\'s performance for AI-powered search engines and intelligent assistants</p>', unsafe_allow_html=True)

# Main content
st.markdown("---")

# Input section with enhanced options
st.markdown("### Enter Website URL")
st.markdown("Provide the URL of any publicly accessible website to receive a comprehensive analysis.")

# Create columns for input and options
col1, col2 = st.columns([3, 1])

with col1:
    url_input = st.text_input(
        "Enter website URL",
        placeholder="https://www.yourwebsite.com",
        label_visibility="collapsed"
    )

with col2:
    analyze_button = st.button("START ANALYSIS", type="primary", use_container_width=True)

# Advanced options section
with st.expander("⚙️ Advanced Options", expanded=False):
    col_opt1, col_opt2 = st.columns(2)
    
    with col_opt1:
        # Firecrawl toggle with availability check
        if is_firecrawl_available():
            use_firecrawl = st.checkbox(
                "🔥 **Use Firecrawl** (Enhanced for JavaScript sites)",
                value=config.USE_FIRECRAWL_DEFAULT,
                help="Firecrawl provides better content extraction for JavaScript-heavy sites, SPAs, and dynamic content. Recommended if standard analysis shows low word count."
            )
        else:
            use_firecrawl = False
            st.info("🔥 **Firecrawl not configured** - Add FIRECRAWL_API_KEY to enable enhanced scraping for JavaScript sites")
    
    with col_opt2:
        # Option to provide API key
        user_firecrawl_key = st.text_input(
            "Firecrawl API Key (optional)",
            type="password",
            help="Provide your own Firecrawl API key for enhanced scraping. Get one at firecrawl.dev",
            placeholder="fc-..."
        )

# Feature highlights
st.markdown("")
st.markdown("#### What We Analyze")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🤖 AI Readiness**")
    st.markdown("""
    Evaluate how well your content is structured for AI systems to understand, process, and cite in responses.
    """)

with col2:
    st.markdown("**📱 Mobile Experience**")
    st.markdown("""
    Assess mobile optimization, responsive design, and performance on mobile devices.
    """)

with col3:
    st.markdown("**🔍 Search Visibility**")
    st.markdown("""
    Review technical SEO, structured data, and crawlability for search engines.
    """)

# Show Firecrawl benefits if selected
if use_firecrawl or user_firecrawl_key:
    st.info("""
    **🔥 Firecrawl Enhanced Mode Active**
    - Better JavaScript rendering and SPA support
    - Clean markdown extraction for improved AI analysis
    - Advanced content structuring
    - LLM-powered insight extraction
    """)

# Analysis logic
if analyze_button and url_input:
    # Validate URL
    if not is_valid_url(url_input):
        st.error("❌ Please enter a valid URL (including https:// or http://)")
    else:
        # Progress indicator
        progress_container = st.container()
        
        with progress_container:
            st.markdown("### ⚙️ Running Analysis...")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_messages = [
                '"Evaluating content structure and semantic clarity..."',
                '"Assessing technical infrastructure and accessibility..."',
                '"Measuring performance and user experience metrics..."'
            ]
            
            try:
                # Determine which fetcher to use
                use_enhanced_fetcher = False
                firecrawl_api_key = None
                
                if user_firecrawl_key:
                    # User provided their own key
                    use_enhanced_fetcher = True
                    firecrawl_api_key = user_firecrawl_key
                elif use_firecrawl and is_firecrawl_available():
                    # Use system Firecrawl key
                    use_enhanced_fetcher = True
                    firecrawl_api_key = config.FIRECRAWL_API_KEY
                
                # Stage 1: Fetching
                if use_enhanced_fetcher:
                    status_text.markdown("**🔥 Fetching website with Firecrawl (enhanced mode)...**")
                    st.markdown('<span class="firecrawl-badge">FIRECRAWL ACTIVE</span>', unsafe_allow_html=True)
                else:
                    status_text.markdown("**🌐 Fetching website data...**")
                
                progress_bar.progress(10)
                
                # Import and use appropriate fetcher
                if use_enhanced_fetcher:
                    try:
                        from utils.fetcher_firecrawl import FirecrawlFetcher
                        fetcher = FirecrawlFetcher(url_input, api_key=firecrawl_api_key)
                        fetcher.fetch()
                        
                        # Show enhanced insights if available
                        insights = fetcher.get_structured_insights()
                        if insights:
                            with st.expander("🎯 AI-Extracted Insights", expanded=False):
                                if 'questions_answered' in insights:
                                    st.markdown("**Questions Answered:**")
                                    for q in insights['questions_answered'][:5]:
                                        st.markdown(f"- {q}")
                                if 'key_facts' in insights:
                                    st.markdown("**Key Facts:**")
                                    for fact in insights['key_facts'][:5]:
                                        st.markdown(f"- {fact}")
                    except Exception as e:
                        # Fallback to standard fetcher if Firecrawl fails
                        st.warning(f"⚠️ Firecrawl failed, using standard fetcher: {str(e)}")
                        fetcher = WebsiteFetcher(url_input)
                        fetcher.fetch()
                else:
                    fetcher = WebsiteFetcher(url_input)
                    fetcher.fetch()
                
                time.sleep(0.5)
                progress_bar.progress(25)
                
                # Stage 2: Performance Analysis
                status_text.markdown(f"**🚀 Checking performance metrics...**\n\n*{status_messages[1]}*")
                
                perf_analyzer = PerformanceAnalyzer(url_input)
                perf_result = perf_analyzer.analyze()
                progress_bar.progress(35)
                
                # Stage 3: Content Analysis
                status_text.markdown(f"**📝 Analyzing content structure...**\n\n*{status_messages[0]}*")
                
                # Run all analyzers
                ai_opt_analyzer = AIOptimizationAnalyzer(fetcher)
                ai_opt_result = ai_opt_analyzer.analyze()
                progress_bar.progress(45)
                
                eeat_analyzer = EEATAnalyzer(fetcher)
                eeat_result = eeat_analyzer.analyze()
                progress_bar.progress(50)
                
                tech_seo_analyzer = TechnicalSEOAnalyzer(fetcher)
                tech_seo_result = tech_seo_analyzer.analyze()
                progress_bar.progress(55)
                
                content_analyzer = ContentQualityAnalyzer(fetcher)
                content_result = content_analyzer.analyze()
                progress_bar.progress(65)
                
                status_text.markdown(f"**📱 Analyzing mobile experience...**\n\n*{status_messages[2]}*")
                mobile_analyzer = MobileOptimizationAnalyzer(fetcher, perf_result)
                mobile_result = mobile_analyzer.analyze()
                progress_bar.progress(75)
                
                schema_analyzer = SchemaAnalyzer(fetcher)
                schema_result = schema_analyzer.analyze()
                progress_bar.progress(80)
                
                crawl_analyzer = TechnicalCrawlabilityAnalyzer(fetcher)
                crawl_result = crawl_analyzer.analyze()
                progress_bar.progress(85)
                
                # Stage 4: Scoring
                status_text.markdown(f"**🎯 Calculating final scores...**\n\n*{status_messages[2]}*")
                
                # Calculate category scores
                category_scores = {
                    'ai_optimization': calculate_category_score(ai_opt_result['scores']),
                    'eeat_signals': calculate_category_score(eeat_result['scores']),
                    'technical_seo': calculate_category_score(tech_seo_result['scores']),
                    'content_quality': calculate_category_score(content_result['scores']),
                    'mobile_optimization': calculate_category_score(mobile_result['scores']),
                    'schema_analysis': calculate_category_score(schema_result['scores']),
                    'technical_crawlability': calculate_category_score(crawl_result['scores'])
                }
                
                overall_score = calculate_overall_score(category_scores)
                status_label = get_status_label(overall_score)
                
                progress_bar.progress(100)
                time.sleep(0.5)
                
                # Clear progress
                progress_container.empty()
                
                # Display results
                st.markdown("---")
                st.markdown("# 📄 Analysis Results")
                
                # Show if Firecrawl was used
                if use_enhanced_fetcher:
                    st.markdown('<span class="firecrawl-badge">Enhanced with Firecrawl</span>', unsafe_allow_html=True)
                
                # Website info and overall score
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### Site Details")
                    st.markdown(f"**URL:** {url_input}")
                    st.markdown(f"**Page Title:** {fetcher.get_title()}")
                    st.markdown(f"**Report Generated:** {datetime.now().strftime('%B %d, %Y')}")
                    st.markdown(f"**Analysis Mode:** {'🔥 Firecrawl Enhanced' if use_enhanced_fetcher else '⚡ Standard'}")
                    
                    # Show word count - important indicator
                    word_count = fetcher.get_word_count()
                    if word_count < 100:
                        st.warning(f"⚠️ **Low content extracted:** {word_count} words - Consider using Firecrawl mode for JavaScript sites")
                    else:
                        st.markdown(f"**Content Extracted:** {word_count} words")
                
                with col2:
                    st.markdown('<div class="score-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="score-number">{overall_score}%</div>', unsafe_allow_html=True)
                    status_color = get_status_color(status_label)
                    st.markdown(f'<div class="status-badge" style="background-color: {status_color}; color: white;">{status_label.upper()}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Export buttons
                st.markdown("### 📥 Download Report")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Generate markdown report
                    category_results = {
                        'ai_optimization': ai_opt_result,
                        'eeat_signals': eeat_result,
                        'technical_seo': tech_seo_result,
                        'content_quality': content_result,
                        'mobile_optimization': mobile_result,
                        'schema_analysis': schema_result,
                        'technical_crawlability': crawl_result
                    }
                    
                    markdown_report = generate_markdown_report(
                        url_input,
                        fetcher.get_title(),
                        overall_score,
                        status_label,
                        category_results,
                        perf_result
                    )
                    
                    # Add Firecrawl note to report if used
                    if use_enhanced_fetcher:
                        markdown_report = markdown_report.replace(
                            "## Executive Summary",
                            "## Executive Summary\n\n*This report was generated using Firecrawl enhanced scraping for improved JavaScript content extraction.*"
                        )
                    
                    st.download_button(
                        label="📄 Export Markdown",
                        data=markdown_report,
                        file_name=f"ai-grader-report-{urlparse(url_input).netloc.replace('.', '-')}-{datetime.now().strftime('%Y-%m-%d')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                # Category breakdown
                st.markdown("---")
                st.markdown("## 📈 Detailed Scores by Category")
                st.markdown("Expand each section below to view specific metrics, findings, and improvement suggestions.")
                st.markdown("")
                
                # Display each category
                categories = [
                    ('ai_optimization', 'AI Readiness & Optimization', ai_opt_result, 25),
                    ('mobile_optimization', 'Mobile Experience', mobile_result, 20),
                    ('technical_crawlability', 'Crawlability & Indexing', crawl_result, 16),
                    ('schema_analysis', 'Structured Data Implementation', schema_result, 12),
                    ('technical_seo', 'Technical SEO Fundamentals', tech_seo_result, 10),
                    ('content_quality', 'Content Quality & Depth', content_result, 10),
                    ('eeat_signals', 'Expertise & Trust Signals', eeat_result, 7),
                ]
                
                for category_key, category_name, result, weight in categories:
                    score = category_scores[category_key]
                    
                    with st.expander(f"**{category_name}** • Score: {score}% • Impact: {weight}%"):
                        # Detailed scores
                        st.markdown("**Individual Metrics:**")
                        for metric, metric_score in result['scores'].items():
                            metric_name = metric.replace('_', ' ').title()
                            st.markdown(f"- {metric_name}: {metric_score}%")
                        
                        # Findings
                        if result['findings']:
                            st.markdown("")
                            st.markdown("**What We Found:**")
                            for finding in result['findings']:
                                st.markdown(f"{finding}")
                        
                        # Recommendations
                        if result['recommendations']:
                            st.markdown("")
                            st.markdown("**Improvement Suggestions:**")
                            for rec in result['recommendations']:
                                priority = rec['priority']
                                title = rec['title']
                                st.markdown(f"**[{priority}] {title}**")
                                for detail in rec['details']:
                                    st.markdown(f"  - {detail}")
                
                st.success("✅ Analysis completed successfully!")
                
                # Firecrawl recommendation if low content and not using it
                if word_count < 200 and not use_enhanced_fetcher:
                    st.info("""
                    💡 **Tip: Low Content Detected**
                    
                    Only {word_count} words were extracted, which suggests this might be a JavaScript-heavy site.
                    Consider re-running the analysis with **Firecrawl enabled** in Advanced Options for better content extraction.
                    """.format(word_count=word_count))
                
            except Exception as e:
                progress_container.empty()
                st.error(f"❌ Analysis Error: {str(e)}")
                st.info("💡 **Troubleshooting Tips:**\n\n"
                       "- Verify the URL is correct and includes https:// or http://\n"
                       "- Ensure the website is publicly accessible (not behind a login)\n"
                       "- If you're seeing JavaScript/content issues, try enabling Firecrawl in Advanced Options\n"
                       "- Some websites may block automated access - try a different URL")

# Footer
st.markdown("---")

with st.expander("📚 How This Tool Works"):
    st.markdown("""
    This analyzer evaluates your website across seven weighted categories to assess how effectively 
    it can be understood and utilized by AI-powered search systems, chatbots, and intelligent assistants.
    
    **Evaluation Framework:**
    - **AI Readiness (25%):** How well AI systems can parse, understand, and reference your content
    - **Mobile Experience (20%):** Responsive design, mobile usability, and viewport configuration
    - **Crawlability & Indexing (16%):** Technical accessibility for search engine bots
    - **Structured Data (12%):** Implementation of schema markup and rich data formats
    - **Technical SEO (10%):** Foundational on-page optimization elements
    - **Content Quality (10%):** Depth, comprehensiveness, and readability of content
    - **Trust Signals (7%):** Indicators of expertise, authority, and credibility
    
    **Technology Stack:**
    - **Standard Mode:** Uses open-source libraries (BeautifulSoup, Requests) for basic HTML extraction
    - **Firecrawl Mode:** Advanced JavaScript rendering, markdown extraction, and LLM-powered insights
    - **APIs:** Google PageSpeed Insights and W3C Validator for performance metrics
    """)

with st.expander("🔥 About Firecrawl Integration"):
    st.markdown("""
    **What is Firecrawl?**
    
    Firecrawl is an advanced web scraping API that excels at extracting content from modern websites,
    especially those heavy on JavaScript, SPAs (Single Page Applications), and dynamic content.
    
    **When to Use Firecrawl:**
    - Website shows very low word count (< 200 words) in standard mode
    - Site is known to use React, Vue, Angular, or other JS frameworks
    - Content loads dynamically after page load
    - You need clean markdown extraction
    - You want AI-powered content insights
    
    **Benefits:**
    - Renders JavaScript before extraction
    - Provides clean, structured markdown
    - Extracts content that standard scrapers miss
    - Offers LLM-powered content analysis
    
    **How to Enable:**
    1. Click "Advanced Options" above the analyze button
    2. Check "Use Firecrawl" or provide your own API key
    3. Get a free API key at [firecrawl.dev](https://firecrawl.dev) (500 credits/month free)
    """)

with st.expander("🎯 Understanding Your Score"):
    st.markdown("""
    Your overall score is calculated using a weighted average across all seven categories, 
    with each category contributing based on its relative importance for AI visibility.
    
    **Score Interpretation:**
    - **90-100 (Excellent):** Your site is highly optimized for AI-powered systems
    - **80-89 (Good):** Strong foundation with room for minor enhancements
    - **70-79 (Fair):** Adequate but would benefit from targeted improvements
    - **Below 70 (Needs Work):** Significant optimization opportunities exist
    
    **Focus Areas:**
    The highest-weighted categories (AI Readiness, Mobile Experience, and Crawlability) 
    have the greatest impact on your overall score and should be prioritized for improvements.
    """)

st.markdown("---")
st.markdown("*Powered by Streamlit • Enhanced with Firecrawl • Open Source Analysis Tool*")
