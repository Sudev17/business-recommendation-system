"""
Business Recommendation System - Streamlit Frontend
A user-friendly web interface for getting business recommendations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from recommendation_engine import BusinessRecommendationEngine
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Business Recommendation System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern clean theme similar to Qoder
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Black background with royal cream light glow theme */
    .stApp {
        background-color: #000000;
        color: #F5E8C9;
        font-family: 'Inter', sans-serif;
        text-shadow: 0 0 10px rgba(245, 232, 201, 0.3);
    }
    
    /* Sidebar styling - Royal cream glow */
    .sidebar-container {
        background-color: #000000;
        border-right: 1px solid #F5E8C9;
        box-shadow: 0 0 15px rgba(245, 232, 201, 0.2);
    }
    
    .sidebar-container .stSelectbox > label,
    .sidebar-container .stSlider > label,
    .sidebar-container .stMultiSelect > label,
    .sidebar-container .stTextInput > label,
    .sidebar-container .stCheckbox > label {
        color: #F5E8C9 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        font-family: 'Inter', sans-serif !important;
        text-shadow: 0 0 8px rgba(245, 232, 201, 0.5);
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background-color: #000000 !important;
        color: #F5E8C9 !important;
        border: 1px solid #F5E8C9 !important;
        box-shadow: 0 0 10px rgba(245, 232, 201, 0.3) !important;
    }
    
    .stSlider > div > div > div > div {
        background-color: #F5E8C9 !important;
    }
    
    .stSlider > div > div > div > div:hover {
        background-color: #F5E8C9 !important;
        box-shadow: 0 0 15px rgba(245, 232, 201, 0.6) !important;
    }
    
    /* Main content area - Royal cream glow */
    .main .block-container {
        background-color: #000000;
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: inset 0 0 30px rgba(245, 232, 201, 0.1);
    }
    
    /* Headers - Royal cream glow styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        text-align: center;
        color: #F5E8C9;
        margin-bottom: 2rem;
        letter-spacing: -0.025em;
        text-shadow: 0 0 20px rgba(245, 232, 201, 0.7);
    }
    
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        color: #F5E8C9;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #F5E8C9;
        letter-spacing: -0.025em;
        text-shadow: 0 0 15px rgba(245, 232, 201, 0.5);
    }
    
    /* Cards - Royal cream glow modules */
    .metric-card {
        background-color: #000000;
        padding: 1.5rem;
        border-radius: 6px;
        border: 1px solid #F5E8C9;
        margin: 1rem 0;
        box-shadow: 0 0 15px rgba(245, 232, 201, 0.1);
    }
    
    .recommendation-card {
        background-color: #000000;
        padding: 1.5rem;
        border-radius: 6px;
        border: 1px solid #F5E8C9;
        margin: 1.5rem 0;
        transition: all 0.2s ease;
        box-shadow: 0 0 20px rgba(245, 232, 201, 0.15);
    }
    
    .recommendation-card:hover {
        background-color: #111111;
        border-color: #F5E8C9;
        box-shadow: 0 0 30px rgba(245, 232, 201, 0.3);
    }
    
    /* Score colors - Royal cream glow theme */
    .score-excellent { 
        background-color: #000000;
        color: #F5E8C9 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        padding: 0.25em 0.5em;
        border-radius: 4px;
        display: inline-block;
        font-family: 'JetBrains Mono', monospace !important;
        border: 1px solid #F5E8C9;
        box-shadow: 0 0 10px rgba(245, 232, 201, 0.5);
    }
    .score-good { 
        background-color: #000000;
        color: #F5E8C9 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        padding: 0.25em 0.5em;
        border-radius: 4px;
        display: inline-block;
        font-family: 'JetBrains Mono', monospace !important;
        border: 1px solid #F5E8C9;
        box-shadow: 0 0 10px rgba(245, 232, 201, 0.4);
    }
    .score-average { 
        background-color: #000000;
        color: #F5E8C9 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        padding: 0.25em 0.5em;
        border-radius: 4px;
        display: inline-block;
        font-family: 'JetBrains Mono', monospace !important;
        border: 1px solid #F5E8C9;
        box-shadow: 0 0 10px rgba(245, 232, 201, 0.3);
    }
    .score-poor { 
        background-color: #000000;
        color: #F5E8C9 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        padding: 0.25em 0.5em;
        border-radius: 4px;
        display: inline-block;
        font-family: 'JetBrains Mono', monospace !important;
        border: 1px solid #F5E8C9;
        box-shadow: 0 0 10px rgba(245, 232, 201, 0.2);
    }
    
    /* Text improvements - Royal cream glow text */
    .stMarkdown p, .stMarkdown div, .element-container p, .element-container div,
    .stAlert > div, .content-text p, .content-text div {
        color: #F5E8C9 !important;
        line-height: 1.6 !important;
        font-weight: 400 !important;
        font-family: 'Inter', sans-serif !important;
        text-shadow: 0 0 5px rgba(245, 232, 201, 0.3);
    }
    
    .stMarkdown strong, .element-container strong {
        color: #F5E8C9 !important;
        font-weight: 600 !important;
        text-shadow: 0 0 10px rgba(245, 232, 201, 0.5);
    }
    
    /* Streamlit specific text elements */
    .stWrite, .stWrite > div, .stWrite p {
        color: #F5E8C9 !important;
        font-family: 'Inter', sans-serif !important;
        text-shadow: 0 0 5px rgba(245, 232, 201, 0.3);
    }
    
    /* Labels and help text */
    label, .stFormSubmitButton label, .stSelectbox label, .stTextInput label,
    .stMultiSelect label, .stSlider label, .stCheckbox label {
        color: #F5E8C9 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        text-shadow: 0 0 8px rgba(245, 232, 201, 0.4);
    }
    
    /* Main page slider styling */
    .stSlider > div > div > div {
        background-color: #000000 !important;
        color: #F5E8C9 !important;
        border: 1px solid #F5E8C9 !important;
        box-shadow: 0 0 10px rgba(245, 232, 201, 0.3) !important;
    }
    
    .stSlider > div > div > div > div {
        background-color: #F5E8C9 !important;
    }
    
    .stSlider > div > div > div > div:hover {
        background-color: #F5E8C9 !important;
        box-shadow: 0 0 15px rgba(245, 232, 201, 0.6) !important;
    }
    
    /* Metrics styling - Royal cream glow design */
    .business-metric-card {
        background-color: #000000 !important;
        color: #F5E8C9 !important;
        border-radius: 6px !important;
        padding: 1rem !important;
        border: 1px solid #F5E8C9 !important;
        box-shadow: 0 0 15px rgba(245, 232, 201, 0.1);
    }
    
    .business-metric-card .metric-value {
        color: #F5E8C9 !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
        font-family: 'JetBrains Mono', monospace !important;
        text-shadow: 0 0 10px rgba(245, 232, 201, 0.5);
    }
    
    .business-metric-card .metric-label {
        color: #F5E8C9 !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        text-shadow: 0 0 5px rgba(245, 232, 201, 0.3);
    }
    
    /* Button styling - Royal cream glow buttons */
    .stButton > button {
        background-color: #000000 !important;
        color: #F5E8C9 !important;
        border: 1px solid #F5E8C9 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 0 10px rgba(245, 232, 201, 0.2);
    }
    
    .stButton > button:hover {
        background-color: #111111 !important;
        border-color: #F5E8C9 !important;
        box-shadow: 0 0 20px rgba(245, 232, 201, 0.4);
    }
    
    /* Dataframe styling - Royal cream glow panel */
    .stDataFrame {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.9) 0%, rgba(20, 20, 20, 0.8) 100%) !important;
        border-radius: 15px !important;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.7),
            0 0 30px rgba(245, 232, 201, 0.2) !important;
        border: 2px solid rgba(245, 232, 201, 0.4) !important;
        backdrop-filter: blur(5px) !important;
    }
    
    /* Info/warning boxes - Royal cream glow alerts */
    .stInfo, .stWarning, .stSuccess, .stError,
    .stAlert, .stAlert > div, .stAlert p {
        border-radius: 12px !important;
        border-left: 4px solid #F5E8C9 !important;
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.9) 0%, rgba(20, 20, 20, 0.8) 100%) !important;
        color: #F5E8C9 !important;
        font-weight: 400 !important;
        box-shadow: 
            0 8px 25px rgba(0, 0, 0, 0.6),
            0 0 20px rgba(245, 232, 201, 0.3) !important;
        backdrop-filter: blur(5px) !important;
        border: 2px solid rgba(245, 232, 201, 0.3) !important;
        font-family: 'Inter', sans-serif !important;
        text-shadow: 0 0 10px rgba(245, 232, 201, 0.5) !important;
    }
    
    /* Spinner text */
    .stSpinner > div {
        color: #F5E8C9 !important;
        font-family: 'Inter', sans-serif !important;
        text-shadow: 0 0 10px rgba(245, 232, 201, 0.5) !important;
    }
    
    /* Select boxes and inputs - Light royal cream glow controls */
    .stSelectbox > div > div,
    .stSelectbox > div > div:hover,
    .stSelectbox > div > div:focus,
    .stMultiSelect > div > div,
    .stMultiSelect > div > div:hover,
    .stMultiSelect > div > div:focus,
    .stTextInput > div > div > input,
    .stTextInput > div > div > input:hover,
    .stTextInput > div > div > input:focus {
        background-color: #000000 !important;
        color: #F5E8C9 !important;
        border: 1px solid #F5E8C9 !important;
        border-radius: 6px !important;
        box-shadow: 0 0 20px rgba(245, 232, 201, 0.6) !important;
    }
    
    /* Placeholder text styling */
    .stSelectbox > div > div::after,
    .stMultiSelect > div > div::after,
    .stTextInput > div > div > input::placeholder {
        color: #D4C8B0 !important;
        font-style: italic !important;
    }
    
    /* Dropdown menu styling */
    .stSelectbox > div > div [data-baseweb='select'] > div,
    .stMultiSelect > div > div [data-baseweb='select'] > div {
        background-color: #000000 !important;
        color: #F5E8C9 !important;
    }
    
    /* Dropdown arrows */
    .stSelectbox svg,
    .stMultiSelect svg {
        fill: #F5E8C9 !important;
    }
    
    /* Options in dropdown */
    [data-baseweb='menu'] > div > div,
    [data-baseweb='menu'] > div > div:hover {
        background-color: #000000 !important;
        color: #F5E8C9 !important;
    }
    
    [data-baseweb='menu'] > div > div:hover {
        background-color: #111111 !important;
    }
    
    /* Selected tags in multiselect */
    .stMultiSelect span[data-baseweb='tag'] {
        background-color: #000000 !important;
        color: #F5E8C9 !important;
        border: 1px solid #F5E8C9 !important;
        box-shadow: 0 0 10px rgba(245, 232, 201, 0.3) !important;
    }
    
    /* Delete button on tags */
    .stMultiSelect span[data-baseweb='tag'] svg {
        fill: #F5E8C9 !important;
    }
    
    /* Footer styling - Royal cream glow */
    .footer-text {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.95) 0%, rgba(20, 20, 20, 0.9) 100%);
        color: #F5E8C9;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.7),
            0 0 30px rgba(245, 232, 201, 0.3);
        border: 2px solid rgba(245, 232, 201, 0.4);
        font-family: 'Inter', sans-serif;
        backdrop-filter: blur(10px);
        position: relative;
    }
    
    .footer-text::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 30% 30%, rgba(0, 229, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 70% 70%, rgba(138, 43, 226, 0.1) 0%, transparent 50%);
        border-radius: 15px;
        pointer-events: none;
    }
    
    /* Sidebar elements - Light royal cream glow interface */
    .sidebar-container .stTextInput > div > div > input,
    .sidebar-container .stTextInput > div > div > input:hover,
    .sidebar-container .stTextInput > div > div > input:focus {
        background-color: #000000 !important;
        color: #F5E8C9 !important;
        border: 1px solid #F5E8C9 !important;
        border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 0 20px rgba(245, 232, 201, 0.6) !important;
    }
    
    .stTextInput > div > div > input,
    .stTextInput > div > div > input:hover,
    .stTextInput > div > div > input:focus {
        background-color: #000000 !important;
        color: #F5E8C9 !important;
        border: 1px solid #F5E8C9 !important;
        border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 0 20px rgba(245, 232, 201, 0.6) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #D4C8B0 !important;
        font-style: italic !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_recommendation_engine():
    """Load and cache the recommendation engine."""
    return BusinessRecommendationEngine(use_ml=True)

def get_score_color_class(score):
    """Get CSS class based on score value."""
    if score >= 80:
        return "score-excellent"
    elif score >= 65:
        return "score-good"
    elif score >= 50:
        return "score-average"
    else:
        return "score-poor"

def format_currency(amount):
    """Format currency in Indian format."""
    if amount >= 10000000:  # 1 crore
        return f"₹{amount/10000000:.1f} Cr"
    elif amount >= 100000:  # 1 lakh
        return f"₹{amount/100000:.1f} L"
    else:
        return f"₹{amount:,}"

def create_opportunity_heatmap(engine, selected_interests, top_cities=15):
    """Create opportunity heatmap data for top cities and categories."""
    try:
        # Get all cities and calculate market scores
        cities = engine.get_available_cities()
        categories = selected_interests if selected_interests else engine.get_available_categories()
        
        heatmap_data = []
        
        for city in cities:
            city_scores = []
            for category in categories:
                # Get category data for the city
                city_category_data = engine.df[
                    (engine.df['City'] == city) & (engine.df['Category'] == category)
                ]
                
                if not city_category_data.empty:
                    avg_demand = city_category_data['Demand'].mean()
                    avg_competition = city_category_data['Competition'].mean()
                    market_score = avg_demand - avg_competition
                    city_scores.append(market_score)
                else:
                    city_scores.append(0)  # No data available
            
            # Calculate average score for the city
            avg_city_score = np.mean(city_scores) if city_scores else 0
            heatmap_data.append({
                'city': city,
                'avg_score': avg_city_score,
                **{f'{cat}': score for cat, score in zip(categories, city_scores)}
            })
        
        # Convert to DataFrame and select top cities
        df_heatmap = pd.DataFrame(heatmap_data)
        df_heatmap = df_heatmap.sort_values('avg_score', ascending=False).head(top_cities)
        
        # Create the heatmap matrix
        heatmap_matrix = df_heatmap.set_index('city')[categories]
        
        return heatmap_matrix
        
    except Exception as e:
        print(f"Error creating heatmap: {str(e)}")
        return pd.DataFrame()

def main():
    # Load the recommendation engine
    with st.spinner("Loading Business Recommendation System..."):
        engine = load_recommendation_engine()
    
    # Main header with modern clean design
    st.markdown('<div class="main-header">📊 Business Intelligence</div>', 
                unsafe_allow_html=True)
    
    # Modern professional description
    st.markdown("""
    <div style="text-align: center; background-color: #000000; 
                padding: 2rem; border-radius: 8px; margin-bottom: 2rem; 
                border: 1px solid #F5E8C9; box-shadow: 0 0 20px rgba(245, 232, 201, 0.1);">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1.2rem;">
            <div style="width: 60px; height: 60px; border-radius: 50%; 
                        background: linear-gradient(135deg, #F5E8C9, #D4C8B0); 
                        display: flex; align-items: center; justify-content: center; margin-right: 1rem; box-shadow: 0 0 15px rgba(245, 232, 201, 0.5);">
                <span style="color: #000000; font-size: 1.5rem; font-weight: bold; text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);">💼</span>
            </div>
            <div>
                <h2 style="margin: 0; color: #F5E8C9; font-weight: 600; font-size: 1.5rem;
                           font-family: 'Inter', sans-serif; text-shadow: 0 0 10px rgba(245, 232, 201, 0.5);">
                    Business Intelligence
                </h2>
                <p style="margin: 0; color: #D4C8B0; font-weight: 400; font-size: 1rem;
                         font-family: 'Inter', sans-serif; text-shadow: 0 0 5px rgba(245, 232, 201, 0.3);">
                    Advanced Analytics & Market Insights
                </p>
            </div>
        </div>
        <p style="font-size: 1rem; color: #F5E8C9; font-weight: 400; line-height: 1.6; margin: 0;
                  font-family: 'Inter', sans-serif; text-shadow: 0 0 5px rgba(245, 232, 201, 0.3);">
            Intelligent algorithms analyze <strong style="color: #F5E8C9; text-shadow: 0 0 10px rgba(245, 232, 201, 0.5);">30,000+ business opportunities</strong> 
            across <strong style="color: #F5E8C9; text-shadow: 0 0 10px rgba(245, 232, 201, 0.5);">50+ strategic markets</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # User Guide Section
    with st.expander("📘 User Guide - How to Use This Tool", expanded=False):
        st.markdown("""
### Step-by-Step Guide

1. 📍 **Select Your City**

Pick the city where you want to open your business.

2. 💰 **Set Your Budget**

Tell us how much money you have to invest.

3. ❤️ **Choose Interests**

Pick the types of businesses you're interested in.

4. 🚀 **Get Recommendations**

We'll suggest the best opportunities for you.

### Understanding Your Results

📊 **Budget Analysis**: Green means it fits your budget, red means it's too expensive.

📈 **Market Opportunities**: Shows which business types are popular but not overcrowded.

🗺️ **Opportunity Map**: A map highlighting the best places in your city.

🏦 **City Comparison**: Compare how your idea performs across different cities.

### How We Find Your Best Opportunities

We analyzed 30,000+ real business examples to learn what works.
Each business idea gets a Smart Score (0-100).

- **Market Opportunity (50%)**: High demand, low competition (Demand - Competition)
- **Budget Fit (30%)**: Can you afford it?
- **Interest Match (20%)**: Does it align with what you like?

Our system (Random Forest) works like 30,000+ experts giving advice.
It helps us predict:
- How much customers will want each business
- How much competition there will be
- How confident we are in our predictions

Think of it as having a crystal ball backed by real data!
        """, unsafe_allow_html=True)
    
    # Settings moved to main page instead of sidebar
    st.markdown('<div class="sub-header">⚙️ Configure Your Search</div>', 
                unsafe_allow_html=True)
    
    # Create columns for settings in main page
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # City selection
        cities = engine.get_available_cities()
        if 'selected_city' not in st.session_state:
            st.session_state.selected_city = "Mumbai" if "Mumbai" in cities else cities[0] if cities else ""
        selected_city = st.selectbox(
            "📍 Select Your City",
            cities,
            index=cities.index(st.session_state.selected_city) if st.session_state.selected_city in cities else 0,
            help="Choose the city where you want to start your business",
            placeholder="Select your city...",
            key="city_select"
        )
        st.session_state.selected_city = selected_city
    
    with col2:
        # Budget input
        min_investment, max_investment = engine.get_investment_range()
        if 'budget' not in st.session_state:
            st.session_state.budget = 3000000
        budget = st.slider(
            "💰 Your Budget (₹)",
            min_value=min_investment,
            max_value=max_investment,
            value=st.session_state.budget,
            step=100000,
            format="₹%d",
            help="Select your available investment budget",
            key="budget_slider"
        )
        st.session_state.budget = budget
    
    with col3:
        # Interest selection
        categories = engine.get_available_categories()
        if 'selected_interests' not in st.session_state:
            st.session_state.selected_interests = ["Food", "Tech"]
        selected_interests = st.multiselect(
            "❤️ Your Interests",
            categories,
            default=st.session_state.selected_interests,
            help="Select business categories that interest you",
            placeholder="Select your interests...",
            key="interests_select"
        )
        st.session_state.selected_interests = selected_interests
    
    with col4:
        # Number of recommendations
        if 'num_recommendations' not in st.session_state:
            st.session_state.num_recommendations = 3
        num_recommendations = st.slider(
            "📊 Number of Recommendations",
            min_value=1,
            max_value=10,
            value=st.session_state.num_recommendations,
            help="How many business recommendations would you like to see?",
            key="num_recommendations_slider"
        )
        st.session_state.num_recommendations = num_recommendations
    
    # Advanced AI Features Section
    st.markdown('<div class="sub-header">🤖 Analytics Engine</div>', 
                unsafe_allow_html=True)
    
    col5, col6 = st.columns([1, 2])
    
    with col5:
        if 'enable_ml' not in st.session_state:
            st.session_state.enable_ml = True
        enable_ml = st.checkbox(
            "Enable ML Predictions",
            value=st.session_state.enable_ml,
            help="Use machine learning for enhanced demand and competition predictions",
            key="ml_checkbox"
        )
        st.session_state.enable_ml = enable_ml
    
    with col6:
        # Prediction for new business
        if 'predict_business_name' not in st.session_state:
            st.session_state.predict_business_name = ""
        predict_business_name = st.text_input(
            "🔮 Predict New Business Name",
            value=st.session_state.predict_business_name,
            placeholder="e.g., Tech Solutions Hub, Green Cafe Express...",
            help="Enter name for your new business idea",
            key="business_name_input"
        )
        st.session_state.predict_business_name = predict_business_name
    
    # Buttons
    col7, col8 = st.columns(2)
    
    with col7:
        get_recommendations = st.button(
            "🚀 Get Recommendations",
            type="primary",
            use_container_width=True
        )
    
    with col8:
        predict_new_business = st.button(
            "🔮 Predict New Business",
            use_container_width=True,
            help="Get ML prediction for your new business idea"
        )
    
    # ML Prediction Section
    if predict_new_business:
        st.markdown('<div class="sub-header">🔮 ML Business Prediction</div>', 
                   unsafe_allow_html=True)
        
        if predict_business_name and selected_interests:
            with st.spinner("Analyzing market with ML models..."):
                # Use first selected interest as category
                selected_category = selected_interests[0]
                
                prediction = engine.predict_new_business_opportunity(
                    selected_city, selected_category, predict_business_name, budget
                )
                
                col_pred1, col_pred2, col_pred3 = st.columns(3)
                
                with col_pred1:
                    st.metric(
                        "📈 Predicted Demand", 
                        f"{prediction['demand']}/100",
                        help="Predicted market demand for this business"
                    )
                
                with col_pred2:
                    st.metric(
                        "📋 Predicted Competition", 
                        f"{prediction['competition']}/100",
                        help="Predicted competition level"
                    )
                
                with col_pred3:
                    st.metric(
                        "⚖️ Market Gap", 
                        f"{prediction['market_gap']}",
                        help="Demand minus competition (higher is better)"
                    )
                
                # Confidence and interpretation
                confidence_color = "#00FF88" if prediction['confidence'] > 0.8 else "#FFD700" if prediction['confidence'] > 0.6 else "#FF6B6B"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(0, 0, 0, 0.95) 0%, rgba(20, 20, 20, 0.9) 50%, rgba(0, 0, 0, 0.95) 100%); 
                            padding: 2.5rem; border-radius: 20px; margin: 2rem 0;
                            border: 2px solid rgba(245, 232, 201, 0.5); 
                            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 50px rgba(245, 232, 201, 0.3);
                            backdrop-filter: blur(15px);
                            position: relative;">
                    <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px;
                                background: linear-gradient(90deg, #F5E8C9, #D4C8B0, #F5E8C9);
                                background-size: 300% 100%; border-radius: 20px 20px 0 0;"></div>
                    <h3 style="color: #F5E8C9; margin-bottom: 1.5rem; font-weight: 800; font-size: 1.6rem;
                               display: flex; align-items: center; font-family: 'Inter', sans-serif;
                               text-shadow: 0 0 20px rgba(245, 232, 201, 0.8); letter-spacing: 2px;">
                        <span style="margin-right: 1rem; color: #F5E8C9;">🚀</span>
                        <span style="background: linear-gradient(45deg, #F5E8C9, #D4C8B0);
                                     -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                            QUANTUM ANALYSIS: "{predict_business_name}"
                        </span>
                    </h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem;">
                        <div style="background: linear-gradient(135deg, rgba(245, 232, 201, 0.2) 0%, rgba(245, 232, 201, 0.1) 100%); 
                                    padding: 1.5rem; border-radius: 12px; border: 2px solid rgba(245, 232, 201, 0.5);
                                    box-shadow: 0 8px 25px rgba(245, 232, 201, 0.3);">
                            <strong style="color: #F5E8C9; font-size: 1.1rem; font-family: 'Inter', sans-serif;
                                           text-shadow: 0 0 15px rgba(245, 232, 201, 0.8);">CONFIDENCE:</strong><br>
                            <span style="color: {confidence_color}; font-weight: 800; font-size: 1.5rem;
                                         font-family: 'Inter', sans-serif; text-shadow: 0 0 20px {confidence_color};
                                         letter-spacing: 1px;">
                                {prediction['confidence']:.1%} ({prediction['prediction_quality']})
                            </span>
                        </div>
                        <div style="background: linear-gradient(135deg, rgba(245, 232, 201, 0.2) 0%, rgba(245, 232, 201, 0.1) 100%); 
                                    padding: 1.5rem; border-radius: 12px; border: 2px solid rgba(245, 232, 201, 0.5);
                                    box-shadow: 0 8px 25px rgba(245, 232, 201, 0.3);">
                            <strong style="color: #F5E8C9; font-size: 1.1rem; font-family: 'Inter', sans-serif;
                                           text-shadow: 0 0 15px rgba(245, 232, 201, 0.8);">MARKET GAP:</strong><br>
                            <span style="color: #F5E8C9; font-weight: 800; font-size: 1.5rem;
                                         font-family: 'Inter', sans-serif; text-shadow: 0 0 20px rgba(245, 232, 201, 0.8);
                                         letter-spacing: 1px;">
                                {prediction['market_gap']} POINTS
                            </span>
                        </div>
                    </div>
                    <div style="background: linear-gradient(135deg, rgba(245, 232, 201, 0.2) 0%, rgba(245, 232, 201, 0.1) 100%); 
                                padding: 1.5rem; border-radius: 12px; border: 2px solid rgba(245, 232, 201, 0.5); 
                                margin-bottom: 1.5rem; box-shadow: 0 8px 25px rgba(245, 232, 201, 0.3);">
                        <strong style="color: #F5E8C9; font-size: 1.1rem; font-family: 'Inter', sans-serif;
                                       text-shadow: 0 0 15px rgba(245, 232, 201, 0.8);">STELLAR ANALYSIS:</strong><br>
                        <span style="color: #F5E8C9; font-weight: 400; font-size: 1.1rem; line-height: 1.6;
                                     font-family: 'Inter', sans-serif; text-shadow: 0 0 10px rgba(245, 232, 201, 0.5);">
                            {prediction.get('interpretation', 'Analysis complete')}
                        </span>
                    </div>
                    <div style="background: linear-gradient(135deg, rgba(245, 232, 201, 0.2) 0%, rgba(245, 232, 201, 0.1) 100%); 
                                padding: 1.5rem; border-radius: 12px; border: 2px solid rgba(245, 232, 201, 0.5);
                                box-shadow: 0 8px 25px rgba(245, 232, 201, 0.3);">
                        <strong style="color: #F5E8C9; font-size: 1.1rem; font-family: 'Inter', sans-serif;
                                       text-shadow: 0 0 15px rgba(245, 232, 201, 0.8);">COSMIC RECOMMENDATION:</strong><br>
                        <span style="color: #F5E8C9; font-weight: 400; font-size: 1.1rem; line-height: 1.6;
                                     font-family: 'Inter', sans-serif; text-shadow: 0 0 10px rgba(245, 232, 201, 0.5);">
                            {prediction.get('recommendation', 'Consider market research')}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Display recommendations in main area
    if get_recommendations or 'recommendations' not in st.session_state:
        # Get recommendations
        with st.spinner("Analyzing business opportunities..."):
            recommendations = engine.get_recommendations(
                selected_city, budget, selected_interests, num_recommendations
            )
            st.session_state.recommendations = recommendations
            st.session_state.last_city = selected_city
            st.session_state.last_budget = budget
            st.session_state.last_interests = selected_interests
    
    # Display recommendations
    if 'recommendations' in st.session_state:
        recommendations = st.session_state.recommendations
        
        if recommendations:
            st.markdown('<div class="sub-header">🎯 Top Business Recommendations</div>', 
                       unsafe_allow_html=True)
            
            for i, rec in enumerate(recommendations, 1):
                score_class = get_score_color_class(rec['score'])
                
                st.markdown(f"""
                <div class="recommendation-card">
                    <h3 style="color: #F5E8C9; margin-bottom: 0.8rem; font-family: 'Inter', sans-serif;
                               text-shadow: 0 0 20px rgba(245, 232, 201, 0.8); letter-spacing: 1px;">
                        {i}. {rec['business_name']} 
                        <span style="font-size: 0.8em; color: #D4C8B0;">({rec['category']})</span>
                    </h3>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem;">
                        <span style="font-size: 1.3rem; font-weight: 600; color: #F5E8C9; font-family: 'Inter', sans-serif;
                                     text-shadow: 0 0 15px rgba(245, 232, 201, 0.6);">
                            💰 Investment: {format_currency(rec['investment_required'])}
                        </span>
                        <span class="{score_class}" style="font-size: 1.3rem;">
                            Score: {rec['score']}%
                        </span>
                    </div>
                    <div style="margin-bottom: 1.2rem; color: #D4C8B0; font-family: 'Inter', sans-serif;
                                text-shadow: 0 0 10px rgba(245, 232, 201, 0.5);">
                        <strong>📈 Market Analysis:</strong> 
                        Demand: {rec['demand']}% | Competition: {rec['competition']}% | 
                        Market Gap: {rec['market_gap']:.1f} points
                    </div>
                    <div style="background: linear-gradient(135deg, rgba(245, 232, 201, 0.1) 0%, rgba(212, 200, 176, 0.1) 100%); 
                                padding: 1.2rem; border-radius: 10px; border-left: 4px solid #F5E8C9;
                                box-shadow: 0 8px 20px rgba(245, 232, 201, 0.2);">
                        <strong style="color: #F5E8C9; font-family: 'Inter', sans-serif;
                                       text-shadow: 0 0 15px rgba(245, 232, 201, 0.8);">💡 Business Intelligence:</strong><br>
                        <span style="color: #F5E8C9; font-family: 'Inter', sans-serif; line-height: 1.6;
                                     text-shadow: 0 0 10px rgba(245, 232, 201, 0.5);">{rec['explanation']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning(f"No business opportunities found in {selected_city} matching your criteria.")
            st.info("Try adjusting your budget or selecting different interests.")
        # Budget analysis
        if 'recommendations' in st.session_state:
            st.markdown('<div class="sub-header">💰 Budget Analysis</div>', 
                       unsafe_allow_html=True)
            
            recommendations = st.session_state.recommendations
            if recommendations:
                # Create budget fit chart
                business_names = [rec['business_name'][:15] + "..." if len(rec['business_name']) > 15 
                                else rec['business_name'] for rec in recommendations]
                investments = [rec['investment_required'] for rec in recommendations]
                budget_fits = [rec['budget_fit'] for rec in recommendations]
                
                fig = go.Figure()
                
                # Budget line
                fig.add_hline(y=budget, line_dash="dash", line_color="#FF6B6B",
                             annotation_text=f"Your Budget: {format_currency(budget)}")
                
                # Investment bars
                fig.add_trace(go.Bar(
                    x=business_names,
                    y=investments,
                    name="Required Investment",
                    marker_color=['#00E5FF' if inv <= budget else '#FF6B6B' for inv in investments]
                ))
                
                fig.update_layout(
                    title="Investment vs Your Budget",
                    xaxis_title="Business",
                    yaxis_title="Amount (₹)",
                    height=400,
                    showlegend=False,
                    plot_bgcolor='rgba(0, 0, 0, 0.9)',
                    paper_bgcolor='rgba(0, 0, 0, 0.9)',
                    font=dict(family='Inter', color='#F5E8C9')
                )
                
                st.plotly_chart(fig, width='stretch')
    
    # Market Analysis Section
    if 'recommendations' in st.session_state and st.session_state.recommendations:
        st.markdown('<div class="sub-header">📊 Market Analysis Dashboard</div>', 
                   unsafe_allow_html=True)
        
        # Category analysis for the selected city
        category_data = engine.get_category_analysis(selected_city)
        
        if category_data:
            col3, col4 = st.columns(2)
            
            with col3:
                # Market gap by category
                categories = list(category_data.keys())
                market_gaps = [category_data[cat]['market_gap'] for cat in categories]
                
                fig_gap = px.bar(
                    x=categories,
                    y=market_gaps,
                    title=f"Market Opportunity by Category in {selected_city}",
                    labels={'x': 'Category', 'y': 'Market Gap (Demand - Competition)'},
                    color=market_gaps,
                    color_continuous_scale=[[0, '#8B7D6B'], [0.5, '#D4C8B0'], [1, '#F5E8C9']]
                )
                fig_gap.update_layout(
                    height=400, 
                    showlegend=False,
                    plot_bgcolor='rgba(0, 0, 0, 0.9)',
                    paper_bgcolor='rgba(0, 0, 0, 0.9)',
                    font=dict(family='Inter', color='#F5E8C9')
                )
                st.plotly_chart(fig_gap, width='stretch')
            
            with col4:
                # Investment vs Business count
                business_counts = [category_data[cat]['business_count'] for cat in categories]
                avg_investments = [category_data[cat]['avg_investment'] for cat in categories]
                
                # Create DataFrame for scatter plot
                scatter_df = pd.DataFrame({
                    'Categories': categories,
                    'Business_Count': business_counts,
                    'Avg_Investment': avg_investments,
                    'Market_Gap': market_gaps
                })
                
                fig_scatter = px.scatter(
                    scatter_df,
                    x='Business_Count',
                    y='Avg_Investment',
                    size='Market_Gap',
                    color='Categories',
                    title="Investment vs Market Size by Category",
                    labels={'Business_Count': 'Number of Businesses', 'Avg_Investment': 'Average Investment (₹)'},
                    hover_data=['Categories', 'Market_Gap'],
                    color_discrete_sequence=['#F5E8C9', '#D4C8B0', '#B8A890', '#A09078', '#8B7D6B', '#706550']
                )
                fig_scatter.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0, 0, 0, 0.9)',
                    paper_bgcolor='rgba(0, 0, 0, 0.9)',
                    font=dict(family='Inter', color='#F5E8C9')
                )
                st.plotly_chart(fig_scatter, width='stretch')
    
    # Heatmap Section
    if 'recommendations' in st.session_state and st.session_state.recommendations:
        st.markdown('<div class="sub-header">🗺️ Opportunity Heatmap</div>', 
                   unsafe_allow_html=True)
        
        # Create city-category heatmap
        heatmap_data = create_opportunity_heatmap(engine, selected_interests)
        
        if not heatmap_data.empty:
            fig_heatmap = px.imshow(
                heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                color_continuous_scale=[[0, '#8B7D6B'], [0.5, '#D4C8B0'], [1, '#F5E8C9']],
                title="Market Opportunity Heatmap (Top Cities vs Categories)",
                labels=dict(x="Category", y="City", color="Market Score")
            )
            
            fig_heatmap.update_layout(
                height=600,
                xaxis_title="Business Categories",
                yaxis_title="Cities",
                plot_bgcolor='rgba(0, 0, 0, 0.9)',
                paper_bgcolor='rgba(0, 0, 0, 0.9)',
                font=dict(family='Inter', color='#F5E8C9')
            )
            
            st.plotly_chart(fig_heatmap, width='stretch')
            
            # Add explanation
            st.info("💡 **How to read this heatmap:** Light areas indicate high opportunity (high demand, low competition), while darker areas suggest more competitive markets. Use this to identify the best city-category combinations.")
    
    # City Comparison Feature
    st.markdown('<div class="sub-header">🏦 City Comparison</div>', 
               unsafe_allow_html=True)
    
    if 'comparison_cities' not in st.session_state:
        st.session_state.comparison_cities = [selected_city] + (["Delhi", "Bangalore"] if selected_city not in ["Delhi", "Bangalore"] else ["Mumbai"])
    comparison_cities = st.multiselect(
        "Select cities to compare",
        engine.get_available_cities(),
        default=st.session_state.comparison_cities,
        max_selections=5,
        placeholder="Select cities to compare...",
        key="comparison_cities_select"
    )
    st.session_state.comparison_cities = comparison_cities
    
    if len(comparison_cities) >= 2:
        comparison_data = []
        for city in comparison_cities:
            summary = engine.get_city_summary(city)
            if summary:
                comparison_data.append({
                    'City': city,
                    'Total Businesses': summary['total_businesses'],
                    'Avg Demand': summary['avg_demand'],
                    'Avg Competition': summary['avg_competition'],
                    'Market Gap': round(summary['avg_demand'] - summary['avg_competition'], 1),
                    'Avg Investment (₹L)': round(summary['avg_investment'] / 100000, 1),
                    'Popular Category': summary['top_category']
                })
        
        if comparison_data:
            comparison_df = pd.DataFrame(comparison_data)
            
            # Display comparison table
            st.dataframe(
                comparison_df.set_index('City'),
                width='stretch'
            )
            
            # Create comparison charts
            col_comp1, col_comp2 = st.columns(2)
            
            with col_comp1:
                fig_demand_comp = px.bar(
                    comparison_df,
                    x='City',
                    y='Market Gap',
                    title="Market Gap Comparison",
                    color='Market Gap',
                    color_continuous_scale=[[0, '#8B7D6B'], [0.5, '#D4C8B0'], [1, '#F5E8C9']]
                )
                fig_demand_comp.update_layout(
                    height=400, 
                    showlegend=False,
                    plot_bgcolor='rgba(0, 0, 0, 0.9)',
                    paper_bgcolor='rgba(0, 0, 0, 0.9)',
                    font=dict(family='Inter', color='#F5E8C9')
                )
                st.plotly_chart(fig_demand_comp, width='stretch')
            
            with col_comp2:
                fig_investment_comp = px.bar(
                    comparison_df,
                    x='City',
                    y='Avg Investment (₹L)',
                    title="Average Investment Comparison",
                    color='Avg Investment (₹L)',
                    color_continuous_scale=[[0, '#8B7D6B'], [1, '#F5E8C9']]
                )
                fig_investment_comp.update_layout(
                    height=400, 
                    showlegend=False,
                    plot_bgcolor='rgba(0, 0, 0, 0.9)',
                    paper_bgcolor='rgba(0, 0, 0, 0.9)',
                    font=dict(family='Inter', color='#F5E8C9')
                )
                st.plotly_chart(fig_investment_comp, width='stretch')
    
    # Clean Professional Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer-text">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.4rem; margin-right: 0.8rem;">🚀</span>
            <strong style="color: #F5E8C9; font-family: 'Inter', sans-serif;
                           font-weight: 600; letter-spacing: 0px; text-shadow: 0 0 10px rgba(245, 232, 201, 0.5);">Business Intelligence</strong>
        </div>
        <div style="font-size: 0.9rem; opacity: 0.9; color: #D4C8B0; font-family: 'Inter', sans-serif;
                    letter-spacing: 0px; text-shadow: 0 0 5px rgba(245, 232, 201, 0.3);">
            Advanced Analytics | Data Insights | Smart Decisions
        </div>
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #F5E8C9;
                    font-size: 0.8rem; color: #D4C8B0; font-family: 'Inter', sans-serif; text-shadow: 0 0 5px rgba(245, 232, 201, 0.3);">
            <span style="opacity: 0.8;">Developed by</span> 
            <strong style="color: #F5E8C9; font-weight: 500; text-shadow: 0 0 10px rgba(245, 232, 201, 0.5);">Sudev Basti</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()