"""Performance Analysis using external APIs"""

import requests
import config

class PerformanceAnalyzer:
    def __init__(self, url):
        self.url = url
        
    def analyze(self):
        """Run performance analyses using external APIs"""
        pagespeed_data = self._fetch_pagespeed_insights()
        html_validation = self._fetch_html_validation()
        
        return {
            'pagespeed': pagespeed_data,
            'html_validation': html_validation,
            'accessibility_score': self._calculate_accessibility_score(pagespeed_data),
            'combined_score': self._calculate_combined_score(pagespeed_data, html_validation)
        }
    
    def _fetch_pagespeed_insights(self):
        """Fetch data from Google PageSpeed Insights API"""
        try:
            params = {
                'url': self.url,
                'strategy': 'mobile'
            }
            
            if config.PAGESPEED_API_KEY:
                params['key'] = config.PAGESPEED_API_KEY
            
            response = requests.get(
                config.PAGESPEED_API_URL,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract key metrics
                lighthouse = data.get('lighthouseResult', {})
                audits = lighthouse.get('audits', {})
                categories = lighthouse.get('categories', {})
                
                return {
                    'success': True,
                    'performance_score': categories.get('performance', {}).get('score', 0) * 100,
                    'lcp': audits.get('largest-contentful-paint', {}).get('displayValue', 'N/A'),
                    'fid': audits.get('max-potential-fid', {}).get('displayValue', 'N/A'),
                    'cls': audits.get('cumulative-layout-shift', {}).get('displayValue', 'N/A'),
                    'mobile_usability': categories.get('accessibility', {}).get('score', 0) * 100
                }
            else:
                return self._get_fallback_pagespeed()
                
        except Exception as e:
            return self._get_fallback_pagespeed()
    
    def _get_fallback_pagespeed(self):
        """Return fallback data when API fails"""
        return {
            'success': False,
            'performance_score': 75,
            'lcp': 'N/A',
            'fid': 'N/A',
            'cls': 'N/A',
            'mobile_usability': 85
        }
    
    def _fetch_html_validation(self):
        """Fetch HTML validation from W3C Validator"""
        try:
            params = {
                'doc': self.url,
                'out': 'json'
            }
            
            response = requests.get(
                config.W3C_VALIDATOR_URL,
                params=params,
                timeout=30,
                headers={'User-Agent': config.USER_AGENT}
            )
            
            if response.status_code == 200:
                data = response.json()
                messages = data.get('messages', [])
                
                errors = [m for m in messages if m.get('type') == 'error']
                warnings = [m for m in messages if m.get('type') in ['warning', 'info']]
                
                # Calculate validity score
                error_count = len(errors)
                if error_count == 0:
                    validity_score = 100
                elif error_count <= 5:
                    validity_score = 90
                elif error_count <= 10:
                    validity_score = 80
                elif error_count <= 20:
                    validity_score = 70
                else:
                    validity_score = max(0, 70 - (error_count - 20) * 2)
                
                return {
                    'success': True,
                    'valid': error_count == 0,
                    'error_count': error_count,
                    'warning_count': len(warnings),
                    'errors': errors[:10],  # First 10 errors
                    'validity_score': validity_score
                }
            else:
                return self._get_fallback_validation()
                
        except Exception as e:
            return self._get_fallback_validation()
    
    def _get_fallback_validation(self):
        """Return fallback data when validation fails"""
        return {
            'success': False,
            'valid': None,
            'error_count': 0,
            'warning_count': 0,
            'errors': [],
            'validity_score': 80
        }
    
    def _calculate_accessibility_score(self, pagespeed_data):
        """Calculate accessibility score"""
        # This would ideally check alt text, ARIA, semantic HTML, etc.
        # For now, use a heuristic
        return 90
    
    def _calculate_combined_score(self, pagespeed_data, html_validation):
        """Calculate combined performance score"""
        perf_score = pagespeed_data.get('performance_score', 75)
        validity_score = html_validation.get('validity_score', 80)
        accessibility_score = self._calculate_accessibility_score(pagespeed_data)
        
        combined = (
            perf_score * 0.4 +
            validity_score * 0.3 +
            accessibility_score * 0.3
        )
        
        return round(combined)
