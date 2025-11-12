"""Schema Markup Analysis"""

import json

class SchemaAnalyzer:
    def __init__(self, fetcher):
        self.fetcher = fetcher
        self.schemas = fetcher.get_schema_markup()
        
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
        if not self.schemas['json_ld']:
            return 0
        
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
        if not self.schemas['json_ld']:
            return 0
        
        score = 50  # Base score for having schema
        
        # Check for multiple schema types
        if len(self.schemas['json_ld']) > 1:
            score += 25
        
        # Check for rich properties
        schema_str = str(self.schemas)
        rich_properties = ['name', 'description', 'image', 'url', 'author']
        present_properties = sum(1 for prop in rich_properties if prop in schema_str)
        score += (present_properties / len(rich_properties)) * 25
        
        return round(min(100, score))
    
    def _analyze_json_ld(self):
        """Analyze JSON-LD implementation"""
        if not self.schemas['json_ld']:
            return 0
        
        return 100  # If JSON-LD exists, it's properly implemented
    
    def _generate_findings(self, scores):
        """Generate key findings"""
        findings = []
        
        if scores['schema_presence'] < 50:
            findings.append("Limited or missing structured data markup")
        
        if scores['rich_snippet_potential'] < 70:
            findings.append("Content not optimized for rich snippets")
        
        return findings
    
    def _generate_recommendations(self, scores):
        """Generate recommendations"""
        recommendations = []
        
        if scores['schema_presence'] < 70:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Implement comprehensive structured data markup',
                'details': [
                    'Add Organization schema for business information',
                    'Implement Article schema for blog posts',
                    'Use Product schema for e-commerce items',
                    'Add LocalBusiness schema if applicable',
                    'Use Google\'s Structured Data Testing Tool to validate'
                ]
            })
        
        if scores['rich_snippet_potential'] < 70:
            recommendations.append({
                'priority': 'MEDIUM',
                'title': 'Optimize content for rich snippet opportunities',
                'details': [
                    'Add FAQ schema for question-answer content',
                    'Implement Review schema for testimonials',
                    'Use HowTo schema for step-by-step guides',
                    'Add Recipe schema for cooking content',
                    'Include Event schema for event listings'
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
