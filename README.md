# Heart Health Tracker

An interactive dashboard application that analyzes the relationship between exercise patterns and cardiovascular health metrics, providing personalized exercise recommendations through LLM integration.

## Key Features

- **Blood Pressure Analysis**: Track and visualize blood pressure trends with AHA category classification
- **Exercise Tracking**: Monitor exercise patterns including type, duration, and intensity
- **Correlation Analysis**: Identify relationships between exercise and blood pressure changes
- **FHIR Integration**: Connect to health records for comprehensive health data integration
- **Personalized Recommendations**: Generate tailored exercise plans based on your unique cardiovascular response

## Technical Architecture

The application uses a multi-layered architecture:

1. **Data Processing Layer**
   - Integration with Omron blood pressure device data
   - Integration with Google Fit exercise data
   - FHIR server connectivity for healthcare records
   - Synthetic data generation for testing

2. **Analysis Layer**
   - Blood pressure categorization using AHA guidelines
   - Statistical correlation analysis between exercise and blood pressure
   - Pattern detection in cardiovascular responses to exercise types

3. **AI Layer**
   - LLM-powered recommendation engine via OpenRouter API
   - Dynamic prompt engineering for personalized exercise plans
   - Contextual analysis of health records and exercise patterns

4. **Visualization Layer**
   - Interactive dashboards for data exploration
   - Time-series analysis of BP and exercise data
   - Correlation visualization and statistical significance indicators

## Getting Started

### Prerequisites

- Python 3.9+
- Streamlit
- Required Python packages (see requirements.txt)
- OpenRouter API key for LLM recommendations

### Installation

1. Clone the repository
git clone https://github.com/yourusername/heart-health-tracker.git cd heart-health-tracker
2. Install required packages
pip install -r requirements.txt
3. Set up environment variables
Create a `.env` file in the project root with:
OPENROUTER_API_KEY=your_openrouter_api_key
### Running the Application

Start the Streamlit application with:
streamlit run app.py
The application will be accessible at http://localhost:8501

## Project Structure

```plaintext
heart/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Dependencies
├── synthetic_data_generator.py # Creates test data
├── data/                       # Data storage
│   ├── synthetic/              # Synthetic data
│   └── user_data/              # User uploaded data
└── src/                        # Source code
    ├── analysis/               # Analysis modules
    │   ├── bp_categories.py    # BP classification
    │   └── correlation.py      # Correlation engine
    ├── data_processing/        # Data processing
    │   ├── data_loader.py      # Data loading utilities
    │   └── fhir.py             # FHIR integration
    ├── llm/                    # LLM components
    │   ├── prompts.py          # Prompt templates
    │   └── recommendation.py   # Recommendation engine
    └── visualization/          # Visualization components
        └── dashboard.py        # Dashboard creation
```
## Using FHIR Integration


The application supports connecting to any FHIR R4 compliant server:

1. In the sidebar, select "Connect FHIR Server"
2. Enter a valid username (firstname_lastname) and password
3. Click "Connect and Import"

The application will retrieve patient demographics, conditions, medications, and vital signs, which will be incorporated into the personalized exercise recommendations.

## Data Format Requirements

If uploading your own data, please use the following CSV format:

### Blood Pressure CSV
date,time,systolic,diastolic,pulse,time_of_day 2025-01-15,07:30,120,80,72,Morning 2025-01-15,19:15,118,78,70,Evening
### Exercise Data CSV
date,time,exercise_type,duration_minutes,intensity,calories_burned,avg_heart_rate,steps 2025-01-15,17:30,Walking,30,Moderate,150,95,3000 2025-01-16,08:15,Running,20,High,200,130,2500
## Authors

- Chetan Reddy Bojja
- Kartheek Bellamkonda 
- Rishitha Komatineni
