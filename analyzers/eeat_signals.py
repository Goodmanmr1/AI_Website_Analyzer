"""E-E-A-T Signals Analysis (Expertise, Experience, Authoritativeness, Trustworthiness)"""

import re

class EEATAnalyzer:
    def __init__(self, fetcher):
        self.fetcher = fetcher
        self.text = fetcher.get_text_content()
        self.html = fetcher.html_content
        
    def analyze(self):
        """Run all E-E-A-T analyses"""
        scores = {
            'expertise_experience': self._analyze_expertise_experience(),
            'authoritativeness': self._analyze_authoritativeness(),
            'trustworthiness': self._analyze_trustworthiness(),
            'factual_accuracy': self._analyze_factual_accuracy()
        }
        
        findings = self._generate_findings(scores)
        recommendations = self._generate_recommendations(scores)
        
        return {
            'scores': scores,
            'findings': findings,
            'recommendations': recommendations
        }
    
    def _analyze_expertise_experience(self):
        """Analyze expertise and experience signals"""
        score = 0
        
        # Check for author information
        author_patterns = ['author', 'written by', 'by:', 'posted by']
        has_author = any(pattern in self.text.lower() for pattern in author_patterns)
        if has_author:
            score += 25
        
        # Check for credentials
        credential_patterns = ['phd', 'md', 'certified', 'expert', 'specialist', 'professor', 'dr.']
        has_credentials = any(pattern in self.text.lower() for pattern in credential_patterns)
        if has_credentials:
            score += 25
        
        # Check for first-person experience
        experience_patterns = ['i have', 'we have', 'my experience', 'our experience', 'i worked']
        has_experience = any(pattern in self.text.lower() for pattern in experience_patterns)
        if has_experience:
            score += 25
        
        # Check for case studies or examples
        example_patterns = ['case study', 'for example', 'in our case', 'we found that']
        has_examples = any(pattern in self.text.lower() for pattern in example_patterns)
        if has_examples:
            score += 25
        
        return score
    
    def _analyze_authoritativeness(self):
        """Analyze authoritativeness signals"""
        score = 0
        
        # Check for external citations
        links = self.fetcher.get_links()
        external_links = len(links['external'])
        if external_links > 0:
            score += min(40, external_links * 5)
        
        # Check for authoritative sources
        authoritative_domains = ['.gov', '.edu', '.org']
        authoritative_links = sum(1 for link in links['external'] 
                                 if any(domain in link for domain in authoritative_domains))
        if authoritative_links > 0:
            score += min(30, authoritative_links * 10)
        
        # Check for awards or recognition
        recognition_patterns = ['award', 'recognized', 'featured in', 'published in']
        has_recognition = any(pattern in self.text.lower() for pattern in recognition_patterns)
        if has_recognition:
            score += 30
        
        return min(100, score)
    
    def _analyze_trustworthiness(self):
        """Analyze trustworthiness signals"""
        score = 0
        
        # Check for HTTPS
        if self.fetcher.url.startswith('https://'):
            score += 20
        
        # Check for contact information
        contact_patterns = ['contact', 'email', '@', 'phone', 'address']
        has_contact = any(pattern in self.text.lower() for pattern in contact_patterns)
        if has_contact:
            score += 20
        
        # Check for privacy policy
        if 'privacy' in self.text.lower():
            score += 15
        
        # Check for about page indicators
        if 'about us' in self.text.lower() or 'about' in self.text.lower():
            score += 15
        
        # Check for citations and references
        citation_patterns = ['according to', 'source:', 'reference', 'cited', 'study shows']
        citation_count = sum(self.text.lower().count(pattern) for pattern in citation_patterns)
        if citation_count > 0:
            score += min(30, citation_count * 10)
        
        return min(100, score)
    
    def _analyze_factual_accuracy(self):
        """Analyze factual accuracy indicators"""
        score = 50  # Base score
        
        # Check for dates (indicates currency)
        dates = re.findall(r'\b20\d{2}\b', self.text)
        if dates:
            score += 20
        
        # Check for data and statistics
        statistics = len(re.findall(r'\b\d+\.?\d*\s*(percent|%)\b', self.text, re.IGNORECASE))
        if statistics > 0:
            score += min(20, statistics * 5)
        
        # Check for citations
        if '[' in self.text and ']' in self.text:
            score += 10
        
        return min(100, score)
    
    def _generate_findings(self, scores):
        """Generate key findings"""
        findings = []
        
        if scores['expertise_experience'] < 30:
            findings.append("Limited demonstration of expertise and experience")
        
        if scores['authoritativeness'] < 30:
            findings.append("Authoritativeness signals need improvement")
        
        if scores['trustworthiness'] < 50:
            findings.append("Trustworthiness and transparency need improvement")
        
        return findings
    
    def _generate_recommendations(self, scores):
        """Generate recommendations"""
        recommendations = []
        
        if scores['expertise_experience'] < 50:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Strengthen expertise and experience signals',
                'details': [
                    'Add author credentials and detailed bios',
                    'Include industry-specific experience details',
                    'Highlight relevant qualifications and certifications',
                    'Showcase first-hand experience with case studies',
                    'Demonstrate deep subject matter knowledge'
                ]
            })
        
        if scores['authoritativeness'] < 50:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Enhance authoritativeness and recognition',
                'details': [
                    'Build domain authority through quality backlinks',
                    'Gain industry recognition and awards',
                    'Establish thought leadership through original research',
                    'Get cited by authoritative sources',
                    'Build strong brand presence in your niche'
                ]
            })
        
        if scores['trustworthiness'] < 70:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Improve trustworthiness and transparency',
                'details': [
                    'Add comprehensive citations and sources',
                    'Include clear contact information',
                    'Add privacy policies and terms of service',
                    'Provide business verification details',
                    'Include transparent pricing and policies'
                ]
            })
        
        return recommendations
