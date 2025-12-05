"""
Fairness & Bias Prevention Service
Enhanced with custom lightweight fairness engine for Render deployment compatibility
"""

import pandas as pd
import numpy as np
from collections import defaultdict
from typing import Dict, List, Optional

# Import our custom lightweight fairness engine
from backend.services.fairness_engine import (
    analyze_hiring_fairness_comprehensive,
    calculate_fairness_score,
    get_fairness_badge as get_badge_info,
    calculate_demographic_parity,
    calculate_equal_opportunity,
    calculate_disparate_impact,
    FairnessMetrics,
    BiasDetector
)

# AIF360 is NOT used anymore - all fairness metrics calculated in-house
AIF360_AVAILABLE = False
print("✅ Using custom lightweight fairness engine (AIF360 not required)")

def calculate_demographic_parity(selection_rates):
    """
    Calculate demographic parity difference
    
    Demographic Parity: P(Ŷ=1|D=unprivileged) = P(Ŷ=1|D=privileged)
    
    Args:
        selection_rates: dict with {group: selection_rate}
    
    Returns:
        float: Parity difference (0 = perfect parity)
    """
    if not selection_rates or len(selection_rates) < 2:
        return 0.0
    
    rates = list(selection_rates.values())
    max_rate = max(rates)
    min_rate = min(rates)
    
    parity_diff = max_rate - min_rate
    return round(parity_diff, 4)

def calculate_equal_opportunity(true_positive_rates):
    """
    Calculate equal opportunity difference
    
    Equal Opportunity: P(Ŷ=1|Y=1,D=unprivileged) = P(Ŷ=1|Y=1,D=privileged)
    
    Args:
        true_positive_rates: dict with {group: TPR}
    
    Returns:
        float: Opportunity difference (0 = perfect equality)
    """
    if not true_positive_rates or len(true_positive_rates) < 2:
        return 0.0
    
    rates = list(true_positive_rates.values())
    max_rate = max(rates)
    min_rate = min(rates)
    
    opportunity_diff = max_rate - min_rate
    return round(opportunity_diff, 4)

def calculate_disparate_impact(selection_rates):
    """
    Calculate disparate impact ratio
    
    Disparate Impact = P(Ŷ=1|D=unprivileged) / P(Ŷ=1|D=privileged)
    
    A value < 0.8 indicates potential discrimination (80% rule)
    
    Args:
        selection_rates: dict with {group: selection_rate}
    
    Returns:
        dict: Disparate impact ratios
    """
    if not selection_rates or len(selection_rates) < 2:
        return {}
    
    groups = list(selection_rates.keys())
    ratios = {}
    
    for i, group1 in enumerate(groups):
        for group2 in groups[i+1:]:
            rate1 = selection_rates[group1]
            rate2 = selection_rates[group2]
            
            if rate2 > 0:
                ratio = rate1 / rate2
                ratios[f"{group1}_vs_{group2}"] = round(ratio, 4)
    
    return ratios

def analyze_hiring_fairness(applications_df, protected_attribute='gender', favorable_label=1):
    """
    Comprehensive fairness analysis of hiring decisions
    
    Now uses custom lightweight fairness engine instead of AIF360
    
    Args:
        applications_df: DataFrame with columns [protected_attribute, decision, ground_truth]
        protected_attribute: Column name for protected attribute (e.g., 'gender', 'race')
        favorable_label: Label for positive outcome (e.g., 1 for hired, 0 for rejected)
    
    Returns:
        dict: Fairness metrics and recommendations
    """
    if applications_df.empty:
        return {
            'error': 'No data provided',
            'bias_detected': False
        }
    
    # Use our comprehensive fairness engine
    analysis = analyze_hiring_fairness_comprehensive(
        applications=applications_df,
        protected_attribute=protected_attribute,
        decision_column='decision',
        ground_truth_column='ground_truth' if 'ground_truth' in applications_df.columns else None,
        favorable_label=favorable_label
    )
    
    if 'error' in analysis:
        return analysis
    
    # Format results for backward compatibility
    results = {
        'total_applications': analysis['summary']['total_applications'],
        'demographic_breakdown': {},
        'selection_rates': {},
        'fairness_metrics': analysis['fairness_metrics'],
        'bias_detected': analysis['summary']['bias_detected'],
        'bias_groups': analysis['bias_analysis']['violations'],
        'recommendations': analysis['recommendations'],
        'fairness_score': analysis['summary']['fairness_score'],
        'group_statistics': analysis['group_statistics']
    }
    
    # Extract demographic breakdown and selection rates
    for group, stats in analysis['group_statistics'].items():
        results['demographic_breakdown'][group] = stats['count']
        results['selection_rates'][group] = stats['selection_rate']
    
    return results

def generate_fairness_report(job_id, applications_data, protected_attributes=['gender', 'age_group', 'ethnicity']):
    """
    Generate comprehensive fairness audit report
    
    Args:
        job_id: Job posting ID
        applications_data: List of application dicts
        protected_attributes: List of attributes to check for fairness
    
    Returns:
        dict: Complete fairness audit report
    """
    df = pd.DataFrame(applications_data)
    
    report = {
        'job_id': job_id,
        'audit_date': pd.Timestamp.now().isoformat(),
        'total_applications': len(df),
        'analyses': {},
        'overall_bias_detected': False,
        'summary_recommendations': []
    }
    
    for attribute in protected_attributes:
        if attribute in df.columns:
            analysis = analyze_hiring_fairness(df, protected_attribute=attribute)
            report['analyses'][attribute] = analysis
            
            if analysis.get('bias_detected'):
                report['overall_bias_detected'] = True
    
    # Generate summary recommendations
    if report['overall_bias_detected']:
        report['summary_recommendations'] = [
            "Implement blind resume screening to remove identifiable information",
            "Use structured interviews with standardized questions",
            "Diversify the interview panel",
            "Set diversity hiring goals and track progress",
            "Regular fairness audits using this tool",
            "Train recruiters on unconscious bias"
        ]
    else:
        report['summary_recommendations'] = [
            "Continue monitoring hiring outcomes for fairness",
            "Maintain current fair hiring practices",
            "Conduct periodic fairness audits"
        ]
    
    return report

def get_fairness_badge(fairness_score):
    """
    Get fairness badge based on metrics
    
    Now uses custom fairness engine
    
    Args:
        fairness_score: Score from 0-100 (100 = perfectly fair)
    
    Returns:
        dict: Badge information
    """
    return get_badge_info(fairness_score)
