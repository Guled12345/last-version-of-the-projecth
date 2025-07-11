import pickle
import numpy as np
import os
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

def get_model_path():
    """Get the correct path for the model file"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Check for user's trained model first, then fall back to sample model
    user_model_path = os.path.join(base_path, 'data', 'learning_difficulty_detector.pkl')
    sample_model_path = os.path.join(base_path, 'data', 'sample_model.pkl')
    
    if os.path.exists(user_model_path) and os.path.getsize(user_model_path) > 100:
        return user_model_path
    else:
        return sample_model_path

def create_sample_model():
    """Create a sample model for demonstration purposes"""
    # Generate synthetic training data
    np.random.seed(42)
    n_samples = 1000
    
    # Features: math_score, reading_score, writing_score, attendance, behavior, literacy
    X = np.random.rand(n_samples, 6)
    
    # Scale features to realistic ranges
    X[:, 0] = X[:, 0] * 100  # math_score (0-100)
    X[:, 1] = X[:, 1] * 100  # reading_score (0-100)
    X[:, 2] = X[:, 2] * 100  # writing_score (0-100)
    X[:, 3] = X[:, 3] * 100  # attendance (0-100)
    X[:, 4] = X[:, 4] * 4 + 1  # behavior (1-5)
    X[:, 5] = X[:, 5] * 9 + 1  # literacy (1-10)
    
    # Create realistic target variable
    # Higher risk for lower academic scores, poor attendance, low behavior ratings
    risk_score = (
        (100 - X[:, 0]) * 0.25 +  # Lower math score increases risk
        (100 - X[:, 1]) * 0.25 +  # Lower reading score increases risk
        (100 - X[:, 2]) * 0.2 +   # Lower writing score increases risk
        (100 - X[:, 3]) * 0.2 +   # Lower attendance increases risk
        (5 - X[:, 4]) * 10 +      # Lower behavior rating increases risk
        (10 - X[:, 5]) * 5        # Lower literacy increases risk
    )
    
    # Add some noise
    risk_score += np.random.normal(0, 10, n_samples)
    
    # Convert to binary classification (1 = high risk, 0 = low risk)
    y = (risk_score > np.percentile(risk_score, 70)).astype(int)
    
    # Train the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Test accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Sample model accuracy: {accuracy:.2f}")
    
    return model

def load_model():
    """Load the learning difficulty prediction model"""
    model_path = get_model_path()
    
    try:
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model_package = pickle.load(f)
            
            # Handle both old format (just model) and new format (package with scaler)
            if isinstance(model_package, dict) and 'model' in model_package:
                print(f"User's trained model loaded from {model_path}")
                return model_package
            else:
                # Legacy format - wrap in package format
                return {
                    'model': model_package,
                    'scaler': None,
                    'feature_names': ['math_score', 'reading_score', 'writing_score', 'attendance', 'behavior', 'literacy'],
                    'feature_order': ['math_score', 'reading_score', 'writing_score', 'attendance', 'behavior', 'literacy']
                }
        else:
            # Create and save sample model if none exists
            print("No model found, creating sample model...")
            model = create_sample_model()
            
            # Ensure data directory exists
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            # Save the model
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
            
            return {
                'model': model,
                'scaler': None,
                'feature_names': ['math_score', 'reading_score', 'writing_score', 'attendance', 'behavior', 'literacy'],
                'feature_order': ['math_score', 'reading_score', 'writing_score', 'attendance', 'behavior', 'literacy']
            }
    
    except Exception as e:
        print(f"Error loading model: {e}")
        # Fall back to creating a new sample model
        sample_model = create_sample_model()
        return {
            'model': sample_model,
            'scaler': None,
            'feature_names': ['math_score', 'reading_score', 'writing_score', 'attendance', 'behavior', 'literacy'],
            'feature_order': ['math_score', 'reading_score', 'writing_score', 'attendance', 'behavior', 'literacy']
        }

def make_prediction(student_data):
    """
    Make a prediction for a student based on their data
    
    Args:
        student_data (dict): Dictionary containing student metrics
            - math_score: Math performance score (0-100)
            - reading_score: Reading performance score (0-100)
            - writing_score: Writing performance score (0-100)
            - attendance: Attendance percentage (0-100)
            - behavior: Behavior rating (1-5)
            - literacy: Literacy level (1-10)
    
    Returns:
        tuple: (prediction, probability) where prediction is 0/1 and probability is float
    """
    try:
        model_package = load_model()
        model = model_package['model']
        scaler = model_package.get('scaler')
        
        # Prepare input features in the correct order
        features = np.array([[
            student_data['math_score'],
            student_data['reading_score'],
            student_data['writing_score'],
            student_data['attendance'],
            student_data['behavior'],
            student_data['literacy']
        ]])
        
        # Apply scaling if the model uses StandardScaler (from user's notebook)
        if scaler is not None:
            features = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features)[0]
        prediction_proba = model.predict_proba(features)[0]
        
        # Get probability of positive class (learning difficulty risk)
        risk_probability = prediction_proba[1] if len(prediction_proba) > 1 else prediction_proba[0]
        
        return int(prediction), float(risk_probability)
    
    except Exception as e:
        print(f"Error making prediction: {e}")
        # Fallback prediction based on simple rules
        academic_avg = (student_data['math_score'] + student_data['reading_score'] + student_data['writing_score']) / 3
        
        # Simple risk calculation
        risk_factors = 0
        if academic_avg < 70:
            risk_factors += 2
        if student_data['attendance'] < 80:
            risk_factors += 1
        if student_data['behavior'] < 3:
            risk_factors += 1
        if student_data['literacy'] < 5:
            risk_factors += 1
        
        # Convert to probability
        risk_probability = min(risk_factors / 5.0, 1.0)
        prediction = 1 if risk_probability > 0.5 else 0
        
        return prediction, risk_probability

def get_feature_importance():
    """Get feature importance from the model"""
    try:
        model_package = load_model()
        model = model_package['model']
        
        if hasattr(model, 'feature_importances_'):
            feature_names = ['Math Score', 'Reading Score', 'Writing Score', 'Attendance', 'Behavior', 'Literacy']
            importance_dict = dict(zip(feature_names, model.feature_importances_))
            return importance_dict
        else:
            # Return default importance if model doesn't support it
            return {
                'Math Score': 0.20,
                'Reading Score': 0.25,
                'Writing Score': 0.15,
                'Attendance': 0.15,
                'Behavior': 0.15,
                'Literacy': 0.10
            }
    
    except Exception as e:
        print(f"Error getting feature importance: {e}")
        return {
            'Math Score': 0.20,
            'Reading Score': 0.25,
            'Writing Score': 0.15,
            'Attendance': 0.15,
            'Behavior': 0.15,
            'Literacy': 0.10
        }

def validate_student_data(student_data):
    """Validate student data before making prediction"""
    required_fields = ['math_score', 'reading_score', 'writing_score', 'attendance', 'behavior', 'literacy']
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in student_data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate ranges
    if not (0 <= student_data['math_score'] <= 100):
        raise ValueError("Math score must be between 0 and 100")
    if not (0 <= student_data['reading_score'] <= 100):
        raise ValueError("Reading score must be between 0 and 100")
    if not (0 <= student_data['writing_score'] <= 100):
        raise ValueError("Writing score must be between 0 and 100")
    if not (0 <= student_data['attendance'] <= 100):
        raise ValueError("Attendance must be between 0 and 100")
    if not (1 <= student_data['behavior'] <= 5):
        raise ValueError("Behavior rating must be between 1 and 5")
    if not (1 <= student_data['literacy'] <= 10):
        raise ValueError("Literacy level must be between 1 and 10")
    
    return True
