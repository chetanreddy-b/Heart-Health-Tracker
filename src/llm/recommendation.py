import os
import json
import requests
from .prompts import RecommendationPrompts

class LLMRecommendationEngine:
    """
    LLM-powered recommendation engine for generating personalized
    exercise recommendations based on health data
    """
    
    def __init__(self, api_key=None, model="anthropic/claude-3-haiku"):
        """
        Initialize the recommendation engine
        
        Parameters:
        - api_key: API key for OpenRouter (fallback to env variable OPENROUTER_API_KEY)
        - model: Model to use for recommendations
        """
        self.api_key = "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"
        if not self.api_key:
            raise ValueError("OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable or pass api_key parameter.")
            
        self.model = model
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def generate_recommendations(self, user_data, correlation_summary, bp_stats, exercise_history, fhir_data=None):
        """
        Generate personalized exercise recommendations
        
        Parameters:
        - user_data: Dictionary with user information
        - correlation_summary: Dictionary with correlation analysis results
        - bp_stats: Dictionary with blood pressure statistics
        - exercise_history: DataFrame with recent exercise history
        - fhir_data: Optional FHIR health record data
        
        Returns:
        Dictionary with recommendation information
        """
        # Generate the prompt
        prompt = RecommendationPrompts.generate_exercise_recommendation_prompt(
            user_data, correlation_summary, bp_stats, exercise_history, fhir_data
        )
        
        # Add few-shot examples for better formatting
        prompt += self._add_few_shot_examples()
        
        # Call the LLM API
        try:
            response = self._call_openrouter_api(prompt)
            
            # Parse and format the recommendation
            recommendation = self._format_recommendation(response)
            
            return {
                "status": "success",
                "recommendation": recommendation,
                "raw_response": response
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "recommendation": None,
                "raw_response": None
            }
    
    def _call_openrouter_api(self, prompt):
        """
        Call the OpenRouter API to generate a recommendation
        
        Parameters:
        - prompt: Formatted prompt string
        
        Returns:
        Raw API response
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI-powered health recommendation system specializing in cardiovascular health. Your task is to generate personalized weekly exercise plans based on health data and research."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1500
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        
        if response.status_code != 200:
            raise Exception(f"API call failed with status code {response.status_code}: {response.text}")
            
        return response.json()
    
    def _format_recommendation(self, response):
        """
        Format the raw API response into a structured recommendation
        
        Parameters:
        - response: Raw API response
        
        Returns:
        Formatted recommendation
        """
        try:
            # Extract the generated text
            content = response['choices'][0]['message']['content']
            
            # Split into sections
            sections = {}
            
            # Try to split by section headers
            if "Summary of Analysis" in content:
                parts = content.split("Summary of Analysis", 1)
                summary_and_rest = "Summary of Analysis" + parts[1]
                
                # Split weekly plan
                if "Weekly Exercise Plan" in summary_and_rest:
                    summary, rest = summary_and_rest.split("Weekly Exercise Plan", 1)
                    sections["summary"] = summary.replace("Summary of Analysis", "").strip()
                    
                    plan_and_insights = "Weekly Exercise Plan" + rest
                    
                    # Split insights
                    if "Key Insights and Guidelines" in plan_and_insights:
                        plan, insights_and_rest = plan_and_insights.split("Key Insights and Guidelines", 1)
                        sections["plan"] = plan.replace("Weekly Exercise Plan", "").strip()
                        
                        insights_and_monitoring = "Key Insights and Guidelines" + insights_and_rest
                        
                        # Split monitoring
                        if "Monitoring Recommendations" in insights_and_monitoring:
                            insights, monitoring = insights_and_monitoring.split("Monitoring Recommendations", 1)
                            sections["insights"] = insights.replace("Key Insights and Guidelines", "").strip()
                            sections["monitoring"] = "Monitoring Recommendations" + monitoring
                        else:
                            sections["insights"] = insights_and_monitoring.strip()
                    else:
                        sections["plan"] = plan_and_insights.strip()
                        sections["insights"] = ""
                else:
                    sections["summary"] = summary_and_rest.strip()
                    sections["plan"] = ""
                    sections["insights"] = ""
            else:
                # Fallback if we can't parse sections
                sections["full_text"] = content.strip()
            
            # Add HTML formatted versions for better display
            sections["html"] = self._convert_to_html(sections)
            
            return sections
        except Exception as e:
            # If parsing fails, return the raw text
            try:
                return {"full_text": response['choices'][0]['message']['content']}
            except:
                return {"error": "Failed to parse recommendation", "details": str(e)}
    
    def _convert_to_html(self, sections):
        """Convert recommendation sections to formatted HTML for better display"""
        html = ""
        
        # Summary section
        # if "summary" in sections and sections["summary"]:
        #     html += f'<div class="recommendation-section summary-section">'
        #     # html += f'<h3 class="section-title">Summary of Analysis</h3>'
        #     html += f'<div class="section-content">{self._markdown_to_html(sections["summary"])}</div>'
        #     html += '</div>'
        
        # Plan section
        if "plan" in sections and sections["plan"]:
            html += f'<div class="recommendation-section plan-section">'
            html += f'<h3 class="section-title">Weekly Exercise Plan</h3>'
            html += f'<div class="section-content">{self._markdown_to_html(sections["plan"])}</div>'
            html += '</div>'
        
        # Insights section
        if "insights" in sections and sections["insights"]:
            html += f'<div class="recommendation-section insights-section">'
            html += f'<h3 class="section-title">Key Insights and Guidelines</h3>'
            html += f'<div class="section-content">{self._markdown_to_html(sections["insights"])}</div>'
            html += '</div>'
        
        # Monitoring section
        if "monitoring" in sections and sections["monitoring"]:
            html += f'<div class="recommendation-section monitoring-section">'
            html += f'<h3 class="section-title">Monitoring Recommendations</h3>'
            html += f'<div class="section-content">{self._markdown_to_html(sections["monitoring"])}</div>'
            html += '</div>'
        
        # Full text fallback
        if "full_text" in sections and sections["full_text"]:
            html += f'<div class="recommendation-section full-text-section">'
            html += f'<div class="section-content">{self._markdown_to_html(sections["full_text"])}</div>'
            html += '</div>'
        
        return html
    
    def _markdown_to_html(self, text):
        """Convert markdown text to HTML with proper formatting"""
        import re
        
        # Replace markdown headers
        text = re.sub(r'^### (.*?)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^# (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        
        # Replace bullet points
        text = re.sub(r'^\* (.*?)$', r'<li>\1</li>', text, flags=re.MULTILINE)
        text = re.sub(r'^- (.*?)$', r'<li>\1</li>', text, flags=re.MULTILINE)
        
        # Wrap lists in <ul> tags
        text = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', text, flags=re.DOTALL)
        # Fix nested lists (remove extra <ul> tags)
        text = re.sub(r'</ul>\s*<ul>', '', text)
        
        # Handle bold and italic text
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        
        # Handle line breaks
        text = re.sub(r'\n\n', r'</p><p>', text)
        
        # Wrap in paragraph tags
        text = f'<p>{text}</p>'
        
        # Fix any double paragraph tags
        text = re.sub(r'<p><p>', r'<p>', text)
        text = re.sub(r'</p></p>', r'</p>', text)
        
        return text
    
    def _add_few_shot_examples(self):
        """Add few-shot examples to guide the LLM's response format"""
        return """
\n\n--- EXAMPLE FORMAT ---
Here is an example of how your response should be structured:

Summary of Analysis
The patient is a 45-year-old male with Stage 1 Hypertension (average BP 135/85 mmHg). His exercise history shows a preference for walking and cycling at moderate intensity 2-3 times per week. Correlation analysis indicates a significant negative relationship between exercise frequency and systolic blood pressure (-0.31, p<0.05), suggesting that consistent exercise has been beneficial for blood pressure management. Given his current BP readings and the correlation data, a structured exercise program emphasizing both aerobic activity and appropriate strength training should help optimize his cardiovascular health.

Weekly Exercise Plan
### Monday
- **Morning**: 30-minute brisk walk at moderate intensity (50-65% of max heart rate)
  * Form focus: Maintain upright posture, engage core, heel-to-toe foot strike
  * Route suggestion: Choose a route with minimal hills to start the week
- **Evening**: 15-minute gentle stretching routine
  * Focus areas: Hamstrings, calves, chest, and shoulders
  * Hold each stretch for 30 seconds, breathe deeply throughout

### Tuesday
- **Morning**: Rest or light activity
- **Evening**: 30-minute strength training focusing on major muscle groups
  * Exercise 1: Modified push-ups (2 sets of 10-12 reps)
     - Form: Hands slightly wider than shoulders, maintain straight body line
     - Modification option: Do against wall if needed for blood pressure management
  * Exercise 2: Chair squats (2 sets of 12-15 reps)
     - Lower only until thighs are parallel to floor, keep weight in heels
     - Focus on controlled movement to minimize BP spikes
  * Exercise 3: Standing rows with resistance band (2 sets of 12-15 reps)
     - Keep band at chest height, squeeze shoulder blades together
  * Exercise a resistance band (2 sets of 12-15 reps each side)
     - Maintain stable positioning to avoid twisting

### Wednesday
- **Morning**: 25-minute cycling at moderate intensity
  * Target heart rate: 105-120 BPM (based on patient's resting heart rate)
  * Maintain steady cadence rather than tackling steep inclines
- **Evening**: 15-minute yoga sequence focusing on breathing and flexibility
  * Include cat-cow pose, gentle spinal twists, and modified downward dog
  * Emphasize deep breathing throughout (4 counts in, 6 counts out)

[REMAINING DAYS FOLLOW SIMILAR DETAILED FORMAT...]

Key Insights and Guidelines
1. **Blood Pressure Monitoring**: Monitor BP before and 30 minutes after exercise initially to understand your body's response.
2. **Progression Plan**: After 2-3 weeks of consistency, increase duration by 5-10% before increasing intensity.
3. **Warning Signs**: Stop exercise immediately if you experience chest pain, severe shortness of breath, dizziness, or if systolic BP exceeds 180 mmHg.
4. **Hydration**: Drink 16-20oz of water 1-2 hours before exercise and 8oz every 15-20 minutes during activity, especially for longer sessions.
5. **Medication Timing**: If taking blood pressure medication, exercise 1-2 hours after taking it when levels are most stable.

Monitoring Recommendations
- Check blood pressure 3 times per week: before exercise, 30 minutes after exercise, and on a non-exercise morning
- Record heart rate during exercise sessions using a fitness tracker or manually
- Log perceived exertion (scale 1-10) after each workout
- Schedule a follow-up evaluation after 6 weeks to reassess your exercise prescription and make adjustments
- Contact healthcare provider if consistently experiencing BP readings over 180/110 mmHg or symptoms like dizziness during exercise
"""