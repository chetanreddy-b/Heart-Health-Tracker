import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_exercise_bp_correlation_plot(correlation_results):
    """
    Create a scatter plot showing correlation between exercise intensity and BP changes
    
    Parameters:
    - correlation_results: Dictionary with correlation analysis results
    
    Returns:
    Plotly figure
    """
    if (correlation_results is None or 
        'exercise_impact_data' not in correlation_results or 
        correlation_results['exercise_impact_data'] is None or 
        len(correlation_results['exercise_impact_data']) == 0):
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No correlation data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Get impact data
    impact_data = correlation_results['exercise_impact_data']
    
    # Create scatter plot for systolic BP
    fig = px.scatter(
        impact_data, 
        x='intensity_score', 
        y='systolic_change',
        color='exercise_type',
        size='duration_minutes',
        hover_data=['intensity', 'baseline_systolic', 'avg_after_systolic'],
        title='Exercise Intensity vs. Systolic BP Change',
        labels={
            'intensity_score': 'Exercise Intensity Score',
            'systolic_change': 'Systolic BP Change (mmHg)',
            'exercise_type': 'Exercise Type',
            'duration_minutes': 'Duration (min)'
        }
    )
    
    # Add regression line
    if len(impact_data) >= 5:
        # Calculate regression line
        x = impact_data['intensity_score']
        y = impact_data['systolic_change']
        
        # Add line of best fit
        fig.add_trace(go.Scatter(
            x=x,
            y=np.poly1d(np.polyfit(x, y, 1))(x),
            mode='lines',
            name='Trend',
            line=dict(color='rgba(0,0,0,0.5)', width=2, dash='dash')
        ))
        
        # Add correlation coefficient
        correlation = correlation_results['overall_correlation'].get('systolic', {})
        if 'correlation' in correlation:
            corr_value = correlation['correlation']
            p_value = correlation.get('p_value', 1.0)
            significant = correlation.get('significant', False)
            
            annotation_text = f"Correlation: {corr_value:.3f}"
            if significant:
                annotation_text += " (significant)"
            
            fig.add_annotation(
                xref="paper", yref="paper",
                x=0.02, y=0.98,
                text=annotation_text,
                showarrow=False,
                font=dict(
                    size=12,
                    color="black" if significant else "gray"
                ),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0.5)",
                borderwidth=1,
                borderpad=4,
                align="left"
            )
    
    # Add zero line
    fig.add_shape(
        type="line",
        x0=min(impact_data['intensity_score']),
        x1=max(impact_data['intensity_score']),
        y0=0, y1=0,
        line=dict(color="red", width=1, dash="dot"),
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title='Exercise Intensity Score',
        yaxis_title='Systolic BP Change (mmHg)',
        template='plotly_white',
        height=450
    )
    
    # Add hover template
    fig.update_traces(
        hovertemplate='<b>%{customdata[0]} %{hovertext}</b><br>Intensity Score: %{x:.2f}<br>Systolic Change: %{y:.1f} mmHg<br>Duration: %{marker.size} min<br>Baseline: %{customdata[1]} mmHg<br>After: %{customdata[2]:.1f} mmHg<extra></extra>'
    )
    
    return fig

def create_diastolic_correlation_plot(correlation_results):
    """
    Create a scatter plot showing correlation between exercise intensity and diastolic BP changes
    
    Parameters:
    - correlation_results: Dictionary with correlation analysis results
    
    Returns:
    Plotly figure
    """
    if (correlation_results is None or 
        'exercise_impact_data' not in correlation_results or 
        correlation_results['exercise_impact_data'] is None or 
        len(correlation_results['exercise_impact_data']) == 0):
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No correlation data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Get impact data
    impact_data = correlation_results['exercise_impact_data']
    
    # Create scatter plot for diastolic BP
    fig = px.scatter(
        impact_data, 
        x='intensity_score', 
        y='diastolic_change',
        color='exercise_type',
        size='duration_minutes',
        hover_data=['intensity', 'baseline_diastolic', 'avg_after_diastolic'],
        title='Exercise Intensity vs. Diastolic BP Change',
        labels={
            'intensity_score': 'Exercise Intensity Score',
            'diastolic_change': 'Diastolic BP Change (mmHg)',
            'exercise_type': 'Exercise Type',
            'duration_minutes': 'Duration (min)'
        }
    )
    
    # Add regression line
    if len(impact_data) >= 5:
        # Calculate regression line
        x = impact_data['intensity_score']
        y = impact_data['diastolic_change']
        
        # Add line of best fit
        fig.add_trace(go.Scatter(
            x=x,
            y=np.poly1d(np.polyfit(x, y, 1))(x),
            mode='lines',
            name='Trend',
            line=dict(color='rgba(0,0,0,0.5)', width=2, dash='dash')
        ))
        
        # Add correlation coefficient
        correlation = correlation_results['overall_correlation'].get('diastolic', {})
        if 'correlation' in correlation:
            corr_value = correlation['correlation']
            p_value = correlation.get('p_value', 1.0)
            significant = correlation.get('significant', False)
            
            annotation_text = f"Correlation: {corr_value:.3f}"
            if significant:
                annotation_text += " (significant)"
            
            fig.add_annotation(
                xref="paper", yref="paper",
                x=0.02, y=0.98,
                text=annotation_text,
                showarrow=False,
                font=dict(
                    size=12,
                    color="black" if significant else "gray"
                ),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0.5)",
                borderwidth=1,
                borderpad=4,
                align="left"
            )
    
    # Add zero line
    fig.add_shape(
        type="line",
        x0=min(impact_data['intensity_score']),
        x1=max(impact_data['intensity_score']),
        y0=0, y1=0,
        line=dict(color="red", width=1, dash="dot"),
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title='Exercise Intensity Score',
        yaxis_title='Diastolic BP Change (mmHg)',
        template='plotly_white',
        height=450
    )
    
    # Add hover template
    fig.update_traces(
        hovertemplate='<b>%{customdata[0]} %{hovertext}</b><br>Intensity Score: %{x:.2f}<br>Diastolic Change: %{y:.1f} mmHg<br>Duration: %{marker.size} min<br>Baseline: %{customdata[1]} mmHg<br>After: %{customdata[2]:.1f} mmHg<extra></extra>'
    )
    
    return fig

def create_exercise_type_impact_chart(correlation_results):
    """
    Create a bar chart showing the impact of different exercise types on BP
    
    Parameters:
    - correlation_results: Dictionary with correlation analysis results
    
    Returns:
    Plotly figure
    """
    if (correlation_results is None or 
        'exercise_type_impact' not in correlation_results or 
        not correlation_results['exercise_type_impact']):
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No exercise type impact data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Extract exercise type impact data
    type_impact = correlation_results['exercise_type_impact']
    
    # Prepare data for plotting
    exercise_types = []
    systolic_changes = []
    diastolic_changes = []
    counts = []
    
    for ex_type, impact in type_impact.items():
        if impact.get('count', 0) >= 2:  # Only include types with at least 2 data points
            exercise_types.append(ex_type)
            systolic_changes.append(impact.get('avg_systolic_change', 0))
            diastolic_changes.append(impact.get('avg_diastolic_change', 0))
            counts.append(impact.get('count', 0))
    
    if not exercise_types:
        # No valid exercise types found
        fig = go.Figure()
        fig.add_annotation(
            text="Insufficient data for exercise type analysis",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Create figure
    fig = go.Figure()
    
    # Add systolic bars
    fig.add_trace(go.Bar(
        x=exercise_types,
        y=systolic_changes,
        name='Systolic Change',
        marker_color='#ff7f0e',
        text=counts,
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Systolic Change: %{y:.1f} mmHg<br>Sessions: %{text}<extra></extra>'
    ))
    
    # Add diastolic bars
    fig.add_trace(go.Bar(
        x=exercise_types,
        y=diastolic_changes,
        name='Diastolic Change',
        marker_color='#1f77b4',
        text=counts,
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Diastolic Change: %{y:.1f} mmHg<br>Sessions: %{text}<extra></extra>'
    ))
    
    # Add zero line
    fig.add_shape(
        type="line",
        x0=-0.5,
        x1=len(exercise_types) - 0.5,
        y0=0, y1=0,
        line=dict(color="black", width=1, dash="dot"),
    )
    
    # Update layout
    fig.update_layout(
        title='Average BP Change by Exercise Type',
        xaxis_title='Exercise Type',
        yaxis_title='Blood Pressure Change (mmHg)',
        template='plotly_white',
        height=400,
        barmode='group'
    )
    
    return fig

def create_correlation_summary_card(correlation_results):
    """
    Create a text summary of correlation findings
    
    Parameters:
    - correlation_results: Dictionary with correlation analysis results
    
    Returns:
    Plotly figure with text annotations
    """
    if correlation_results is None or 'overall_correlation' not in correlation_results:
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No correlation data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Extract correlation summary
    summary = correlation_results.get('overall_correlation', {})
    
    # Create figure
    fig = go.Figure()
    
    # Add systolic correlation
    systolic = summary.get('systolic', {})
    systolic_corr = systolic.get('correlation', 0)
    systolic_sig = systolic.get('significant', False)
    
    systolic_text = f"Systolic BP Correlation: {systolic_corr:.3f}"
    if systolic_sig:
        systolic_text += " (statistically significant)"
    
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=0.8,
        text=systolic_text,
        showarrow=False,
        font=dict(
            size=14,
            color="black" if systolic_sig else "gray"
        ),
        align="center"
    )
    
    # Add diastolic correlation
    diastolic = summary.get('diastolic', {})
    diastolic_corr = diastolic.get('correlation', 0)
    diastolic_sig = diastolic.get('significant', False)
    
    diastolic_text = f"Diastolic BP Correlation: {diastolic_corr:.3f}"
    if diastolic_sig:
        diastolic_text += " (statistically significant)"
    
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=0.6,
        text=diastolic_text,
        showarrow=False,
        font=dict(
            size=14,
            color="black" if diastolic_sig else "gray"
        ),
        align="center"
    )
    
    # Add interpretations
    interpretations = correlation_results.get('interpretations', [])
    if interpretations:
        y_pos = 0.4
        for interpretation in interpretations[:3]:  # Limit to 3 interpretations
            fig.add_annotation(
                xref="paper", yref="paper",
                x=0.5, y=y_pos,
                text=interpretation,
                showarrow=False,
                font=dict(size=12),
                align="center",
                width=500
            )
            y_pos -= 0.1
    
    # Update layout
    fig.update_layout(
        title='Correlation Analysis Summary',
        template='plotly_white',
        height=300,
        showlegend=False
    )
    
    return fig

def create_combined_timeline(bp_data, exercise_data):
    """
    Create a combined timeline showing both BP readings and exercise events
    
    Parameters:
    - bp_data: DataFrame with blood pressure readings
    - exercise_data: DataFrame with exercise records
    
    Returns:
    Plotly figure
    """
    if (bp_data is None or len(bp_data) == 0) and (exercise_data is None or len(exercise_data) == 0):
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for timeline",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Create figure
    fig = go.Figure()
    
    # Add BP data if available
    if bp_data is not None and len(bp_data) > 0:
        # Sort by date
        sorted_bp = bp_data.sort_values('datetime')
        
        # Add systolic line
        fig.add_trace(go.Scatter(
            x=sorted_bp['datetime'],
            y=sorted_bp['systolic'],
            mode='lines+markers',
            name='Systolic BP',
            line=dict(color='#ff7f0e', width=2),
            marker=dict(
                size=8,
                color=sorted_bp['category_color'],
                line=dict(width=1, color='#333')
            )
        ))
        
        # Add diastolic line
        fig.add_trace(go.Scatter(
            x=sorted_bp['datetime'],
            y=sorted_bp['diastolic'],
            mode='lines+markers',
            name='Diastolic BP',
            line=dict(color='#1f77b4', width=2),
            marker=dict(
                size=8,
                color=sorted_bp['category_color'],
                line=dict(width=1, color='#333')
            )
        ))
    
    # Add exercise data if available
    if exercise_data is not None and len(exercise_data) > 0:
        # Sort by date
        sorted_exercise = exercise_data.sort_values('datetime')
        
        # Map intensity to numeric value for y-axis position
        intensity_map = {'Low': 40, 'Moderate': 50, 'High': 60}
        sorted_exercise['y_position'] = sorted_exercise['intensity'].map(intensity_map)
        
        # Create color map
        type_colors = {}
        ex_types = sorted_exercise['exercise_type'].unique()
        colors = px.colors.qualitative.Set3[:len(ex_types)]
        for i, ex_type in enumerate(ex_types):
            type_colors[ex_type] = colors[i]
        
        # Add exercise markers
        fig.add_trace(go.Scatter(
            x=sorted_exercise['datetime'],
            y=sorted_exercise['y_position'],
            mode='markers',
            name='Exercise',
            marker=dict(
                size=sorted_exercise['duration_minutes'] / 5 + 10,
                color=[type_colors[t] for t in sorted_exercise['exercise_type']],
                line=dict(width=1, color='#333'),
                symbol='star'
            ),
            text=sorted_exercise['exercise_type'],
            hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Intensity: %{customdata[0]}<br>Duration: %{customdata[1]} min<extra></extra>',
            customdata=sorted_exercise[['intensity', 'duration_minutes']]
        ))
    
    # Add reference lines for BP categories
    if bp_data is not None and len(bp_data) > 0:
        min_date = min(sorted_bp['datetime'])
        max_date = max(sorted_bp['datetime'])
        
        fig.add_shape(
            type="line",
            x0=min_date,
            x1=max_date,
            y0=120, y1=120,
            line=dict(color="#2ecc71", width=1, dash="dash"),
            name="Normal Systolic Threshold"
        )
        
        fig.add_shape(
            type="line",
            x0=min_date,
            x1=max_date,
            y0=130, y1=130,
            line=dict(color="#f1c40f", width=1, dash="dash"),
            name="Elevated Systolic Threshold"
        )
        
        fig.add_shape(
            type="line",
            x0=min_date,
            x1=max_date,
            y0=140, y1=140,
            line=dict(color="#e74c3c", width=1, dash="dash"),
            name="Stage 1 Hypertension Threshold"
        )
        
        fig.add_shape(
            type="line",
            x0=min_date,
            x1=max_date,
            y0=80, y1=80,
            line=dict(color="#2ecc71", width=1, dash="dot"),
            name="Normal Diastolic Threshold"
        )
        
        fig.add_shape(
            type="line",
            x0=min_date,
            x1=max_date,
            y0=90, y1=90,
            line=dict(color="#e74c3c", width=1, dash="dot"),
            name="Stage 1 Hypertension Diastolic Threshold"
        )
    
    # Update layout
    fig.update_layout(
        title='Combined Blood Pressure and Exercise Timeline',
        xaxis_title='Date',
        yaxis_title='Blood Pressure (mmHg) / Exercise',
        template='plotly_white',
        height=500,
        hovermode='closest'
    )
    
    # Add exercise intensity legend as annotations
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.01, y=0.15,
        text="◆ Low Intensity",
        showarrow=False,
        font=dict(size=10),
        align="left"
    )
    
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.01, y=0.12,
        text="◆ Moderate Intensity",
        showarrow=False,
        font=dict(size=10),
        align="left"
    )
    
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.01, y=0.09,
        text="◆ High Intensity",
        showarrow=False,
        font=dict(size=10),
        align="left"
    )
    
    return fig