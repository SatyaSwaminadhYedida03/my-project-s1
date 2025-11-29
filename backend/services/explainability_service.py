"""
Model Explainability Service
Provides transparency into candidate scoring and ranking decisions
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from bson import ObjectId

logger = logging.getLogger(__name__)


class ExplainabilityService:
    """Service for explaining AI/ML decisions in hiring process"""
    
    def __init__(self, database):
        self.db = database
        
    def generate_score_explanation(
        self,
        application_id: str,
        candidate_data: Dict[str, Any],
        job_requirements: Dict[str, Any],
        scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Generate detailed explanation of candidate scoring
        
        Args:
            application_id: Application ID
            candidate_data: Candidate profile data
            job_requirements: Job requirements
            scores: Calculated scores breakdown
        
        Returns:
            Detailed explanation with feature importance
        """
        explanation = {
            'application_id': application_id,
            'timestamp': datetime.utcnow(),
            'overall_score': scores.get('overall_score', 0),
            'components': [],
            'feature_importance': [],
            'recommendations': [],
            'transparency_level': 'high'
        }
        
        # Explain Resume Match Score
        resume_score = scores.get('resume_match_score', 0)
        explanation['components'].append({
            'component': 'Resume Match',
            'score': resume_score,
            'weight': 0.30,
            'contribution': resume_score * 0.30,
            'explanation': self._explain_resume_match(
                candidate_data, 
                job_requirements, 
                resume_score
            )
        })
        
        # Explain Skill Match Score
        skill_score = scores.get('skill_match_score', 0)
        explanation['components'].append({
            'component': 'Skill Match',
            'score': skill_score,
            'weight': 0.40,
            'contribution': skill_score * 0.40,
            'explanation': self._explain_skill_match(
                candidate_data.get('skills', []),
                job_requirements.get('required_skills', []),
                skill_score
            )
        })
        
        # Explain CCI Score
        cci_score = scores.get('cci_score', 0)
        explanation['components'].append({
            'component': 'Career Consistency (CCI)',
            'score': cci_score,
            'weight': 0.20,
            'contribution': cci_score * 0.20,
            'explanation': self._explain_cci_score(
                candidate_data.get('experience', []),
                cci_score
            )
        })
        
        # Explain Quiz Score (if available)
        if 'quiz_score' in scores:
            quiz_score = scores['quiz_score']
            explanation['components'].append({
                'component': 'Assessment Score',
                'score': quiz_score,
                'weight': 0.10,
                'contribution': quiz_score * 0.10,
                'explanation': f"Candidate scored {quiz_score:.1f}% on technical assessment"
            })
        
        # Calculate feature importance
        explanation['feature_importance'] = self._calculate_feature_importance(
            candidate_data,
            job_requirements,
            scores
        )
        
        # Generate recommendations
        explanation['recommendations'] = self._generate_recommendations(
            candidate_data,
            job_requirements,
            scores
        )
        
        # Store explanation for audit trail
        self._store_explanation(application_id, explanation)
        
        return explanation
    
    def _explain_resume_match(
        self,
        candidate_data: Dict[str, Any],
        job_requirements: Dict[str, Any],
        score: float
    ) -> str:
        """Explain resume match score"""
        if score >= 80:
            return "Excellent match. Resume demonstrates strong alignment with job description and keywords."
        elif score >= 60:
            return "Good match. Resume shows relevant experience with most key requirements."
        elif score >= 40:
            return "Moderate match. Resume contains some relevant keywords and experience."
        else:
            return "Limited match. Resume shows minimal alignment with job requirements."
    
    def _explain_skill_match(
        self,
        candidate_skills: List[str],
        required_skills: List[str],
        score: float
    ) -> str:
        """Explain skill match score"""
        matched = set(s.lower() for s in candidate_skills) & set(s.lower() for s in required_skills)
        missing = set(s.lower() for s in required_skills) - set(s.lower() for s in candidate_skills)
        
        explanation = f"Candidate has {len(matched)} of {len(required_skills)} required skills. "
        
        if matched:
            explanation += f"Matched skills: {', '.join(list(matched)[:5])}. "
        
        if missing:
            explanation += f"Missing skills: {', '.join(list(missing)[:5])}."
        
        return explanation
    
    def _explain_cci_score(
        self,
        experience: List[Dict[str, Any]],
        score: float
    ) -> str:
        """Explain Career Consistency Index"""
        if not experience:
            return "No work experience data available for CCI calculation."
        
        if score >= 80:
            return "Excellent career consistency. Demonstrates stable career progression with logical job transitions."
        elif score >= 60:
            return "Good career consistency. Shows reasonable job stability and career growth."
        elif score >= 40:
            return "Moderate career consistency. Some job changes but overall acceptable pattern."
        else:
            return "Lower career consistency. Multiple short-term positions may indicate instability."
    
    def _calculate_feature_importance(
        self,
        candidate_data: Dict[str, Any],
        job_requirements: Dict[str, Any],
        scores: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Calculate which features contributed most to the final score"""
        importance = []
        
        # Component contributions
        components = [
            ('resume_match_score', 'Resume Match', 0.30),
            ('skill_match_score', 'Skill Match', 0.40),
            ('cci_score', 'Career Consistency', 0.20),
            ('quiz_score', 'Assessment', 0.10)
        ]
        
        for score_key, name, weight in components:
            if score_key in scores:
                contribution = scores[score_key] * weight
                importance.append({
                    'feature': name,
                    'importance': weight,
                    'score': scores[score_key],
                    'contribution': contribution,
                    'impact': 'high' if contribution >= 25 else 'medium' if contribution >= 15 else 'low'
                })
        
        # Sort by contribution
        importance.sort(key=lambda x: x['contribution'], reverse=True)
        
        return importance
    
    def _generate_recommendations(
        self,
        candidate_data: Dict[str, Any],
        job_requirements: Dict[str, Any],
        scores: Dict[str, Any]
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Skill gap recommendations
        if scores.get('skill_match_score', 0) < 70:
            candidate_skills = set(s.lower() for s in candidate_data.get('skills', []))
            required_skills = set(s.lower() for s in job_requirements.get('required_skills', []))
            missing = list(required_skills - candidate_skills)[:3]
            
            if missing:
                recommendations.append(
                    f"Consider developing skills in: {', '.join(missing)}"
                )
        
        # Experience recommendations
        if scores.get('cci_score', 0) < 60:
            recommendations.append(
                "Focus on building consistent career progression with longer tenure in roles"
            )
        
        # Resume optimization
        if scores.get('resume_match_score', 0) < 60:
            recommendations.append(
                "Optimize resume to highlight relevant experience and keywords for this role"
            )
        
        # Assessment improvement
        if 'quiz_score' in scores and scores['quiz_score'] < 70:
            recommendations.append(
                "Consider taking additional technical courses to strengthen assessment performance"
            )
        
        return recommendations
    
    def _store_explanation(self, application_id: str, explanation: Dict[str, Any]) -> None:
        """Store explanation in database for audit trail"""
        try:
            self.db.explanations.insert_one({
                'application_id': application_id,
                'explanation': explanation,
                'created_at': datetime.utcnow()
            })
        except Exception as e:
            logger.error(f"Failed to store explanation: {e}")
    
    def get_explanation(self, application_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored explanation for an application"""
        try:
            result = self.db.explanations.find_one({'application_id': application_id})
            if result:
                return result['explanation']
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve explanation: {e}")
            return None
    
    def compare_candidates(
        self,
        application_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Compare multiple candidates to show why one ranked higher
        
        Args:
            application_ids: List of application IDs to compare
        
        Returns:
            Comparative analysis
        """
        explanations = []
        
        for app_id in application_ids:
            explanation = self.get_explanation(app_id)
            if explanation:
                explanations.append(explanation)
        
        if not explanations:
            return {'error': 'No explanations found for comparison'}
        
        # Sort by overall score
        explanations.sort(key=lambda x: x['overall_score'], reverse=True)
        
        comparison = {
            'candidates': [],
            'key_differentiators': []
        }
        
        for exp in explanations:
            comparison['candidates'].append({
                'application_id': exp['application_id'],
                'overall_score': exp['overall_score'],
                'strengths': self._identify_strengths(exp),
                'weaknesses': self._identify_weaknesses(exp)
            })
        
        # Identify key differentiators
        if len(explanations) >= 2:
            top = explanations[0]
            second = explanations[1]
            
            for comp in top['components']:
                comp_name = comp['component']
                top_score = comp['score']
                
                second_comp = next(
                    (c for c in second['components'] if c['component'] == comp_name),
                    None
                )
                
                if second_comp:
                    diff = top_score - second_comp['score']
                    if abs(diff) >= 10:  # Significant difference
                        comparison['key_differentiators'].append({
                            'component': comp_name,
                            'difference': diff,
                            'impact': 'Gave top candidate an advantage' if diff > 0 else 'Top candidate scored lower here'
                        })
        
        return comparison
    
    def _identify_strengths(self, explanation: Dict[str, Any]) -> List[str]:
        """Identify candidate's strengths from explanation"""
        strengths = []
        
        for comp in explanation['components']:
            if comp['score'] >= 75:
                strengths.append(f"Strong {comp['component']} ({comp['score']:.1f}%)")
        
        return strengths[:3]
    
    def _identify_weaknesses(self, explanation: Dict[str, Any]) -> List[str]:
        """Identify candidate's weaknesses from explanation"""
        weaknesses = []
        
        for comp in explanation['components']:
            if comp['score'] < 50:
                weaknesses.append(f"Needs improvement in {comp['component']} ({comp['score']:.1f}%)")
        
        return weaknesses[:3]


# Factory function to create service instance
def create_explainability_service(database):
    """Create explainability service instance"""
    return ExplainabilityService(database)
