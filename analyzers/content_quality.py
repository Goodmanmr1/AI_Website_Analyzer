"""Content Quality Analysis"""

import re
import config

class ContentQualityAnalyzer:
    def __init__(self, fetcher):
        self.fetcher = fetcher
        self.text = fetcher.get_text_content()
        self.word_count = len(self.text.split())
        
    def analyze(self):
        """Run all content quality analyses"""
        scores = {
            'long_tail_keywords': self._analyze_long_tail_keywords(),
            'comprehensive_coverage': self._analyze_comprehensive_coverage(),
            'user_intent': self._analyze_user_intent(),
            'accuracy_currency': self._analyze_accuracy_currency(),
            'natural_language': self._analyze_natural_language()
        }
        
        findings = self._generate_findings(scores)
        recommendations = self._generate_recommendations(scores)
        
        return {
            'scores': scores,
            'findings': findings,
            'recommendations': recommendations
        }
    
    def _analyze_long_tail_keywords(self):
        """Analyze presence of long-tail keywords"""
        if not self.text:
            return 0
        
        # Find phrases of 3+ words
        words = self.text.lower().split()
        three_word_phrases = []
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            # Check if phrase contains meaningful words (not just stop words)
            if len(phrase) > 10:
                three_word_phrases.append(phrase)
        
        # Score based on long-tail phrase density
        if self.word_count == 0:
            return 0
        
        phrase_density = (len(three_word_phrases) / self.word_count) * 100
        score = min(100, phrase_density * 20)
        
        return round(score)
    
    def _analyze_comprehensive_coverage(self):
        """Analyze content comprehensiveness"""
        score = 0
        
        # Word count (ideal: 1500+)
        if self.word_count >= config.IDEAL_WORD_COUNT:
            score += 40
        elif self.word_count >= config.MIN_WORD_COUNT:
            score += (self.word_count / config.IDEAL_WORD_COUNT) * 40
        else:
            score += (self.word_count / config.MIN_WORD_COUNT) * 20
        
        # Check for various content types
        if self.fetcher.soup.find_all(['ul', 'ol']):
            score += 15
        
        if self.fetcher.soup.find_all('table'):
            score += 15
        
        # Check for images
        images = self.fetcher.get_images()
        if images:
            score += 15
        
        # Check for headings (indicates structure)
        headings = self.fetcher.get_headings()
        total_headings = sum(len(h) for h in headings.values())
        if total_headings >= 5:
            score += 15
        elif total_headings >= 3:
            score += 10
        
        return round(min(100, score))
    
    def _analyze_user_intent(self):
        """Analyze alignment with user intent"""
        # This is a simplified heuristic
        score = 0
        
        # Check for actionable content
        action_words = ['how to', 'guide', 'tutorial', 'steps', 'learn', 'tips']
        has_action = any(word in self.text.lower() for word in action_words)
        if has_action:
            score += 30
        
        # Check for informational content
        info_words = ['what is', 'definition', 'meaning', 'about', 'overview']
        has_info = any(word in self.text.lower() for word in info_words)
        if has_info:
            score += 30
        
        # Check for examples
        if 'example' in self.text.lower() or 'for instance' in self.text.lower():
            score += 20
        
        # Check for clear structure
        headings = self.fetcher.get_headings()
        if sum(len(h) for h in headings.values()) >= 3:
            score += 20
        
        return min(100, score)
    
    def _analyze_accuracy_currency(self):
        """Analyze accuracy and currency indicators"""
        score = 0
        
        # Check for dates
        current_year = 2025
        recent_years = [str(year) for year in range(current_year - 2, current_year + 1)]
        has_recent_date = any(year in self.text for year in recent_years)
        if has_recent_date:
            score += 30
        
        # Check for "updated" or "published" indicators
        date_indicators = ['updated', 'published', 'last modified', 'revised']
        has_date_indicator = any(indicator in self.text.lower() for indicator in date_indicators)
        if has_date_indicator:
            score += 20
        
        # Check for author information
        if 'author' in self.text.lower() or 'written by' in self.text.lower():
            score += 20
        
        # Check for sources/citations
        citation_patterns = ['source:', 'according to', 'study', 'research']
        has_citations = any(pattern in self.text.lower() for pattern in citation_patterns)
        if has_citations:
            score += 30
        
        return min(100, score)
    
    def _analyze_natural_language(self):
        """Analyze natural language quality"""
        if self.word_count < 50:
            return 0
        
        score = 70  # Base score
        
        # Check sentence variety (average sentence length)
        sentences = re.split(r'[.!?]+', self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            
            # Ideal: 15-20 words per sentence
            if 15 <= avg_sentence_length <= 20:
                score += 30
            elif 10 <= avg_sentence_length <= 25:
                score += 20
            else:
                score += 10
        
        return min(100, score)
    
    def _generate_findings(self, scores):
        """Generate key findings"""
        findings = []
        
        if scores['comprehensive_coverage'] < 50:
            findings.append("Content lacks comprehensive coverage of the topic")
        
        if scores['user_intent'] < 50:
            findings.append("Content may not fully address user search intent")
        
        if scores['accuracy_currency'] < 50:
            findings.append("Content lacks indicators of accuracy and currency")
        
        return findings
    
    def _generate_recommendations(self, scores):
        """Generate recommendations"""
        recommendations = []
        
        if scores['comprehensive_coverage'] < 70:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Expand content to provide comprehensive topic coverage',
                'details': [
                    'Aim for 1500+ words for pillar content',
                    'Include background information and context',
                    'Add step-by-step guides and how-tos',
                    'Include examples and case studies',
                    'Provide actionable takeaways',
                    'Answer related questions and subtopics'
                ]
            })
        
        if scores['user_intent'] < 70:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Better align content with user search intent',
                'details': [
                    'Analyze search intent for target keywords',
                    'Include practical examples and advice',
                    'Answer common user questions directly',
                    'Use Google\'s "People also ask" for insights',
                    'Match content format to intent (informational, transactional, etc.)'
                ]
            })
        
        if scores['accuracy_currency'] < 70:
            recommendations.append({
                'priority': 'MEDIUM',
                'title': 'Add credibility and freshness indicators',
                'details': [
                    'Include publication and last updated dates',
                    'Add author information and credentials',
                    'Cite authoritative sources with links',
                    'Include expert quotes and statistics',
                    'Add references and footnotes where appropriate'
                ]
            })
        
        return recommendations
