import pandas as pd
import numpy as np
from datetime import timedelta
from scipy.stats import pearsonr

class CorrelationAnalyzer:
    """
    Analyzes correlations between exercise data and blood pressure readings
    """
    
    def __init__(self):
        # Track correlation results
        self.results = {}
    
    def analyze_exercise_bp_correlation(self, bp_data, exercise_data, time_window=3):
        """
        Analyze the correlation between exercise and subsequent blood pressure readings
        
        Parameters:
        - bp_data: DataFrame with blood pressure readings
        - exercise_data: DataFrame with exercise activities
        - time_window: Number of days to look for BP changes after exercise
        
        Returns:
        Dictionary of correlation results
        """
        if bp_data is None or exercise_data is None:
            return None
            
        if len(bp_data) == 0 or len(exercise_data) == 0:
            return None
            
        # Prepare data for correlation analysis
        exercise_impact = self._prepare_exercise_impact_data(bp_data, exercise_data, time_window)
        
        # Overall correlation between exercise and BP
        correlation_results = {}
        
        # Calculate correlations if we have enough data points
        if len(exercise_impact) >= 5:
            # Correlation between exercise and systolic BP
            if 'systolic_change' in exercise_impact.columns and 'intensity_score' in exercise_impact.columns:
                try:
                    systolic_corr, systolic_p = pearsonr(
                        exercise_impact['intensity_score'], 
                        exercise_impact['systolic_change']
                    )
                    correlation_results['systolic'] = {
                        'correlation': systolic_corr,
                        'p_value': systolic_p,
                        'significant': systolic_p < 0.05
                    }
                except:
                    correlation_results['systolic'] = {
                        'correlation': 0,
                        'p_value': 1,
                        'significant': False,
                        'error': 'Calculation failed'
                    }
            
            # Correlation between exercise and diastolic BP
            if 'diastolic_change' in exercise_impact.columns and 'intensity_score' in exercise_impact.columns:
                try:
                    diastolic_corr, diastolic_p = pearsonr(
                        exercise_impact['intensity_score'], 
                        exercise_impact['diastolic_change']
                    )
                    correlation_results['diastolic'] = {
                        'correlation': diastolic_corr,
                        'p_value': diastolic_p,
                        'significant': diastolic_p < 0.05
                    }
                except:
                    correlation_results['diastolic'] = {
                        'correlation': 0,
                        'p_value': 1,
                        'significant': False,
                        'error': 'Calculation failed'
                    }
            
            # Correlation between exercise and pulse
            if 'pulse_change' in exercise_impact.columns and 'intensity_score' in exercise_impact.columns:
                try:
                    pulse_corr, pulse_p = pearsonr(
                        exercise_impact['intensity_score'], 
                        exercise_impact['pulse_change']
                    )
                    correlation_results['pulse'] = {
                        'correlation': pulse_corr,
                        'p_value': pulse_p,
                        'significant': pulse_p < 0.05
                    }
                except:
                    correlation_results['pulse'] = {
                        'correlation': 0,
                        'p_value': 1,
                        'significant': False,
                        'error': 'Calculation failed'
                    }
        
        # Exercise type specific analysis
        exercise_type_impact = self._analyze_exercise_type_impact(exercise_impact)
        
        # Combine results
        self.results = {
            'overall_correlation': correlation_results,
            'exercise_type_impact': exercise_type_impact,
            'exercise_impact_data': exercise_impact
        }
        
        return self.results
    
    def _prepare_exercise_impact_data(self, bp_data, exercise_data, time_window=3):
        """
        Prepare data for correlation analysis by matching exercise events
        with subsequent BP readings
        
        Parameters:
        - bp_data: DataFrame with BP readings
        - exercise_data: DataFrame with exercise data
        - time_window: Days to look for BP changes after exercise
        
        Returns:
        DataFrame with exercise events and corresponding BP changes
        """
        # Create a copy of exercise data for our analysis
        exercise_impact = exercise_data.copy()
        
        # Add intensity score based on intensity and duration
        intensity_scores = {
            'Low': 1,
            'Moderate': 2,
            'High': 3
        }
        
        # Calculate intensity score as intensity level × duration
        exercise_impact['intensity_score'] = exercise_impact.apply(
            lambda row: intensity_scores.get(row['intensity'], 1) * row['duration_minutes'] / 30,
            axis=1
        )
        
        # For each exercise event, find BP readings before and after
        bp_changes = []
        
        for _, exercise in exercise_impact.iterrows():
            exercise_date = exercise['date']
            
            # Find BP readings before the exercise (baseline)
            before_bp = bp_data[bp_data['date'] < exercise_date].sort_values('date', ascending=False)
            
            if len(before_bp) == 0:
                continue  # Skip if no baseline available
                
            baseline_bp = before_bp.iloc[0]  # Most recent BP reading before exercise
            
            # Find BP readings after exercise within the time window
            after_date = exercise_date + timedelta(days=time_window)
            after_bp = bp_data[(bp_data['date'] > exercise_date) & (bp_data['date'] <= after_date)]
            
            if len(after_bp) == 0:
                continue  # Skip if no follow-up readings
                
            # Get the average of BP readings after exercise
            avg_after_systolic = after_bp['systolic'].mean()
            avg_after_diastolic = after_bp['diastolic'].mean()
            avg_after_pulse = after_bp['pulse'].mean()
            
            # Calculate changes
            systolic_change = avg_after_systolic - baseline_bp['systolic']
            diastolic_change = avg_after_diastolic - baseline_bp['diastolic']
            pulse_change = avg_after_pulse - baseline_bp['pulse']
            
            # Add to the list
            bp_changes.append({
                'exercise_date': exercise_date,
                'exercise_type': exercise['exercise_type'],
                'intensity': exercise['intensity'],
                'duration_minutes': exercise['duration_minutes'],
                'intensity_score': exercise['intensity_score'],
                'baseline_systolic': baseline_bp['systolic'],
                'baseline_diastolic': baseline_bp['diastolic'],
                'baseline_pulse': baseline_bp['pulse'],
                'avg_after_systolic': avg_after_systolic,
                'avg_after_diastolic': avg_after_diastolic,
                'avg_after_pulse': avg_after_pulse,
                'systolic_change': systolic_change,
                'diastolic_change': diastolic_change,
                'pulse_change': pulse_change
            })
        
        # Convert to DataFrame
        impact_df = pd.DataFrame(bp_changes)
        
        return impact_df
    
    def _analyze_exercise_type_impact(self, exercise_impact):
        """
        Analyze the impact of different exercise types on BP
        
        Parameters:
        - exercise_impact: DataFrame with exercise events and BP changes
        
        Returns:
        Dictionary with exercise type specific analysis
        """
        if exercise_impact is None or len(exercise_impact) == 0:
            return {}
            
        # Group by exercise type
        if 'exercise_type' not in exercise_impact.columns:
            return {}
            
        type_results = {}
        
        # Get unique exercise types
        exercise_types = exercise_impact['exercise_type'].unique()
        
        for ex_type in exercise_types:
            # Filter for this exercise type
            type_data = exercise_impact[exercise_impact['exercise_type'] == ex_type]
            
            if len(type_data) < 3:  # Need at least 3 data points for meaningful analysis
                continue
                
            # Calculate average changes
            avg_systolic_change = type_data['systolic_change'].mean()
            avg_diastolic_change = type_data['diastolic_change'].mean()
            avg_pulse_change = type_data['pulse_change'].mean()
            
            # Store results
            type_results[ex_type] = {
                'count': len(type_data),
                'avg_systolic_change': avg_systolic_change,
                'avg_diastolic_change': avg_diastolic_change,
                'avg_pulse_change': avg_pulse_change
            }
            
            # Add intensity breakdown if we have enough data
            if len(type_data) >= 5:
                intensity_breakdown = {}
                
                for intensity in ['Low', 'Moderate', 'High']:
                    intensity_data = type_data[type_data['intensity'] == intensity]
                    
                    if len(intensity_data) >= 2:
                        intensity_breakdown[intensity] = {
                            'count': len(intensity_data),
                            'avg_systolic_change': intensity_data['systolic_change'].mean(),
                            'avg_diastolic_change': intensity_data['diastolic_change'].mean(),
                            'avg_pulse_change': intensity_data['pulse_change'].mean()
                        }
                
                type_results[ex_type]['intensity_breakdown'] = intensity_breakdown
        
        return type_results
    
    def get_correlation_summary(self):
        """
        Get a summary of correlation results in a format suitable for display
        
        Returns:
        Dictionary with correlation summary
        """
        if not self.results:
            return {
                'status': 'No correlation analysis available',
                'message': 'Please run the correlation analysis first.'
            }
            
        # Extract key information
        overall = self.results.get('overall_correlation', {})
        
        # Systolic summary
        systolic = overall.get('systolic', {})
        systolic_corr = systolic.get('correlation', 0)
        systolic_sig = systolic.get('significant', False)
        
        # Diastolic summary
        diastolic = overall.get('diastolic', {})
        diastolic_corr = diastolic.get('correlation', 0)
        diastolic_sig = diastolic.get('significant', False)
        
        # Generate interpretations
        interpretations = []
        
        if systolic_sig:
            if systolic_corr < -0.3:
                interpretations.append("Exercise appears to significantly reduce systolic blood pressure.")
            elif systolic_corr > 0.3:
                interpretations.append("Exercise appears to be associated with increased systolic blood pressure, which is unusual. Consider consulting a healthcare provider.")
        
        if diastolic_sig:
            if diastolic_corr < -0.3:
                interpretations.append("Exercise appears to significantly reduce diastolic blood pressure.")
            elif diastolic_corr > 0.3:
                interpretations.append("Exercise appears to be associated with increased diastolic blood pressure, which is unusual. Consider consulting a healthcare provider.")
        
        # Add exercise type insights
        type_impact = self.results.get('exercise_type_impact', {})
        for ex_type, impact in type_impact.items():
            sys_change = impact.get('avg_systolic_change', 0)
            dia_change = impact.get('avg_diastolic_change', 0)
            
            if abs(sys_change) > 5 or abs(dia_change) > 3:
                direction = "decrease" if (sys_change < 0 and dia_change < 0) else "increase"
                interpretations.append(f"{ex_type} appears to {direction} your blood pressure by an average of {abs(sys_change):.1f}/{abs(dia_change):.1f} mmHg.")
        
        return {
            'status': 'Correlation analysis complete',
            'systolic_correlation': systolic_corr,
            'systolic_significant': systolic_sig,
            'diastolic_correlation': diastolic_corr,
            'diastolic_significant': diastolic_sig,
            'interpretations': interpretations,
            'exercise_types': list(type_impact.keys())
        }