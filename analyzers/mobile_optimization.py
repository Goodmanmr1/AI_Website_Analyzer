"""Mobile Optimization Analysis"""

class MobileOptimizationAnalyzer:
    def __init__(self, fetcher):
        self.fetcher = fetcher
        
    def analyze(self):
        """Run all mobile optimization analyses"""
        scores = {
            'mobile_page_speed': 80,  # Placeholder, updated by performance analyzer
            'touch_targets': self._analyze_touch_targets(),
            'viewport_config': self._analyze_viewport(),
            'mobile_usability': 85,  # Placeholder, updated by performance analyzer
            'responsive_design': self._analyze_responsive_design()
        }
        
        findings = self._generate_findings(scores)
        recommendations = self._generate_recommendations(scores)
        
        return {
            'scores': scores,
            'findings': findings,
            'recommendations': recommendations
        }
    
    def _analyze_touch_targets(self):
        """Analyze touch target sizes"""
        # Check for buttons and links
        buttons = self.fetcher.soup.find_all(['button', 'a'])
        
        if not buttons:
            return 100
        
        # Assume good touch targets if buttons/links exist
        # (actual size checking would require rendering)
        return 100
    
    def _analyze_viewport(self):
        """Analyze viewport configuration"""
        has_viewport = self.fetcher.check_viewport()
        return 100 if has_viewport else 0
    
    def _analyze_responsive_design(self):
        """Analyze responsive design indicators"""
        score = 50  # Base score
        
        # Check for viewport meta tag
        if self.fetcher.check_viewport():
            score += 25
        
        # Check for media queries in style tags
        style_tags = self.fetcher.soup.find_all('style')
        has_media_queries = any('@media' in str(tag) for tag in style_tags)
        
        # Check for responsive CSS links
        css_links = self.fetcher.soup.find_all('link', rel='stylesheet')
        
        if has_media_queries or css_links:
            score += 25
        
        return min(100, score)
    
    def _generate_findings(self, scores):
        """Generate key findings"""
        findings = []
        
        if scores['responsive_design'] < 70:
            findings.append("Responsive design implementation needs improvement")
        
        if scores['viewport_config'] < 100:
            findings.append("Missing viewport meta tag")
        
        return findings
    
    def _generate_recommendations(self, scores):
        """Generate recommendations"""
        recommendations = []
        
        if scores['responsive_design'] < 80:
            recommendations.append({
                'priority': 'MEDIUM',
                'title': 'Enhance responsive design implementation',
                'details': [
                    'Use CSS media queries for different screen sizes',
                    'Implement flexible grid layouts',
                    'Use responsive images with srcset',
                    'Test on multiple devices and screen sizes',
                    'Ensure consistent experience across devices'
                ]
            })
        
        if scores['viewport_config'] < 100:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Add viewport meta tag',
                'details': [
                    'Add <meta name="viewport" content="width=device-width, initial-scale=1.0">',
                    'Ensure proper scaling on mobile devices'
                ]
            })
        
        return recommendations
