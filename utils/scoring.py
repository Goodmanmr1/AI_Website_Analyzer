"""Scoring calculation utilities"""

import config

def calculate_category_score(sub_scores):
    """Calculate average score from sub-scores"""
    if not sub_scores:
        return 0
    return sum(sub_scores.values()) / len(sub_scores)

def calculate_overall_score(category_scores):
    """Calculate weighted overall score"""
    total_score = 0
    for category, score in category_scores.items():
        weight = config.CATEGORY_WEIGHTS.get(category, 0)
        total_score += score * weight
    return round(total_score)

def get_status_label(score):
    """Get status label based on score"""
    if score >= config.EXCELLENT_THRESHOLD:
        return 'excellent'
    elif score >= config.GOOD_THRESHOLD:
        return 'good'
    elif score >= config.NEEDS_IMPROVEMENT_THRESHOLD:
        return 'needs-improvement'
    else:
        return 'critical'

def get_status_color(status):
    """Get color for status label"""
    color_map = {
        'excellent': config.COLORS['success'],
        'good': config.COLORS['success'],
        'needs-improvement': config.COLORS['warning'],
        'critical': config.COLORS['critical']
    }
    return color_map.get(status, config.COLORS['primary'])

def normalize_score(value, min_val, max_val):
    """Normalize a value to 0-100 scale"""
    if max_val == min_val:
        return 100 if value >= max_val else 0
    normalized = ((value - min_val) / (max_val - min_val)) * 100
    return max(0, min(100, normalized))

def calculate_weighted_performance(core_web_vitals_score, html_validity_score, accessibility_score):
    """Calculate combined performance score"""
    return round(
        core_web_vitals_score * 0.4 +
        html_validity_score * 0.3 +
        accessibility_score * 0.3
    )
