"""Firecrawl-based fetcher for enhanced content extraction"""

from firecrawl import Firecrawl
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
        
        # Initialize Firecrawl with the correct API
        self.app = Firecrawl(api_key=self.api_key)
        self.scraped_data = None
        self.soup = None
        self.status_code = None
        self.markdown_content = None
        self.html_content = None
        
    def fetch(self):
        """Fetch using Firecrawl V2 API with advanced capabilities"""
        try:
            # Use the correct V2 scrape method from Firecrawl SDK
            # Note: 'metadata' is NOT a valid format - metadata is returned automatically
            # Valid formats: markdown, html, rawHtml, links, images, screenshot, summary, 
            #                changeTracking, json, attributes, branding
            self.scraped_data = self.app.scrape(
                url=self.url,
                formats=['markdown', 'html', 'links'],
                wait_for=3000,  # Wait 3 seconds for JavaScript to render
                only_main_content=False  # Get full page for complete analysis
            )
            
            if self.scraped_data:
                # The response structure for V2 API
                # Set status code
                self.status_code = 200
                
                # Extract markdown and HTML from the response
                self.markdown_content = self.scraped_data.get('markdown', '')
                self.html_content = self.scraped_data.get('html', '')
                
                # If no HTML but we have markdown, create basic HTML
                if not self.html_content and self.markdown_content:
                    self.html_content = f"<html><body>{self.markdown_content}</body></html>"
                
                # Create BeautifulSoup object for compatibility with existing analyzers
                if self.html_content:
                    self.soup = BeautifulSoup(self.html_content, 'lxml')
                
                return True
            else:
                raise Exception("No data returned from Firecrawl")
                
        except AttributeError as e:
            # If 'scrape' doesn't exist, try 'v1.scrape_url' as fallback
            try:
                self.scraped_data = self.app.v1.scrape_url(
                    self.url,
                    formats=['markdown', 'html']
                )
                
                if self.scraped_data:
                    self.status_code = 200
                    self.markdown_content = self.scraped_data.get('markdown', '')
                    self.html_content = self.scraped_data.get('html', self.scraped_data.get('content', ''))
                    
                    if self.html_content:
                        self.soup = BeautifulSoup(self.html_content, 'lxml')
                    
                    return True
                else:
                    raise Exception("No data returned from Firecrawl v1")
                    
            except Exception as e2:
                raise Exception(f"Firecrawl fetch failed (both v2 and v1): {str(e2)}")
                
        except Exception as e:
            # Fallback status code
            self.status_code = 500
            raise Exception(f"Firecrawl fetch failed: {str(e)}")
    
    def get_title(self):
        """Extract page title"""
        # Try from metadata first (metadata is automatically returned, not requested as format)
        if self.scraped_data and isinstance(self.scraped_data, dict):
            metadata = self.scraped_data.get('metadata', {})
            if metadata and 'title' in metadata:
                return metadata['title'].strip()
            
            # Try direct title field
            if 'title' in self.scraped_data:
                return self.scraped_data['title'].strip()
        
        # Fallback to soup
        if self.soup:
            title_tag = self.soup.find('title')
            return title_tag.get_text().strip() if title_tag else ""
        
        # Try to extract from markdown
        if self.markdown_content:
            lines = self.markdown_content.split('\n')
            for line in lines[:5]:  # Check first 5 lines
                if line.startswith('# '):
                    return line[2:].strip()
        
        return ""
    
    def get_meta_description(self):
        """Extract meta description"""
        # Try from metadata
        if self.scraped_data and isinstance(self.scraped_data, dict):
            metadata = self.scraped_data.get('metadata', {})
            if metadata and 'description' in metadata:
                return metadata['description'].strip()
            
            # Try direct description field
            if 'description' in self.scraped_data:
                return self.scraped_data['description'].strip()
        
        # Fallback to soup
        if self.soup:
            meta_desc = self.soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                return meta_desc['content'].strip()
        
        return ""
    
    def get_headings(self):
        """Extract all headings (H1-H6)"""
        headings = {'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': []}
        
        # Use markdown for cleaner heading extraction
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
        
        # If no headings from markdown, fallback to soup
        if not any(headings.values()) and self.soup:
            for level in range(1, 7):
                tag = f'h{level}'
                for heading in self.soup.find_all(tag):
                    text = heading.get_text().strip()
                    if text:
                        headings[tag].append(text)
        
        return headings
    
    def get_text_content(self):
        """Extract main text content"""
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
            text = re.sub(r'_{1,3}([^_]+)_{1,3}', r'\1', text)
            
            # Remove code blocks
            text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
            text = re.sub(r'`[^`]+`', '', text)
            
            # Remove horizontal rules
            text = re.sub(r'^-{3,}$', '', text, flags=re.MULTILINE)
            text = re.sub(r'^\*{3,}$', '', text, flags=re.MULTILINE)
            
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
        
        # First try to extract from HTML using soup
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
        
        # Also check markdown for images if no HTML
        elif self.markdown_content:
            img_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
            for match in re.finditer(img_pattern, self.markdown_content):
                alt_text = match.group(1).strip()
                src = match.group(2).strip()
                
                has_meaningful_alt = len(alt_text) > 0
                
                images.append({
                    'src': src,
                    'alt': alt_text,
                    'has_alt': has_meaningful_alt,
                    'is_decorative': not has_meaningful_alt,
                    'missing_alt': False
                })
        
        return images
    
    def get_links(self):
        """Extract all links"""
        links = {'internal': [], 'external': [], 'invalid': []}
        
        # Check if links are in the scraped data
        if self.scraped_data and isinstance(self.scraped_data, dict):
            if 'links' in self.scraped_data:
                from urllib.parse import urlparse
                base_domain = urlparse(self.url).netloc
                
                for link in self.scraped_data.get('links', []):
                    if isinstance(link, str):
                        try:
                            link_domain = urlparse(link).netloc
                            
                            if link_domain == base_domain or not link_domain:
                                links['internal'].append(link)
                            else:
                                links['external'].append(link)
                        except:
                            links['invalid'].append(link)
        
        # Fallback to soup-based extraction if no links found
        if not links['internal'] and not links['external'] and self.soup:
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
        
        # First try from Firecrawl metadata
        if self.scraped_data and isinstance(self.scraped_data, dict):
            metadata = self.scraped_data.get('metadata', {})
            
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
        """Fetch and parse robots.txt using standard requests"""
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
        """Extract structured insights if available - gracefully degrade if not supported"""
        # This feature may not be available in all Firecrawl plans or API versions
        # Return None to gracefully degrade
        try:
            # Try to use extract if available (v2 feature)
            if hasattr(self.app, 'extract'):
                # Simple extraction without complex schema for compatibility
                return {
                    'content_length': len(self.markdown_content) if self.markdown_content else 0,
                    'has_markdown': bool(self.markdown_content),
                    'has_html': bool(self.html_content)
                }
        except:
            pass
        
        return None
