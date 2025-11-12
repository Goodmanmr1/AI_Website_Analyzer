"""Schema Markup Analysis - Enhanced with Specific Findings"""

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
        
        # Extract Microdata types
        for schema in self.schemas.get('microdata', []):
            if isinstance(schema, dict):
                schema_type = schema.get('type', '')
                if schema_type:
                    details['microdata_types'].append(schema_type)
        
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
        """Analyze schema markup presence"""
        score = 0
        
        if self.schemas['json_ld']:
            score += 60
        
        if self.schemas['microdata']:
            score += 40
        
        return min(100, score)
    
    def _analyze_schema_validation(self):
        """Analyze schema validation"""
        if not self.schemas['json_ld'] and not self.schemas['microdata']:
            return 0
        
        if not self.schemas['json_ld'] and self.schemas['microdata']:
            return 60
        
        score = 100
        
        # Check if JSON-LD is valid JSON
        for schema in self.schemas['json_ld']:
            try:
                if isinstance(schema, str):
                    json.loads(schema)
                # Check for @context and @type
                if '@context' not in str(schema):
                    score -= 20
                if '@type' not in str(schema):
                    score -= 20
            except:
                score -= 30
        
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
        """Analyze structured data completeness"""
        has_schema = self.schemas['json_ld'] or self.schemas['microdata']
        
        if not has_schema:
            return 0
        
        score = 50
        
        if self.schemas['json_ld'] and len(self.schemas['json_ld']) > 1:
            score += 25
        elif self.schemas['microdata']:
            score += 15
        
        # Check for rich properties
        schema_str = str(self.schemas)
        rich_properties = ['name', 'description', 'image', 'url', 'author']
        present_properties = sum(1 for prop in rich_properties if prop in schema_str)
        score += (present_properties / len(rich_properties)) * 25
        
        return round(min(100, score))
    
    def _analyze_json_ld(self):
        """Analyze JSON-LD implementation"""
        if not self.schemas['json_ld']:
            if self.schemas['microdata']:
                return 50
            return 0
        
        return 100
    
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
        
        # Check robots meta tag
        robots_meta = self.fetcher.check_robots_meta()
        if robots_meta:
            if 'noindex' in robots_meta.lower():
                score -= 50
            if 'nofollow' in robots_meta.lower():
                score -= 30
        
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
        """Generate key findings"""
        findings = []
        
        if scores['robots_access'] < 100:
            findings.append("Robots access may be restricted")
        
        if scores['javascript_dependency'] < 70:
            findings.append("Heavy JavaScript dependency may affect crawlability")
        
        return findings
    
    def _generate_recommendations(self, scores):
        """Generate recommendations"""
        recommendations = []
        
        if scores['robots_access'] < 100:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Review robots.txt and meta robots settings',
                'details': [
                    'Ensure important pages are not blocked',
                    'Remove unnecessary Disallow directives',
                    'Check meta robots tags'
                ]
            })
        
        if scores['javascript_dependency'] < 70:
            recommendations.append({
                'priority': 'MEDIUM',
                'title': 'Reduce JavaScript dependency for content',
                'details': [
                    'Render critical content in HTML',
                    'Use server-side rendering',
                    'Implement progressive enhancement'
                ]
            })
        
        return recommendations
