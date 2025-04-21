import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Import project modules
from src.data_processing.data_loader import DataLoader
from src.analysis.bp_categories import BPCategorizer
from src.analysis.correlation import CorrelationAnalyzer
from src.data_processing.fhir import FHIRIntegration
from src.llm.recommendation import LLMRecommendationEngine
from src.visualization.dashboard import create_dashboard
from src.llm.recommendation_display import (
    display_recommendations, 
    create_recommendation_summary_card
)

# Set page configuration
st.set_page_config(
    page_title="Heart Health Tracker",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'bp_data' not in st.session_state:
    st.session_state.bp_data = None
if 'exercise_data' not in st.session_state:
    st.session_state.exercise_data = None
if 'categorized_bp_data' not in st.session_state:
    st.session_state.categorized_bp_data = None
if 'correlation_results' not in st.session_state:
    st.session_state.correlation_results = None
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = 0
if 'fhir_data' not in st.session_state:
    st.session_state.fhir_data = None
if 'recommendation' not in st.session_state:
    st.session_state.recommendation = None
if 'patient_info' not in st.session_state:
    st.session_state.patient_info = None

# App title
st.title("❤️ Heart Health Tracker")
st.markdown("### Exercise Impact Dashboard & LLM-Powered Recommendations")

# Initialize data loader and FHIR integration
data_loader = DataLoader()
fhir_integration = FHIRIntegration()

# Sidebar
with st.sidebar:
    st.header("Data Sources")
    
    # Data source selection
    data_source = st.radio(
        "Select Data Source",
        ["Synthetic Data", "Upload Your Data", "Connect FHIR Server"]
    )
    
    if data_source == "Synthetic Data":
        if st.button("Load Synthetic Data"):
            with st.spinner("Loading synthetic data..."):
                # Load synthetic data
                bp_data, exercise_data = data_loader.load_synthetic_data()
                
                # Categorize BP data
                bp_categorizer = BPCategorizer()
                categorized_bp_data = bp_categorizer.categorize_bp_dataframe(bp_data)
                
                # Run correlation analysis
                analyzer = CorrelationAnalyzer()
                correlation_results = analyzer.analyze_exercise_bp_correlation(categorized_bp_data, exercise_data)
                
                # Store in session state
                st.session_state.bp_data = bp_data
                st.session_state.exercise_data = exercise_data
                st.session_state.categorized_bp_data = categorized_bp_data
                st.session_state.correlation_results = correlation_results
                st.session_state.data_loaded = True
                
                st.success("Synthetic data loaded successfully!")
    
    elif data_source == "Upload Your Data":
        st.write("Upload your blood pressure and exercise data:")
        
        bp_file = st.file_uploader("Blood Pressure Data (CSV)", type="csv")
        exercise_file = st.file_uploader("Exercise Data (CSV)", type="csv")
        
        if (bp_file or exercise_file) and st.button("Process Uploaded Data"):
            with st.spinner("Processing uploaded data..."):
                # Load user data
                bp_data, exercise_data = data_loader.load_user_data(bp_file, exercise_file)
                
                # Categorize BP data if available
                categorized_bp_data = None
                if bp_data is not None:
                    bp_categorizer = BPCategorizer()
                    categorized_bp_data = bp_categorizer.categorize_bp_dataframe(bp_data)
                
                # Run correlation analysis if both data types are available
                correlation_results = None
                if bp_data is not None and exercise_data is not None:
                    analyzer = CorrelationAnalyzer()
                    correlation_results = analyzer.analyze_exercise_bp_correlation(categorized_bp_data, exercise_data)
                
                # Store in session state
                st.session_state.bp_data = bp_data
                st.session_state.exercise_data = exercise_data
                st.session_state.categorized_bp_data = categorized_bp_data
                st.session_state.correlation_results = correlation_results
                st.session_state.data_loaded = True
                
                st.success("Uploaded data processed successfully!")
    
    # elif data_source == "Local Patient Data":
    #     st.write("Load local patient data:")
        
    #     # Find local patient data directories
    #     patient_data_dir = "data/patient_data"
    #     patient_dirs = [d for d in os.listdir(patient_data_dir) 
    #                     if os.path.isdir(os.path.join(patient_data_dir, d))]
        
    #     selected_patient = st.selectbox("Select Patient", patient_dirs)
        
    #     if st.button("Load Patient Data"):
    #         with st.spinner("Loading patient data..."):
    #             try:
    #                 # Load patient info
    #                 patient_info_path = os.path.join(patient_data_dir, selected_patient, "patient_info.json")
    #                 with open(patient_info_path, 'r') as f:
    #                     patient_data = json.load(f)
                    
    #                 # Load device data (BP and Exercise)
    #                 bp_data, exercise_data = fhir_integration.load_device_data(selected_patient)
                    
    #                 # Categorize BP data
    #                 bp_categorizer = BPCategorizer()
    #                 categorized_bp_data = bp_categorizer.categorize_bp_dataframe(bp_data)
                    
    #                 # Run correlation analysis
    #                 analyzer = CorrelationAnalyzer()
    #                 correlation_results = analyzer.analyze_exercise_bp_correlation(categorized_bp_data, exercise_data)
                    
    #                 # Prepare FHIR data for recommendations
    #                 fhir_data = fhir_integration.prepare_fhir_data_for_llm(patient_data)
                    
    #                 # Store in session state
    #                 st.session_state.patient_info = {
    #                     "name": patient_data.get("name", "Unknown"),
    #                     "age": patient_data.get("age", "Unknown"),
    #                     "gender": patient_data.get("gender", "Unknown"),
    #                     "bp_category": patient_data.get("bp_category", "Unknown"),
    #                     "conditions": patient_data.get("conditions", []),
    #                     "medications": patient_data.get("medications", [])
    #                 }
    #                 st.session_state.bp_data = bp_data
    #                 st.session_state.exercise_data = exercise_data
    #                 st.session_state.categorized_bp_data = categorized_bp_data
    #                 st.session_state.correlation_results = correlation_results
    #                 st.session_state.fhir_data = fhir_data
    #                 st.session_state.data_loaded = True
                    
    #                 st.success(f"Patient data for {patient_data.get('name', selected_patient)} loaded successfully!")
                
    #             except Exception as e:
    #                 st.error(f"Error loading patient data: {str(e)}")
    #                 import traceback
    #                 st.error(traceback.format_exc())
    
    # elif data_source == "Connect FHIR Server":
    #     st.write("Connect to FHIR server to import health data:")
        
    #     fhir_server = st.text_input("FHIR Server URL", value="https://hapi.fhir.org/baseR4")
    #     patient_id = st.text_input("Patient ID")
        
    #     if patient_id and st.button("Connect and Import"):
    #         with st.spinner("Connecting to FHIR server..."):
    #             try:
    #                 # Fetch patient data from FHIR server
    #                 fhir_client = FHIRIntegration(base_url=fhir_server)
    #                 patient_data = fhir_client.fetch_patient(patient_id)
                    
    #                 if patient_data:
    #                     # Load device data
    #                     bp_data, exercise_data = fhir_client.load_device_data(patient_id)
                        
    #                     # Categorize BP data
    #                     bp_categorizer = BPCategorizer()
    #                     categorized_bp_data = bp_categorizer.categorize_bp_dataframe(bp_data)
                        
    #                     # Run correlation analysis
    #                     analyzer = CorrelationAnalyzer()
    #                     correlation_results = analyzer.analyze_exercise_bp_correlation(categorized_bp_data, exercise_data)
                        
    #                     # Prepare FHIR data for recommendations
    #                     fhir_data = fhir_client.prepare_fhir_data_for_llm(patient_data)
                        
    #                     # Store in session state
    #                     st.session_state.patient_info = {
    #                         "name": patient_data.get("name", "Unknown"),
    #                         "age": patient_data.get("age", "Unknown"),
    #                         "gender": patient_data.get("gender", "Unknown"),
    #                         "bp_category": patient_data.get("bp_category", "Unknown"),
    #                         "conditions": patient_data.get("conditions", []),
    #                         "medications": patient_data.get("medications", [])
    #                     }
    #                     st.session_state.bp_data = bp_data
    #                     st.session_state.exercise_data = exercise_data
    #                     st.session_state.categorized_bp_data = categorized_bp_data
    #                     st.session_state.correlation_results = correlation_results
    #                     st.session_state.fhir_data = fhir_data
    #                     st.session_state.data_loaded = True
                        
    #                     st.success(f"Successfully connected to FHIR server and imported data for patient {patient_id}")
    #                 else:
    #                     st.error(f"Failed to fetch data for patient {patient_id}")
    #             except Exception as e:
    #                 st.error(f"Error connecting to FHIR server: {str(e)}")
    #                 import traceback
    #                 st.error(traceback.format_exc())    # Date range selector (only show if data is loaded)
    elif data_source == "Connect FHIR Server":
        st.write("Connect to FHIR Server")
        
        # Username can be anything
        username = st.text_input("Username")
        
        # Password is the patient ID
        patient_id = st.text_input("Password", type="password", value="")
        
        if st.button("Connect and Import"):
            with st.spinner("Connecting to FHIR server..."):
                try:
                    # Fetch patient data from FHIR server
                    fhir_client = FHIRIntegration(base_url="https://hapi.fhir.org/baseR4")
                    patient_data = fhir_client.fetch_patient(patient_id)
                    
                    if patient_data:
                        # Load device data
                        bp_data, exercise_data = fhir_client.load_device_data(patient_id)
                        
                        # Categorize BP data
                        bp_categorizer = BPCategorizer()
                        categorized_bp_data = bp_categorizer.categorize_bp_dataframe(bp_data)
                        
                        # Run correlation analysis
                        analyzer = CorrelationAnalyzer()
                        correlation_results = analyzer.analyze_exercise_bp_correlation(categorized_bp_data, exercise_data)
                        
                        # Prepare FHIR data for recommendations
                        fhir_data = fhir_client.prepare_fhir_data_for_llm(patient_data)
                        
                        # Store in session state
                        st.session_state.patient_info = {
                            "name": patient_data.get("name", "Unknown"),
                            "age": patient_data.get("age", "Unknown"),
                            "gender": patient_data.get("gender", "Unknown"),
                            "bp_category": patient_data.get("bp_category", "Unknown"),
                            "conditions": patient_data.get("conditions", []),
                            "medications": patient_data.get("medications", [])
                        }
                        st.session_state.bp_data = bp_data
                        st.session_state.exercise_data = exercise_data
                        st.session_state.categorized_bp_data = categorized_bp_data
                        st.session_state.correlation_results = correlation_results
                        st.session_state.fhir_data = fhir_data
                        st.session_state.data_loaded = True
                        
                        st.success(f"Successfully connected to FHIR server and imported data for patient")
                    else:
                        st.error(f"Failed to fetch data for patient")
                except Exception as e:
                    st.error(f"Error connecting to FHIR server: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())


    if st.session_state.data_loaded:
        x = 1
        # st.header("Date Range")
        
        # # Get overall date range from data
        # min_date, max_date = data_loader.get_date_range()
        
        # # Create date range selector
        # date_range = st.date_input(
        #     "Select Date Range",
        #     value=[min_date, max_date],
        #     min_value=min_date,
        #     max_value=max_date
        # )
        
        # # Handle single date selection
        # if len(date_range) == 1:
        #     start_date = date_range[0]
        #     end_date = date_range[0]
        # else:
        #     start_date = date_range[0]
        #     end_date = date_range[1]
        
        # # Filter data based on date range
        # if st.button("Apply Date Filter"):
        #     with st.spinner("Filtering data..."):
        #         filtered_bp, filtered_exercise = data_loader.filter_by_date_range(start_date, end_date)
                
        #         # Categorize filtered BP data
        #         categorized_bp = None
        #         if filtered_bp is not None:
        #             bp_categorizer = BPCategorizer()
        #             categorized_bp = bp_categorizer.categorize_bp_dataframe(filtered_bp)
                
        #         # Run correlation analysis on filtered data
        #         correlation_results = None
        #         if filtered_bp is not None and filtered_exercise is not None:
        #             analyzer = CorrelationAnalyzer()
        #             correlation_results = analyzer.analyze_exercise_bp_correlation(categorized_bp, filtered_exercise)
                
        #         # Update session state with filtered data
        #         st.session_state.bp_data = filtered_bp
        #         st.session_state.exercise_data = filtered_exercise
        #         st.session_state.categorized_bp_data = categorized_bp
        #         st.session_state.correlation_results = correlation_results
                
        #         st.success("Data filtered successfully!")
    

# Main content area
if not st.session_state.data_loaded:
    # Show welcome message if no data is loaded
    st.info("Please load or upload data using the sidebar options to get started.")
    
    # Display information about the application
    st.markdown("""
    ## About Heart Health Tracker
    
    This application helps you understand the relationship between your exercise habits and cardiovascular health metrics. By visualizing correlations between physical activity and blood pressure, you can gain insights into how specific exercise patterns affect your heart health.
    
    ### Features:
    
    - **Blood Pressure Analysis**: Track and categorize your blood pressure readings over time
    - **Exercise Tracking**: Visualize your exercise patterns, including type, duration, and intensity
    - **Correlation Analysis**: Discover how your exercise habits impact your blood pressure- **Personalized Recommendations**: Get AI-powered exercise recommendations tailored to your unique cardiovascular response
    
    ### Getting Started:
    
    1. Choose a data source from the sidebar
    2. Load synthetic data for a demo or upload your own BP and exercise data
    3. Explore the dashboard tabs to analyze your heart health
    4. Generate personalized exercise recommendations based on your data
    
    ### Data Requirements:
    
    **Blood Pressure CSV**: Must include columns for date, time, systolic, diastolic, and pulse
    
    **Exercise CSV**: Must include columns for date, time, exercise_type, duration_minutes, and intensity
    """)
    
else:
    # Determine current date range for display
    if hasattr(st.session_state, 'bp_data') and st.session_state.bp_data is not None:
        current_start_date = st.session_state.bp_data['date'].min().date()
        current_end_date = st.session_state.bp_data['date'].max().date()
    elif hasattr(st.session_state, 'exercise_data') and st.session_state.exercise_data is not None:
        current_start_date = st.session_state.exercise_data['date'].min().date()
        current_end_date = st.session_state.exercise_data['date'].max().date()
    else:
        current_start_date = datetime.now().date() - timedelta(days=90)
        current_end_date = datetime.now().date()

    # Create the dashboard
    create_dashboard(
        st.session_state.categorized_bp_data,
        st.session_state.exercise_data,
        st.session_state.correlation_results,
        (current_start_date, current_end_date),
        st.session_state.get('patient_info'),
        st.session_state.get('fhir_data')
    )    
    # Add recommendation generation to the Recommendations tab
    if st.session_state.current_tab == 4:  # Recommendations tab
        st.subheader("Generate Personalized Exercise Recommendations")
        
        # Check if we have the necessary data
        if (st.session_state.categorized_bp_data is None or 
            st.session_state.exercise_data is None or 
            st.session_state.correlation_results is None):
            st.warning("Both blood pressure and exercise data are required to generate recommendations.")
        else:
            # Add button to generate recommendations
            if st.button("Generate Personalized Recommendations"):
                with st.spinner("Analyzing your data and generating personalized recommendations..."):
                    try:
                        # Get API key from environment variable
                        api_key = "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"
                        
                        if not api_key:
                            st.error("OpenRouter API key not found. Please set the OPENROUTER_API_KEY environment variable.")
                        else:
                            # Initialize recommendation engine
                            recommendation_engine = LLMRecommendationEngine(api_key=api_key)
                            
                            # Prepare user data
                            user_data = st.session_state.get('user_info', {})
                            
                            # Prepare BP stats
                            bp_data = st.session_state.categorized_bp_data
                            bp_stats = {
                                'avg_systolic': bp_data['systolic'].mean(),
                                'avg_diastolic': bp_data['diastolic'].mean(),
                                'max_systolic': bp_data['systolic'].max(),
                                'min_systolic': bp_data['systolic'].min(),
                                'max_diastolic': bp_data['diastolic'].max(),
                                'min_diastolic': bp_data['diastolic'].min()
                            }
                            
                            # Add category distribution
                            category_counts = bp_data['category'].value_counts()
                            total = len(bp_data)
                            bp_stats['category_distribution'] = {
                                cat: count / total * 100 
                                for cat, count in category_counts.items()
                            }
                            
                            # Get correlation summary
                            correlation_summary = st.session_state.correlation_results.get('overall_correlation', {})
                            
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
                            type_impact = st.session_state.correlation_results.get('exercise_type_impact', {})
                            for ex_type, impact in type_impact.items():
                                sys_change = impact.get('avg_systolic_change', 0)
                                dia_change = impact.get('avg_diastolic_change', 0)
                                
                                if (abs(sys_change) > 5 or abs(dia_change) > 3) and impact.get('count', 0) >= 3:
                                    direction = "decrease" if (sys_change < 0 and dia_change < 0) else "increase"
                                    correlation_summary['interpretations'].append(
                                        f"{ex_type} appears to {direction} your blood pressure by an average of {abs(sys_change):.1f}/{abs(dia_change):.1f} mmHg."
                                    )
                            
                            # Get recent exercise history
                            exercise_history = st.session_state.exercise_data.sort_values('date', ascending=False).head(10)
                            
                            # Generate recommendations
                            recommendation_response = recommendation_engine.generate_recommendations(
                                user_data, 
                                correlation_summary, 
                                bp_stats, 
                                exercise_history,
                                st.session_state.fhir_data
                            )
                            
                            if recommendation_response.get('status') == 'success':
                                st.session_state.recommendation = recommendation_response
                                
                                # Create a summary card
                                create_recommendation_summary_card(
                                    recommendation_response, 
                                    st.session_state.patient_info
                                )
                                
                                # Display full recommendations
                                display_recommendations(recommendation_response)
                                
                                st.success("Recommendations generated successfully!")
                            else:
                                st.error(f"Failed to generate recommendations: {recommendation_response.get('message')}")
                    
                    except Exception as e:
                        st.error(f"Error generating recommendations: {str(e)}")

# Add footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p>Heart Health Tracker - Exercise Impact Dashboard & LLM-Powered Recommendations</p>
        <p>Created by: Chetan Reddy Bojja, Kartheek Bellamkonda, Rishitha Komatineni</p>
    </div>
    """,
    unsafe_allow_html=True
)