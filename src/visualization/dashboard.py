import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
# Import visualization modules
from .bp_charts import (
    create_bp_trend_chart, 
    create_bp_category_distribution, 
    create_pulse_chart,
    create_bp_statistics_table
)
from .exercise_charts import (
    create_exercise_calendar, 
    create_exercise_type_distribution,
    create_exercise_intensity_chart,
    create_exercise_duration_chart,
    create_exercise_timeline
)
from .correlation_plots import (
    create_exercise_bp_correlation_plot,
    create_diastolic_correlation_plot,
    create_exercise_type_impact_chart,
    create_correlation_summary_card,
    create_combined_timeline
)

def create_dashboard(
    bp_data, 
    exercise_data, 
    correlation_results, 
    date_range, 
    patient_info=None, 
    fhir_data=None
):
    """
    Create the main dashboard layout with all visualizations
    
    Parameters:
    - bp_data: DataFrame with blood pressure readings
    - exercise_data: DataFrame with exercise records
    - correlation_results: Dictionary with correlation analysis results
    - date_range: Tuple of (start_date, end_date)
    - patient_info: Optional dictionary with patient information
    - fhir_data: Optional dictionary with FHIR health record data
    """
    # Create tabs
    tabs = st.tabs(["Overview", "Blood Pressure", "Exercise", "Correlation Analysis", "Recommendations"])
    
    with tabs[0]:  # Overview
        create_overview_tab(bp_data, exercise_data, correlation_results, date_range)
        
    with tabs[1]:  # Blood Pressure
        create_bp_tab(bp_data, date_range)
        
    with tabs[2]:  # Exercise
        create_exercise_tab(exercise_data, date_range)
        
    with tabs[3]:  # Correlation Analysis
        create_correlation_tab(bp_data, exercise_data, correlation_results, date_range)
        
    with tabs[4]:  # Recommendations
        create_recommendation_tab(
            bp_data, 
            exercise_data, 
            correlation_results, 
            patient_info, 
            fhir_data
        )

def create_overview_tab(bp_data, exercise_data, correlation_results, date_range):
    """Create the Overview tab content"""
    st.header("Heart Health Overview")
    
    # Date range information
    start_date, end_date = date_range
    st.write(f"Data from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if bp_data is not None and len(bp_data) > 0:
            avg_systolic = bp_data['systolic'].mean()
            avg_diastolic = bp_data['diastolic'].mean()
            st.metric("Average BP", f"{avg_systolic:.1f}/{avg_diastolic:.1f}")
        else:
            st.metric("Average BP", "No data")
    
    with col2:
        if exercise_data is not None and len(exercise_data) > 0:
            total_sessions = len(exercise_data)
            st.metric("Exercise Sessions", total_sessions)
        else:
            st.metric("Exercise Sessions", "No data")
    
    with col3:
        if correlation_results and 'overall_correlation' in correlation_results:
            systolic_corr = correlation_results['overall_correlation'].get('systolic', {}).get('correlation', 0)
            delta = "Significant" if correlation_results['overall_correlation'].get('systolic', {}).get('significant', False) else "Not significant"
            st.metric("Exercise-BP Correlation", f"{systolic_corr:.3f}", delta=delta)
        else:
            st.metric("Exercise-BP Correlation", "No data")
    
    # Combined timeline
    st.subheader("Blood Pressure and Exercise Timeline")
    timeline_fig = create_combined_timeline(bp_data, exercise_data)
    st.plotly_chart(timeline_fig, use_container_width=True)
    
    # Key insights
    st.subheader("Key Insights")
    
    if correlation_results and 'interpretations' in correlation_results:
        for interpretation in correlation_results['interpretations']:
            st.info(interpretation)
    else:
        st.info("No correlation insights available. Add more data for analysis.")

def create_bp_tab(bp_data, date_range):
    """Create the Blood Pressure tab content"""
    st.header("Blood Pressure Analysis")
    
    if bp_data is None or len(bp_data) == 0:
        st.warning("No blood pressure data available for analysis.")
        return
    
    # BP trend chart
    st.subheader("Blood Pressure Trend")
    bp_trend_fig = create_bp_trend_chart(bp_data)
    st.plotly_chart(bp_trend_fig, use_container_width=True)
    
    # BP statistics and category distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("BP Category Distribution")
        category_fig = create_bp_category_distribution(bp_data)
        st.plotly_chart(category_fig, use_container_width=True)
    
    with col2:
        st.subheader("Pulse Rate Trend")
        pulse_fig = create_pulse_chart(bp_data)
        st.plotly_chart(pulse_fig, use_container_width=True)
    
    # BP statistics table
    st.subheader("Blood Pressure Statistics")
    stats_fig = create_bp_statistics_table(bp_data)
    st.plotly_chart(stats_fig, use_container_width=True)
    
    # Additional BP information
    with st.expander("Blood Pressure Categories (AHA Guidelines)"):
        st.markdown("""
        | Category | Systolic | Diastolic |
        |----------|----------|-----------|
        | Normal | < 120 mmHg | < 80 mmHg |
        | Elevated | 120-129 mmHg | < 80 mmHg |
        | Hypertension Stage 1 | 130-139 mmHg | 80-89 mmHg |
        | Hypertension Stage 2 | ≥ 140 mmHg | ≥ 90 mmHg |
        | Hypertensive Crisis | > 180 mmHg | > 120 mmHg |
        """)

def create_exercise_tab(exercise_data, date_range):
    """Create the Exercise tab content"""
    st.header("Exercise Analysis")
    
    if exercise_data is None or len(exercise_data) == 0:
        st.warning("No exercise data available for analysis.")
        return
    
    # Exercise calendar
    st.subheader("Exercise Activity Calendar")
    calendar_fig = create_exercise_calendar(exercise_data)
    st.plotly_chart(calendar_fig, use_container_width=True)
    
    # Exercise type and intensity distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Exercise Type Distribution")
        type_fig = create_exercise_type_distribution(exercise_data)
        st.plotly_chart(type_fig, use_container_width=True)
    
    with col2:
        st.subheader("Exercise Intensity Distribution")
        intensity_fig = create_exercise_intensity_chart(exercise_data)
        st.plotly_chart(intensity_fig, use_container_width=True)
    
    # Exercise duration by type
    st.subheader("Exercise Duration by Type")
    duration_fig = create_exercise_duration_chart(exercise_data)
    st.plotly_chart(duration_fig, use_container_width=True)
    
    # Exercise timeline
    st.subheader("Exercise Timeline")
    timeline_fig = create_exercise_timeline(exercise_data)
    st.plotly_chart(timeline_fig, use_container_width=True)

def create_correlation_tab(bp_data, exercise_data, correlation_results, date_range):
    """Create the Correlation Analysis tab content"""
    st.header("Correlation Analysis")
    
    if correlation_results is None:
        st.warning("No correlation analysis available. Please ensure you have both blood pressure and exercise data.")
        return
    
    # Correlation summary
    st.subheader("Correlation Summary")
    summary_fig = create_correlation_summary_card(correlation_results)
    st.plotly_chart(summary_fig, use_container_width=True)
    
    # Exercise impact on BP
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Exercise Impact on Systolic BP")
        systolic_fig = create_exercise_bp_correlation_plot(correlation_results)
        st.plotly_chart(systolic_fig, use_container_width=True)
    
    with col2:
        st.subheader("Exercise Impact on Diastolic BP")
        diastolic_fig = create_diastolic_correlation_plot(correlation_results)
        st.plotly_chart(diastolic_fig, use_container_width=True)
    
    # Exercise type impact
    st.subheader("Impact by Exercise Type")
    type_impact_fig = create_exercise_type_impact_chart(correlation_results)
    st.plotly_chart(type_impact_fig, use_container_width=True)
    
    # Correlation explanation
    with st.expander("Understanding Correlation Analysis"):
        st.markdown("""
        ### What does this analysis show?
        
        This correlation analysis examines how different exercise activities affect your blood pressure. Negative correlation values indicate that higher exercise intensity is associated with lower blood pressure readings in subsequent days.
        
        ### How to interpret the results:
        
        - **Correlation values** range from -1 to 1. Values close to -1 suggest exercise strongly reduces BP, while values close to 0 indicate little relationship.
        - **Statistical significance** indicates whether the observed correlation is likely real or due to random chance.
        - **Exercise type impact** shows which activities have the greatest effect on your blood pressure measurements.
        
        For the most accurate analysis, continue tracking both exercise and blood pressure regularly.
        """)
def create_recommendation_tab(
    bp_data, 
    exercise_data, 
    correlation_results, 
    patient_info=None, 
    fhir_data=None
):
    """Create the Recommendations tab content"""
    st.header("Personalized Exercise Recommendations")
    
    # Check if we have the necessary data
    if (bp_data is None or exercise_data is None or correlation_results is None):
        st.warning("Both blood pressure and exercise data are required to generate recommendations.")
    else:
        # Prepare user data based on patient information
        user_data = {
            "age": patient_info.get("age", 45) if patient_info else 45,
            "gender": patient_info.get("gender", "Male") if patient_info else "Male",
            "weight": patient_info.get("vitals", {}).get("Weight", 70.0) if patient_info else 70.0,
            "height": patient_info.get("vitals", {}).get("Height", 170.0) if patient_info else 170.0,
            "bmi": patient_info.get("vitals", {}).get("BMI", 24.2) if patient_info else 24.2,
            "medical_history": patient_info.get("conditions", []) if patient_info else ["None of the above"],
            "goals": ["Lower Blood Pressure"]
        }

        # Add button to generate recommendations
        if st.button("Generate Personalized Recommendations"):
            with st.spinner("Analyzing your data and generating personalized recommendations..."):
                try:
                    # Get API key from environment variable
                    api_key = "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"
                    
                    if not api_key:
                        st.error("OpenRouter API key not found. Please set the OPENROUTER_API_KEY environment variable.")
                    else:
                        # Import here to avoid circular imports
                        from src.llm.recommendation import LLMRecommendationEngine
                        from src.llm.recommendation_display import (
                            display_recommendations, 
                            create_recommendation_summary_card
                        )
                        
                        # Initialize recommendation engine
                        recommendation_engine = LLMRecommendationEngine(api_key=api_key)
                        
                        # Prepare BP stats
                        bp_stats = {
                            'avg_systolic': bp_data['systolic'].mean(),
                            'avg_diastolic': bp_data['diastolic'].mean(),
                            'max_systolic': bp_data['systolic'].max(),
                            'min_systolic': bp_data['systolic'].min(),
                            'max_diastolic': bp_data['diastolic'].max(),
                            'min_diastolic': bp_data['diastolic'].min()
                        }
                        
                        # Add category distribution if available
                        if 'category' in bp_data.columns:
                            category_counts = bp_data['category'].value_counts()
                            total = len(bp_data)
                            bp_stats['category_distribution'] = {
                                cat: count / total * 100 
                                for cat, count in category_counts.items()
                            }
                        
                        # Get correlation summary
                        correlation_summary = correlation_results.get('overall_correlation', {})
                        
                        # Add interpretations
                        correlation_summary['interpretations'] = []
                        
                        # Extract systolic correlation
                        systolic = correlation_summary.get('systolic', {})
                        systolic_corr = systolic.get('correlation', 0)
                        systolic_sig = systolic.get('significant', False)
                        
                        # Extract diastolic correlation
                        diastolic = correlation_summary.get('diastolic', {})
                        diastolic_corr = diastolic.get('correlation', 0)
                        diastolic_sig = diastolic.get('significant', False)
                        
                        # Generate interpretations based on correlation values
                        if systolic_sig and systolic_corr < -0.3:
                            correlation_summary['interpretations'].append(
                                "Your exercise appears to significantly reduce systolic blood pressure."
                            )
                        
                        if diastolic_sig and diastolic_corr < -0.3:
                            correlation_summary['interpretations'].append(
                                "Your exercise appears to significantly reduce diastolic blood pressure."
                            )
                        
                        # Add exercise type insights
                        type_impact = correlation_results.get('exercise_type_impact', {})
                        for ex_type, impact in type_impact.items():
                            sys_change = impact.get('avg_systolic_change', 0)
                            dia_change = impact.get('avg_diastolic_change', 0)
                            
                            if (abs(sys_change) > 5 or abs(dia_change) > 3) and impact.get('count', 0) >= 3:
                                direction = "decrease" if (sys_change < 0 and dia_change < 0) else "increase"
                                correlation_summary['interpretations'].append(
                                    f"{ex_type} appears to {direction} your blood pressure by an average of {abs(sys_change):.1f}/{abs(dia_change):.1f} mmHg."
                                )
                        
                        # Get recent exercise history
                        exercise_history = exercise_data.sort_values('date', ascending=False).head(10)
                        
                        # Generate recommendations
                        recommendation_response = recommendation_engine.generate_recommendations(
                            user_data, 
                            correlation_summary, 
                            bp_stats, 
                            exercise_history,
                            fhir_data
                        )
                        
                        if recommendation_response.get('status') == 'success':
                            # Create a summary card
                            create_recommendation_summary_card(
                                recommendation_response, 
                                patient_info
                            )
                            
                            # Display full recommendations
                            display_recommendations(recommendation_response)
                            
                            st.success("Recommendations generated successfully!")
                        else:
                            st.error(f"Failed to generate recommendations: {recommendation_response.get('message')}")
                
                except Exception as e:
                    st.error(f"Error generating recommendations: {str(e)}")
