"""Firecrawl-based fetcher for enhanced content extraction"""

from firecrawl import FirecrawlApp
import os
from bs4 import BeautifulSoup
import json
import re

class FirecrawlFetcher:
    """Enhanced fetcher using Firecrawl for JavaScript-heavy sites"""
    
    def __init__(self, url, api_key=None):
        self.url = url
        self.api_key = api_key or os.getenv('FIRECRAWL_API_KEY')
        
        if not self.api_key:
            raise ValueError("Firecrawl API key is required. Set FIRECRAWL_API_KEY environment variable or pass api_key parameter.")
        
        self.app = FirecrawlApp(api_key=self.api_key)
        self.scraped_data = None
        self.soup = None
        self.status_code = None
        self.markdown_content = None
        self.html_content = None
        
    def fetch(self):
        """Fetch using Firecrawl with advanced capabilities"""
        try:
            # Scrape with comprehensive options
            self.scraped_data = self.app.scrape_url(
                self.url,
                params={
                    'formats': ['markdown', 'html', 'links', 'metadata', 'screenshot'],
                    'onlyMainContent': False,  # Get full page for complete analysis
                    'waitFor': 3000,  # Wait 3 seconds for JavaScript to render
                    'screenshot': False,  # Set to True if you want screenshots
                    'removeBase64Images': True,  # Remove base64 images for cleaner content
                    'includeTags': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'article', 'main', 'div', 'section', 'ul', 'ol', 'table', 'img', 'a', 'meta', 'title', 'script[type="application/ld+json"]']
                }
            )
            
            if self.scraped_data:
                # Set status code (Firecrawl usually returns 200 for successful scrapes)
                self.status_code = self.scraped_data.get('statusCode', 200)
                
                # Store markdown and HTML
                self.markdown_content = self.scraped_data.get('markdown', '')
                self.html_content = self.scraped_data.get('html', '')
                
                # Create BeautifulSoup object for compatibility with existing analyzers
                if self.html_content:
                    self.soup = BeautifulSoup(self.html_content, 'lxml')
                
                return True
            else:
                raise Exception("No data returned from Firecrawl")
                
        except Exception as e:
            # Fallback status code
            self.status_code = 500
            raise Exception(f"Firecrawl fetch failed: {str(e)}")
    
    def get_title(self):
        """Extract page title"""
        # First try metadata
        if self.scraped_data and 'metadata' in self.scraped_data:
            title = self.scraped_data['metadata'].get('title', '')
            if title:
                return title.strip()
        
        # Fallback to soup
        if self.soup:
            title_tag = self.soup.find('title')
            return title_tag.get_text().strip() if title_tag else ""
        
        return ""
    
    def get_meta_description(self):
        """Extract meta description"""
        # First try metadata
        if self.scraped_data and 'metadata' in self.scraped_data:
            desc = self.scraped_data['metadata'].get('description', '')
            if desc:
                return desc.strip()
        
        # Fallback to soup
        if self.soup:
            meta_desc = self.soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                return meta_desc['content'].strip()
        
        return ""
    
    def get_headings(self):
        """Extract all headings (H1-H6)"""
        headings = {'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': []}
        
        # Use markdown for better heading extraction
        if self.markdown_content:
            lines = self.markdown_content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('#'):
                    # Count the number of # symbols
                    level = 0
                    for char in line:
                        if char == '#':
                            level += 1
                        else:
                            break
                    
                    if 1 <= level <= 6:
                        # Extract the heading text
                        heading_text = line[level:].strip()
                        if heading_text:
                            headings[f'h{level}'].append(heading_text)
        
        # Fallback to soup if markdown parsing didn't work well
        if not any(headings.values()) and self.soup:
            for level in range(1, 7):
                tag = f'h{level}'
                for heading in self.soup.find_all(tag):
                    text = heading.get_text().strip()
                    if text:
                        headings[tag].append(text)
        
        return headings
    
    def get_text_content(self):
        """Extract main text content - uses Firecrawl's clean markdown"""
        if self.markdown_content:
            # Remove markdown formatting for plain text
            text = self.markdown_content
            
            # Remove images
            text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
            
            # Remove links but keep text
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
            
            # Remove headers markdown
            text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
            
            # Remove bold/italic markers
            text = re.sub(r'\*{1,3}([^\*]+)\*{1,3}', r'\1', text)
            
            # Remove code blocks
            text = re.sub(r'```[^`]*```', '', text)
            text = re.sub(r'`[^`]+`', '', text)
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        
        # Fallback to soup
        elif self.soup:
            # Remove script and style elements
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
        """Extract all images with alt text information"""
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
        """Extract all links using Firecrawl's link extraction"""
        links = {'internal': [], 'external': [], 'invalid': []}
        
        # Use Firecrawl's links if available
        if self.scraped_data and 'links' in self.scraped_data:
            from urllib.parse import urlparse
            base_domain = urlparse(self.url).netloc
            
            for link in self.scraped_data.get('links', []):
                try:
                    link_domain = urlparse(link).netloc
                    
                    if link_domain == base_domain or not link_domain:
                        links['internal'].append(link)
                    else:
                        links['external'].append(link)
                except:
                    links['invalid'].append(link)
        
        # Fallback to soup-based extraction
        elif self.soup:
            from urllib.parse import urlparse, urljoin
            base_domain = urlparse(self.url).netloc
            
            for link in self.soup.find_all('a', href=True):
                href = link['href'].strip()
                
                if not href or href.startswith('#') or href.startswith('javascript:'):
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
        
        # First try Firecrawl's metadata
        if self.scraped_data and 'metadata' in self.scraped_data:
            metadata = self.scraped_data['metadata']
            for key, value in metadata.items():
                if value:
                    meta_tags[key] = value
        
        # Add any additional from soup
        if self.soup:
            for meta in self.soup.find_all('meta'):
                name = meta.get('name') or meta.get('property') or meta.get('http-equiv')
                content = meta.get('content')
                if name and content and name not in meta_tags:
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
            from urllib.parse import urlparse
            parsed_url = urlparse(self.url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            
            # Try to fetch robots.txt using Firecrawl
            robots_data = self.app.scrape_url(
                robots_url,
                params={'formats': ['markdown']}
            )
            
            if robots_data and 'markdown' in robots_data:
                return robots_data['markdown']
        except:
            pass
        return None
    
    def get_structured_insights(self):
        """Extract AI-relevant insights using Firecrawl's LLM extraction"""
        try:
            extraction_schema = {
                "type": "object",
                "properties": {
                    "questions_answered": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Main questions this content answers"
                    },
                    "key_facts": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Important facts and statistics mentioned"
                    },
                    "expertise_indicators": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Signs of expertise, credentials, or authority"
                    },
                    "main_topics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Primary topics covered"
                    },
                    "content_depth": {
                        "type": "string",
                        "enum": ["superficial", "moderate", "comprehensive", "expert-level"],
                        "description": "Depth of content coverage"
                    }
                }
            }
            
            result = self.app.scrape_url(
                self.url,
                params={
                    'formats': ['extract'],
                    'extract': {
                        'schema': extraction_schema,
                        'systemPrompt': "Extract key information that would be valuable for AI systems to understand and reference this content."
                    }
                }
            )
            
            if result and 'extract' in result:
                return result['extract']
        except:
            pass
        
        return None
