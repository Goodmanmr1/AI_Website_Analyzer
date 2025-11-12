"""Technical SEO Analysis"""

import config

class TechnicalSEOAnalyzer:
    def __init__(self, fetcher):
        self.fetcher = fetcher
        
    def analyze(self):
        """Run all technical SEO analyses"""
        scores = {
            'heading_structure': self._analyze_heading_structure(),
            'meta_info': self._analyze_meta_info(),
            'alt_text': self._analyze_alt_text(),
            'links': self._analyze_links(),
            'schema_markup': self._analyze_schema_markup(),
            'page_speed': 75  # Placeholder, will be updated by performance analyzer
        }
        
        findings = self._generate_findings(scores)
        recommendations = self._generate_recommendations(scores)
        
        return {
            'scores': scores,
            'findings': findings,
            'recommendations': recommendations
        }
    
    def _analyze_heading_structure(self):
        """Analyze heading hierarchy"""
        headings = self.fetcher.get_headings()
        score = 100
        
        # Check H1 count (should be exactly 1)
        h1_count = len(headings['h1'])
        if h1_count == 0:
            score -= 50
        elif h1_count > 1:
            score -= 30
        
        # Check for logical hierarchy
        total_headings = sum(len(h) for h in headings.values())
        if total_headings < 3:
            score -= 30
        
        # Check if H2s exist
        if len(headings['h2']) == 0 and total_headings > 1:
            score -= 20
        
        return max(0, score)
    
    def _analyze_meta_info(self):
        """Analyze meta information"""
        score = 100
        
        # Check title
        title = self.fetcher.get_title()
        if not title:
            score -= 40
        elif len(title) < config.IDEAL_TITLE_LENGTH[0]:
            score -= 20
        elif len(title) > config.IDEAL_TITLE_LENGTH[1]:
            score -= 10
        
        # Check meta description
        meta_desc = self.fetcher.get_meta_description()
        if not meta_desc:
            score -= 40
        elif len(meta_desc) < config.IDEAL_META_DESC_LENGTH[0]:
            score -= 20
        elif len(meta_desc) > config.IDEAL_META_DESC_LENGTH[1]:
            score -= 10
        
        return max(0, score)
    
    def _analyze_alt_text(self):
        """Analyze image alt text coverage"""
        images = self.fetcher.get_images()
        
        if not images:
            return 100  # No images, no problem
        
        images_with_alt = sum(1 for img in images if img['has_alt'])
        coverage = (images_with_alt / len(images)) * 100
        
        return round(coverage)
    
    def _analyze_links(self):
        """Analyze link structure"""
        links = self.fetcher.get_links()
        score = 100
        
        internal_count = len(links['internal'])
        external_count = len(links['external'])
        total_links = internal_count + external_count
        
        if total_links == 0:
            return 50
        
        # Check for balance (ideal: more internal than external)
        if internal_count == 0:
            score -= 30
        
        if external_count == 0:
            score -= 10
        
        # Check for reasonable link density
        word_count = self.fetcher.get_word_count()
        if word_count > 0:
            link_density = (total_links / word_count) * 100
            if link_density < 1:  # Too few links
                score -= 20
            elif link_density > 5:  # Too many links
                score -= 10
        
        return max(0, score)
    
    def _analyze_schema_markup(self):
        """Analyze schema markup presence"""
        schemas = self.fetcher.get_schema_markup()
        score = 0
        
        # JSON-LD presence
        if schemas['json_ld']:
            score += 50
        
        # Microdata presence
        if schemas['microdata']:
            score += 50
        
        return score
    
    def _generate_findings(self, scores):
        """Generate key findings"""
        findings = []
        
        if scores['heading_structure'] < 70:
            findings.append("Heading structure needs improvement")
        
        if scores['meta_info'] < 70:
            findings.append("Meta information is incomplete or unoptimized")
        
        if scores['schema_markup'] < 50:
            findings.append("Missing or incomplete schema markup")
        
        if scores['alt_text'] < 90:
            findings.append("Some images missing alt text")
        
        return findings
    
    def _generate_recommendations(self, scores):
        """Generate recommendations"""
        recommendations = []
        
        if scores['heading_structure'] < 70:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Implement proper H1-H6 hierarchy with one H1 per page',
                'details': [
                    'Ensure exactly one H1 tag per page',
                    'Use H2 for major sections',
                    'Use H3 for subsections',
                    'Include target keywords naturally in headings',
                    'Maintain logical hierarchy (H1→H2→H3)'
                ]
            })
        
        if scores['meta_info'] < 70:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Create compelling meta descriptions and optimize title tags',
                'details': [
                    'Write meta descriptions 150-160 characters long',
                    'Include target keywords naturally',
                    'Make each meta description unique',
                    'Create action-oriented descriptions',
                    'Optimize title tags (30-60 characters)'
                ]
            })
        
        if scores['schema_markup'] < 50:
            recommendations.append({
                'priority': 'MEDIUM',
                'title': 'Implement structured data markup',
                'details': [
                    'Add Organization schema',
                    'Use Article schema for blog posts',
                    'Implement FAQ schema for Q&A content',
                    'Add Local Business schema if applicable',
                    'Test with Google\'s Structured Data Testing Tool'
                ]
            })
        
        return recommendations
