import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import html

def display_recommendations(recommendation):
    """
    Display the LLM-generated exercise recommendations in a visually appealing format
    
    Parameters:
    - recommendation: Dictionary with recommendation information
    """
    if not recommendation or "status" not in recommendation or recommendation["status"] != "success":
        st.error("No valid recommendation data available")
        return
        
    recommendation_data = recommendation.get("recommendation", {})
    
    # If HTML version is available, use it
    if "html" in recommendation_data:
        display_html_recommendation(recommendation_data)
    else:
        display_text_recommendation(recommendation_data)

def display_html_recommendation(recommendation_data):
    """Display recommendations using the HTML formatted version"""
    
    # Add custom CSS for better styling
    st.markdown("""
    <style>
    .recommendation-section {
        margin-bottom: 30px;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .summary-section {
        background-color: #f0f7ff;
        border-left: 5px solid #4a86e8;
    }
    .plan-section {
        background-color: #f2fff0;
        border-left: 5px solid #6aa84f;
    }
    .insights-section {
        background-color: #fff6e9;
        border-left: 5px solid #e69138;
    }
    .monitoring-section {
        background-color: #f9f0ff;
        border-left: 5px solid #a64d79;
    }
    .section-title {
        color: #333;
        font-size: 24px;
        margin-top: 0;
        margin-bottom: 15px;
    }
    .section-content {
        font-size: 16px;
        line-height: 1.6;
    }
    .section-content h2 {
        font-size: 22px;
        margin-top: 20px;
        margin-bottom: 10px;
        color: #333;
    }
    .section-content h3 {
        font-size: 20px;
        margin-top: 15px;
        margin-bottom: 10px;
        color: #444;
    }
    .section-content h4 {
        font-size: 18px;
        margin-top: 15px;
        margin-bottom: 8px;
        color: #555;
    }
    .section-content ul {
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .section-content li {
        margin-bottom: 5px;
    }
    .section-content p {
        margin-bottom: 15px;
    }
    .section-content strong {
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the HTML formatted content
    st.markdown(recommendation_data["html"], unsafe_allow_html=True)
    
    # Add interactive exercise visuals if available
    if "plan" in recommendation_data:
        display_exercise_visuals(recommendation_data["plan"])

def display_text_recommendation(recommendation_data):
    """Display recommendations using markdown formatted text sections"""
    # if "summary" in recommendation_data:
    #     st.subheader("Summary of Analysis")
    #     st.markdown(recommendation_data["summary"])
        
    if "plan" in recommendation_data:
        st.subheader("Weekly Exercise Plan")
        st.markdown(recommendation_data["plan"])
        
        # Add interactive exercise visuals
        display_exercise_visuals(recommendation_data["plan"])
        
    if "insights" in recommendation_data:
        st.subheader("Key Insights and Guidelines")
        st.markdown(recommendation_data["insights"])
        
    if "monitoring" in recommendation_data:
        st.subheader("Monitoring Recommendations")
        st.markdown(recommendation_data["monitoring"])
        
    if "full_text" in recommendation_data:
        st.markdown(recommendation_data["full_text"])

# def display_exercise_visuals(plan_text):
#     """Extract exercise data from plan text and display visualizations"""
#     # Only show visualizations if we have enough content
#     if len(plan_text) < 100:
#         return
        
#     with st.expander("📊 Exercise Plan Visualizations", expanded=True):
#         col1, col2 = st.columns(2)
        
#         # Extract exercise types and durations from the plan text
#         import re
        
#         # Find all exercise activities with durations
#         exercise_pattern = r'(?:minute|min)(?:s)?\s+([A-Za-z\s]+)'
#         duration_pattern = r'(\d+)(?:-|\s+to\s+)?(\d+)?\s+(?:minute|min)'
        
#         activities = re.findall(exercise_pattern, plan_text.lower())
#         durations = re.findall(duration_pattern, plan_text)
        
#         # Process durations (take average if range is given)
#         processed_durations = []
#         for duration_match in durations:
#             if duration_match[1]:  # If it's a range
#                 avg_duration = (int(duration_match[0]) + int(duration_match[1])) / 2
#                 processed_durations.append(avg_duration)
#             else:
#                 processed_durations.append(int(duration_match[0]))
        
#         # Clean up activities
#         cleaned_activities = []
#         excluded_words = ['at', 'with', 'of', 'and', 'or', 'for', 'the', 'to']
#         for activity in activities:
#             activity = activity.strip()
#             words = activity.split()
#             activity = ' '.join([w for w in words if w not in excluded_words and len(w) > 2])
#             if activity:
#                 cleaned_activities.append(activity)
        
#         # If we have enough activities and durations, create visualizations
#         if len(cleaned_activities) >= 3 and len(processed_durations) >= 3:
#             # Match durations to activities (take min to avoid index out of bounds)
#             activity_data = []
#             for i in range(min(len(cleaned_activities), len(processed_durations))):
#                 activity_data.append({
#                     'Activity': cleaned_activities[i].title(),
#                     'Duration (min)': processed_durations[i]
#                 })
            
#             activity_df = pd.DataFrame(activity_data)
            
#             # Group by activity and sum durations
#             grouped_df = activity_df.groupby('Activity')['Duration (min)'].sum().reset_index()
            
#             with col1:
#                 # Create a bar chart of activity durations with improved styling
#                 fig = px.bar(
#                     grouped_df, 
#                     x='Activity', 
#                     y='Duration (min)',
#                     title='Weekly Exercise Duration by Activity',
#                     color='Duration (min)',
#                     color_continuous_scale='Viridis',
#                     labels={'Duration (min)': 'Minutes'},
#                     text='Duration (min)'
#                 )
#                 fig.update_traces(
#                     texttemplate='%{text:.0f}',
#                     textposition='outside',
#                     marker_line_color='rgb(8,48,107)',
#                     marker_line_width=1.5,
#                     opacity=0.8
#                 )
#                 fig.update_layout(
#                     height=400,
#                     title_font_size=16,
#                     xaxis_title='Exercise Type',
#                     yaxis_title='Total Duration (minutes)',
#                     plot_bgcolor='rgba(240,240,240,0.5)',
#                     paper_bgcolor='white'
#                 )
#                 st.plotly_chart(fig, use_container_width=True)
            
#             with col2:
#                 # Create a pie chart showing distribution of exercise types with improved styling
#                 fig = px.pie(
#                     grouped_df, 
#                     names='Activity', 
#                     values='Duration (min)',
#                     title='Exercise Type Distribution',
#                     hole=0.4,
#                     color_discrete_sequence=px.colors.qualitative.Pastel
#                 )
#                 fig.update_traces(
#                     textinfo='percent+label', 
#                     textposition='inside',
#                     marker=dict(line=dict(color='#FFFFFF', width=2))
#                 )
#                 fig.update_layout(
#                     height=400,
#                     title_font_size=16,
#                     legend_title_text='Exercise Types',
#                     plot_bgcolor='rgba(240,240,240,0.5)',
#                     paper_bgcolor='white'
#                 )
#                 st.plotly_chart(fig, use_container_width=True)
        
#         # Extract daily exercise pattern from plan text
#         day_pattern = r'(?:^|\n)###\s+([A-Za-z]+day)'
#         days = re.findall(day_pattern, plan_text)
        
#         if days:
#             # Create a calendar heatmap visualization
#             st.subheader("Weekly Exercise Schedule")
            
#             # Standardize day names and create order
#             day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#             day_mapping = {
#                 "mon": "Monday", "tue": "Tuesday", "wed": "Wednesday",
#                 "thu": "Thursday", "fri": "Friday", "sat": "Saturday", "sun": "Sunday"
#             }
            
#             # Map found days to standard format
#             standard_days = []
#             for day in days:
#                 day_lower = day.lower()
#                 for short, full in day_mapping.items():
#                     if day_lower.startswith(short):
#                         standard_days.append(full)
#                         break
#                 else:
#                     # If no match found, use as is
#                     standard_days.append(day)
            
#             # Create a binary matrix of which days have activities
#             activity_days = {day: day in standard_days for day in day_order}
            
#             # Create calendar visualization
#             fig = go.Figure()
            
#             # Set up the color scale with more vibrant colors
#             colors = ['#E6E6E6', '#2ECC71']
            
#             # Add rectangles for each day
#             for i, day in enumerate(day_order):
#                 fig.add_trace(go.Scatter(
#                     x=[0.5],
#                     y=[i],
#                     mode='markers',
#                     marker=dict(
#                         symbol='square',
#                         size=40,
#                         color=colors[1] if activity_days[day] else colors[0],
#                         line=dict(width=2, color='#333333')
#                     ),
#                     name=day,
#                     hoverinfo='text',
#                     text=f"{day}: {'Exercise scheduled' if activity_days[day] else 'Rest day'}"
#                 ))
            
#             # Add day labels
#             for i, day in enumerate(day_order):
#                 fig.add_annotation(
#                     x=0.5,
#                     y=i,
#                     text=day[:3],
#                     showarrow=False,
#                     font=dict(color='white' if activity_days[day] else 'black', size=14, family='Arial Black')
#                 )
            
#             # Update layout with modern styling
#             fig.update_layout(
#                 title="Weekly Exercise Schedule",
#                 title_font_size=16,
#                 showlegend=False,
#                 height=350,
#                 xaxis=dict(
#                     showgrid=False,
#                     zeroline=False,
#                     showticklabels=False,
#                     range=[0, 1]
#                 ),
#                 yaxis=dict(
#                     showgrid=False,
#                     zeroline=False,
#                     showticklabels=False,
#                     range=[-0.5, len(day_order) - 0.5]
#                 ),
#                 plot_bgcolor='white',
#                 paper_bgcolor='white',
#                 margin=dict(l=20, r=20, t=50, b=20)
#             )
            
#             st.plotly_chart(fig, use_container_width=True)
def create_recommendation_summary_card(recommendation, patient_info=None):
    """Create a summary card for recommendations with patient information"""
    if not recommendation or "recommendation" not in recommendation:
        return
    
    recommendation_data = recommendation["recommendation"]
    if not recommendation_data:
        return
    
    # Create card container with more modern, appealing design
    st.markdown("""
    <style>
    .recommendation-card {
        background: linear-gradient(135deg, #f6f8f9 0%, #e5ebee 100%);
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        padding: 25px;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .recommendation-card:hover {
        transform: translateY(-5px);
    }
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        border-bottom: 2px solid rgba(0,0,0,0.1);
        padding-bottom: 15px;
    }
    .patient-avatar {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(45deg, #4a86e8, #6a89cc);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 20px;
        color: white;
        font-size: 28px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .patient-details {
        flex-grow: 1;
    }
    .patient-name {
        font-size: 22px;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
        line-height: 1.3;
    }
    .patient-meta {
        font-size: 14px;
        color: #7f8c8d;
        margin: 5px 0 0 0;
    }
    .recommendation-summary {
        background-color: rgba(255,255,255,0.7);
        border-left: 5px solid #4a86e8;
        padding: 15px;
        border-radius: 5px;
        font-size: 16px;
        line-height: 1.6;
        color: #2c3e50;
        margin-top: 15px;
        min-height: 50px;
    }
    .card-badge {
        position: absolute;
        top: 15px;
        right: 15px;
        background-color: #4a86e8;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Start card
    card_html = '<div class="recommendation-card">'
    
    # Add patient info if available
    if patient_info:
        name = patient_info.get("name", "Unknown")
        initials = "".join([n[0].upper() for n in name.split() if n])
        age = patient_info.get("age", "")
        gender = patient_info.get("gender", "").capitalize()
        bp_category = patient_info.get("bp_category", "")
        
        card_html += f'''
        <div class="card-badge">Personalized Plan</div>
        <div class="card-header">
            <div class="patient-avatar">{initials}</div>
            <div class="patient-details">
                <p class="patient-name">{html.escape(name)}</p>
                <p class="patient-meta">{age} years • {gender} • BP: {bp_category}</p>
            </div>
        </div>
        '''
    
    # Add recommendation summary
    summary = ""
    
    # Prioritize summary extraction methods
    summary_sources = [
        lambda: recommendation_data.get("summary", "").strip(),
        lambda: next((line.strip() for line in recommendation_data.get("summary", "").split('\n') if line.strip() and line.strip() != ':'), ""),
        lambda: recommendation_data.get("full_text", "")[:300].strip(),
        lambda: "Personalized exercise plan generated based on your health data."
    ]
    
    # Try each summary source until we get a non-empty summary
    for source in summary_sources:
        summary = source()
        if summary and summary != ':':
            break
    
    # Ensure summary is not just a colon or empty
    if summary and summary != ':':
        # Truncate if too long
        if len(summary) > 30000:
            summary = summary[:30000] + "..."
        
        card_html += f'<div class="recommendation-summary">{html.escape(summary)}</div>'
    else:
        # Fallback summary if nothing works
        card_html += '<div class="recommendation-summary">Personalized exercise recommendations generated to support your cardiovascular health.</div>'
    
    # Close card
    card_html += '</div>'
    
    st.markdown(card_html, unsafe_allow_html=True)


def display_exercise_visuals(plan_text):
    """Extract exercise data from plan text and display visualizations"""
    # Validation and early return
    if not plan_text or len(plan_text) < 50:
        return

    with st.expander("📊 Exercise Plan Visualizations", expanded=True):
        # Improved error handling and logging
        try:
            # Extract exercise types and durations
            import re
            import pandas as pd
            import plotly.express as px
            
            # More comprehensive parsing patterns
            def extract_exercises(text):
                exercises = []
                # Pattern 1: Duration followed by activity
                pattern1 = r'(\d+)(?:-|\s+to\s+)?(\d+)?\s*(?:minute|min)\s+([A-Za-z\s]+)'
                # Pattern 2: Activity followed by duration
                pattern2 = r'([A-Za-z\s]+)\s*:\s*(\d+)(?:-|\s+to\s+)?(\d+)?\s*(?:minute|min)'
                
                # Combine patterns
                all_matches = re.findall(pattern1, text, re.IGNORECASE) + \
                               re.findall(pattern2, text, re.IGNORECASE)
                
                for match in all_matches:
                    # Handle different match lengths
                    if len(match) == 3:
                        try:
                            # Pattern 1 style match
                            duration = int(match[0])
                            activity = match[2].strip()
                        except:
                            continue
                    elif len(match) == 2:
                        try:
                            # Pattern 2 style match
                            duration = int(match[1])
                            activity = match[0].strip()
                        except:
                            continue
                    
                    # Clean up activity name
                    activity = re.sub(r'\s+', ' ', activity).strip()
                    
                    # Validate and add
                    if activity and duration:
                        exercises.append({
                            'Activity': activity.title(),
                            'Duration (min)': duration
                        })
                
                return exercises
            
            # Extract exercises
            exercises = extract_exercises(plan_text)
            
            # Validate data
            if not exercises:
                st.info("Unable to extract detailed exercise information.")
                return
            
            # Create DataFrame
            activity_df = pd.DataFrame(exercises)
            
            # Group and aggregate
            grouped_df = activity_df.groupby('Activity')['Duration (min)'].sum().reset_index()
            
            # Ensure multiple activities for visualization
            if len(grouped_df) < 2:
                st.info("Not enough exercise variety to generate meaningful visualizations.")
                return
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Bar Chart with improved styling
                fig1 = px.bar(
                    grouped_df, 
                    x='Activity', 
                    y='Duration (min)',
                    title='Weekly Exercise Duration',
                    text='Duration (min)',
                    color='Duration (min)',
                    color_continuous_scale='Viridis'
                )
                fig1.update_traces(
                    texttemplate='%{text} min',
                    textposition='outside'
                )
                fig1.update_layout(
                    height=400, 
                    title_x=0.5,
                    xaxis_title='Exercise Type',
                    yaxis_title='Total Duration (minutes)'
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Pie Chart with improved styling
                fig2 = px.pie(
                    grouped_df, 
                    names='Activity', 
                    values='Duration (min)',
                    title='Exercise Type Distribution',
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig2.update_traces(
                    textinfo='percent+label', 
                    textposition='inside'
                )
                fig2.update_layout(
                    height=400, 
                    title_x=0.5
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error generating visualizations: {str(e)}")
            # Log the error for debugging
            import traceback
            traceback.print_exc()