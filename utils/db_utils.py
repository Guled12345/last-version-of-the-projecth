"""
Simplified database utilities for PostgreSQL integration
Direct database operations without SQLAlchemy complexity
"""

import os
import psycopg2
import json
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

def get_db_connection():
    """Get PostgreSQL database connection"""
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

def save_prediction_to_db(prediction_data):
    """Save prediction data to PostgreSQL database"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        
        # Get or create student
        student_name = prediction_data.get('student_name', 'Unknown Student')
        grade_level = prediction_data.get('grade_level', 'Unknown')
        
        cur.execute(
            "SELECT id FROM students WHERE name = %s",
            (student_name,)
        )
        student_record = cur.fetchone()
        
        if student_record:
            student_id = student_record[0]
        else:
            cur.execute(
                "INSERT INTO students (name, grade_level) VALUES (%s, %s) RETURNING id",
                (student_name, grade_level)
            )
            student_id = cur.fetchone()[0]
        
        # Insert prediction
        cur.execute("""
            INSERT INTO predictions (
                student_id, math_score, reading_score, writing_score, 
                attendance, behavior, literacy, prediction, probability, 
                risk_level, notes, timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            student_id,
            prediction_data.get('math_score'),
            prediction_data.get('reading_score'),
            prediction_data.get('writing_score'),
            prediction_data.get('attendance'),
            prediction_data.get('behavior'),
            prediction_data.get('literacy'),
            prediction_data.get('prediction'),
            prediction_data.get('probability'),
            prediction_data.get('risk_level'),
            prediction_data.get('notes', ''),
            datetime.fromisoformat(prediction_data.get('timestamp', datetime.now().isoformat()))
        ))
        
        conn.commit()
        logger.info(f"Prediction saved for student: {student_name}")
        return True
        
    except Exception as e:
        conn.rollback()
        logger.error(f"Error saving prediction: {e}")
        return False
    finally:
        conn.close()

def save_parent_observation_to_db(observation_data):
    """Save parent observation to PostgreSQL database"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        
        # Get or create student
        child_name = observation_data.get('child_name', 'Unknown Child')
        
        cur.execute(
            "SELECT id FROM students WHERE name = %s",
            (child_name,)
        )
        student_record = cur.fetchone()
        
        if student_record:
            student_id = student_record[0]
        else:
            cur.execute(
                "INSERT INTO students (name, grade_level) VALUES (%s, %s) RETURNING id",
                (child_name, 'Unknown')
            )
            student_id = cur.fetchone()[0]
        
        # Convert subjects_struggled list to JSON string
        subjects_struggled = observation_data.get('subjects_struggled', [])
        if isinstance(subjects_struggled, list):
            subjects_struggled = json.dumps(subjects_struggled)
        
        # Insert observation
        cur.execute("""
            INSERT INTO parent_observations (
                student_id, child_name, date, homework_completion, reading_time,
                focus_level, subjects_struggled, behavior_rating, mood_rating,
                sleep_hours, energy_level, social_interactions, learning_wins,
                challenges_faced, strategies_used, screen_time, physical_activity,
                medication_taken, special_events, timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            student_id,
            child_name,
            datetime.fromisoformat(observation_data.get('date', date.today().isoformat())),
            observation_data.get('homework_completion'),
            observation_data.get('reading_time'),
            observation_data.get('focus_level'),
            subjects_struggled,
            observation_data.get('behavior_rating'),
            observation_data.get('mood_rating'),
            observation_data.get('sleep_hours'),
            observation_data.get('energy_level'),
            observation_data.get('social_interactions', ''),
            observation_data.get('learning_wins', ''),
            observation_data.get('challenges_faced', ''),
            observation_data.get('strategies_used', ''),
            observation_data.get('screen_time'),
            observation_data.get('physical_activity'),
            observation_data.get('medication_taken', False),
            observation_data.get('special_events', ''),
            datetime.fromisoformat(observation_data.get('timestamp', datetime.now().isoformat()))
        ))
        
        conn.commit()
        logger.info(f"Parent observation saved for: {child_name}")
        return True
        
    except Exception as e:
        conn.rollback()
        logger.error(f"Error saving parent observation: {e}")
        return False
    finally:
        conn.close()

def load_student_predictions():
    """Load all student prediction data from database"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT p.*, s.name, s.grade_level 
            FROM predictions p 
            JOIN students s ON p.student_id = s.id 
            ORDER BY p.timestamp DESC
        """)
        
        predictions = []
        for row in cur.fetchall():
            prediction_dict = {
                'id': row[0],
                'math_score': row[2],
                'reading_score': row[3],
                'writing_score': row[4],
                'attendance': row[5],
                'behavior': row[6],
                'literacy': row[7],
                'prediction': row[8],
                'probability': row[9],
                'risk_level': row[10],
                'notes': row[11],
                'timestamp': row[12].isoformat(),
                'student_name': row[13],
                'grade_level': row[14]
            }
            predictions.append(prediction_dict)
        
        return predictions
        
    except Exception as e:
        logger.error(f"Error loading predictions: {e}")
        return []
    finally:
        conn.close()

def load_parent_observations():
    """Load all parent observation data from database"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT po.*, s.name 
            FROM parent_observations po 
            JOIN students s ON po.student_id = s.id 
            ORDER BY po.timestamp DESC
        """)
        
        observations = []
        for row in cur.fetchall():
            # Parse subjects_struggled back to list
            subjects_struggled = row[8] or '[]'
            try:
                subjects_struggled = json.loads(subjects_struggled)
            except json.JSONDecodeError:
                subjects_struggled = []
            
            observation_dict = {
                'id': row[0],
                'child_name': row[2],
                'date': row[3].isoformat(),
                'homework_completion': row[4],
                'reading_time': row[5],
                'focus_level': row[6],
                'subjects_struggled': subjects_struggled,
                'behavior_rating': row[9],
                'mood_rating': row[10],
                'sleep_hours': row[11],
                'energy_level': row[12],
                'social_interactions': row[13],
                'learning_wins': row[14],
                'challenges_faced': row[15],
                'strategies_used': row[16],
                'screen_time': row[17],
                'physical_activity': row[18],
                'medication_taken': row[19],
                'special_events': row[20],
                'timestamp': row[21].isoformat()
            }
            observations.append(observation_dict)
        
        return observations
        
    except Exception as e:
        logger.error(f"Error loading observations: {e}")
        return []
    finally:
        conn.close()

def authenticate_user_db(username, password):
    """Authenticate user against database"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, user_type, full_name, email, created_date FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        user_record = cur.fetchone()
        
        if user_record:
            return {
                'id': user_record[0],
                'username': user_record[1],
                'user_type': user_record[2],
                'full_name': user_record[3],
                'email': user_record[4],
                'created_date': user_record[5].isoformat()
            }
        return None
        
    except Exception as e:
        logger.error(f"Error authenticating user: {e}")
        return None
    finally:
        conn.close()

def get_database_stats():
    """Get database statistics"""
    conn = get_db_connection()
    if not conn:
        return {
            'total_students': 0,
            'total_predictions': 0,
            'total_observations': 0,
            'total_users': 0,
            'last_prediction_date': None,
            'last_observation_date': None
        }
    
    try:
        cur = conn.cursor()
        
        # Get counts
        cur.execute("SELECT COUNT(*) FROM students")
        total_students = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM predictions")
        total_predictions = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM parent_observations")
        total_observations = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM users")
        total_users = cur.fetchone()[0]
        
        # Get latest dates
        cur.execute("SELECT MAX(timestamp) FROM predictions")
        latest_prediction = cur.fetchone()[0]
        
        cur.execute("SELECT MAX(timestamp) FROM parent_observations")
        latest_observation = cur.fetchone()[0]
        
        return {
            'total_students': total_students,
            'total_predictions': total_predictions,
            'total_observations': total_observations,
            'total_users': total_users,
            'last_prediction_date': latest_prediction.isoformat() if latest_prediction else None,
            'last_observation_date': latest_observation.isoformat() if latest_observation else None
        }
        
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        return {
            'total_students': 0,
            'total_predictions': 0,
            'total_observations': 0,
            'total_users': 0,
            'last_prediction_date': None,
            'last_observation_date': None
        }
    finally:
        conn.close()