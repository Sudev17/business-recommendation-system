"""
Business Recommendation Engine
Implements the core logic for recommending businesses based on user preferences
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import warnings
import os
from ml_predictor import MLPredictor
warnings.filterwarnings('ignore')

class BusinessRecommendationEngine:
    """
    Core recommendation engine that processes business data and provides recommendations
    based on location, budget, and interest preferences.
    """
    
    def __init__(self, dataset_path: str = "business_dataset_30000.csv", use_ml: bool = True):
        """
        Initialize the recommendation engine with the business dataset.
        
        Args:
            dataset_path (str): Path to the CSV dataset file
            use_ml (bool): Whether to use ML predictions for enhanced recommendations
        """
        # Handle relative paths for Streamlit deployment
        if not os.path.isabs(dataset_path):
            # Try to find the dataset file in common locations
            possible_paths = [
                dataset_path,
                os.path.join(os.path.dirname(__file__), dataset_path),
                os.path.join(os.path.dirname(os.path.dirname(__file__)), dataset_path),
                os.path.join("business-recommendation-system", dataset_path),
                os.path.join(os.getcwd(), dataset_path),
                os.path.join(os.getcwd(), "business-recommendation-system", dataset_path)
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.dataset_path = path
                    break
            else:
                # If no path works, use the original path and let it fail with a clear error
                self.dataset_path = dataset_path
        else:
            self.dataset_path = dataset_path
            
        self.df = None
        self.use_ml = use_ml
        self.ml_predictor = None
        self.load_data()
        
        if self.use_ml:
            self._initialize_ml_predictor()
        
    def load_data(self) -> None:
        """Load the business dataset from CSV file."""
        try:
            self.df = pd.read_csv(self.dataset_path)
            print(f"✅ Dataset loaded successfully: {len(self.df)} businesses")
        except FileNotFoundError:
            raise FileNotFoundError(f"Dataset file not found: {self.dataset_path}")
        except Exception as e:
            raise Exception(f"Error loading dataset: {str(e)}")
    
    def _initialize_ml_predictor(self):
        """Initialize ML predictor for enhanced recommendations."""
        try:
            self.ml_predictor = MLPredictor(self.dataset_path)
            # Try to load existing models, if not available, train new ones
            if not self.ml_predictor.load_models():
                print("🤖 Training ML models for enhanced predictions...")
                self.ml_predictor.train_models()
                self.ml_predictor.save_models()
            print("✅ ML prediction module initialized")
        except Exception as e:
            print(f"⚠️ ML predictor initialization failed: {str(e)}")
            print("📊 Continuing with basic recommendations...")
            self.use_ml = False
            self.ml_predictor = None
    
    def get_available_cities(self) -> List[str]:
        """Get list of available cities from the dataset."""
        return sorted(self.df['City'].unique().tolist())
    
    def get_available_categories(self) -> List[str]:
        """Get list of available business categories from the dataset."""
        return sorted(self.df['Category'].unique().tolist())
    
    def get_investment_range(self) -> Tuple[int, int]:
        """Get the minimum and maximum investment values from the dataset."""
        return int(self.df['Investment'].min()), int(self.df['Investment'].max())
    
    def calculate_market_gap(self, demand: float, competition: float) -> float:
        """
        Calculate market gap score.
        
        Args:
            demand (float): Business demand score (0-100)
            competition (float): Competition level (0-100)
            
        Returns:
            float: Market gap score (higher is better)
        """
        # Market gap = Demand - Competition
        # Normalize to 0-100 scale
        market_gap = demand - competition
        # Add 100 to make all values positive, then scale to 0-100
        normalized_gap = ((market_gap + 100) / 200) * 100
        return normalized_gap
    
    def calculate_budget_fit(self, user_budget: float, required_investment: float) -> float:
        """
        Calculate budget fit score.
        
        Args:
            user_budget (float): User's available budget
            required_investment (float): Required investment for the business
            
        Returns:
            float: Budget fit score (0-100)
        """
        if user_budget >= required_investment:
            # Perfect fit gets 100 points
            return 100.0
        else:
            # Partial fit based on percentage of budget coverage
            fit_percentage = (user_budget / required_investment) * 100
            return min(fit_percentage, 100.0)
    
    def calculate_interest_match(self, user_interests: List[str], business_category: str) -> float:
        """
        Calculate interest match score.
        
        Args:
            user_interests (List[str]): List of user's interested categories
            business_category (str): Business category
            
        Returns:
            float: Interest match score (0-100)
        """
        if business_category in user_interests:
            return 100.0
        else:
            # No match
            return 0.0
    
    def calculate_total_score(self, row: pd.Series, user_budget: float, 
                            user_interests: List[str]) -> float:
        """
        Calculate the total recommendation score for a business.
        
        Args:
            row (pd.Series): Business data row
            user_budget (float): User's available budget
            user_interests (List[str]): User's interested categories
            
        Returns:
            float: Total recommendation score
        """
        # Calculate individual scores
        market_gap = self.calculate_market_gap(row['Demand'], row['Competition'])
        budget_fit = self.calculate_budget_fit(user_budget, row['Investment'])
        interest_match = self.calculate_interest_match(user_interests, row['Category'])
        
        # Weighted total score
        # Market gap: 50% weight, Budget fit: 30% weight, Interest match: 20% weight
        total_score = (market_gap * 0.5) + (budget_fit * 0.3) + (interest_match * 0.2)
        
        return round(total_score, 2)
    
    def get_score_explanation(self, row: pd.Series, user_budget: float, 
                            user_interests: List[str]) -> str:
        """
        Generate explanation for the recommendation score.
        
        Args:
            row (pd.Series): Business data row
            user_budget (float): User's available budget
            user_interests (List[str]): User's interested categories
            
        Returns:
            str: Explanation of the score
        """
        market_gap = self.calculate_market_gap(row['Demand'], row['Competition'])
        budget_fit = self.calculate_budget_fit(user_budget, row['Investment'])
        interest_match = self.calculate_interest_match(user_interests, row['Category'])
        
        explanations = []
        
        # Market analysis
        if market_gap >= 70:
            explanations.append("🎯 High market opportunity (low competition, high demand)")
        elif market_gap >= 50:
            explanations.append("📈 Good market potential")
        else:
            explanations.append("⚠️ Competitive market")
        
        # Budget analysis
        if budget_fit == 100:
            explanations.append("💰 Perfect budget fit")
        elif budget_fit >= 80:
            explanations.append("💵 Good budget alignment")
        elif budget_fit >= 50:
            explanations.append("💲 Moderate budget requirement")
        else:
            explanations.append("💸 High investment needed")
        
        # Interest analysis
        if interest_match == 100:
            explanations.append("❤️ Matches your interests")
        else:
            explanations.append("🔍 Outside your preferred categories")
        
        return " | ".join(explanations)
    
    def get_recommendations(self, city: str, budget: float, interests: List[str], 
                          top_n: int = 3) -> List[Dict]:
        """
        Get top N business recommendations based on user preferences.
        
        Args:
            city (str): Selected city
            budget (float): User's available budget
            interests (List[str]): User's interested categories
            top_n (int): Number of top recommendations to return
            
        Returns:
            List[Dict]: List of recommended businesses with scores and explanations
        """
        # Filter businesses by city
        city_businesses = self.df[self.df['City'] == city].copy()
        
        if city_businesses.empty:
            return []
        
        # Calculate scores for all businesses in the city
        city_businesses['score'] = city_businesses.apply(
            lambda row: self.calculate_total_score(row, budget, interests), axis=1
        )
        
        # Add explanations
        city_businesses['explanation'] = city_businesses.apply(
            lambda row: self.get_score_explanation(row, budget, interests), axis=1
        )
        
        # Sort by score and get top N
        top_businesses = city_businesses.nlargest(top_n, 'score')
        
        # Convert to list of dictionaries
        recommendations = []
        for _, row in top_businesses.iterrows():
            recommendation = {
                'business_name': row['Business'],
                'category': row['Category'],
                'investment_required': row['Investment'],
                'demand': row['Demand'],
                'competition': row['Competition'],
                'score': row['score'],
                'explanation': row['explanation'],
                'market_gap': self.calculate_market_gap(row['Demand'], row['Competition']),
                'budget_fit': self.calculate_budget_fit(budget, row['Investment']),
                'interest_match': self.calculate_interest_match(interests, row['Category'])
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def get_city_summary(self, city: str) -> Dict:
        """
        Get summary statistics for a specific city.
        
        Args:
            city (str): City name
            
        Returns:
            Dict: Summary statistics for the city
        """
        city_data = self.df[self.df['City'] == city]
        
        if city_data.empty:
            return {}
        
        summary = {
            'total_businesses': len(city_data),
            'categories': city_data['Category'].nunique(),
            'avg_demand': round(city_data['Demand'].mean(), 1),
            'avg_competition': round(city_data['Competition'].mean(), 1),
            'min_investment': city_data['Investment'].min(),
            'max_investment': city_data['Investment'].max(),
            'avg_investment': round(city_data['Investment'].mean(), 0),
            'top_category': city_data['Category'].value_counts().index[0]
        }
        
        return summary
    
    def get_category_analysis(self, city: str) -> Dict:
        """
        Get category-wise analysis for a city.
        
        Args:
            city (str): City name
            
        Returns:
            Dict: Category analysis data
        """
        city_data = self.df[self.df['City'] == city]
        
        category_stats = city_data.groupby('Category').agg({
            'Demand': 'mean',
            'Competition': 'mean',
            'Investment': ['mean', 'min', 'max'],
            'Business': 'count'
        }).round(2)
        
        # Flatten column names
        category_stats.columns = [
            'avg_demand', 'avg_competition', 'avg_investment', 
            'min_investment', 'max_investment', 'business_count'
        ]
        
        # Calculate market gap for each category
        category_stats['market_gap'] = (
            category_stats['avg_demand'] - category_stats['avg_competition']
        ).round(2)
        
        return category_stats.to_dict('index')
    
    def predict_new_business_opportunity(self, city: str, category: str, 
                                       business_name: str, investment: float) -> Dict:
        """
        Predict market opportunity for a new business using ML.
        
        Args:
            city (str): City name
            category (str): Business category
            business_name (str): Business name
            investment (float): Investment amount
            
        Returns:
            Dict: Prediction results with demand, competition, and market analysis
        """
        if not self.use_ml or self.ml_predictor is None:
            return self._get_basic_prediction(city, category)
        
        try:
            prediction = self.ml_predictor.predict_single_business(
                city, category, business_name, investment
            )
            
            # Add interpretation
            prediction['interpretation'] = self._interpret_ml_prediction(prediction)
            prediction['recommendation'] = self._get_business_recommendation(prediction)
            
            return prediction
            
        except Exception as e:
            print(f"⚠️ ML prediction failed: {str(e)}")
            return self._get_basic_prediction(city, category)
    
    def _get_basic_prediction(self, city: str, category: str) -> Dict:
        """Get basic prediction without ML."""
        city_data = self.df[(self.df['City'] == city) & (self.df['Category'] == category)]
        
        if city_data.empty:
            # Use category averages
            category_data = self.df[self.df['Category'] == category]
            avg_demand = category_data['Demand'].mean() if not category_data.empty else 70
            avg_competition = category_data['Competition'].mean() if not category_data.empty else 50
        else:
            avg_demand = city_data['Demand'].mean()
            avg_competition = city_data['Competition'].mean()
        
        return {
            'demand': round(avg_demand, 1),
            'competition': round(avg_competition, 1),
            'market_gap': round(avg_demand - avg_competition, 1),
            'confidence': 0.7,
            'prediction_quality': 'Basic'
        }
    
    def _interpret_ml_prediction(self, prediction: Dict) -> str:
        """Interpret ML prediction results."""
        market_gap = prediction['market_gap']
        confidence = prediction['confidence']
        
        if market_gap > 20 and confidence > 0.8:
            return "🚀 Excellent opportunity with high confidence"
        elif market_gap > 15 and confidence > 0.7:
            return "📈 Good opportunity with solid predictions"
        elif market_gap > 5:
            return "📊 Moderate opportunity, consider market research"
        else:
            return "⚠️ Challenging market, high competition expected"
    
    def _get_business_recommendation(self, prediction: Dict) -> str:
        """Get business recommendation based on prediction."""
        demand = prediction['demand']
        competition = prediction['competition']
        confidence = prediction['confidence']
        
        if demand > 80 and competition < 40:
            return "🎯 Highly recommended - High demand, low competition"
        elif demand > 70 and competition < 60:
            return "👍 Recommended - Good market potential"
        elif confidence < 0.6:
            return "🔍 Needs more research - Low prediction confidence"
        else:
            return "⚠️ Proceed with caution - Competitive market"

# Test the recommendation engine
if __name__ == "__main__":
    # Initialize the engine
    engine = BusinessRecommendationEngine()
    
    # Test recommendations
    test_city = "Mumbai"
    test_budget = 3000000
    test_interests = ["Food", "Tech"]
    
    print(f"\n🔍 Testing recommendations for {test_city}")
    print(f"💰 Budget: ₹{test_budget:,}")
    print(f"❤️ Interests: {', '.join(test_interests)}")
    print("-" * 60)
    
    recommendations = engine.get_recommendations(test_city, test_budget, test_interests)
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['business_name']} ({rec['category']})")
        print(f"   💰 Investment: ₹{rec['investment_required']:,}")
        print(f"   📊 Score: {rec['score']}/100")
        print(f"   📈 Demand: {rec['demand']} | Competition: {rec['competition']}")
        print(f"   📝 {rec['explanation']}")
    
    # Test city summary
    print(f"\n\n📍 City Summary for {test_city}:")
    summary = engine.get_city_summary(test_city)
    for key, value in summary.items():
        print(f"   {key}: {value}")