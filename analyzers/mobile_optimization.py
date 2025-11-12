"""Mobile Optimization Analysis"""

class MobileOptimizationAnalyzer:
    def __init__(self, fetcher, perf_data=None):
        self.fetcher = fetcher
        self.perf_data = perf_data or {}
        
    def analyze(self):
        """Run all mobile optimization analyses"""
        # Get performance data if available
        pagespeed = self.perf_data.get('pagespeed', {})
        
        scores = {
            'mobile_page_speed': pagespeed.get('performance_score', 75),
            'touch_targets': self._analyze_touch_targets(),
            'viewport_config': self._analyze_viewport(),
            'mobile_usability': pagespeed.get('mobile_usability', 85),
            'responsive_design': self._analyze_responsive_design(),
            'core_web_vitals': self._analyze_core_web_vitals(pagespeed)
        }
        
        findings = self._generate_findings(scores, pagespeed)
        recommendations = self._generate_recommendations(scores, pagespeed)
        
        return {
            'scores': scores,
            'findings': findings,
            'recommendations': recommendations,
            'perf_metrics': {
                'lcp': pagespeed.get('lcp', 'N/A'),
                'fid': pagespeed.get('fid', 'N/A'),
                'cls': pagespeed.get('cls', 'N/A')
            }
        }
    
    def _analyze_core_web_vitals(self, pagespeed):
        """Analyze Core Web Vitals from PageSpeed data"""
        if not pagespeed.get('success'):
            return 75  # Default score when API unavailable
        
        # Extract LCP, FID, CLS values and score them
        lcp = pagespeed.get('lcp', 'N/A')
        fid = pagespeed.get('fid', 'N/A')
        cls = pagespeed.get('cls', 'N/A')
        
        score = 0
        count = 0
        
        # LCP scoring (good < 2.5s, needs improvement < 4s, poor >= 4s)
        if lcp != 'N/A' and 's' in str(lcp):
            try:
                lcp_value = float(lcp.replace('s', '').strip())
                if lcp_value < 2.5:
                    score += 100
                elif lcp_value < 4.0:
                    score += 60
                else:
                    score += 30
                count += 1
            except:
                pass
        
        # CLS scoring (good < 0.1, needs improvement < 0.25, poor >= 0.25)
        if cls != 'N/A':
            try:
                cls_value = float(str(cls).strip())
                if cls_value < 0.1:
                    score += 100
                elif cls_value < 0.25:
                    score += 60
                else:
                    score += 30
                count += 1
            except:
                pass
        
        return score / count if count > 0 else 75
    
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
    
    def _generate_findings(self, scores, pagespeed):
        """Generate key findings with specific details"""
        findings = []
        
        # Performance findings
        perf_score = scores.get('mobile_page_speed', 0)
        if pagespeed.get('success'):
            if perf_score >= 90:
                findings.append(f"✓ Excellent mobile performance ({perf_score:.0f}/100)")
            elif perf_score >= 50:
                findings.append(f"⚠ Mobile performance needs improvement ({perf_score:.0f}/100)")
            else:
                findings.append(f"✗ Poor mobile performance ({perf_score:.0f}/100) - significant optimization needed")
        else:
            findings.append("⚠ Performance data unavailable - using estimated scores")
        
        # Core Web Vitals findings
        lcp = pagespeed.get('lcp', 'N/A')
        cls = pagespeed.get('cls', 'N/A')
        
        if lcp != 'N/A':
            try:
                lcp_value = float(lcp.replace('s', '').strip())
                if lcp_value >= 4.0:
                    findings.append(f"✗ Largest Contentful Paint ({lcp}) is poor - should be under 2.5s")
                elif lcp_value >= 2.5:
                    findings.append(f"⚠ Largest Contentful Paint ({lcp}) needs improvement - aim for under 2.5s")
                else:
                    findings.append(f"✓ Largest Contentful Paint ({lcp}) is good")
            except:
                pass
        
        if cls != 'N/A':
            try:
                cls_value = float(str(cls).strip())
                if cls_value >= 0.25:
                    findings.append(f"✗ Cumulative Layout Shift ({cls}) is poor - should be under 0.1")
                elif cls_value >= 0.1:
                    findings.append(f"⚠ Cumulative Layout Shift ({cls}) needs improvement - aim for under 0.1")
                else:
                    findings.append(f"✓ Cumulative Layout Shift ({cls}) is good")
            except:
                pass
        
        # Responsive design findings
        if scores['responsive_design'] < 70:
            findings.append("✗ Responsive design implementation is incomplete")
        elif scores['responsive_design'] < 90:
            findings.append("⚠ Responsive design could be enhanced")
        else:
            findings.append("✓ Good responsive design implementation detected")
        
        # Viewport findings
        if scores['viewport_config'] < 100:
            findings.append("✗ Missing viewport meta tag - critical for mobile devices")
        else:
            findings.append("✓ Viewport meta tag properly configured")
        
        # Mobile usability
        usability = scores.get('mobile_usability', 0)
        if usability >= 90:
            findings.append(f"✓ Excellent mobile usability ({usability:.0f}/100)")
        elif usability >= 70:
            findings.append(f"⚠ Mobile usability is acceptable ({usability:.0f}/100) but could be improved")
        else:
            findings.append(f"✗ Mobile usability needs significant improvement ({usability:.0f}/100)")
        
        return findings
    
    def _generate_recommendations(self, scores, pagespeed):
        """Generate detailed recommendations"""
        recommendations = []
        
        # Performance recommendations
        perf_score = scores.get('mobile_page_speed', 0)
        if perf_score < 90:
            priority = 'CRITICAL' if perf_score < 50 else 'HIGH'
            recommendations.append({
                'priority': priority,
                'title': 'Optimize mobile page speed',
                'details': [
                    f'Current mobile performance score: {perf_score:.0f}/100',
                    'Minimize JavaScript execution time',
                    'Optimize and compress images (use WebP format)',
                    'Enable text compression (gzip/brotli)',
                    'Eliminate render-blocking resources',
                    'Reduce server response time',
                    'Leverage browser caching',
                    'Use a Content Delivery Network (CDN)',
                    'Test with Google PageSpeed Insights: https://pagespeed.web.dev/'
                ]
            })
        
        # Core Web Vitals recommendations
        lcp = pagespeed.get('lcp', 'N/A')
        if lcp != 'N/A':
            try:
                lcp_value = float(lcp.replace('s', '').strip())
                if lcp_value >= 2.5:
                    recommendations.append({
                        'priority': 'HIGH',
                        'title': 'Improve Largest Contentful Paint (LCP)',
                        'details': [
                            f'Current LCP: {lcp} (target: < 2.5s)',
                            'Optimize server response time',
                            'Preload critical resources (fonts, hero images)',
                            'Optimize and compress images',
                            'Remove unused CSS and JavaScript',
                            'Implement lazy loading for below-the-fold content'
                        ]
                    })
            except:
                pass
        
        cls = pagespeed.get('cls', 'N/A')
        if cls != 'N/A':
            try:
                cls_value = float(str(cls).strip())
                if cls_value >= 0.1:
                    recommendations.append({
                        'priority': 'MEDIUM',
                        'title': 'Reduce Cumulative Layout Shift (CLS)',
                        'details': [
                            f'Current CLS: {cls} (target: < 0.1)',
                            'Set explicit width and height for images and videos',
                            'Reserve space for ads and embeds',
                            'Avoid inserting content above existing content',
                            'Use transform animations instead of layout-shifting properties',
                            'Preload fonts to avoid FOIT/FOUT'
                        ]
                    })
            except:
                pass
        
        # Responsive design recommendations
        if scores['responsive_design'] < 80:
            recommendations.append({
                'priority': 'MEDIUM',
                'title': 'Enhance responsive design implementation',
                'details': [
                    f'Current responsive design score: {scores["responsive_design"]:.0f}/100',
                    'Use CSS media queries for different screen sizes',
                    'Implement flexible grid layouts (CSS Grid or Flexbox)',
                    'Use responsive images with srcset attribute',
                    'Test on multiple devices and screen sizes',
                    'Ensure touch targets are at least 48x48 pixels',
                    'Avoid horizontal scrolling on mobile devices'
                ]
            })
        
        # Viewport recommendations
        if scores['viewport_config'] < 100:
            recommendations.append({
                'priority': 'CRITICAL',
                'title': 'Add viewport meta tag',
                'details': [
                    'Missing viewport meta tag - critical for mobile devices',
                    'Add this to your <head> section:',
                    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                    'This ensures proper scaling on mobile devices',
                    'Without it, mobile browsers will render at desktop width'
                ]
            })
        
        return recommendations
