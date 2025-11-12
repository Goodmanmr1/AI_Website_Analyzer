"""Utilities for fetching and parsing website content - Snowflake Edition"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
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
        """Extract main text content"""
        if self.soup:
            # Remove script and style elements
            for script in self.soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            text = self.soup.get_text()
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            return text
        return ""
    
    def get_images(self):
        """Extract all images with alt text info"""
        images = []
        if self.soup:
            for img in self.soup.find_all('img'):
                alt_text = img.get('alt')
                # Check if alt attribute exists (even if empty)
                has_alt_attr = 'alt' in img.attrs
                # Empty alt="" is valid for decorative images
                # Missing alt is the actual problem
                images.append({
                    'src': img.get('src', ''),
                    'alt': alt_text if alt_text else '',
                    'has_alt': has_alt_attr,  # True even if alt=""
                    'is_decorative': has_alt_attr and not alt_text  # Empty alt
                })
        return images
    
    def get_links(self):
        """Extract all links (internal and external)"""
        links = {'internal': [], 'external': []}
        if self.soup:
            base_domain = urlparse(self.url).netloc
            for link in self.soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(self.url, href)
                link_domain = urlparse(absolute_url).netloc
                
                if link_domain == base_domain or not link_domain:
                    links['internal'].append(absolute_url)
                else:
                    links['external'].append(absolute_url)
        return links
    
    def get_schema_markup(self):
        """Extract JSON-LD and Microdata schema"""
        schemas = {'json_ld': [], 'microdata': []}
        
        if self.soup:
            # JSON-LD
            for script in self.soup.find_all('script', type='application/ld+json'):
                try:
                    import json
                    schema_data = json.loads(script.string)
                    schemas['json_ld'].append(schema_data)
                except:
                    pass
            
            # Microdata
            for item in self.soup.find_all(attrs={'itemtype': True}):
                schemas['microdata'].append(item.get('itemtype'))
        
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
            return viewport is not None
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
        return len(text.split())
    
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
