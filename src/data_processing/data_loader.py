import pandas as pd
import os
from datetime import datetime

class DataLoader:
    """
    General utility for loading and managing data from various sources
    """
    
    def __init__(self):
        # Define paths
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        self.synthetic_dir = os.path.join(self.data_dir, 'synthetic')
        self.user_data_dir = os.path.join(self.data_dir, 'user_data')
        
        # Ensure directories exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.synthetic_dir, exist_ok=True)
        os.makedirs(self.user_data_dir, exist_ok=True)
        
        # Initialize data containers
        self.bp_data = None
        self.exercise_data = None
        self.fhir_data = None
        
    def load_synthetic_data(self):
        """Load synthetic data for demonstration"""
        bp_path = os.path.join(self.synthetic_dir, 'omron_data.csv')
        exercise_path = os.path.join(self.synthetic_dir, 'google_fit.csv')
        
        if not os.path.exists(bp_path) or not os.path.exists(exercise_path):
            # Generate synthetic data if it doesn't exist
            from synthetic_data_generator import main as generate_data
            generate_data()
        
        # Load the data
        self.bp_data = pd.read_csv(bp_path)
        self.exercise_data = pd.read_csv(exercise_path)
        
        # Convert date columns
        self.bp_data['date'] = pd.to_datetime(self.bp_data['date'])
        self.exercise_data['date'] = pd.to_datetime(self.exercise_data['date'])
        
        # Create datetime columns by combining date and time
        self.bp_data['datetime'] = pd.to_datetime(
            self.bp_data['date'].dt.strftime('%Y-%m-%d') + ' ' + self.bp_data['time']
        )
        self.exercise_data['datetime'] = pd.to_datetime(
            self.exercise_data['date'].dt.strftime('%Y-%m-%d') + ' ' + self.exercise_data['time']
        )
        
        return self.bp_data, self.exercise_data
    
    def load_user_data(self, bp_file=None, exercise_file=None):
        """
        Load user-provided data files
        
        Parameters:
        - bp_file: File object for blood pressure data
        - exercise_file: File object for exercise data
        
        Returns:
        Tuple of (bp_data, exercise_data) DataFrames
        """
        # Save uploaded files
        if bp_file is not None:
            bp_path = os.path.join(self.user_data_dir, 'omron_data.csv')
            with open(bp_path, 'wb') as f:
                f.write(bp_file.getbuffer())
            self.bp_data = pd.read_csv(bp_path)
            self.bp_data['date'] = pd.to_datetime(self.bp_data['date'])
            self.bp_data['datetime'] = pd.to_datetime(
                self.bp_data['date'].dt.strftime('%Y-%m-%d') + ' ' + self.bp_data['time']
            )
        
        if exercise_file is not None:
            exercise_path = os.path.join(self.user_data_dir, 'google_fit.csv')
            with open(exercise_path, 'wb') as f:
                f.write(exercise_file.getbuffer())
            self.exercise_data = pd.read_csv(exercise_path)
            self.exercise_data['date'] = pd.to_datetime(self.exercise_data['date'])
            self.exercise_data['datetime'] = pd.to_datetime(
                self.exercise_data['date'].dt.strftime('%Y-%m-%d') + ' ' + self.exercise_data['time']
            )
        
        return self.bp_data, self.exercise_data
    
    def get_date_range(self):
        """Get the overall date range covered by the data"""
        bp_min = self.bp_data['date'].min() if self.bp_data is not None else None
        bp_max = self.bp_data['date'].max() if self.bp_data is not None else None
        ex_min = self.exercise_data['date'].min() if self.exercise_data is not None else None
        ex_max = self.exercise_data['date'].max() if self.exercise_data is not None else None
        
        # Combine date ranges
        all_dates = [d for d in [bp_min, bp_max, ex_min, ex_max] if d is not None]
        if not all_dates:
            return datetime.now().date(), datetime.now().date()
        
        return min(all_dates).date(), max(all_dates).date()
    
    def filter_by_date_range(self, start_date, end_date):
        """Filter data to a specific date range"""
        if self.bp_data is not None:
            self.filtered_bp_data = self.bp_data[
                (self.bp_data['date'] >= pd.Timestamp(start_date)) & 
                (self.bp_data['date'] <= pd.Timestamp(end_date))
            ]
        else:
            self.filtered_bp_data = None
            
        if self.exercise_data is not None:
            self.filtered_exercise_data = self.exercise_data[
                (self.exercise_data['date'] >= pd.Timestamp(start_date)) & 
                (self.exercise_data['date'] <= pd.Timestamp(end_date))
            ]
        else:
            self.filtered_exercise_data = None
            
        return self.filtered_bp_data, self.filtered_exercise_data