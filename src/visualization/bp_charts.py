import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_bp_trend_chart(bp_data):
    """
    Create a time series chart of blood pressure readings
    
    Parameters:
    - bp_data: DataFrame with blood pressure readings including categories
    
    Returns:
    Plotly figure
    """
    if bp_data is None or len(bp_data) == 0:
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No blood pressure data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Sort by date and time
    sorted_data = bp_data.sort_values('datetime')
    
    # Create figure
    fig = go.Figure()
    
    # Add systolic line
    fig.add_trace(go.Scatter(
        x=sorted_data['datetime'],
        y=sorted_data['systolic'],
        mode='lines+markers',
        name='Systolic',
        line=dict(color='#ff7f0e', width=2),
        marker=dict(
            size=8,
            color=sorted_data['category_color'],
            line=dict(width=1, color='#333')
        )
    ))
    
    # Add diastolic line
    fig.add_trace(go.Scatter(
        x=sorted_data['datetime'],
        y=sorted_data['diastolic'],
        mode='lines+markers',
        name='Diastolic',
        line=dict(color='#1f77b4', width=2),
        marker=dict(
            size=8,
            color=sorted_data['category_color'],
            line=dict(width=1, color='#333')
        )
    ))
    
    # Add reference lines for BP categories
    fig.add_shape(
        type="line",
        x0=sorted_data['datetime'].min(),
        x1=sorted_data['datetime'].max(),
        y0=120, y1=120,
        line=dict(color="#2ecc71", width=1, dash="dash"),
        name="Normal Systolic Threshold"
    )
    
    fig.add_shape(
        type="line",
        x0=sorted_data['datetime'].min(),
        x1=sorted_data['datetime'].max(),
        y0=130, y1=130,
        line=dict(color="#f1c40f", width=1, dash="dash"),
        name="Elevated Systolic Threshold"
    )
    
    fig.add_shape(
        type="line",
        x0=sorted_data['datetime'].min(),
        x1=sorted_data['datetime'].max(),
        y0=140, y1=140,
        line=dict(color="#e74c3c", width=1, dash="dash"),
        name="Stage 1 Hypertension Threshold"
    )
    
    fig.add_shape(
        type="line",
        x0=sorted_data['datetime'].min(),
        x1=sorted_data['datetime'].max(),
        y0=80, y1=80,
        line=dict(color="#2ecc71", width=1, dash="dot"),
        name="Normal Diastolic Threshold"
    )
    
    fig.add_shape(
        type="line",
        x0=sorted_data['datetime'].min(),
        x1=sorted_data['datetime'].max(),
        y0=90, y1=90,
        line=dict(color="#e74c3c", width=1, dash="dot"),
        name="Stage 1 Hypertension Diastolic Threshold"
    )
    
    # Update layout
    fig.update_layout(
        title='Blood Pressure Trend',
        xaxis_title='Date',
        yaxis_title='Blood Pressure (mmHg)',
        legend_title='Measurement',
        hovermode='closest',
        template='plotly_white',
        height=500
    )
    
    # Add hover template
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>%{y} mmHg<extra></extra>'
    )
    
    return fig

def create_bp_category_distribution(bp_data):
    """
    Create a pie chart showing distribution of BP categories
    
    Parameters:
    - bp_data: DataFrame with categorized blood pressure readings
    
    Returns:
    Plotly figure
    """
    if bp_data is None or len(bp_data) == 0:
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No blood pressure data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Count categories
    category_counts = bp_data['category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']
    
    # Get colors for each category
    category_colors = {}
    for cat in category_counts['Category']:
        color = bp_data[bp_data['category'] == cat]['category_color'].iloc[0]
        category_colors[cat] = color
    
    # Create pie chart
    fig = px.pie(
        category_counts, 
        values='Count', 
        names='Category',
        color='Category',
        color_discrete_map=category_colors,
        title='Blood Pressure Category Distribution'
    )
    
    # Update layout
    fig.update_layout(
        legend_title='BP Category',
        template='plotly_white',
        height=400
    )
    
    # Update traces
    fig.update_traces(
        textinfo='percent+label',
        hovertemplate='%{label}<br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    return fig

def create_pulse_chart(bp_data):
    """
    Create a time series chart of pulse readings
    
    Parameters:
    - bp_data: DataFrame with blood pressure readings including pulse
    
    Returns:
    Plotly figure
    """
    if bp_data is None or len(bp_data) == 0:
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No pulse data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Sort by date and time
    sorted_data = bp_data.sort_values('datetime')
    
    # Create figure
    fig = go.Figure()
    
    # Add pulse line
    fig.add_trace(go.Scatter(
        x=sorted_data['datetime'],
        y=sorted_data['pulse'],
        mode='lines+markers',
        name='Pulse',
        line=dict(color='#9b59b6', width=2),
        marker=dict(
            size=8,
            color='#9b59b6',
            line=dict(width=1, color='#333')
        )
    ))
    
    # Add reference lines for normal pulse range
    fig.add_shape(
        type="line",
        x0=sorted_data['datetime'].min(),
        x1=sorted_data['datetime'].max(),
        y0=60, y1=60,
        line=dict(color="#2ecc71", width=1, dash="dash"),
        name="Lower Normal Range"
    )
    
    fig.add_shape(
        type="line",
        x0=sorted_data['datetime'].min(),
        x1=sorted_data['datetime'].max(),
        y0=100, y1=100,
        line=dict(color="#e74c3c", width=1, dash="dash"),
        name="Upper Normal Range"
    )
    
    # Update layout
    fig.update_layout(
        title='Pulse Rate Trend',
        xaxis_title='Date',
        yaxis_title='Pulse Rate (BPM)',
        hovermode='closest',
        template='plotly_white',
        height=350
    )
    
    # Add hover template
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>%{y} BPM<extra></extra>'
    )
    
    return fig

def create_bp_statistics_table(bp_data):
    """
    Create statistics table for blood pressure data
    
    Parameters:
    - bp_data: DataFrame with blood pressure readings
    
    Returns:
    Plotly figure
    """
    if bp_data is None or len(bp_data) == 0:
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No blood pressure data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Calculate statistics
    stats = {
        'Metric': ['Average', 'Minimum', 'Maximum', 'Standard Deviation'],
        'Systolic': [
            f"{bp_data['systolic'].mean():.1f}",
            f"{bp_data['systolic'].min()}",
            f"{bp_data['systolic'].max()}",
            f"{bp_data['systolic'].std():.1f}"
        ],
        'Diastolic': [
            f"{bp_data['diastolic'].mean():.1f}",
            f"{bp_data['diastolic'].min()}",
            f"{bp_data['diastolic'].max()}",
            f"{bp_data['diastolic'].std():.1f}"
        ],
        'Pulse': [
            f"{bp_data['pulse'].mean():.1f}",
            f"{bp_data['pulse'].min()}",
            f"{bp_data['pulse'].max()}",
            f"{bp_data['pulse'].std():.1f}"
        ]
    }
    
    # Create table
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(stats.keys()),
            fill_color='#075E9B',
            align='center',
            font=dict(color='white', size=14)
        ),
        cells=dict(
            values=[stats[k] for k in stats.keys()],
            fill_color='#F9F9F9',
            align='center',
            font=dict(size=12)
        )
    )])
    
    # Update layout
    fig.update_layout(
        title='Blood Pressure Statistics',
        height=200
    )
    
    return fig