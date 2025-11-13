"""Schema Markup Analysis"""
import json

class SchemaAnalyzer:
    def __init__(self, fetcher):
        self.fetcher = fetcher
        self.schemas = fetcher.get_schema_markup()
        self.schema_details = self._extract_schema_details()
        
    def _extract_schema_details(self):
        """Extract detailed information about schemas found"""
        details = {
            'json_ld_types': [],
            'microdata_types': [],
            'total_json_ld': len(self.schemas.get('json_ld', [])),
            'total_microdata': len(self.schemas.get('microdata', [])),
            'properties_found': set(),
            'has_organization': False,
            'has_article': False,
            'has_product': False,
            'has_local_business': False,
            'has_faq': False,
            'has_howto': False,
            'has_breadcrumb': False,
            'has_review': False
        }
        
        # Extract JSON-LD types
        for schema in self.schemas.get('json_ld', []):
            if isinstance(schema, dict):
                schema_type = schema.get('@type', '')
                if schema_type:
                    details['json_ld_types'].append(schema_type)
                    # Check for specific types
                    schema_type_lower = schema_type.lower()
                    if 'organization' in schema_type_lower:
                        details['has_organization'] = True
                    if 'article' in schema_type_lower:
                        details['has_article'] = True
                    if 'product' in schema_type_lower:
                        details['has_product'] = True
                    if 'localbusiness' in schema_type_lower:
                        details['has_local_business'] = True
                    if 'faqpage' in schema_type_lower:
                        details['has_faq'] = True
                    if 'howto' in schema_type_lower:
                        details['has_howto'] = True
                    if 'breadcrumb' in schema_type_lower:
                        details['has_breadcrumb'] = True
                    if 'review' in schema_type_lower:
                        details['has_review'] = True
                
                # Extract properties
                for key in schema.keys():
                    if not key.startswith('@'):
                        details['properties_found'].add(key)
            elif isinstance(schema, list):
                # Handle arrays of schemas
                for item in schema:
                    if isinstance(item, dict):
                        schema_type = item.get('@type', '')
                        if schema_type:
                            details['json_ld_types'].append(schema_type)
                            schema_type_lower = schema_type.lower()
                            if 'organization' in schema_type_lower:
                                details['has_organization'] = True
                            if 'article' in schema_type_lower:
                                details['has_article'] = True
                            if 'product' in schema_type_lower:
                                details['has_product'] = True
                            if 'localbusiness' in schema_type_lower:
                                details['has_local_business'] = True
                            if 'faqpage' in schema_type_lower:
                                details['has_faq'] = True
                            if 'howto' in schema_type_lower:
                                details['has_howto'] = True
                            if 'breadcrumb' in schema_type_lower:
                                details['has_breadcrumb'] = True
                            if 'review' in schema_type_lower:
                                details['has_review'] = True
                        
                        # Extract properties
                        for key in item.keys():
                            if not key.startswith('@'):
                                details['properties_found'].add(key)
        
        # Extract Microdata types
        for schema in self.schemas.get('microdata', []):
            if isinstance(schema, str):
                details['microdata_types'].append(schema)
        
        return details
    
    def analyze(self):
        """Run all schema analyses"""
        scores = {
            'schema_presence': self._analyze_schema_presence(),
            'schema_validation': self._analyze_schema_validation(),
            'rich_snippet_potential': self._analyze_rich_snippet_potential(),
            'structured_data_completeness': self._analyze_completeness(),
            'json_ld_implementation': self._analyze_json_ld()
        }
        
        findings = self._generate_findings(scores)
        recommendations = self._generate_recommendations(scores)
        
        return {
            'scores': scores,
            'findings': findings,
            'recommendations': recommendations
        }
    
    def _analyze_schema_presence(self):
        """Analyze schema markup presence - FIXED"""
        score = 0
        
        # CRITICAL FIX #6: Check length properly
        json_ld_count = len(self.schemas.get('json_ld', []))
        microdata_count = len(self.schemas.get('microdata', []))
        
        if json_ld_count > 0:
            score += 60
        
        if microdata_count > 0:
            score += 40
        
        return min(100, score)
    
    def _analyze_schema_validation(self):
        """Analyze schema validation - IMPROVED"""
        json_ld_schemas = self.schemas.get('json_ld', [])
        microdata_schemas = self.schemas.get('microdata', [])
        
        # If no schemas at all
        if not json_ld_schemas and not microdata_schemas:
            return 0
        
        # If only microdata (less preferred)
        if not json_ld_schemas and microdata_schemas:
            return 60
        
        score = 100
        
        # Validate JSON-LD structure
        for schema in json_ld_schemas:
            if isinstance(schema, dict):
                # Check for @context
                if '@context' not in schema and '@context' not in str(schema):
                    score -= 15
                    
                # Check for @type
                if '@type' not in schema:
                    score -= 15
                    
                # Check if schema has meaningful properties (not just @context and @type)
                content_keys = [k for k in schema.keys() if not k.startswith('@')]
                if len(content_keys) < 2:
                    score -= 10
                    
            elif isinstance(schema, list):
                # For schema arrays, check if at least one item is valid
                valid_items = 0
                for item in schema:
                    if isinstance(item, dict) and '@type' in item:
                        valid_items += 1
                
                if valid_items == 0:
                    score -= 20
        
        return max(0, score)
    
    def _analyze_rich_snippet_potential(self):
        """Analyze potential for rich snippets"""
        score = 0
        
        # Check for common rich snippet types
        rich_snippet_types = [
            'FAQPage', 'HowTo', 'Recipe', 'Review', 'Product',
            'Article', 'Event', 'Organization', 'LocalBusiness'
        ]
        
        schema_str = str(self.schemas).lower()
        
        for schema_type in rich_snippet_types:
            if schema_type.lower() in schema_str:
                score += 20
        
        # Check content for FAQ patterns
        text = self.fetcher.get_text_content().lower()
        if '?' in text and ('answer' in text or 'question' in text):
            score += 20
        
        return min(100, score)
    
    def _analyze_completeness(self):
        """Analyze structured data completeness - FIXED"""
        json_ld_schemas = self.schemas.get('json_ld', [])
        microdata_schemas = self.schemas.get('microdata', [])
        
        # CRITICAL FIX: Check actual content
        has_schema = len(json_ld_schemas) > 0 or len(microdata_schemas) > 0
        
        if not has_schema:
            return 0
        
        score = 50
        
        # Bonus for multiple schemas
        if len(json_ld_schemas) > 1:
            score += 25
        elif len(microdata_schemas) > 0:
            score += 15
        
        # Check for rich properties
        schema_str = str(self.schemas)
        rich_properties = ['name', 'description', 'image', 'url', 'author']
        present_properties = sum(1 for prop in rich_properties if prop in schema_str)
        score += (present_properties / len(rich_properties)) * 25
        
        return round(min(100, score))
    
    def _analyze_json_ld(self):
        """Analyze JSON-LD implementation - FIXED"""
        json_ld_count = len(self.schemas.get('json_ld', []))
        microdata_count = len(self.schemas.get('microdata', []))
        
        if json_ld_count == 0:
            if microdata_count > 0:
                return 50  # Has microdata but not JSON-LD
            return 0  # No structured data at all
        
        return 100  # Has JSON-LD
    
    def _generate_findings(self, scores):
        """Generate specific, actionable findings"""
        findings = []
        
        # Schema presence - be specific about what was found
        if self.schema_details['total_json_ld'] > 0:
            types_str = ', '.join(self.schema_details['json_ld_types'][:3])  # Show first 3
            if len(self.schema_details['json_ld_types']) > 3:
                types_str += f" (+{len(self.schema_details['json_ld_types']) - 3} more)"
            findings.append(f"✓ Found {self.schema_details['total_json_ld']} JSON-LD schema(s): {types_str}")
        elif self.schema_details['total_microdata'] > 0:
            findings.append(f"⚠ Found {self.schema_details['total_microdata']} Microdata schema(s) - consider upgrading to JSON-LD")
        else:
            findings.append("✗ No structured data markup found - missing critical SEO opportunity")
        
        # Specific schema types present
        schema_types_present = []
        if self.schema_details['has_organization']:
            schema_types_present.append("Organization")
        if self.schema_details['has_article']:
            schema_types_present.append("Article")
        if self.schema_details['has_product']:
            schema_types_present.append("Product")
        if self.schema_details['has_local_business']:
            schema_types_present.append("LocalBusiness")
        if self.schema_details['has_faq']:
            schema_types_present.append("FAQPage")
        if self.schema_details['has_howto']:
            schema_types_present.append("HowTo")
        if self.schema_details['has_breadcrumb']:
            schema_types_present.append("BreadcrumbList")
        if self.schema_details['has_review']:
            schema_types_present.append("Review")
        
        if schema_types_present:
            findings.append(f"Schema types implemented: {', '.join(schema_types_present)}")
        
        # Specific missing schema types based on content
        missing_schemas = self._identify_missing_schemas()
        if missing_schemas:
            findings.append(f"⚠ Recommended schema types to add: {', '.join(missing_schemas)}")
        
        # Properties completeness
        if self.schema_details['properties_found']:
            key_properties = ['name', 'description', 'image', 'url']
            present_key_props = [p for p in key_properties if p in self.schema_details['properties_found']]
            missing_key_props = [p for p in key_properties if p not in self.schema_details['properties_found']]
            
            if missing_key_props:
                findings.append(f"Missing key schema properties: {', '.join(missing_key_props)}")
        
        # Rich snippet potential
        if scores['rich_snippet_potential'] < 70:
            if not self.schema_details['has_faq'] and '?' in self.fetcher.get_text_content():
                findings.append("Content has questions but no FAQPage schema - add FAQ schema for rich snippets")
            if not self.schema_details['has_howto'] and any(word in self.fetcher.get_text_content().lower() for word in ['step', 'how to', 'guide']):
                findings.append("Content appears to be a guide but lacks HowTo schema")
        
        return findings
    
    def _identify_missing_schemas(self):
        """Identify what schema types should be added based on content"""
        missing = []
        text = self.fetcher.get_text_content().lower()
        
        # Check for Organization
        if not self.schema_details['has_organization']:
            if any(word in text for word in ['company', 'business', 'about us', 'contact']):
                missing.append("Organization")
        
        # Check for Article
        if not self.schema_details['has_article']:
            headings = self.fetcher.get_headings()
            if headings.get('h1') and len(text.split()) > 300:
                missing.append("Article")
        
        # Check for FAQPage
        if not self.schema_details['has_faq']:
            question_count = text.count('?')
            if question_count >= 3:
                missing.append("FAQPage")
        
        # Check for HowTo
        if not self.schema_details['has_howto']:
            if any(word in text for word in ['step 1', 'step 2', 'how to', 'instructions']):
                missing.append("HowTo")
        
        # Check for BreadcrumbList
        if not self.schema_details['has_breadcrumb']:
            # Most pages benefit from breadcrumbs
            missing.append("BreadcrumbList")
        
        # Check for LocalBusiness
        if not self.schema_details['has_local_business']:
            if any(word in text for word in ['address', 'hours', 'location', 'phone']):
                # Only suggest if looks like a local business
                if 'store' in text or 'shop' in text or 'restaurant' in text:
                    missing.append("LocalBusiness")
        
        return missing[:3]  # Return top 3 recommendations
    
    def _generate_recommendations(self, scores):
        """Generate specific, actionable recommendations"""
        recommendations = []
        
        # No schema at all
        if scores['schema_presence'] == 0:
            recommendations.append({
                'priority': 'CRITICAL',
                'title': 'Add structured data markup immediately',
                'details': [
                    f'Start with Organization schema (add company name, logo, contact info)',
                    f'Add Article schema for content pages (requires headline, author, datePublished)',
                    f'Implement BreadcrumbList schema for navigation',
                    f'Use JSON-LD format (recommended by Google)',
                    f'Test with Google Rich Results Test: https://search.google.com/test/rich-results'
                ]
            })
        
        # Has some schema but incomplete
        elif scores['schema_presence'] < 70:
            missing_schemas = self._identify_missing_schemas()
            if missing_schemas:
                details = []
                for schema_type in missing_schemas:
                    if schema_type == "Organization":
                        details.append('Add Organization schema: {"@type": "Organization", "name": "...", "url": "...", "logo": "..."}')
                    elif schema_type == "Article":
                        details.append('Add Article schema: {"@type": "Article", "headline": "...", "author": {...}, "datePublished": "..."}')
                    elif schema_type == "FAQPage":
                        details.append('Add FAQPage schema: {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "...", "acceptedAnswer": {...}}]}')
                    elif schema_type == "HowTo":
                        details.append('Add HowTo schema: {"@type": "HowTo", "name": "...", "step": [{"@type": "HowToStep", "text": "..."}]}')
                    elif schema_type == "BreadcrumbList":
                        details.append('Add BreadcrumbList schema: {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "...", "item": "..."}]}')
                
                recommendations.append({
                    'priority': 'HIGH',
                    'title': f'Add missing schema types: {", ".join(missing_schemas)}',
                    'details': details if details else [
                        'Review content type and add appropriate schema',
                        'Use schema.org to find the right schema type',
                        'Validate with Google Rich Results Test'
                    ]
                })
        
        # Has Microdata but not JSON-LD
        if self.schema_details['total_microdata'] > 0 and self.schema_details['total_json_ld'] == 0:
            recommendations.append({
                'priority': 'MEDIUM',
                'title': 'Upgrade from Microdata to JSON-LD',
                'details': [
                    'JSON-LD is easier to implement and maintain',
                    'Google recommends JSON-LD over Microdata',
                    'JSON-LD can be added without modifying HTML structure',
                    'Use a script tag with type="application/ld+json"',
                    'Convert existing Microdata to JSON-LD format'
                ]
            })
        
        # Missing key properties
        if self.schema_details['properties_found']:
            key_properties = ['name', 'description', 'image', 'url']
            missing_props = [p for p in key_properties if p not in self.schema_details['properties_found']]
            if missing_props and scores['structured_data_completeness'] < 80:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'title': f'Add missing schema properties: {", ".join(missing_props)}',
                    'details': [
                        f'Add "{prop}" property to improve schema completeness' for prop in missing_props
                    ] + [
                        'Complete schemas are more likely to generate rich results',
                        'Each property provides more context to search engines'
                    ]
                })
        
        # Rich snippet optimization
        if scores['rich_snippet_potential'] < 70:
            recommendations.append({
                'priority': 'MEDIUM',
                'title': 'Optimize for rich snippet opportunities',
                'details': [
                    'Add FAQ schema if content has Q&A format',
                    'Implement Review schema for testimonials or product reviews',
                    'Use HowTo schema for step-by-step guides',
                    'Add Recipe schema for cooking content',
                    'Include Event schema for event listings',
                    'Test eligibility with Google Rich Results Test'
                ]
            })
        
        return recommendations


"""Technical Crawlability Analysis - ENHANCED with Detailed Findings"""

class TechnicalCrawlabilityAnalyzer:
    def __init__(self, fetcher):
        self.fetcher = fetcher
        
    def analyze(self):
        """Run all crawlability analyses"""
        scores = {
            'robots_access': self._analyze_robots_access(),
            'bot_accessibility': self._analyze_bot_accessibility(),
            'content_delivery': self._analyze_content_delivery(),
            'javascript_dependency': self._analyze_javascript_dependency(),
            'load_speed': 70  # Placeholder, updated by performance analyzer
        }
        
        findings = self._generate_findings(scores)
        recommendations = self._generate_recommendations(scores)
        
        return {
            'scores': scores,
            'findings': findings,
            'recommendations': recommendations
        }
    
    def _analyze_robots_access(self):
        """Analyze robots.txt and meta robots"""
        score = 100
        issues = []
        
        # Check robots meta tag
        robots_meta = self.fetcher.check_robots_meta()
        if robots_meta:
            if 'noindex' in robots_meta.lower():
                score -= 50
                issues.append('noindex')
            if 'nofollow' in robots_meta.lower():
                score -= 30
                issues.append('nofollow')
        
        return max(0, score)
    
    def _analyze_bot_accessibility(self):
        """Analyze bot accessibility"""
        score = 100
        
        # Check for common blocking patterns
        robots_txt = self.fetcher.fetch_robots_txt()
        if robots_txt:
            if 'Disallow: /' in robots_txt:
                score -= 50
        
        # Check for CAPTCHA or bot detection
        text = self.fetcher.get_text_content().lower()
        if 'captcha' in text or 'bot detection' in text:
            score -= 20
        
        return max(0, score)
    
    def _analyze_content_delivery(self):
        """Analyze content delivery"""
        # Check status code
        if self.fetcher.status_code == 200:
            return 100
        elif self.fetcher.status_code in [301, 302]:
            return 80
        else:
            return 50
    
    def _analyze_javascript_dependency(self):
        """Analyze JavaScript dependency"""
        # Check if main content is in HTML
        text_content = self.fetcher.get_text_content()
        word_count = len(text_content.split())
        
        if word_count > 100:
            return 100
        elif word_count > 50:
            return 70
        else:
            return 40
    
    def _generate_findings(self, scores):
        """Generate detailed, actionable findings - ENHANCED"""
        findings = []
        
        # ROBOTS ACCESS
        robots_meta = self.fetcher.check_robots_meta()
        
        if robots_meta:
            if 'noindex' in robots_meta.lower():
                findings.append("✗ CRITICAL: Page has 'noindex' directive - blocking search engines from indexing this page")
            if 'nofollow' in robots_meta.lower():
                findings.append("⚠ Page has 'nofollow' directive - search engines won't follow links on this page")
            
            if 'noindex' not in robots_meta.lower() and 'nofollow' not in robots_meta.lower():
                findings.append(f"✓ Robots meta tag present with permissive settings: {robots_meta}")
        else:
            findings.append("✓ No robots meta restrictions - page is indexable")
        
        # ROBOTS.TXT
        robots_txt = self.fetcher.fetch_robots_txt()
        if robots_txt:
            if 'Disallow: /' in robots_txt:
                findings.append("✗ CRITICAL: robots.txt contains 'Disallow: /' - blocking all crawlers from entire site")
            else:
                # Count specific disallows
                disallow_count = robots_txt.count('Disallow:')
                if disallow_count > 10:
                    findings.append(f"⚠ robots.txt has {disallow_count} Disallow rules - verify these are intentional")
                elif disallow_count > 0:
                    findings.append(f"✓ robots.txt exists with {disallow_count} specific Disallow rules (targeted blocking)")
                else:
                    findings.append("✓ robots.txt exists with no restrictions - full site access granted")
        else:
            findings.append("⚠ No robots.txt found - consider adding one for crawler guidance")
        
        # BOT ACCESSIBILITY
        text = self.fetcher.get_text_content().lower()
        has_captcha = 'captcha' in text or 'bot detection' in text or 'cloudflare' in text
        
        if has_captcha:
            findings.append("⚠ Page may contain CAPTCHA or bot detection - can block AI crawlers")
        else:
            findings.append("✓ No obvious bot blocking mechanisms detected")
        
        # CONTENT DELIVERY
        status_code = self.fetcher.status_code
        
        if status_code == 200:
            findings.append(f"✓ Excellent: Page returns HTTP 200 (OK) - content delivered successfully")
        elif status_code in [301, 302]:
            findings.append(f"⚠ Page redirects (HTTP {status_code}) - consolidates properly but adds latency")
        elif status_code == 404:
            findings.append(f"✗ CRITICAL: HTTP 404 (Not Found) - page doesn't exist or is broken")
        elif status_code >= 500:
            findings.append(f"✗ CRITICAL: Server error (HTTP {status_code}) - content not accessible")
        else:
            findings.append(f"⚠ Unexpected status code: HTTP {status_code}")
        
        # JAVASCRIPT DEPENDENCY
        word_count = len(self.fetcher.get_text_content().split())
        
        if word_count > 500:
            findings.append(f"✓ Excellent: {word_count} words available in initial HTML - minimal JavaScript dependency")
        elif word_count > 100:
            findings.append(f"✓ Good: {word_count} words in initial HTML - content accessible to basic crawlers")
        elif word_count > 50:
            findings.append(f"⚠ Moderate JavaScript dependency - only {word_count} words in initial HTML (may require JS rendering)")
        else:
            findings.append(f"✗ Heavy JavaScript dependency - only {word_count} words in initial HTML - AI crawlers may miss content")
        
        # Check for semantic HTML
        has_main = self.fetcher.soup.find('main') is not None
        has_article = self.fetcher.soup.find('article') is not None
        
        if has_main or has_article:
            findings.append(f"✓ Semantic HTML detected (<main> or <article>) - helps crawlers identify primary content")
        else:
            findings.append("⚠ No semantic HTML5 tags (<main>, <article>) - harder for crawlers to identify main content")
        
        # XML SITEMAP
        sitemap_url = f"{self.fetcher.url.rstrip('/')}/sitemap.xml"
        findings.append(f"💡 TIP: Verify XML sitemap exists at {sitemap_url} for optimal crawling")
        
        # OVERALL ASSESSMENT
        avg_score = sum(scores.values()) / len(scores)
        if avg_score < 50:
            findings.append("⚠ CRITICAL: Overall crawlability is poor - AI systems may struggle to access and index your content")
        elif avg_score < 70:
            findings.append("⚠ Crawlability needs improvement - some AI crawlers may have limited access")
        else:
            findings.append("✓ Good overall crawlability - content is accessible to AI systems and search engines")
        
        return findings
    
    def _generate_recommendations(self, scores):
        """Generate detailed, prioritized recommendations - ENHANCED"""
        recommendations = []
        
        if scores['robots_access'] < 100:
            robots_meta = self.fetcher.check_robots_meta()
            
            details = []
            if robots_meta and 'noindex' in robots_meta.lower():
                details.append('CRITICAL: Remove "noindex" directive from meta robots tag immediately')
                details.append('This is blocking search engines and AI crawlers from indexing your page')
                details.append('If intentional, verify this page should be hidden from search')
            
            if robots_meta and 'nofollow' in robots_meta.lower():
                details.append('Consider removing "nofollow" directive unless you specifically want to prevent link following')
                details.append('This prevents search engines from discovering other pages through your links')
            
            robots_txt = self.fetcher.fetch_robots_txt()
            if robots_txt and 'Disallow: /' in robots_txt:
                details.append('CRITICAL: robots.txt blocks entire site with "Disallow: /"')
                details.append('Remove this or make it specific to certain paths only')
            
            if details:
                recommendations.append({
                    'priority': 'CRITICAL',
                    'title': 'Fix robots directives blocking crawlers',
                    'details': details
                })
        
        if scores['bot_accessibility'] < 70:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Improve bot accessibility',
                'details': [
                    'Audit CAPTCHA usage - avoid on content pages as it blocks AI crawlers',
                    'If using Cloudflare or bot protection, whitelist known AI crawler user-agents',
                    'Implement rate limiting instead of blanket bot blocking',
                    'Test your site with common AI crawler user-agents (GPTBot, Claude-Web, etc.)',
                    'Check robots.txt for overly restrictive "Disallow" rules',
                    'Ensure your CDN/firewall isn\'t blocking legitimate AI crawlers',
                    'Monitor server logs for bot access patterns and adjust blocking rules'
                ]
            })
        
        if scores['content_delivery'] < 80:
            status_code = self.fetcher.status_code
            
            details = []
            if status_code in [301, 302]:
                details.append(f'Page uses redirects (HTTP {status_code}) - consolidate to final URL when possible')
                details.append('Excessive redirect chains slow down crawler access')
                details.append('Use 301 redirects for permanent moves, 302 for temporary')
            elif status_code == 404:
                details.append('Page returns 404 Not Found - fix broken links or restore content')
                details.append('Update sitemap to remove dead pages')
                details.append('Implement proper 410 (Gone) for permanently deleted content')
            elif status_code >= 500:
                details.append(f'Server error (HTTP {status_code}) - urgent server-side fix needed')
                details.append('Check server logs for root cause')
                details.append('Implement health monitoring and alerting')
            
            if details:
                recommendations.append({
                    'priority': 'HIGH' if status_code >= 400 else 'MEDIUM',
                    'title': 'Fix content delivery issues',
                    'details': details
                })
        
        if scores['javascript_dependency'] < 70:
            word_count = len(self.fetcher.get_text_content().split())
            
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Reduce JavaScript dependency for AI accessibility',
                'details': [
                    f'Current: Only {word_count} words available in initial HTML',
                    f'Goal: Deliver 300+ words of main content in HTML (before JavaScript)',
                    'Implement server-side rendering (SSR) or static site generation (SSG)',
                    'Use progressive enhancement - deliver core content in HTML, enhance with JS',
                    'For React/Vue apps: use Next.js, Nuxt.js, or similar frameworks with SSR',
                    'Avoid client-side only rendering for content pages',
                    'Test with JavaScript disabled to see what crawlers see',
                    'Use dynamic rendering (detect crawler user-agents, serve pre-rendered HTML)',
                    'Implement proper <noscript> fallbacks for critical content'
                ]
            })
        
        # Always include best practices
        recommendations.append({
            'priority': 'BEST PRACTICE',
            'title': 'Crawlability optimization checklist',
            'details': [
                'Create and submit XML sitemap to Google Search Console',
                'Implement proper canonical tags to avoid duplicate content',
                'Use descriptive, SEO-friendly URLs (avoid IDs and parameters when possible)',
                'Ensure proper use of rel="nofollow" on user-generated content links',
                'Implement proper 404 and 410 status codes for missing content',
                'Set up Google Search Console and monitor for crawl errors',
                'Create robots.txt with strategic Disallow rules (block admin, private sections)',
                'Add Sitemap location to robots.txt file',
                'Test crawlability with Google Search Console URL Inspection tool',
                'Monitor server response times - aim for <200ms TTFB',
                'Use semantic HTML5 tags (<main>, <article>, <nav>, <aside>)',
                'Implement breadcrumb navigation for site structure',
                'Ensure internal linking connects all important pages (3 clicks from homepage)',
                'Use rel="alternate" for mobile versions if separate',
                'Implement hreflang tags for international/multilingual sites'
            ]
        })
        
        return recommendations
