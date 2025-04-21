def add_recommendation_styles():
    """Add custom CSS for recommendation display"""
    return """
    <style>
    .recommendation-section {
        margin-bottom: 30px;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: white;
    }
    
    .summary-section {
        border-left: 5px solid #4a86e8;
    }
    
    .plan-section {
        border-left: 5px solid #6aa84f;
    }
    
    .insights-section {
        border-left: 5px solid #e69138;
    }
    
    .monitoring-section {
        border-left: 5px solid #a64d79;
    }
    
    .section-title {
        color: #333;
        font-size: 24px;
        margin-top: 0;
        margin-bottom: 15px;
        font-weight: 600;
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
    
    /* Patient card styling */
    .patient-card {
        display: flex;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 15px;
        margin-bottom: 20px;
    }
    
    .patient-avatar {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: #FF4B4B;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: white;
        margin-right: 15px;
    }
    
    .patient-info {
        flex-grow: 1;
    }
    
    .patient-name {
        font-size: 18px;
        font-weight: bold;
        margin: 0;
    }
    
    .patient-details {
        font-size: 14px;
        color: #666;
        margin: 5px 0;
    }
    
    /* Weekly schedule styling */
    .schedule-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 10px;
        margin: 20px 0;
    }
    
    .day-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
    }
    
    .day-header {
        font-weight: bold;
        margin-bottom: 5px;
        color: #333;
    }
    
    .exercise-item {
        font-size: 12px;
        background-color: #e8f4f8;
        border-radius: 5px;
        padding: 5px;
        margin-bottom: 5px;
    }
    
    /* HR zones and charts styling */
    .hr-zones {
        display: flex;
        justify-content: space-between;
        margin: 15px 0;
    }
    
    .zone {
        flex: 1;
        padding: 10px;
        text-align: center;
        border-radius: 5px;
        margin: 0 5px;
    }
    
    .zone-light {
        background-color: #d9ead3;
    }
    
    .zone-moderate {
        background-color: #fff2cc;
    }
    
    .zone-vigorous {
        background-color: #f4cccc;
    }
    
    .zone-header {
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .zone-bpm {
        font-size: 16px;
    }
    </style>
    """

def apply_dashboard_theming():
    """Apply custom theming for dashboard"""
    return """
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f2f2f2;
        border-radius: 4px 4px 0 0;
        padding: 10px 16px;
        color: #525252;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FF4B4B !important;
        color: white !important;
    }
    
    /* Cards and containers */
    .data-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    
    .metric-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 15px;
    }
    
    .metric {
        flex: 1;
        min-width: 140px;
        background-color: white;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }
    
    .metric-label {
        font-size: 14px;
        color: #666;
    }
    
    /* Custom plot styling */
    .custom-plot {
        background-color: white;
        border-radius: 10px;
        padding: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
    }
    </style>
    """