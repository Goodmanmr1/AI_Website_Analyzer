"""Utilities for fetching and parsing website content"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re
import config

class WebsiteFetcher:
    def __init__(self, url):
        self.url = url
        self.html_content = None
        self.soup = None
        self.status_code = None
        
    def fetch(self):
        """Fetch HTML content from URL with retry logic for Snowflake"""
        max_retries = getattr(config, 'MAX_RETRIES', 2)
        retry_delay = getattr(config, 'RETRY_DELAY', 1)
        
        for attempt in range(max_retries + 1):
            try:
                # Use improved headers from config for better bot detection bypass
                headers = getattr(config, 'DEFAULT_HEADERS', {'User-Agent': config.USER_AGENT})
                response = requests.get(
                    self.url, 
                    headers=headers, 
                    timeout=config.REQUEST_TIMEOUT,
                    allow_redirects=True,
                    verify=True  # SSL verification
                )
                response.raise_for_status()  # Raise exception for bad status codes
                self.status_code = response.status_code
                self.html_content = response.text
                self.soup = BeautifulSoup(self.html_content, 'lxml')
                return True
            except requests.exceptions.Timeout:
                if attempt < max_retries:
                    time.sleep(retry_delay)
                    continue
                raise Exception(config.ERROR_MESSAGES.get('timeout_error', 'Request timed out'))
            except requests.exceptions.ConnectionError:
                if attempt < max_retries:
                    time.sleep(retry_delay)
                    continue
                raise Exception(config.ERROR_MESSAGES.get('network_error', 'Network connection failed'))
            except requests.exceptions.HTTPError as e:
                # Handle specific HTTP errors
                if e.response.status_code == 403:
                    raise Exception(config.ERROR_MESSAGES.get('forbidden', 'Website is blocking automated access (403 Forbidden)'))
                elif e.response.status_code == 404:
                    raise Exception(config.ERROR_MESSAGES.get('not_found', 'Page not found (404)'))
                elif e.response.status_code >= 500:
                    raise Exception(config.ERROR_MESSAGES.get('server_error', 'Website server error'))
                else:
                    raise Exception(f"HTTP {e.response.status_code}: {str(e)}")
            except requests.exceptions.RequestException as e:
                raise Exception(f"Failed to fetch URL: {str(e)}")
            except Exception as e:
                raise Exception(f"Unexpected error: {str(e)}")
    
    def get_title(self):
        """Extract page title"""
        if self.soup:
            title_tag = self.soup.find('title')
            return title_tag.get_text().strip() if title_tag else ""
        return ""
    
    def get_meta_description(self):
        """Extract meta description"""
        if self.soup:
            meta_desc = self.soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                return meta_desc['content'].strip()
        return ""
    
    def get_headings(self):
        """Extract all headings (H1-H6)"""
        headings = {'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': []}
        if self.soup:
            for level in range(1, 7):
                tag = f'h{level}'
                for heading in self.soup.find_all(tag):
                    text = heading.get_text().strip()
                    if text:
                        headings[tag].append(text)
        return headings
    
    def get_text_content(self):
        """Extract main text content with improved prioritization - FIXED"""
        if not self.soup:
            return ""
        
        # Create a copy to avoid modifying original
        soup_copy = BeautifulSoup(str(self.soup), 'lxml')
        
        # CRITICAL FIX #1: Prioritize main content areas
        # Try to find the main content container in order of priority
        main_content = None
        
        # 1. Look for <main> tag (HTML5 semantic)
        main_content = soup_copy.find('main')
        
        # 2. Look for <article> tag
        if not main_content:
            main_content = soup_copy.find('article')
        
        # 3. Look for role="main"
        if not main_content:
            main_content = soup_copy.find(attrs={'role': 'main'})
        
        # 4. Look for common content class/id patterns
        if not main_content:
            content_patterns = ['content', 'main-content', 'post-content', 'article-content', 'page-content']
            for pattern in content_patterns:
                main_content = soup_copy.find(['div', 'section'], class_=re.compile(pattern, re.I))
                if main_content:
                    break
        
        # 5. Look for common content ID patterns
        if not main_content:
            for pattern in content_patterns:
                main_content = soup_copy.find(['div', 'section'], id=re.compile(pattern, re.I))
                if main_content:
                    break
        
        # If we found a main content area, use it. Otherwise, use the whole body
        content_area = main_content if main_content else soup_copy.find('body')
        
        if not content_area:
            content_area = soup_copy
        
        # Remove non-content elements from the content area
        for element in content_area(["script", "style", "nav", "footer", "header", "aside", "form", "iframe"]):
            element.decompose()
        
        # Also remove elements with common non-content classes
        non_content_patterns = ['sidebar', 'menu', 'navigation', 'nav', 'breadcrumb', 'advertisement', 'ad', 'social', 'share', 'related', 'comment']
        for pattern in non_content_patterns:
            for element in content_area.find_all(class_=re.compile(pattern, re.I)):
                element.decompose()
        
        text = content_area.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # FALLBACK: If we got almost nothing, try getting ALL body text
        # This helps with JavaScript-heavy sites
        word_count = len(text.split())
        if word_count < 50:
            # Try less aggressive filtering
            body = soup_copy.find('body')
            if body:
                # Only remove scripts and styles
                for element in body(["script", "style"]):
                    element.decompose()
                
                text = body.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def get_images(self):
        """Extract all images with FIXED alt text detection"""
        images = []
        if self.soup:
            for img in self.soup.find_all('img'):
                alt_text = img.get('alt', '').strip()
                has_alt_attr = 'alt' in img.attrs
                
                # CRITICAL FIX #2: Properly detect meaningful alt text
                # Empty alt="" is valid for decorative images, but shouldn't count as "has alt"
                # for accessibility scoring purposes
                has_meaningful_alt = has_alt_attr and len(alt_text) > 0
                is_decorative = has_alt_attr and len(alt_text) == 0
                
                images.append({
                    'src': img.get('src', ''),
                    'alt': alt_text,
                    'has_alt': has_meaningful_alt,  # FIXED: Only True if alt has actual content
                    'is_decorative': is_decorative,  # Track decorative images separately
                    'missing_alt': not has_alt_attr  # Track completely missing alt attribute
                })
        return images
    
    def get_links(self):
        """Extract all links (internal and external) - IMPROVED"""
        links = {'internal': [], 'external': [], 'invalid': []}
        if self.soup:
            base_domain = urlparse(self.url).netloc
            for link in self.soup.find_all('a', href=True):
                href = link['href'].strip()
                
                # Skip empty hrefs, anchors, and javascript
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
        """Extract JSON-LD and Microdata schema - FIXED validation"""
        schemas = {'json_ld': [], 'microdata': []}
        
        if self.soup:
            # JSON-LD - CRITICAL FIX #3: Validate the schema is parseable
            for script in self.soup.find_all('script', type='application/ld+json'):
                try:
                    import json
                    if script.string:
                        schema_data = json.loads(script.string)
                        # Only add if it's valid and has content
                        if schema_data and isinstance(schema_data, (dict, list)):
                            # Ensure it has @type or is a list of objects with @type
                            if isinstance(schema_data, dict):
                                if '@type' in schema_data or '@context' in schema_data:
                                    schemas['json_ld'].append(schema_data)
                            elif isinstance(schema_data, list) and len(schema_data) > 0:
                                # For arrays, check if at least one item has @type
                                if any('@type' in item for item in schema_data if isinstance(item, dict)):
                                    schemas['json_ld'].append(schema_data)
                except json.JSONDecodeError:
                    # Skip invalid JSON
                    continue
                except Exception:
                    # Skip any other errors
                    continue
            
            # Microdata - FIXED: Only count valid microdata
            for item in self.soup.find_all(attrs={'itemtype': True}):
                itemtype = item.get('itemtype')
                if itemtype:  # Only add if itemtype has a value
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
        """Check for viewport meta tag - IMPROVED with validation"""
        if self.soup:
            viewport = self.soup.find('meta', attrs={'name': 'viewport'})
            if viewport:
                content = viewport.get('content', '')
                # Check if it has the expected viewport properties
                if 'width=' in content.lower() or 'initial-scale' in content.lower():
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
        # Filter out very short "words" that are likely artifacts
        meaningful_words = [w for w in words if len(w) > 1]
        return len(meaningful_words)
    
    def fetch_robots_txt(self):
        """Fetch and parse robots.txt"""
        try:
            parsed_url = urlparse(self.url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            response = requests.get(robots_url, timeout=10)
            if response.status_code == 200:
                return response.text
        except:
            pass
        return None
