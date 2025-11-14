"""Firecrawl-based fetcher for enhanced content extraction"""

from firecrawl import Firecrawl
import os
from bs4 import BeautifulSoup
import json
import re

class FirecrawlFetcher:
    """Enhanced fetcher using Firecrawl V2 API for JavaScript-heavy sites"""
    
    def __init__(self, url, api_key=None):
        self.url = url
        self.api_key = api_key or os.getenv('FIRECRAWL_API_KEY')
        
        if not self.api_key:
            raise ValueError("Firecrawl API key is required. Set FIRECRAWL_API_KEY environment variable or pass api_key parameter.")
        
        # Initialize Firecrawl with the V2 API
        self.app = Firecrawl(api_key=self.api_key)
        self.scraped_data = None
        self.soup = None
        self.status_code = None
        self.markdown_content = None
        self.html_content = None
        
    def fetch(self):
        """Fetch using Firecrawl V2 API - Returns object with attributes, not dict"""
        try:
            # V2 API: scrape() returns an object with attributes like .markdown, .html
            # NOT a dictionary - this was the main issue!
            scrape_result = self.app.scrape(
                url=self.url,
                formats=['markdown', 'html', 'links']
            )
            
            if scrape_result:
                self.status_code = 200
                
                # KEY FIX: Access as attributes, not dictionary
                # The V2 SDK returns an object with attributes like scrape_result.markdown
                try:
                    # Try attribute access (correct for V2)
                    self.markdown_content = scrape_result.markdown if hasattr(scrape_result, 'markdown') else ''
                    self.html_content = scrape_result.html if hasattr(scrape_result, 'html') else ''
                    
                    # Debug: if both are empty, try inspecting the object
                    if not self.markdown_content and not self.html_content:
                        # Try to get the data attribute (alternative structure)
                        if hasattr(scrape_result, 'data'):
                            data = scrape_result.data
                            self.markdown_content = data.get('markdown', '') if isinstance(data, dict) else ''
                            self.html_content = data.get('html', '') if isinstance(data, dict) else ''
                        
                except AttributeError as e:
                    raise Exception(f"Unexpected response structure from Firecrawl: {str(e)}. Response object: {type(scrape_result)}")
                
                # If no HTML but we have markdown, create basic HTML
                if not self.html_content and self.markdown_content:
                    self.html_content = self._markdown_to_html(self.markdown_content)
                
                # Create BeautifulSoup object for compatibility with existing analyzers
                if self.html_content:
                    self.soup = BeautifulSoup(self.html_content, 'lxml')
                elif self.markdown_content:
                    # Fallback: wrap markdown in HTML tags if no HTML provided
                    html = self._markdown_to_html(self.markdown_content)
                    self.soup = BeautifulSoup(html, 'lxml')
                
                return True
            else:
                raise Exception("No data returned from Firecrawl")
                
        except Exception as e:
            error_msg = str(e)
            
            # Provide helpful error messages
            if "unauthorized" in error_msg.lower() or "invalid" in error_msg.lower() or "401" in error_msg:
                raise Exception(f"❌ Firecrawl API Error: Invalid API key. Check your FIRECRAWL_API_KEY. Full error: {error_msg}")
            elif "403" in error_msg or "forbidden" in error_msg.lower():
                raise Exception(f"❌ Firecrawl API Error: Access forbidden. Your API key may not have permission for this operation. Error: {error_msg}")
            elif "timeout" in error_msg.lower():
                raise Exception(f"❌ Firecrawl request timed out: The target website took too long to respond. Error: {error_msg}")
            elif "rate" in error_msg.lower():
                raise Exception(f"❌ Firecrawl Rate Limited: You've exceeded your API quota. Error: {error_msg}")
            else:
                raise Exception(f"❌ Firecrawl fetch failed: {error_msg}")
    
    def _markdown_to_html(self, markdown_text):
        """Convert markdown to basic HTML for BeautifulSoup parsing"""
        html = markdown_text
        
        # Convert markdown headers to HTML
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Convert markdown lists to HTML
        html = re.sub(r'^\- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        
        # Convert paragraph breaks
        html = re.sub(r'\n\n+', '</p><p>', html)
        
        # Wrap in HTML tags
        html = f"<html><body><p>{html}</p></body></html>"
        return html
    
    def get_title(self):
        """Extract page title"""
        if self.soup:
            title_tag = self.soup.find('title')
            return title_tag.get_text().strip() if title_tag else ""
        
        # Try to extract from first H1 in markdown
        if self.markdown_content:
            lines = self.markdown_content.split('\n')
            for line in lines[:10]:
                if line.startswith('# '):
                    return line[2:].strip()
        
        return ""
    
    def get_meta_description(self):
        """Extract meta description"""
        if self.soup:
            meta_desc = self.soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                return meta_desc['content'].strip()
        
        # Fallback to first paragraph
        if self.markdown_content:
            lines = [l.strip() for l in self.markdown_content.split('\n') if l.strip() and not l.startswith('#')]
            if lines:
                desc = lines[0][:160]
                return desc
        
        return ""
    
    def get_headings(self):
        """Extract all headings from markdown or HTML"""
        headings = {'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': []}
        
        # Extract from markdown (more reliable)
        if self.markdown_content:
            lines = self.markdown_content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('#'):
                    level = 0
                    for char in line:
                        if char == '#':
                            level += 1
                        else:
                            break
                    
                    if 1 <= level <= 6:
                        heading_text = line[level:].strip()
                        if heading_text:
                            headings[f'h{level}'].append(heading_text)
        
        # Fallback to HTML if no markdown headings
        if not any(headings.values()) and self.soup:
            for level in range(1, 7):
                tag = f'h{level}'
                for heading in self.soup.find_all(tag):
                    text = heading.get_text().strip()
                    if text:
                        headings[tag].append(text)
        
        return headings
    
    def get_text_content(self):
        """Extract main text content from markdown"""
        if self.markdown_content:
            text = self.markdown_content
            
            # Remove images
            text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
            
            # Remove links but keep text
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
            
            # Remove headers markdown
            text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
            
            # Remove bold/italic markers
            text = re.sub(r'\*{1,3}([^\*]+)\*{1,3}', r'\1', text)
            text = re.sub(r'_{1,3}([^_]+)_{1,3}', r'\1', text)
            
            # Remove code blocks
            text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
            text = re.sub(r'`[^`]+`', '', text)
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        
        # Fallback to soup
        elif self.soup:
            for element in self.soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()
            
            text = self.soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            return text
        
        return ""
    
    def get_markdown_content(self):
        """Get clean markdown - perfect for AI analysis"""
        return self.markdown_content or ''
    
    def get_images(self):
        """Extract images from HTML"""
        images = []
        
        if self.soup:
            for img in self.soup.find_all('img'):
                alt_text = img.get('alt', '').strip()
                has_alt_attr = 'alt' in img.attrs
                has_meaningful_alt = has_alt_attr and len(alt_text) > 0
                is_decorative = has_alt_attr and len(alt_text) == 0
                
                images.append({
                    'src': img.get('src', ''),
                    'alt': alt_text,
                    'has_alt': has_meaningful_alt,
                    'is_decorative': is_decorative,
                    'missing_alt': not has_alt_attr
                })
        
        return images
    
    def get_links(self):
        """Extract internal and external links"""
        links = {'internal': [], 'external': [], 'invalid': []}
        
        if self.soup:
            from urllib.parse import urlparse, urljoin
            base_domain = urlparse(self.url).netloc
            
            for link in self.soup.find_all('a', href=True):
                href = link['href'].strip()
                
                if not href or href.startswith('#') or href.startswith('javascript:') or href.startswith('mailto:') or href.startswith('tel:'):
                    continue
                
                try:
                    absolute_url = urljoin(self.url, href)
                    link_domain = urlparse(absolute_url).netloc
                    
                    if link_domain == base_domain or not link_domain:
                        links['internal'].append(absolute_url)
                    else:
                        links['external'].append(absolute_url)
                except:
                    links['invalid'].append(href)
        
        return links
    
    def get_schema_markup(self):
        """Extract JSON-LD and Microdata schema"""
        schemas = {'json_ld': [], 'microdata': []}
        
        if self.soup:
            # JSON-LD
            for script in self.soup.find_all('script', type='application/ld+json'):
                try:
                    if script.string:
                        schema_data = json.loads(script.string)
                        if schema_data and isinstance(schema_data, (dict, list)):
                            schemas['json_ld'].append(schema_data)
                except json.JSONDecodeError:
                    continue
            
            # Microdata
            for item in self.soup.find_all(attrs={'itemtype': True}):
                itemtype = item.get('itemtype')
                if itemtype:
                    schemas['microdata'].append(itemtype)
        
        return schemas
    
    def get_meta_tags(self):
        """Extract all meta tags"""
        meta_tags = {}
        
        if self.soup:
            for meta in self.soup.find_all('meta'):
                name = meta.get('name') or meta.get('property') or meta.get('http-equiv')
                content = meta.get('content')
                if name and content:
                    meta_tags[name] = content
        
        return meta_tags
    
    def check_viewport(self):
        """Check for viewport meta tag"""
        if self.soup:
            viewport = self.soup.find('meta', attrs={'name': 'viewport'})
            if viewport:
                content = viewport.get('content', '')
                if 'width=' in content.lower():
                    return True
        return False
    
    def check_robots_meta(self):
        """Check robots meta tag"""
        if self.soup:
            robots = self.soup.find('meta', attrs={'name': 'robots'})
            if robots:
                return robots.get('content', '')
        return None
    
    def get_word_count(self):
        """Get word count of main content"""
        text = self.get_text_content()
        words = text.split()
        meaningful_words = [w for w in words if len(w) > 1]
        return len(meaningful_words)
    
    def fetch_robots_txt(self):
        """Fetch and parse robots.txt"""
        try:
            import requests
            from urllib.parse import urlparse
            
            parsed_url = urlparse(self.url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                return response.text
        except:
            pass
        return None
    
    def get_structured_insights(self):
        """Extract any structured insights from Firecrawl response (graceful degradation)"""
        # This may not be available in all Firecrawl plans
        # Return basic info instead
        return {
            'content_length': len(self.markdown_content) if self.markdown_content else 0,
            'has_markdown': bool(self.markdown_content),
            'has_html': bool(self.html_content),
            'word_count': self.get_word_count()
        }
