import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_exercise_calendar(exercise_data):
    """
    Create a heatmap calendar of exercise activity
    
    Parameters:
    - exercise_data: DataFrame with exercise records
    
    Returns:
    Plotly figure
    """
    if exercise_data is None or len(exercise_data) == 0:
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No exercise data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Group by date and calculate total duration
    daily_exercise = exercise_data.groupby('date')['duration_minutes'].sum().reset_index()
    
    # Create a date range for all days in the range
    date_range = pd.date_range(
        start=daily_exercise['date'].min(),
        end=daily_exercise['date'].max(),
        freq='D'
    )
    
    # Create a complete DataFrame with all dates
    complete_dates = pd.DataFrame({'date': date_range})
    
    # Merge with exercise data
    merged_data = pd.merge(complete_dates, daily_exercise, on='date', how='left')
    merged_data['duration_minutes'] = merged_data['duration_minutes'].fillna(0)
    
    # Extract day, week, and month
    merged_data['day'] = merged_data['date'].dt.day_name()
    merged_data['week'] = merged_data['date'].dt.isocalendar().week
    merged_data['month'] = merged_data['date'].dt.month_name()
    
    # Order days correctly
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    merged_data['day_num'] = merged_data['day'].apply(lambda x: day_order.index(x))
    merged_data = merged_data.sort_values(['week', 'day_num'])
    
    # Create heatmap
    fig = px.imshow(
        merged_data.pivot(index='day', columns='week', values='duration_minutes'),
        labels=dict(x="Week", y="Day", color="Minutes"),
        color_continuous_scale="YlGnBu",
        title="Exercise Activity Calendar (minutes per day)"
    )
    
    # Update layout
    fig.update_layout(
        xaxis_nticks=len(merged_data['week'].unique()),
        template='plotly_white',
        height=350
    )
    
    # Add hover template
    fig.update_traces(
        hovertemplate='Week: %{x}<br>Day: %{y}<br>Duration: %{z} minutes<extra></extra>'
    )
    
    return fig

def create_exercise_type_distribution(exercise_data):
    """
    Create a bar chart showing distribution of exercise types
    
    Parameters:
    - exercise_data: DataFrame with exercise records
    
    Returns:
    Plotly figure
    """
    if exercise_data is None or len(exercise_data) == 0:
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No exercise data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Count exercise types
    type_counts = exercise_data['exercise_type'].value_counts().reset_index()
    type_counts.columns = ['Exercise Type', 'Count']
    
    # Create color map
    colors = px.colors.qualitative.Set3
    
    # Create bar chart
    fig = px.bar(
        type_counts, 
        x='Exercise Type', 
        y='Count',
        color='Exercise Type',
        color_discrete_sequence=colors,
        title='Exercise Type Distribution'
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title='Exercise Type',
        yaxis_title='Number of Sessions',
        template='plotly_white',
        height=350,
        showlegend=False
    )
    
    # Add hover template
    fig.update_traces(
        hovertemplate='%{x}<br>Sessions: %{y}<extra></extra>'
    )
    
    return fig

def create_exercise_intensity_chart(exercise_data):
    """
    Create a pie chart showing distribution of exercise intensity
    
    Parameters:
    - exercise_data: DataFrame with exercise records
    
    Returns:
    Plotly figure
    """
    if exercise_data is None or len(exercise_data) == 0:
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No exercise data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Count intensity levels
    intensity_counts = exercise_data['intensity'].value_counts().reset_index()
    intensity_counts.columns = ['Intensity', 'Count']
    
    # Create color map
    color_map = {
        'Low': '#ADD8E6',  # Light blue
        'Moderate': '#4682B4',  # Steel blue
        'High': '#000080'  # Navy
    }
    
    # Create pie chart
    fig = px.pie(
        intensity_counts, 
        values='Count', 
        names='Intensity',
        color='Intensity',
        color_discrete_map=color_map,
        title='Exercise Intensity Distribution'
    )
    
    # Update layout
    fig.update_layout(
        legend_title='Intensity',
        template='plotly_white',
        height=350
    )
    
    # Update traces
    fig.update_traces(
        textinfo='percent+label',
        hovertemplate='%{label}<br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    return fig

def create_exercise_duration_chart(exercise_data):
    """
    Create a box plot of exercise duration by type
    
    Parameters:
    - exercise_data: DataFrame with exercise records
    
    Returns:
    Plotly figure
    """
    if exercise_data is None or len(exercise_data) == 0:
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No exercise data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Create box plot
    fig = px.box(
        exercise_data, 
        x='exercise_type', 
        y='duration_minutes',
        color='exercise_type',
        title='Exercise Duration by Type',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title='Exercise Type',
        yaxis_title='Duration (minutes)',
        template='plotly_white',
        height=350,
        showlegend=False
    )
    
    # Add hover template
    fig.update_traces(
        hovertemplate='%{x}<br>Duration: %{y} minutes<extra></extra>'
    )
    
    return fig

def create_exercise_timeline(exercise_data):
    """
    Create a timeline/scatter plot of exercise sessions
    
    Parameters:
    - exercise_data: DataFrame with exercise records
    
    Returns:
    Plotly figure
    """
    if exercise_data is None or len(exercise_data) == 0:
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No exercise data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Create color map for intensity
    color_map = {
        'Low': '#ADD8E6',  # Light blue
        'Moderate': '#4682B4',  # Steel blue
        'High': '#000080'  # Navy
    }
    
    # Create size map based on duration
    # Min size 10, max size 25
    min_duration = exercise_data['duration_minutes'].min()
    max_duration = exercise_data['duration_minutes'].max()
    
    exercise_data['marker_size'] = exercise_data['duration_minutes'].apply(
        lambda x: 10 + (x - min_duration) / (max_duration - min_duration) * 15
        if max_duration > min_duration else 15
    )
    
    # Create scatter plot
    fig = px.scatter(
        exercise_data, 
        x='datetime', 
        y='exercise_type',
        color='intensity',
        size='marker_size',
        color_discrete_map=color_map,
        title='Exercise Timeline',
        hover_data=['duration_minutes', 'calories_burned']
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Exercise Type',
        template='plotly_white',
        height=400,
        legend_title='Intensity'
    )
    
    # Update traces
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Type: %{y}<br>Intensity: %{marker.color}<br>Duration: %{customdata[0]} minutes<br>Calories: %{customdata[1]}<extra></extra>'
    )
    
    return fig