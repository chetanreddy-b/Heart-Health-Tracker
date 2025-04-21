import pandas as pd
import numpy as np

class BPCategorizer:
    """
    Class for categorizing blood pressure readings according to AHA guidelines
    """
    
    # AHA Blood Pressure Categories
    BP_CATEGORIES = {
        'Normal': {'systolic': (0, 120), 'diastolic': (0, 80)},
        'Elevated': {'systolic': (120, 130), 'diastolic': (0, 80)},
        'Hypertension Stage 1': {'systolic': (130, 140), 'diastolic': (80, 90)},
        'Hypertension Stage 2': {'systolic': (140, 180), 'diastolic': (90, 120)},
        'Hypertensive Crisis': {'systolic': (180, 300), 'diastolic': (120, 200)}
    }
    
    # Colors for each category
    CATEGORY_COLORS = {
        'Normal': '#2ecc71',  # Green
        'Elevated': '#f1c40f',  # Yellow
        'Hypertension Stage 1': '#e67e22',  # Orange
        'Hypertension Stage 2': '#e74c3c',  # Red
        'Hypertensive Crisis': '#c0392b'  # Dark Red
    }
    
    def __init__(self):
        pass
    
    def categorize_bp(self, systolic, diastolic):
        """
        Categorize a single blood pressure reading
        
        Parameters:
        - systolic: Systolic blood pressure (mmHg)
        - diastolic: Diastolic blood pressure (mmHg)
        
        Returns:
        Category string and color
        """
        # Logic based on AHA guidelines
        if systolic >= 180 or diastolic >= 120:
            category = 'Hypertensive Crisis'
        elif systolic >= 140 or diastolic >= 90:
            category = 'Hypertension Stage 2'
        elif (systolic >= 130 or diastolic >= 80):
            category = 'Hypertension Stage 1'
        elif systolic >= 120:
            category = 'Elevated'
        else:
            category = 'Normal'
            
        return category, self.CATEGORY_COLORS[category]
    
    def categorize_bp_dataframe(self, bp_data):
        """
        Add category columns to a blood pressure DataFrame
        
        Parameters:
        - bp_data: DataFrame containing 'systolic' and 'diastolic' columns
        
        Returns:
        DataFrame with added 'category' and 'category_color' columns
        """
        if bp_data is None or len(bp_data) == 0:
            return None
            
        # Create a copy to avoid modifying the original
        categorized_data = bp_data.copy()
        
        # Apply categorization function to each row
        categories = []
        colors = []
        
        for _, row in categorized_data.iterrows():
            category, color = self.categorize_bp(row['systolic'], row['diastolic'])
            categories.append(category)
            colors.append(color)
            
        categorized_data['category'] = categories
        categorized_data['category_color'] = colors
        
        return categorized_data
    
    def get_category_distribution(self, categorized_data):
        """
        Calculate the distribution of BP categories
        
        Parameters:
        - categorized_data: DataFrame with 'category' column
        
        Returns:
        Dictionary with category counts and percentages
        """
        if categorized_data is None or len(categorized_data) == 0:
            return {}
            
        # Count occurrences of each category
        category_counts = categorized_data['category'].value_counts().to_dict()
        
        # Calculate percentages
        total = len(categorized_data)
        category_percentages = {cat: count/total*100 for cat, count in category_counts.items()}
        
        return {
            'counts': category_counts,
            'percentages': category_percentages
        }
    
    def get_category_trends(self, categorized_data, freq='W'):
        """
        Calculate trends in BP categories over time
        
        Parameters:
        - categorized_data: DataFrame with 'date' and 'category' columns
        - freq: Frequency for resampling ('D' for daily, 'W' for weekly, 'M' for monthly)
        
        Returns:
        DataFrame with category counts over time
        """
        if categorized_data is None or len(categorized_data) == 0:
            return None
            
        # Create pivoted DataFrame with categories as columns
        # First create a DataFrame with 1s for each category
        category_data = pd.DataFrame({
            'date': categorized_data['date'],
            'category': categorized_data['category'],
            'count': 1
        })
        
        # Pivot to get categories as columns
        pivoted = category_data.pivot_table(
            index='date', 
            columns='category', 
            values='count', 
            aggfunc='sum',
            fill_value=0
        )
        
        # Ensure all categories are present
        for category in self.BP_CATEGORIES.keys():
            if category not in pivoted.columns:
                pivoted[category] = 0
        
        # Resample to desired frequency
        resampled = pivoted.resample(freq).sum()
        
        return resampled