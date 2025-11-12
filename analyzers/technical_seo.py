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
        
        # JSON-LD presence (check length, not just truthiness)
        if schemas.get('json_ld') and len(schemas['json_ld']) > 0:
            score += 50
        
        # Microdata presence
        if schemas.get('microdata') and len(schemas['microdata']) > 0:
            score += 50
        
        return score
    
    def _generate_findings(self, scores):
        """Generate detailed findings with specific metrics"""
        findings = []
        
        # Heading structure with detailed breakdown
        headings = self.fetcher.get_headings()
        h1_count = len(headings['h1'])
        h2_count = len(headings['h2'])
        h3_count = len(headings['h3'])
        total_headings = sum(len(h) for h in headings.values())
        
        if h1_count == 0:
            findings.append(f"✗ Missing H1 tag - found {total_headings} total headings (H2: {h2_count}, H3: {h3_count}) but no H1")
        elif h1_count > 1:
            findings.append(f"✗ Multiple H1 tags ({h1_count}) detected - should have exactly one H1 per page")
        elif h1_count == 1 and total_headings >= 5:
            findings.append(f"✓ Excellent heading structure: 1 H1, {h2_count} H2s, {h3_count} H3s ({total_headings} total)")
        elif h1_count == 1:
            findings.append(f"⚠ Has H1 but limited heading structure - only {total_headings} headings total (add more H2/H3 for better organization)")
        
        # Meta information with specific details
        title = self.fetcher.get_title()
        meta_desc = self.fetcher.get_meta_description()
        
        if not title:
            findings.append("✗ Missing page title - critical for SEO and AI understanding")
        elif len(title) < 30:
            findings.append(f"✗ Title too short ({len(title)} chars) - expand to 30-60 chars for better SEO")
        elif len(title) > 60:
            findings.append(f"⚠ Title too long ({len(title)} chars) - may be truncated in search results (ideal: 30-60 chars)")
        else:
            findings.append(f"✓ Title length optimal ({len(title)} chars)")
        
        if not meta_desc:
            findings.append("✗ Missing meta description - add 150-160 char summary for search snippets")
        elif len(meta_desc) < 120:
            findings.append(f"✗ Meta description too short ({len(meta_desc)} chars) - expand to 150-160 chars")
        elif len(meta_desc) > 160:
            findings.append(f"⚠ Meta description too long ({len(meta_desc)} chars) - may be truncated (ideal: 150-160 chars)")
        else:
            findings.append(f"✓ Meta description length optimal ({len(meta_desc)} chars)")
        
        # Schema markup with detailed analysis
        schemas = self.fetcher.get_schema_markup()
        json_ld_count = len(schemas.get('json_ld', []))
        microdata_count = len(schemas.get('microdata', []))
        
        if json_ld_count == 0 and microdata_count == 0:
            findings.append("✗ No structured data found - add JSON-LD schema for better AI and search understanding")
        elif json_ld_count > 0 and microdata_count > 0:
            findings.append(f"✓ Excellent: {json_ld_count} JSON-LD + {microdata_count} Microdata schemas implemented")
        elif json_ld_count > 0:
            findings.append(f"✓ Good: {json_ld_count} JSON-LD schema block(s) found (preferred format for AI)")
        elif microdata_count > 0:
            findings.append(f"⚠ Using {microdata_count} Microdata schema(s) - consider upgrading to JSON-LD for better AI compatibility")
        
        # Alt text with detailed breakdown
        images = self.fetcher.get_images()
        if images:
            images_with_alt = sum(1 for img in images if img['has_alt'])
            decorative = sum(1 for img in images if img.get('is_decorative', False))
            missing_alt = len(images) - images_with_alt
            
            if images_with_alt == len(images):
                findings.append(f"✓ Perfect image accessibility: all {len(images)} images have alt attributes ({decorative} decorative)")
            elif images_with_alt / len(images) >= 0.8:
                findings.append(f"⚠ Good image accessibility: {images_with_alt}/{len(images)} images have alt attributes ({missing_alt} missing, {decorative} decorative)")
            else:
                findings.append(f"✗ Poor image accessibility: only {images_with_alt}/{len(images)} images have alt attributes ({missing_alt} missing)")
        else:
            findings.append("✓ No images on page (no alt text issues)")
        
        # Link analysis
        links = self.fetcher.get_links()
        internal_count = len(links['internal'])
        external_count = len(links['external'])
        total_links = internal_count + external_count
        
        if total_links == 0:
            findings.append("✗ No links found - add internal and external links for better SEO")
        elif internal_count == 0:
            findings.append(f"✗ No internal links - add links to other pages on your site ({external_count} external links found)")
        elif external_count == 0:
            findings.append(f"⚠ No external links - consider linking to authoritative sources ({internal_count} internal links found)")
        elif internal_count > external_count * 2:
            findings.append(f"✓ Good link balance: {internal_count} internal, {external_count} external links")
        else:
            findings.append(f"⚠ Link balance: {internal_count} internal, {external_count} external - consider more internal linking")
        
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
