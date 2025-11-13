"""AI Optimization Analysis"""

import re
from textstat import flesch_reading_ease

class AIOptimizationAnalyzer:
    def __init__(self, fetcher):
        self.fetcher = fetcher
        self.text = fetcher.get_text_content()
        self.word_count = len(self.text.split())
        
    def analyze(self):
        """Run all AI optimization analyses"""
        scores = {
            'chunkability': self._analyze_chunkability(),
            'qa_format': self._analyze_qa_format(),
            'entity_recognition': self._analyze_entity_recognition(),
            'factual_density': self._analyze_factual_density(),
            'semantic_clarity': self._analyze_semantic_clarity(),
            'content_structure': self._analyze_content_structure(),
            'contextual_relevance': self._analyze_contextual_relevance()
        }
        
        findings = self._generate_findings(scores)
        recommendations = self._generate_recommendations(scores)
        
        return {
            'scores': scores,
            'findings': findings,
            'recommendations': recommendations
        }
    
    def _analyze_chunkability(self):
        """Analyze content chunkability for AI processing"""
        # Use HTML paragraph tags instead of text splitting
        paragraphs = self.fetcher.soup.find_all('p')
        
        if not paragraphs:
            return 0
        
        # Ideal paragraph length: 50-150 words
        ideal_chunks = 0
        for para in paragraphs:
            text = para.get_text(strip=True)
            word_count = len(text.split())
            if 50 <= word_count <= 150:
                ideal_chunks += 1
        
        score = (ideal_chunks / len(paragraphs)) * 100
        return round(score)
    
    def _analyze_qa_format(self):
        """Analyze Q&A format optimization - IMPROVED for content type awareness"""
        if not self.text:
            return 0
        
        questions = self.text.count('?')
        
        # IMPROVED: Recognize different content types
        headings = self.fetcher.get_headings()
        h2_count = len(headings.get('h2', []))
        has_sections = h2_count >= 5
        is_long_form = self.word_count > 1500
        
        # Encyclopedic/informational content (like Wikipedia)
        # These are valuable for AI without explicit Q&A format
        if is_long_form and has_sections:
            # For encyclopedic content, Q&A is a bonus, not required
            if questions == 0:
                return 70  # Still excellent for AI (factual, structured)
            elif questions < 5:
                return 80  # Some questions enhance it
            elif questions < 20:
                return 90  # Good mix of questions
            else:
                return 95  # Excellent Q&A integration
        
        # Short-form or unstructured content needs Q&A more
        else:
            if questions == 0:
                return 5  # Missing opportunity for engagement
            
            # Calculate questions per 100 words
            questions_per_100 = (questions / max(self.word_count, 1)) * 100
            
            # Scoring: 2-5 questions per 100 words is ideal for short content
            if 2 <= questions_per_100 <= 5:
                score = 100
            elif questions_per_100 < 2:
                score = min(90, questions_per_100 * 50)
            else:
                # Too many questions can be overwhelming
                score = max(60, 100 - (questions_per_100 - 5) * 10)
            
            return round(score)
    
    def _analyze_entity_recognition(self):
        """Analyze entity recognition potential"""
        if not self.text:
            return 0
        
        # Simple entity detection patterns
        # Capitalized words (potential proper nouns)
        capitalized = len(re.findall(r'\b[A-Z][a-z]+\b', self.text))
        
        # Numbers and dates
        numbers = len(re.findall(r'\b\d+\b', self.text))
        
        # URLs and emails
        urls = len(re.findall(r'https?://\S+', self.text))
        emails = len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', self.text))
        
        total_entities = capitalized + numbers + urls + emails
        
        # Score based on entity density per 100 words
        entity_density = (total_entities / max(self.word_count, 1)) * 100
        score = min(100, entity_density * 10)
        return round(score, 1)
    
    def _analyze_factual_density(self):
        """Analyze factual density (facts per content) - FIXED"""
        if not self.text or self.word_count < 50:
            return 0
        
        # CRITICAL FIX #4: Filter out non-factual numbers
        text_cleaned = self.text
        
        # Remove copyright years (e.g., "© 2024", "Copyright 2023")
        text_cleaned = re.sub(r'©\s*20\d{2}', '', text_cleaned)
        text_cleaned = re.sub(r'\b(copyright|©)\s+20\d{2}\b', '', text_cleaned, flags=re.IGNORECASE)
        
        # Remove common non-factual small numbers (1-10) when used as list items or standalone
        text_cleaned = re.sub(r'\b([1-9]|10)\.\s', '', text_cleaned)  # List items like "1. "
        
        # Remove navigation/pagination numbers
        text_cleaned = re.sub(r'\b(page|step)\s+\d+\b', '', text_cleaned, flags=re.IGNORECASE)
        
        # Now count meaningful numbers (2+ digits or percentages)
        meaningful_numbers = len(re.findall(r'\b\d{2,}\.?\d*%?\b', text_cleaned))
        
        # Count dates more carefully (4-digit years, but not in URLs or standalone)
        dates = len(re.findall(r'\b(19|20)\d{2}\b(?!\s*©)', text_cleaned))
        
        # Count statistics (numbers with context)
        statistics = len(re.findall(r'\b\d+\.?\d*\s*(percent|%|million|billion|thousand|dozen)\b', text_cleaned, re.IGNORECASE))
        
        # Count currency/prices
        currency = len(re.findall(r'[$€£¥]\s*\d+', text_cleaned))
        
        total_facts = meaningful_numbers + dates + statistics + currency
        
        # Facts per 100 words
        facts_per_100 = (total_facts / max(self.word_count, 1)) * 100
        
        # IMPROVED: More nuanced scoring
        # Ideal is 3-12 facts per 100 words (adjusted from original)
        if 3 <= facts_per_100 <= 12:
            score = 100
        elif facts_per_100 < 3:
            # Scale linearly from 0 to 100
            score = (facts_per_100 / 3) * 100
        else:
            # Gentle penalty for being too data-heavy
            score = max(60, 100 - (facts_per_100 - 12) * 3)
        
        return round(score, 2)
    
    def _analyze_semantic_clarity(self):
        """Analyze semantic clarity using readability - FIXED error handling"""
        if not self.text or self.word_count < 100:
            return 0
        
        # CRITICAL FIX #5: Better error handling for readability
        try:
            # Clean the text before analysis
            # Remove URLs which can confuse readability scores
            text_for_analysis = re.sub(r'https?://\S+', '', self.text)
            
            # Remove excessive whitespace
            text_for_analysis = ' '.join(text_for_analysis.split())
            
            # Ensure we have enough sentences
            sentences = re.split(r'[.!?]+', text_for_analysis)
            sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
            
            if len(sentences) < 3:
                # Not enough sentences for reliable analysis
                return 50
            
            # Flesch Reading Ease: 60-70 is ideal (8th-9th grade)
            reading_ease = flesch_reading_ease(text_for_analysis)
            
            # Convert to 0-100 score (60-70 = 100, outside range = lower)
            if 60 <= reading_ease <= 70:
                score = 100
            elif reading_ease < 60:
                # Harder to read
                score = max(0, (reading_ease / 60) * 100)
            else:
                # Too easy/simple
                score = max(50, 100 - (reading_ease - 70))
            
            return round(score, 2)
            
        except ZeroDivisionError:
            # Happens when text is too short or has no sentences
            return 40
        except ValueError as e:
            # Happens with unusual text patterns
            print(f"Readability calculation error: {e}")
            return 50
        except Exception as e:
            # Catch-all for other issues
            print(f"Unexpected readability error: {e}")
            # Return a neutral score rather than failing
            return 50
    
    def _analyze_content_structure(self):
        """Analyze content structure for AI"""
        score = 100
        
        # Check for lists
        if not self.fetcher.soup.find_all(['ul', 'ol']):
            score -= 20
        
        # Check for tables
        if not self.fetcher.soup.find_all('table'):
            score -= 20
        
        # Check for clear sections (headings)
        headings = self.fetcher.get_headings()
        total_headings = sum(len(h) for h in headings.values())
        if total_headings < 3:
            score -= 30
        
        # Check for semantic HTML
        semantic_tags = ['article', 'section', 'aside', 'nav', 'header', 'footer']
        has_semantic = any(self.fetcher.soup.find_all(tag) for tag in semantic_tags)
        if not has_semantic:
            score -= 30
        
        return max(0, score)
    
    def _analyze_contextual_relevance(self):
        """Analyze contextual relevance"""
        if not self.text:
            return 0
        
        # Simple keyword density check
        words = self.text.lower().split()
        if not words:
            return 0
        
        # Count unique words vs total words (lexical diversity)
        unique_words = len(set(words))
        lexical_diversity = (unique_words / len(words)) * 100
        
        # Ideal lexical diversity: 40-60%
        if 40 <= lexical_diversity <= 60:
            score = 100
        elif lexical_diversity < 40:
            score = (lexical_diversity / 40) * 100
        else:
            score = max(50, 100 - (lexical_diversity - 60))
        
        return round(score)
    
    def _generate_findings(self, scores):
        """Generate key findings with specific details"""
        findings = []
        
        # Chunkability with details
        paragraphs = self.fetcher.soup.find_all('p')
        if paragraphs:
            ideal_count = sum(1 for p in paragraphs if 50 <= len(p.get_text(strip=True).split()) <= 150)
            if scores['chunkability'] < 50:
                findings.append(f"Only {ideal_count} of {len(paragraphs)} paragraphs ({scores['chunkability']}%) are in the ideal 50-150 word range for AI processing")
            else:
                findings.append(f"Good: {ideal_count} of {len(paragraphs)} paragraphs ({scores['chunkability']}%) are optimally sized for AI")
        
        # Q&A format - context-aware findings
        question_count = self.text.count('?')
        headings = self.fetcher.get_headings()
        h2_count = len(headings.get('h2', []))
        is_long_form = self.word_count > 1500
        
        if scores['qa_format'] < 30:
            findings.append(f"Limited Q&A format: Found only {question_count} questions in {self.word_count} words")
        elif scores['qa_format'] >= 70 and is_long_form and h2_count >= 5:
            # Recognize well-structured encyclopedic content
            findings.append(f"Good: Well-structured informational content with {question_count} questions across {self.word_count} words - excellent for AI knowledge extraction")
        
        # Semantic clarity
        if scores['semantic_clarity'] < 70:
            findings.append(f"Readability score: {scores['semantic_clarity']}% - content may be too complex or too simple for AI processing")
        
        # Factual density
        if scores['factual_density'] < 50:
            findings.append(f"Low factual density ({scores['factual_density']}%) - add more specific data, statistics, and dates")
        elif scores['factual_density'] > 90:
            findings.append(f"Excellent factual density ({scores['factual_density']}%) - rich in data and statistics")
        
        return findings
    
    def _generate_recommendations(self, scores):
        """Generate recommendations"""
        recommendations = []
        
        if scores['semantic_clarity'] < 70:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Improve semantic structure for AI processing',
                'details': [
                    'Use proper heading hierarchy (H1-H6)',
                    'Implement schema markup',
                    'Structure content with clear sections',
                    'Use descriptive link text',
                    'Add structured data for key information'
                ]
            })
        
        if scores['qa_format'] < 30:
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Optimize content for answer potential',
                'details': [
                    'Structure content with clear Q&A format',
                    'Include specific, factual information',
                    'Use bullet points and numbered lists',
                    'Add FAQ sections with direct answers',
                    'Include data and statistics'
                ]
            })
        
        if scores['chunkability'] < 50:
            recommendations.append({
                'priority': 'MEDIUM',
                'title': 'Improve content chunkability',
                'details': [
                    'Break long paragraphs into 50-150 word chunks',
                    'Use clear section breaks',
                    'Add subheadings every 200-300 words',
                    'Use lists for scannable content'
                ]
            })
        
        return recommendations
