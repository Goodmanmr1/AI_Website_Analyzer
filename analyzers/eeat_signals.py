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
        """Generate detailed, actionable findings - ENHANCED"""
        findings = []
        
        # EXPERTISE & EXPERIENCE
        author_patterns = ['author', 'written by', 'by:', 'posted by']
        has_author = any(pattern in self.text.lower() for pattern in author_patterns)
        
        credential_patterns = ['phd', 'md', 'certified', 'expert', 'specialist', 'professor', 'dr.']
        has_credentials = any(pattern in self.text.lower() for pattern in credential_patterns)
        
        experience_patterns = ['i have', 'we have', 'my experience', 'our experience', 'i worked']
        has_experience = any(pattern in self.text.lower() for pattern in experience_patterns)
        
        example_patterns = ['case study', 'for example', 'in our case', 'we found that']
        has_examples = any(pattern in self.text.lower() for pattern in example_patterns)
        
        expertise_signals = []
        if has_author:
            expertise_signals.append("author attribution")
        if has_credentials:
            expertise_signals.append("professional credentials")
        if has_experience:
            expertise_signals.append("first-hand experience")
        if has_examples:
            expertise_signals.append("case studies/examples")
        
        if scores['expertise_experience'] < 30:
            findings.append(f"✗ Very limited expertise signals - only {len(expertise_signals)} of 4 indicators present")
        elif scores['expertise_experience'] < 60:
            findings.append(f"⚠ Moderate expertise demonstration - found: {', '.join(expertise_signals) if expertise_signals else 'none'}")
        else:
            findings.append(f"✓ Strong expertise signals - {len(expertise_signals)}/4 indicators: {', '.join(expertise_signals)}")
        
        # AUTHORITATIVENESS
        links = self.fetcher.get_links()
        external_links = len(links['external'])
        
        authoritative_domains = ['.gov', '.edu', '.org']
        authoritative_links = sum(1 for link in links['external'] 
                                 if any(domain in link for domain in authoritative_domains))
        
        recognition_patterns = ['award', 'recognized', 'featured in', 'published in']
        has_recognition = any(pattern in self.text.lower() for pattern in recognition_patterns)
        
        if scores['authoritativeness'] < 30:
            findings.append(f"✗ Low authoritativeness - {external_links} external links, {authoritative_links} to authoritative domains (.gov/.edu/.org)")
        elif scores['authoritativeness'] < 60:
            findings.append(f"⚠ Moderate authoritativeness - {external_links} external links ({authoritative_links} authoritative), {'with' if has_recognition else 'no'} recognition indicators")
        else:
            findings.append(f"✓ Strong authoritativeness - {external_links} external links, {authoritative_links} to trusted domains, {'' if has_recognition else 'no '}industry recognition")
        
        # TRUSTWORTHINESS
        is_https = self.fetcher.url.startswith('https://')
        
        contact_patterns = ['contact', 'email', '@', 'phone', 'address']
        has_contact = any(pattern in self.text.lower() for pattern in contact_patterns)
        
        has_privacy = 'privacy' in self.text.lower()
        has_about = 'about us' in self.text.lower() or 'about' in self.text.lower()
        
        citation_patterns = ['according to', 'source:', 'reference', 'cited', 'study shows']
        citation_count = sum(self.text.lower().count(pattern) for pattern in citation_patterns)
        
        trust_signals = []
        if is_https:
            trust_signals.append("HTTPS encryption")
        if has_contact:
            trust_signals.append("contact information")
        if has_privacy:
            trust_signals.append("privacy policy")
        if has_about:
            trust_signals.append("about page")
        if citation_count > 0:
            trust_signals.append(f"{citation_count} citations")
        
        if scores['trustworthiness'] < 50:
            findings.append(f"✗ Limited trustworthiness signals - only {len(trust_signals)}/5 indicators: {', '.join(trust_signals) if trust_signals else 'none detected'}")
        elif scores['trustworthiness'] < 70:
            findings.append(f"⚠ Moderate trust signals - {len(trust_signals)}/5 present: {', '.join(trust_signals)}")
        else:
            findings.append(f"✓ Strong trustworthiness - {len(trust_signals)}/5 indicators: {', '.join(trust_signals)}")
        
        # FACTUAL ACCURACY
        dates = re.findall(r'\b20\d{2}\b', self.text)
        recent_dates = [d for d in dates if int(d) >= 2023]
        
        statistics = len(re.findall(r'\b\d+\.?\d*\s*(percent|%)\b', self.text, re.IGNORECASE))
        has_citations = '[' in self.text and ']' in self.text
        
        if scores['factual_accuracy'] < 50:
            findings.append(f"✗ Low factual accuracy indicators - {len(recent_dates)} recent dates, {statistics} statistics, {'with' if has_citations else 'no'} citation brackets")
        elif scores['factual_accuracy'] < 70:
            findings.append(f"⚠ Moderate factual support - {len(dates)} date references ({len(recent_dates)} recent), {statistics} statistical claims")
        else:
            findings.append(f"✓ Strong factual support - {len(dates)} dates ({len(recent_dates)} recent), {statistics} statistics, {'' if has_citations else 'no '}citation format")
        
        # OVERALL E-E-A-T ASSESSMENT
        avg_score = sum(scores.values()) / len(scores)
        if avg_score < 40:
            findings.append("⚠ CRITICAL: Overall E-E-A-T score is very low - this significantly impacts AI and search visibility")
        elif avg_score < 60:
            findings.append("⚠ Overall E-E-A-T needs improvement - focus on adding expertise credentials and trust signals")
        
        return findings
    
    def _generate_recommendations(self, scores):
        """Generate detailed, prioritized recommendations - ENHANCED"""
        recommendations = []
        
        if scores['expertise_experience'] < 50:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Strengthen expertise and experience signals',
                'details': [
                    'Add detailed author bio with credentials (education, certifications, years of experience)',
                    'Include professional headshots and LinkedIn profiles for content authors',
                    'Showcase industry-specific expertise with portfolio or case study examples',
                    'Use first-person narrative to demonstrate hands-on experience ("In my 10 years...", "We tested...")',
                    'Add "About the Author" sections with relevant qualifications',
                    'Display team credentials on About page with specific expertise areas',
                    'Include awards, certifications, or professional memberships',
                    'Show years of experience or projects completed in your field'
                ]
            })
        
        if scores['authoritativeness'] < 50:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Build authoritativeness and industry recognition',
                'details': [
                    'Link to authoritative sources (.gov, .edu, peer-reviewed journals) when making claims',
                    'Get featured in or cited by industry publications - actively pitch guest posts',
                    'Display media mentions, press coverage, or "As Featured In" badges',
                    'Build relationships with established industry websites for backlinks',
                    'Create original research or data studies that others will cite',
                    'Pursue speaking engagements, webinars, or conference presentations',
                    'Apply for industry awards or "best of" lists in your niche',
                    'Partner with recognized brands or institutions in your field',
                    'Publish white papers or in-depth guides that demonstrate thought leadership'
                ]
            })
        
        if scores['trustworthiness'] < 70:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Improve trustworthiness and transparency',
                'details': [
                    'Add comprehensive contact page with multiple contact methods (email, phone, address, form)',
                    'Display physical business address and phone number in footer (for local businesses)',
                    'Create detailed "About Us" page explaining company history, mission, and team',
                    'Implement clear privacy policy and terms of service pages',
                    'Add trust badges: SSL certificate, payment security, industry certifications',
                    'Include customer testimonials with real names and photos (with permission)',
                    'Display refund/return policies clearly for e-commerce',
                    'Show business registration, licenses, or accreditation information',
                    'Add "Last Updated" dates to content to show currency',
                    'Include editorial policy or content standards documentation',
                    'Link to social media profiles to demonstrate active presence',
                    'Display customer reviews from verified platforms (Google, Trustpilot)'
                ]
            })
        
        if scores['factual_accuracy'] < 60:
            recommendations.append({
                'priority': 'MEDIUM',
                'title': 'Enhance factual accuracy and citation quality',
                'details': [
                    'Add inline citations for all factual claims and statistics',
                    'Include publication dates on all content ("Published: Jan 15, 2025")',
                    'Link to original data sources when citing statistics or research',
                    'Use numbered footnotes or reference sections for academic-style citations',
                    'Add "Last Reviewed" or "Medically Reviewed" dates for health content',
                    'Include methodology explanations for original research or data',
                    'Fact-check content against multiple authoritative sources',
                    'Update outdated statistics and information regularly',
                    'Add data visualizations (charts/graphs) for complex statistics',
                    'Include expert quotes with full attribution and credentials'
                ]
            })
        
        # Add specific quick wins based on what's missing
        quick_wins = []
        
        if not self.fetcher.url.startswith('https://'):
            quick_wins.append('Migrate to HTTPS immediately - this is a critical trust factor')
        
        if 'privacy' not in self.text.lower():
            quick_wins.append('Add a privacy policy page - required for GDPR and builds trust')
        
        author_patterns = ['author', 'written by', 'by:', 'posted by']
        if not any(pattern in self.text.lower() for pattern in author_patterns):
            quick_wins.append('Add author bylines to all content - even if it\'s just "By [Company Name] Team"')
        
        if quick_wins:
            recommendations.append({
                'priority': 'QUICK WIN',
                'title': 'Immediate E-E-A-T improvements (implement today)',
                'details': quick_wins
            })
        
        return recommendations
