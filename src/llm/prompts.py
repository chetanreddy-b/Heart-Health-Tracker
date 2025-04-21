class RecommendationPrompts:
    """
    Prompt templates for LLM-powered exercise recommendations
    """
    
    @staticmethod
    def generate_exercise_recommendation_prompt(
        user_data, 
        correlation_summary, 
        bp_stats, 
        exercise_history,
        fhir_data=None
    ):
        """
        Generate a prompt for the LLM to create exercise recommendations
        
        Parameters:
        - user_data: Dictionary with user information
        - correlation_summary: Dictionary with correlation analysis results
        - bp_stats: Dictionary with blood pressure statistics
        - exercise_history: DataFrame with recent exercise history
        - fhir_data: Optional FHIR health record data
        
        Returns:
        Formatted prompt string
        """
        # Start with system context
        prompt = """
You are an AI-powered cardiovascular health expert specializing in personalized exercise recommendations. Your task is to generate a detailed, personalized weekly exercise plan based on the user's blood pressure data, exercise history, health conditions, and observed correlations between exercise and blood pressure changes.

You should follow these specific guidelines:

1. CREATE A COMPREHENSIVE PLAN: Recommend exercises that have shown positive correlation with blood pressure improvements for this specific user, with specific descriptions of each exercise type.

2. INCLUDE DETAILED INSTRUCTIONS: For each exercise, provide specific information on:
   - Exact techniques or movements (especially for weight training, provide specific exercises)
   - Proper form guidance
   - Appropriate intensity levels
   - Specific duration recommendations
   - Progression paths as fitness improves

3. BALANCE DIFFERENT MODALITIES: Include a mix of:
   - Cardiovascular exercise (specific types based on patient data)
   - Strength training (with specific movements tailored to their conditions)
   - Flexibility/mobility work
   - Recovery techniques

4. MEDICAL CONSIDERATIONS: Carefully consider the user's health conditions, medications, and BP category when making recommendations

5. WEEKLY SCHEDULE: Create a day-by-day plan with specific activities, duration, intensity, and rest periods

6. SAFETY GUIDELINES: Include precautions specific to their cardiovascular health status

Your recommendations must be evidence-based, drawing from both the correlation data provided and established clinical guidelines for cardiovascular health from organizations like the American Heart Association and American College of Sports Medicine.

Please format your response in the following sections:
- Summary of Analysis (concise overview of their data and key findings)
- Weekly Exercise Plan (detailed day-by-day schedule with specific exercises and instructions)
- Key Insights and Guidelines (important safety information and progression guidelines)
- Monitoring Recommendations (guidance on tracking progress and warning signs)
"""

        # # Add user information
        # if user_data:
        #     prompt += "\n\n--- USER INFORMATION ---\n"
        #     for key, value in user_data.items():
        #         prompt += f"{key}: {value}\n"
        
        # # Add blood pressure statistics
        # if bp_stats:
        #     prompt += "\n\n--- BLOOD PRESSURE STATISTICS ---\n"
        #     if 'avg_systolic' in bp_stats:
        #         prompt += f"Average systolic: {bp_stats['avg_systolic']:.1f} mmHg\n"
        #     if 'avg_diastolic' in bp_stats:
        #         prompt += f"Average diastolic: {bp_stats['avg_diastolic']:.1f} mmHg\n"
        #     if 'max_systolic' in bp_stats:
        #         prompt += f"Maximum systolic: {bp_stats['max_systolic']} mmHg\n"
        #     if 'min_systolic' in bp_stats:
        #         prompt += f"Minimum systolic: {bp_stats['min_systolic']} mmHg\n"
        #     if 'category_distribution' in bp_stats:
        #         prompt += "BP Category Distribution:\n"
        #         for category, percentage in bp_stats['category_distribution'].items():
        #             prompt += f"- {category}: {percentage:.1f}%\n"
# Add more detailed user information section
        if user_data:
            prompt += "\n\n--- USER INFORMATION ---\n"
            prompt += f"Age: {user_data.get('age', 'Unknown')} years\n"
            prompt += f"Gender: {user_data.get('gender', 'Unknown')}\n"
            prompt += f"Weight: {user_data.get('weight', 'Unknown')} kg\n"
            prompt += f"Height: {user_data.get('height', 'Unknown')} cm\n"
            prompt += f"BMI: {user_data.get('bmi', 'Unknown')}\n"
            
            # Add conditions
            conditions = user_data.get('conditions', [])
            if conditions:
                prompt += "Medical Conditions:\n"
                for condition in conditions:
                    prompt += f"- {condition}\n"
            
            # Add medical history
            medical_history = user_data.get('medical_history', [])
            if medical_history and medical_history != ["None of the above"]:
                prompt += "Medical History:\n"
                for history in medical_history:
                    prompt += f"- {history}\n"        
        # Add correlation information
        if correlation_summary:
            prompt += "\n\n--- CORRELATION ANALYSIS ---\n"
            
            if 'systolic_correlation' in correlation_summary:
                prompt += f"Systolic BP correlation with exercise: {correlation_summary['systolic_correlation']:.3f}"
                if correlation_summary.get('systolic_significant', False):
                    prompt += " (statistically significant)\n"
                else:
                    prompt += " (not statistically significant)\n"
                    
            if 'diastolic_correlation' in correlation_summary:
                prompt += f"Diastolic BP correlation with exercise: {correlation_summary['diastolic_correlation']:.3f}"
                if correlation_summary.get('diastolic_significant', False):
                    prompt += " (statistically significant)\n"
                else:
                    prompt += " (not statistically significant)\n"
            
            if 'interpretations' in correlation_summary:
                prompt += "\nInterpretations:\n"
                for interpretation in correlation_summary['interpretations']:
                    prompt += f"- {interpretation}\n"
        
        # Add exercise history summary
        if exercise_history is not None and not exercise_history.empty:
            prompt += "\n\n--- EXERCISE HISTORY ---\n"
            
            # Most frequent exercise types
            ex_type_counts = exercise_history['exercise_type'].value_counts()
            prompt += "Most frequent exercise types:\n"
            for ex_type, count in ex_type_counts.head(3).items():
                prompt += f"- {ex_type}: {count} sessions\n"
            
            # Average duration
            avg_duration = exercise_history['duration_minutes'].mean()
            prompt += f"\nAverage exercise duration: {avg_duration:.1f} minutes\n"
            
            # Intensity distribution
            intensity_dist = exercise_history['intensity'].value_counts(normalize=True) * 100
            prompt += "\nIntensity distribution:\n"
            for intensity, percentage in intensity_dist.items():
                prompt += f"- {intensity}: {percentage:.1f}%\n"
        
        # Add FHIR health record information if available
        if fhir_data:
            prompt += "\n\n--- HEALTH RECORD INFORMATION ---\n"
            
            if 'conditions' in fhir_data:
                prompt += "Medical conditions:\n"
                for condition in fhir_data['conditions']:
                    prompt += f"- {condition}\n"
            
            if 'medications' in fhir_data:
                prompt += "\nMedications:\n"
                for medication in fhir_data['medications']:
                    prompt += f"- {medication}\n"
            
            if 'allergies' in fhir_data:
                prompt += "\nAllergies:\n"
                for allergy in fhir_data['allergies']:
                    prompt += f"- {allergy}\n"
                    
            if 'vital_signs' in fhir_data:
                prompt += "\nVital signs:\n"
                for vital, value in fhir_data['vital_signs'].items():
                    prompt += f"- {vital}: {value}\n"
        
        # Add training guidelines for specific exercise types
        prompt += """
\n\n--- EXERCISE TYPE GUIDELINES ---
For strength training recommendations, include specific exercises from these categories:
- Upper body (e.g., chest press, rows, shoulder press, bicep curls, tricep extensions)
- Lower body (e.g., squats, lunges, leg press, calf raises)
- Core work (e.g., planks, bird-dogs, bridges)

For cardiovascular exercise, include:
- Specific intensity targets (either by heart rate or perceived exertion)
- Duration progression guidelines
- Interval training options when appropriate

For flexibility/mobility, include:
- Specific stretches for major muscle groups
- Duration recommendations
- Frequency guidelines

For all exercises, provide specific form cues and modification options based on the patient's health conditions.
"""
        
        # Add final instruction
        prompt += """
\n\n--- TASK ---
Based on the information above, generate a personalized, comprehensive weekly exercise plan optimized for improving this user's cardiovascular health. Focus on the exercise types that show the strongest correlation with blood pressure improvements for this specific user and provide detailed instructions for each recommended exercise, including specific techniques, intensity guidelines, and progression paths.
"""
        
        return prompt