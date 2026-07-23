import re

class ImpactAnalyzer:
    """
    Analyzes resume text to evaluate quantifiable metrics, action verbs, 
    and measurable achievements (percentages, dollar amounts, scale).
    """
    
    ACTION_VERBS = {
        'built', 'created', 'developed', 'engineered', 'designed', 'implemented',
        'optimized', 'reduced', 'increased', 'improved', 'scaled', 'automated',
        'led', 'managed', 'saved', 'generated', 'launched', 'architected'
    }

    @staticmethod
    def calculate_impact_score(resume_text: str) -> dict:
        resume_lower = resume_text.lower()
        lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
        
        # Regex patterns for metric detection
        metric_pattern = r'(\d+%\b|\$\d+|\b\d+x\b|\b\d+\s*k\b|\b\d+\s*m\b|\b\d+\s*percent\b|\b\d+\s*users\b|\b\d+\s*customers\b|\b\d+\b)'
        
        lines_with_metrics = 0
        total_metrics_found = 0
        verbs_found = set()
        
        for line in lines:
            matches = re.findall(metric_pattern, line, re.IGNORECASE)
            if matches:
                lines_with_metrics += 1
                total_metrics_found += len(matches)
                
            words = set(re.findall(r'\b[a-zA-Z]+\b', line.lower()))
            matched_verbs = words.intersection(ImpactAnalyzer.ACTION_VERBS)
            verbs_found.update(matched_verbs)
            
        total_lines = max(len(lines), 1)
        metric_ratio = (lines_with_metrics / total_lines) * 100
        
        # Score calculation out of 100
        score = min(100.0, round((lines_with_metrics * 15) + (len(verbs_found) * 5), 2))
        if score == 0 and total_metrics_found > 0:
            score = 50.0
            
        return {
            "impact_score": score,
            "total_metrics_count": total_metrics_found,
            "action_verbs_count": len(verbs_found),
            "action_verbs_list": sorted(list(verbs_found)),
            "metric_density_pct": round(metric_ratio, 2)
        }
