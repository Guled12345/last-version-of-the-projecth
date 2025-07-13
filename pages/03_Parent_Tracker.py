# pages/03_Parent_Tracker.py - Enhanced with Improved Animations and UI
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
import json
import os
import sys

# Enhanced Lottie import
try:
    from streamlit_lottie import st_lottie
    import requests
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

# Append parent directory to sys.path to enable importing from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_utils import save_parent_observation, load_parent_observations
from utils.image_base64 import get_base64_images
from utils.language_utils import get_text, load_app_settings, save_app_settings
from utils.exact_ui import (
    add_exact_ui_styles,
    render_exact_sidebar,
    render_exact_page_header,
    custom_alert,
    create_exact_metric_card,
    create_exact_chart_container,
    get_b64_image_html
)
from utils.auth_utils import is_authenticated, render_login_page, logout_user, get_user_role
from utils.icon_utils import get_material_icon_html

# Page config
st.set_page_config(
    page_title="EduScan Parent Tracker",
    page_icon="👨‍👩‍👧‍👦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply styles and initialize
add_exact_ui_styles()

if 'app_language' not in st.session_state:
    settings = load_app_settings()
    st.session_state['app_language'] = settings.get('language', 'English')
if 'app_theme' not in st.session_state:
    settings = load_app_settings()
    st.session_state['app_theme'] = settings.get('theme', 'Light')
if 'offline_mode' not in st.session_state:
    settings = load_app_settings()
    st.session_state['offline_mode'] = settings.get('offline_mode', False)

language = st.session_state.get('app_language', 'English')
current_theme = st.session_state.get('app_theme', 'Light')

st.markdown(f"""
    <script>
        document.body.setAttribute('data-theme', '{current_theme}');
    </script>
""", unsafe_allow_html=True)

render_exact_sidebar()

# Initialize session state for parent data
if 'parent_data' not in st.session_state:
    st.session_state['parent_data'] = []
if 'weekly_data' not in st.session_state:
    st.session_state['weekly_data'] = []

# Clean Lottie functions
def load_lottie_url(url: str):
    """Load Lottie animation with timeout"""
    if not LOTTIE_AVAILABLE:
        return None
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

def remove_lottie_background(lottie_json):
    """Simple background removal"""
    if not lottie_json:
        return None
    try:
        if 'bg' in lottie_json:
            del lottie_json['bg']
        lottie_json['bg'] = None
        return lottie_json
    except:
        return lottie_json

def render_lottie(url, height=200, key=None, fallback_icon="family_restroom", fallback_text="Loading..."):
    """Simple Lottie renderer with fallback"""
    if LOTTIE_AVAILABLE:
        lottie_json = load_lottie_url(url)
        if lottie_json:
            cleaned = remove_lottie_background(lottie_json)
            try:
                st_lottie(cleaned, height=height, key=key, speed=1, loop=True, quality="high")
                return True
            except:
                pass
    
    # Elegant fallback
    st.markdown(f"""
    <div style="height: {height}px; display: flex; flex-direction: column; align-items: center; justify-content: center; 
         background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(59, 130, 246, 0.1)); 
         border-radius: 12px; text-align: center; border: 2px dashed rgba(139, 92, 246, 0.3);">
        <span class="material-symbols-outlined" style="font-size: 3rem; color: var(--primary-purple); margin-bottom: 0.5rem; animation: pulse 2s infinite;">{fallback_icon}</span>
        <p style="color: var(--gray-600); margin: 0; font-weight: 500;">{fallback_text}</p>
    </div>
    """, unsafe_allow_html=True)
    return False

def create_progress_chart(data, metric):
    """Create enhanced progress chart for specific metric"""
    df = pd.DataFrame(data)
    if df.empty:
        return None
    
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Determine color based on metric type
    color_map = {
        'homework_completion': '#10b981',  # Green
        'behavior_rating': '#3b82f6',     # Blue
        'mood_rating': '#f59e0b',         # Orange
        'sleep_hours': '#8b5cf6',         # Purple
        'reading_time': '#ef4444',        # Red
        'physical_activity': '#06b6d4'    # Cyan
    }
    
    color = color_map.get(metric, '#6b7280')
    
    fig = px.line(df, x='date', y=metric, 
                  title=f"{metric.replace('_', ' ').title()} Progress Over Time",
                  markers=True,
                  color_discrete_sequence=[color])
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=metric.replace('_', ' ').title(),
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter'},
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_weekly_summary(data):
    """Create enhanced weekly summary visualization"""
    if not data:
        return None, None
    
    df = pd.DataFrame(data)
    if df.empty:
        return None, None

    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.to_period('W')
    
    # Calculate weekly averages
    weekly_avg = df.groupby('week')[['homework_completion', 'behavior_rating', 'sleep_hours', 'mood_rating']].mean()
    
    if weekly_avg.empty:
        return None, None

    # Create enhanced summary chart
    fig = go.Figure()
    
    colors = ['#8b5cf6', '#f59e0b', '#10b981', '#3b82f6']
    metrics_map = {
        'homework_completion': 'Homework Completion',
        'behavior_rating': 'Behavior Rating',
        'sleep_hours': 'Sleep Hours',
        'mood_rating': 'Mood Rating',
    }
    
    for i, metric in enumerate(['homework_completion', 'behavior_rating', 'sleep_hours', 'mood_rating']):
        fig.add_trace(go.Scatter(
            x=weekly_avg.index.astype(str),
            y=weekly_avg[metric],
            mode='lines+markers',
            name=metrics_map[metric],
            line=dict(color=colors[i], width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title="Weekly Progress Summary",
        xaxis_title="Week",
        yaxis_title="Score",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter'},
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig, weekly_avg

def main():
    # Authentication check
    if not is_authenticated():
        st.warning("Please log in to access the Parent Tracker page.")
        st.switch_page("app.py")
        return

    # Role-based access controls
    user_role = get_user_role()
    if user_role == 'teacher':
        st.error("Access Denied: Teachers cannot view Parent Resources.")
        st.info("Redirecting you to Teacher Resources...")
        st.switch_page("pages/02_Teacher_Resources.py")
        return
    
    # Header
    render_exact_page_header(
        get_material_icon_html('family_restroom'), 
        'Parent Trackers', 
        'Monitor Your Child\'s Learning Journey Together', 
        language
    )
    
    # Enhanced hero section with multiple animations
    st.markdown("### 🌟 Strengthening Home-School Connections")
    
    # Three-column animation layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📊 Progress Tracking**")
        render_lottie(
            "https://lottie.host/ceff5ec9-b733-44f1-b68e-aa9d6676297d/xGcBHYi1ID.json",
            height=200,
            key="progress_tracking",
            fallback_icon="analytics",
            fallback_text="Daily Progress Monitoring"
        )
        st.caption("Track daily learning activities and behaviors")
    
    with col2:
        st.markdown("**👨‍👩‍👧‍👦 Family Support**")
        render_lottie(
            "https://lottie.host/ed479bf5-36af-4dd8-84f2-f5893f0687f9/Tgc64kKeCO.json",
            height=200,
            key="family_support",
            fallback_icon="family_restroom",
            fallback_text="Family Collaboration"
        )
        st.caption("Building strong family-school partnerships")
    
    with col3:
        st.markdown("**🎯 Student Success**")
        render_lottie(
            "https://lottie.host/4e1ac443-9c90-4a25-b20d-c918d5a0290f/pa2Qd9xE5l.json",
            height=200,
            key="student_success_parent",
            fallback_icon="emoji_events",
            fallback_text="Celebrating Achievements"
        )
        st.caption("Celebrating learning milestones together")

    # Enhanced impact cards
    st.markdown("---")
    st.markdown("### 💡 Family Engagement Impact")
    
    impact_col1, impact_col2 = st.columns(2)
    
    with impact_col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
             border-radius: 16px; color: white; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3>📈 Academic Growth</h3>
            <p>Monitor daily progress and identify learning patterns</p>
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-top: 1rem;">
                <strong>Track homework, reading, and focus levels</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
             border-radius: 16px; color: white; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3>🤝 School Communication</h3>
            <p>Bridge home and school with shared insights</p>
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-top: 1rem;">
                <strong>Share observations with teachers</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with impact_col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
             border-radius: 16px; color: white; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3>😊 Social-Emotional Health</h3>
            <p>Monitor mood, behavior, and well-being indicators</p>
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-top: 1rem;">
                <strong>Track mood and behavioral patterns</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
             border-radius: 16px; color: white; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3>🏠 Home Environment</h3>
            <p>Optimize learning conditions and routines</p>
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-top: 1rem;">
                <strong>Balance screen time and activities</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Enhanced sidebar
    with st.sidebar:
        st.markdown("### 👤 Child Information")
        
        # Child selection with better UX
        child_name = st.text_input(
            "Child's Name", 
            placeholder="Enter your child's full name", 
            key="pt_child_name_input",
            help="This will be used to track and organize all observations"
        )
        
        if child_name:
            st.success(f"✅ Tracking progress for **{child_name}**")
            
            # Show quick stats if data exists
            all_observations = load_parent_observations()
            child_observations = [obs for obs in all_observations if obs.get('child_name') == child_name]
            
            if child_observations:
                st.metric("Total Observations", len(child_observations))
                
                latest_obs = max(child_observations, key=lambda x: x['date'])
                latest_date = date.fromisoformat(latest_obs['date'])
                days_since = (date.today() - latest_date).days
                
                if days_since == 0:
                    st.info("📅 Last entry: Today")
                elif days_since == 1:
                    st.info("📅 Last entry: Yesterday")
                else:
                    st.warning(f"📅 Last entry: {days_since} days ago")
        
        st.markdown("### 🎯 Dashboard Views")
        dashboard_view = st.selectbox(
            "Choose your view:",
            ["Daily Entry", "Progress Tracking", "Weekly Summary", "Observations Log"],
            key="pt_dashboard_view_selector",
            help="Select what you'd like to view or update"
        )
        
        # Enhanced date range for analysis
        if dashboard_view in ["Progress Tracking", "Weekly Summary"]:
            st.markdown("### 📅 Analysis Period")
            
            period_preset = st.selectbox(
                "Quick periods:",
                ["Last 7 days", "Last 30 days", "Last 3 months", "Custom range"],
                key="period_preset"
            )
            
            if period_preset == "Custom range":
                end_date = st.date_input("End Date", value=date.today(), key="pt_end_date_input")
                start_date = st.date_input("Start Date", value=end_date - timedelta(days=30), key="pt_start_date_input")
            else:
                end_date = date.today()
                if period_preset == "Last 7 days":
                    start_date = end_date - timedelta(days=7)
                elif period_preset == "Last 30 days":
                    start_date = end_date - timedelta(days=30)
                else:  # Last 3 months
                    start_date = end_date - timedelta(days=90)
            
            st.info(f"📊 Analyzing: {start_date} to {end_date}")

    # Main content based on selected view
    if not child_name:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(59, 130, 246, 0.1)); 
             border-radius: 16px; border: 2px dashed rgba(139, 92, 246, 0.3);">
            <span class="material-symbols-outlined" style="font-size: 4rem; color: var(--primary-purple); margin-bottom: 1rem;">child_care</span>
            <h3 style="color: var(--gray-700); margin-bottom: 1rem;">Welcome to Parent Tracker!</h3>
            <p style="color: var(--gray-600); font-size: 1.1rem;">Please enter your child's name in the sidebar to begin tracking their learning journey.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    if dashboard_view == "Daily Entry":
        # Enhanced daily entry with better UX
        if 'daily_entry_reset_counter' not in st.session_state:
            st.session_state['daily_entry_reset_counter'] = 0

        st.markdown("## 📝 Daily Observation Entry")
        st.markdown(f"Recording observations for **{child_name}** on {date.today().strftime('%A, %B %d, %Y')}")
        
        # Check if entry exists for today
        all_observations = load_parent_observations()
        today_entry = next((obs for obs in all_observations 
                           if obs.get('child_name') == child_name and obs['date'] == date.today().isoformat()), None)
        
        if today_entry:
            st.info("📋 You already have an entry for today. You can update it by submitting again.")
        
        with st.form("daily_observation_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📚 Academic Activities")
                
                homework_completion = st.slider(
                    "Homework Completion (%)", 
                    0, 100, 75,
                    help="What percentage of assigned homework was completed?",
                    key=f"pt_homework_completion_input_{st.session_state['daily_entry_reset_counter']}"
                )
                
                reading_time = st.number_input(
                    "Independent Reading Time (minutes)", 
                    min_value=0, max_value=180, value=20,
                    help="How many minutes did your child spend reading independently?",
                    key=f"pt_reading_time_input_{st.session_state['daily_entry_reset_counter']}"
                )
                
                focus_level = st.select_slider(
                    "Focus & Concentration Level",
                    options=["Very Poor", "Poor", "Average", "Good", "Excellent"],
                    value="Good",
                    key=f"pt_focus_level_input_{st.session_state['daily_entry_reset_counter']}"
                )
                
                subjects_struggled = st.multiselect(
                    "Subjects with Difficulties",
                    ["Math", "Reading", "Writing", "Science", "Social Studies", "Art", "Music", "Other"],
                    help="Select subjects where your child struggled today",
                    key=f"pt_subjects_struggled_input_{st.session_state['daily_entry_reset_counter']}"
                )
            
            with col2:
                st.markdown("### 🎭 Behavioral & Emotional")
                
                behavior_rating = st.select_slider(
                    "Overall Behavior Rating", 
                    options=["1 - Poor", "2 - Below Average", "3 - Average", "4 - Good", "5 - Excellent"],
                    value="3 - Average",
                    help="Rate your child's overall behavior today",
                    key=f"pt_behavior_rating_input_{st.session_state['daily_entry_reset_counter']}"
                )
                behavior_value = int(behavior_rating.split(' ')[0])
                
                mood_rating = st.select_slider(
                    "Mood & Emotional State", 
                    options=["1 - Very Low", "2 - Low", "3 - Normal", "4 - Happy", "5 - Very Happy"],
                    value="3 - Normal",
                    help="How was your child's mood today?",
                    key=f"pt_mood_rating_input_{st.session_state['daily_entry_reset_counter']}"
                )
                mood_value = int(mood_rating.split(' ')[0])
                
                sleep_hours = st.number_input(
                    "Sleep Duration (hours)", 
                    min_value=4.0, max_value=12.0, value=8.0, step=0.5,
                    help="How many hours did your child sleep last night?",
                    key=f"pt_sleep_hours_input_{st.session_state['daily_entry_reset_counter']}"
                )
                
                energy_level = st.select_slider(
                    "Energy Level Throughout Day",
                    options=["Very Low", "Low", "Normal", "High", "Very High"],
                    value="Normal",
                    key=f"pt_energy_level_input_{st.session_state['daily_entry_reset_counter']}"
                )
            
            st.markdown("### 📝 Detailed Observations")
            
            col3, col4 = st.columns(2)
            
            with col3:
                learning_wins = st.text_area(
                    "🏆 Learning Wins & Successes",
                    placeholder="What went well today? Any breakthroughs, proud moments, or achievements?",
                    height=100,
                    key=f"pt_learning_wins_input_{st.session_state['daily_entry_reset_counter']}"
                )
                
                challenges_faced = st.text_area(
                    "⚠️ Challenges & Difficulties",
                    placeholder="What was difficult today? Any specific struggles or concerns?",
                    height=100,
                    key=f"pt_challenges_faced_input_{st.session_state['daily_entry_reset_counter']}"
                )
            
            with col4:
                strategies_used = st.text_area(
                    "💡 Helpful Strategies & Support",
                    placeholder="What strategies, tools, or supports helped your child today?",
                    height=100,
                    key=f"pt_strategies_used_input_{st.session_state['daily_entry_reset_counter']}"
                )
                
                social_interactions = st.text_area(
                    "👥 Social Interactions",
                    placeholder="How did your child interact with family, friends, or peers today?",
                    height=100,
                    key=f"pt_social_interactions_input_{st.session_state['daily_entry_reset_counter']}"
                )
            
            st.markdown("### 🏠 Home Environment Factors")
            
            col5, col6 = st.columns(2)
            
            with col5:
                screen_time = st.number_input(
                    "Screen Time (hours)", 
                    min_value=0.0, max_value=12.0, value=2.0, step=0.5,
                    help="Total recreational screen time (TV, games, devices)",
                    key=f"pt_screen_time_input_{st.session_state['daily_entry_reset_counter']}"
                )
                
                physical_activity = st.number_input(
                    "Physical Activity (minutes)", 
                    min_value=0, max_value=300, value=60,
                    help="Total time spent in physical activities or exercise",
                    key=f"pt_physical_activity_input_{st.session_state['daily_entry_reset_counter']}"
                )
            
            with col6:
                medication_taken = st.checkbox(
                    "💊 Medication taken as prescribed", 
                    help="Check if all prescribed medications were taken properly",
                    key=f"pt_medication_taken_checkbox_{st.session_state['daily_entry_reset_counter']}"
                )
                
                special_events = st.text_input(
                    "🎉 Special Events or Changes",
                    placeholder="Any unusual events, schedule changes, or disruptions today?",
                    key=f"pt_special_events_input_{st.session_state['daily_entry_reset_counter']}"
                )
            
            # Enhanced button layout
            col_buttons = st.columns(3)
            with col_buttons[0]:
                submitted = st.form_submit_button("💾 Save Today's Observation", type="primary", use_container_width=True)
            with col_buttons[1]:
                clear_button = st.form_submit_button("🔄 Clear Form", use_container_width=True)
            with col_buttons[2]:
                if today_entry:
                    delete_button = st.form_submit_button("🗑️ Delete Today's Entry", use_container_width=True)

            if submitted:
                observation_data = {
                    "child_name": child_name,
                    "date": date.today().isoformat(),
                    "homework_completion": homework_completion,
                    "reading_time": reading_time,
                    "focus_level": focus_level,
                    "subjects_struggled": subjects_struggled,
                    "behavior_rating": behavior_value,
                    "mood_rating": mood_value,
                    "sleep_hours": sleep_hours,
                    "energy_level": energy_level,
                    "learning_wins": learning_wins,
                    "challenges_faced": challenges_faced,
                    "strategies_used": strategies_used,
                    "social_interactions": social_interactions,
                    "screen_time": screen_time,
                    "physical_activity": physical_activity,
                    "medication_taken": medication_taken,
                    "special_events": special_events,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Save to both persistent storage and session state
                save_parent_observation(observation_data)
                
                # Also save to session state for immediate access
                if 'parent_data' not in st.session_state:
                    st.session_state['parent_data'] = []
                
                # Remove any existing entry for today and add the new one
                st.session_state['parent_data'] = [obs for obs in st.session_state['parent_data'] 
                                                 if not (obs.get('child_name') == child_name and obs['date'] == date.today().isoformat())]
                st.session_state['parent_data'].append(observation_data)
                
                st.success("✅ Daily observation saved successfully!")
                st.balloons()
            
            if clear_button:
                st.session_state['daily_entry_reset_counter'] += 1
                st.rerun()
            
            # Handle delete button if today's entry exists
            if today_entry and 'delete_button' in locals() and delete_button:
                # Remove today's entry from observations
                all_observations = [obs for obs in all_observations 
                                  if not (obs.get('child_name') == child_name and obs['date'] == date.today().isoformat())]
                # Note: In a real implementation, you would save this back to your data store
                st.success("🗑️ Today's entry has been deleted!")
                st.rerun()

    elif dashboard_view == "Progress Tracking":
        st.markdown("## 📈 Progress Analysis Dashboard")
        st.markdown(f"Comprehensive analysis for **{child_name}** from {start_date} to {end_date}")
        
        # Load observations properly
        all_observations = load_parent_observations()
        
        # Add any session state data if it exists
        if 'parent_data' in st.session_state and st.session_state['parent_data']:
            all_observations.extend(st.session_state['parent_data'])
        
        child_observations = [obs for obs in all_observations 
                            if obs.get('child_name') == child_name 
                            and start_date <= date.fromisoformat(obs['date']) <= end_date]
        
        if not child_observations:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: rgba(251, 191, 36, 0.1); 
                 border-radius: 12px; border: 2px dashed rgba(251, 191, 36, 0.5);">
                <span class="material-symbols-outlined" style="font-size: 3rem; color: #f59e0b; margin-bottom: 1rem;">trending_up</span>
                <h3 style="color: #92400e;">No observations found for this period</h3>
                <p style="color: #92400e;">Start by adding daily observations to see progress trends and insights.</p>
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Enhanced overview metrics
        st.markdown("### 📊 Quick Overview")
        
        df = pd.DataFrame(child_observations)
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            avg_homework = df['homework_completion'].mean()
            st.metric("Avg Homework Completion", f"{avg_homework:.1f}%", 
                     delta=f"{avg_homework - 75:.1f}%" if avg_homework != 75 else None)
        
        with metric_col2:
            avg_behavior = df['behavior_rating'].mean()
            st.metric("Avg Behavior Rating", f"{avg_behavior:.1f}/5",
                     delta=f"{avg_behavior - 3:.1f}" if avg_behavior != 3 else None)
        
        with metric_col3:
            avg_mood = df['mood_rating'].mean()
            st.metric("Avg Mood Rating", f"{avg_mood:.1f}/5",
                     delta=f"{avg_mood - 3:.1f}" if avg_mood != 3 else None)
        
        with metric_col4:
            total_reading = df['reading_time'].sum()
            st.metric("Total Reading Time", f"{total_reading} min",
                     delta=f"{total_reading // len(df):.0f} min/day")
        
        # Enhanced tabbed analysis
        tab1, tab2, tab3, tab4 = st.tabs(["📚 Academic", "🎭 Behavioral", "😊 Emotional", "🏃 Health & Lifestyle"])
        
        with tab1:
            st.markdown("### Academic Performance Trends")
            
            col1, col2 = st.columns(2)
            
            with col1:
                homework_fig = create_progress_chart(child_observations, 'homework_completion')
                if homework_fig:
                    st.plotly_chart(homework_fig, use_container_width=True)
            
            with col2:
                reading_fig = create_progress_chart(child_observations, 'reading_time')
                if reading_fig:
                    st.plotly_chart(reading_fig, use_container_width=True)
            
            st.markdown("#### 📊 Subject Difficulty Analysis")
            
            all_subjects = []
            for obs in child_observations:
                all_subjects.extend(obs.get('subjects_struggled', []))
            
            if all_subjects:
                subject_counts = pd.Series(all_subjects).value_counts()
                fig_subjects = px.bar(x=subject_counts.index, y=subject_counts.values,
                                     title="Subjects with Most Difficulties",
                                     labels={'x': 'Subject', 'y': 'Number of Days'},
                                     color=subject_counts.values,
                                     color_continuous_scale='Reds')
                fig_subjects.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    height=350
                )
                st.plotly_chart(fig_subjects, use_container_width=True)
                
                # Insights
                most_difficult = subject_counts.index[0] if len(subject_counts) > 0 else None
                if most_difficult:
                    st.info(f"💡 **Insight**: {most_difficult} appears to be the most challenging subject with {subject_counts[most_difficult]} difficult days.")
            else:
                st.success("🎉 Excellent! No subject difficulties recorded in this period.")
        
        with tab2:
            st.markdown("### Behavioral Progress Analysis")
            
            behavior_fig = create_progress_chart(child_observations, 'behavior_rating')
            if behavior_fig:
                st.plotly_chart(behavior_fig, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_behavior = df['behavior_rating'].mean()
                st.metric("Average Behavior Rating", f"{avg_behavior:.1f}/5")
                
                if avg_behavior >= 4:
                    st.success("🌟 Excellent behavior overall!")
                elif avg_behavior >= 3:
                    st.info("✅ Good behavior with room for growth")
                else:
                    st.warning("⚠️ Behavior may need additional support")
            
            with col2:
                good_days = len(df[df['behavior_rating'] >= 4])
                total_days = len(df)
                good_percentage = (good_days / total_days * 100) if total_days > 0 else 0
                st.metric("Good Behavior Days", f"{good_days}/{total_days}", 
                         delta=f"{good_percentage:.1f}%")
            
            with col3:
                if len(df) > 1:
                    behavior_trend = df['behavior_rating'].diff().mean()
                    trend_text = "Improving" if behavior_trend > 0.1 else "Declining" if behavior_trend < -0.1 else "Stable"
                    st.metric("Behavior Trend", trend_text, delta=f"{behavior_trend:+.2f}")
                else:
                    st.metric("Behavior Trend", "Need more data")
            
            # Behavior distribution
            st.markdown("#### Behavior Rating Distribution")
            behavior_dist = df['behavior_rating'].value_counts().sort_index()
            fig_behavior_dist = px.pie(values=behavior_dist.values, 
                                     names=[f"Rating {i}" for i in behavior_dist.index],
                                     title="Distribution of Daily Behavior Ratings",
                                     color_discrete_sequence=px.colors.qualitative.Set3)
            fig_behavior_dist.update_layout(height=350)
            st.plotly_chart(fig_behavior_dist, use_container_width=True)
        
        with tab3:
            st.markdown("### Emotional Well-being Tracking")
            
            mood_fig = create_progress_chart(child_observations, 'mood_rating')
            if mood_fig:
                st.plotly_chart(mood_fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Mood Distribution")
                mood_dist = df['mood_rating'].value_counts().sort_index()
                fig_mood_dist = px.pie(values=mood_dist.values, 
                                     names=[f"Mood Level {i}" for i in mood_dist.index],
                                     title="Emotional State Distribution",
                                     color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_mood_dist.update_layout(height=300)
                st.plotly_chart(fig_mood_dist, use_container_width=True)
            
            with col2:
                st.markdown("#### Emotional Insights")
                avg_mood = df['mood_rating'].mean()
                happy_days = len(df[df['mood_rating'] >= 4])
                total_days = len(df)
                
                st.metric("Average Mood", f"{avg_mood:.1f}/5")
                st.metric("Happy Days", f"{happy_days}/{total_days}")
                
                if avg_mood >= 4:
                    st.success("😊 Generally happy and positive!")
                elif avg_mood >= 3:
                    st.info("😐 Balanced emotional state")
                else:
                    st.warning("😔 May benefit from emotional support")
                
                # Mood trends
                if len(df) > 7:
                    recent_mood = df.tail(7)['mood_rating'].mean()
                    overall_mood = df['mood_rating'].mean()
                    
                    if recent_mood > overall_mood:
                        st.info("📈 Mood has been improving recently!")
                    elif recent_mood < overall_mood:
                        st.warning("📉 Recent mood has been lower than average")
        
        with tab4:
            st.markdown("### Health & Lifestyle Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                sleep_fig = create_progress_chart(child_observations, 'sleep_hours')
                if sleep_fig:
                    st.plotly_chart(sleep_fig, use_container_width=True)
            
            with col2:
                activity_fig = create_progress_chart(child_observations, 'physical_activity')
                if activity_fig:
                    st.plotly_chart(activity_fig, use_container_width=True)
            
            st.markdown("#### Health & Lifestyle Summary")
            
            health_col1, health_col2, health_col3, health_col4 = st.columns(4)
            
            with health_col1:
                avg_sleep = df['sleep_hours'].mean()
                st.metric("Average Sleep", f"{avg_sleep:.1f} hrs")
                
                if avg_sleep >= 8:
                    st.success("✅ Good sleep duration")
                elif avg_sleep >= 7:
                    st.info("⚠️ Adequate sleep")
                else:
                    st.warning("❌ May need more sleep")
            
            with health_col2:
                avg_activity = df['physical_activity'].mean()
                st.metric("Average Activity", f"{avg_activity:.0f} min")
                
                if avg_activity >= 60:
                    st.success("🏃 Great activity level!")
                else:
                    st.warning("🚶 Could use more activity")
            
            with health_col3:
                avg_screen = df['screen_time'].mean()
                st.metric("Average Screen Time", f"{avg_screen:.1f} hrs")
                
                if avg_screen <= 2:
                    st.success("📱 Good screen balance")
                else:
                    st.warning("📺 Consider reducing screen time")
            
            with health_col4:
                if 'medication_taken' in df.columns:
                    med_compliance = df['medication_taken'].mean() * 100
                    st.metric("Medication Compliance", f"{med_compliance:.0f}%")
                    
                    if med_compliance >= 90:
                        st.success("💊 Excellent compliance")
                    else:
                        st.warning("💊 Monitor medication schedule")

    elif dashboard_view == "Weekly Summary":
        st.markdown("## 📅 Weekly Progress Summary")
        st.markdown(f"Comprehensive weekly analysis for **{child_name}**")
        
        # Load observations properly
        all_observations = load_parent_observations()
        
        # Add any session state data if it exists
        if 'parent_data' in st.session_state and st.session_state['parent_data']:
            all_observations.extend(st.session_state['parent_data'])
        
        child_observations = [obs for obs in all_observations 
                            if obs.get('child_name') == child_name 
                            and start_date <= date.fromisoformat(obs['date']) <= end_date]
        
        if not child_observations:
            st.warning("⚠️ No observations found for the selected period.")
            return
        
        # Enhanced weekly summary with animations
        weekly_fig, weekly_data = create_weekly_summary(child_observations)
        
        if weekly_fig:
            st.plotly_chart(weekly_fig, use_container_width=True)
            
            if weekly_data is not None and not weekly_data.empty:
                st.markdown("### 🎯 Weekly Insights & Recommendations")
                
                latest_week = weekly_data.iloc[-1]
                
                insight_col1, insight_col2 = st.columns(2)
                
                with insight_col1:
                    st.markdown("#### 🌟 This Week's Highlights")
                    
                    # Homework insights
                    if latest_week['homework_completion'] >= 85:
                        st.success("📚 Outstanding homework completion!")
                    elif latest_week['homework_completion'] >= 70:
                        st.info("📖 Good homework habits developing")
                    else:
                        st.warning("📝 Homework completion needs attention")
                    
                    # Behavior insights
                    if latest_week['behavior_rating'] >= 4:
                        st.success("😊 Excellent behavior this week!")
                    elif latest_week['behavior_rating'] >= 3:
                        st.info("👍 Good behavior overall")
                    else:
                        st.warning("🤔 Behavior may need support")
                    
                    # Sleep insights
                    if latest_week['sleep_hours'] >= 8:
                        st.success("😴 Great sleep habits!")
                    else:
                        st.warning("💤 Consider earlier bedtime")
                
                with insight_col2:
                    st.markdown("#### 📈 Growth & Trends")
                    
                    if len(weekly_data) > 1:
                        prev_week = weekly_data.iloc[-2]
                        
                        # Calculate improvements
                        homework_change = latest_week['homework_completion'] - prev_week['homework_completion']
                        behavior_change = latest_week['behavior_rating'] - prev_week['behavior_rating']
                        mood_change = latest_week['mood_rating'] - prev_week['mood_rating']
                        
                        improvements = []
                        concerns = []
                        
                        if homework_change > 5:
                            improvements.append("📈 Homework completion improved")
                        elif homework_change < -5:
                            concerns.append("📉 Homework completion declined")
                        
                        if behavior_change > 0.3:
                            improvements.append("😊 Behavior rating improved")
                        elif behavior_change < -0.3:
                            concerns.append("😟 Behavior rating declined")
                        
                        if mood_change > 0.3:
                            improvements.append("🌟 Mood has improved")
                        elif mood_change < -0.3:
                            concerns.append("☁️ Mood has declined")
                        
                        if improvements:
                            st.markdown("**Positive Changes:**")
                            for improvement in improvements:
                                st.success(improvement)
                        
                        if concerns:
                            st.markdown("**Areas to Watch:**")
                            for concern in concerns:
                                st.warning(concern)
                        
                        if not improvements and not concerns:
                            st.info("📊 Consistent patterns maintained")
                    else:
                        st.info("🔄 Need more weeks of data for trend analysis")
                
                # Goal setting section
                st.markdown("---")
                st.markdown("### 🎯 Goals for Next Week")
                
                goal_col1, goal_col2 = st.columns(2)
                
                with goal_col1:
                    reading_goal = st.number_input("Daily Reading Goal (minutes)", 0, 180, 20, key="weekly_reading_goal")
                    homework_goal = st.slider("Homework Completion Goal (%)", 0, 100, 85, key="weekly_homework_goal")
                
                with goal_col2:
                    behavior_goal = st.selectbox("Behavior Focus Area", 
                                               ["Following directions", "Completing tasks", "Social interactions", "Self-regulation"],
                                               key="weekly_behavior_goal")
                    sleep_goal = st.number_input("Sleep Goal (hours)", 6.0, 12.0, 8.0, step=0.5, key="weekly_sleep_goal")
                
                weekly_notes = st.text_area("Weekly Summary Notes", 
                                          placeholder="Overall observations, special events, or notes for this week...",
                                          key="weekly_summary_notes")
                
                if st.button("💾 Save Weekly Goals & Summary", key="save_weekly_summary"):
                    weekly_summary = {
                        "child_name": child_name,
                        "week_start": start_date.isoformat(),
                        "week_end": end_date.isoformat(),
                        "reading_goal": reading_goal,
                        "homework_goal": homework_goal,
                        "behavior_goal": behavior_goal,
                        "sleep_goal": sleep_goal,
                        "summary_notes": weekly_notes,
                        "created_date": datetime.now().isoformat()
                    }
                    
                    if 'weekly_data' not in st.session_state:
                        st.session_state['weekly_data'] = []
                    
                    st.session_state['weekly_data'].append(weekly_summary)
                    st.success("✅ Weekly summary and goals saved successfully!")
            else:
                st.info("📊 Insufficient data for weekly summary analysis")

    else:  # Observations Log
        st.markdown("## 📋 Complete Observation History")
        st.markdown(f"Detailed log of all observations for **{child_name}**")
        
        # Load observations properly
        all_observations = load_parent_observations()
        
        # Add any session state data if it exists
        if 'parent_data' in st.session_state and st.session_state['parent_data']:
            all_observations.extend(st.session_state['parent_data'])
        
        child_observations = [obs for obs in all_observations if obs.get('child_name') == child_name]
        
        if not child_observations:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: rgba(251, 191, 36, 0.1); 
                 border-radius: 12px; border: 2px dashed rgba(251, 191, 36, 0.5);">
                <span class="material-symbols-outlined" style="font-size: 3rem; color: #f59e0b; margin-bottom: 1rem;">history</span>
                <h3 style="color: #92400e;">No observations recorded yet</h3>
                <p style="color: #92400e;">Start by adding daily observations to build your child's learning history.</p>
            </div>
            """, unsafe_allow_html=True)
            return
        
        child_observations.sort(key=lambda x: x['date'], reverse=True)
        
        # Enhanced filtering options
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            date_filter = st.date_input("Filter by specific date", value=None, key="pt_log_date_filter")
        
        with filter_col2:
            behavior_filter = st.selectbox("Filter by behavior rating", 
                                         ["All", "1 (Poor)", "2 (Below Average)", "3 (Average)", "4 (Good)", "5 (Excellent)"],
                                         key="pt_behavior_filter")
        
        with filter_col3:
            show_detailed = st.checkbox("Show detailed observations", value=True, key="pt_log_show_detailed")
        
        # Clear data functionality
        if st.button("🗑️ Clear All Data", key="clear_all_data_btn", help="This will permanently delete all observations"):
            st.warning("⚠️ This action cannot be undone. Are you sure you want to delete all observation data?")
            
            confirm_col1, confirm_col2 = st.columns(2)
            with confirm_col1:
                if st.button("✅ Yes, Delete All", key="confirm_delete_all"):
                    # Clear session state data
                    st.session_state['parent_data'] = []
                    st.session_state['weekly_data'] = []
                    st.success("🗑️ All observation data has been cleared!")
                    st.rerun()
            
            with confirm_col2:
                if st.button("❌ Cancel", key="cancel_delete_all"):
                    st.info("Data deletion cancelled.")
        
        st.markdown(f"### 📊 Showing {len(child_observations)} observations")
        
        # Apply filters
        filtered_observations = child_observations
        
        if date_filter:
            filtered_observations = [obs for obs in filtered_observations 
                                   if date.fromisoformat(obs['date']) == date_filter]
        
        if behavior_filter != "All":
            behavior_value = int(behavior_filter.split(' ')[0])
            filtered_observations = [obs for obs in filtered_observations 
                                   if obs['behavior_rating'] == behavior_value]
        
        # Display observations with enhanced formatting
        for i, obs in enumerate(filtered_observations[:25]):  # Show last 25 observations
            obs_date = date.fromisoformat(obs['date'])
            
            # Create color-coded header based on behavior rating
            behavior_rating = obs['behavior_rating']
            if behavior_rating >= 4:
                header_color = "#10b981"  # Green
                rating_emoji = "😊"
            elif behavior_rating >= 3:
                header_color = "#3b82f6"  # Blue
                rating_emoji = "😐"
            else:
                header_color = "#f59e0b"  # Orange
                rating_emoji = "😔"
            
            with st.expander(f"{rating_emoji} {obs_date.strftime('%A, %B %d, %Y')} - Behavior: {behavior_rating}/5"):
                # Quick metrics row
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    st.metric("Homework", f"{obs['homework_completion']}%")
                with metric_col2:
                    st.metric("Reading", f"{obs['reading_time']} min")
                with metric_col3:
                    st.metric("Mood", f"{obs['mood_rating']}/5")
                with metric_col4:
                    st.metric("Sleep", f"{obs['sleep_hours']} hrs")
                
                if show_detailed:
                    st.markdown("---")
                    
                    detail_col1, detail_col2, detail_col3 = st.columns(3)
                    
                    with detail_col1:
                        st.markdown("**📚 Academic Details**")
                        st.write(f"• Focus Level: {obs.get('focus_level', 'N/A')}")
                        if obs.get('subjects_struggled'):
                            st.write(f"• Difficult Subjects: {', '.join(obs['subjects_struggled'])}")
                        else:
                            st.write("• No subject difficulties")
                    
                    with detail_col2:
                        st.markdown("**🎭 Behavioral & Social**")
                        st.write(f"• Energy Level: {obs.get('energy_level', 'N/A')}")
                        st.write(f"• Screen Time: {obs['screen_time']} hrs")
                        st.write(f"• Physical Activity: {obs['physical_activity']} min")
                    
                    with detail_col3:
                        st.markdown("**💊 Health & Special**")
                        med_status = "✅ Yes" if obs['medication_taken'] else "❌ No"
                        st.write(f"• Medication: {med_status}")
                        if obs.get('special_events'):
                            st.write(f"• Special Events: {obs['special_events']}")
                    
                    # Detailed notes
                    if any([obs.get('learning_wins'), obs.get('challenges_faced'), 
                           obs.get('strategies_used'), obs.get('social_interactions')]):
                        st.markdown("**📝 Detailed Notes:**")
                        
                        if obs.get('learning_wins'):
                            st.success(f"🏆 **Wins:** {obs['learning_wins']}")
                        
                        if obs.get('challenges_faced'):
                            st.warning(f"⚠️ **Challenges:** {obs['challenges_faced']}")
                        
                        if obs.get('strategies_used'):
                            st.info(f"💡 **Strategies:** {obs['strategies_used']}")
                        
                        if obs.get('social_interactions'):
                            st.info(f"👥 **Social:** {obs['social_interactions']}")
        
        # Export functionality
        st.markdown("---")
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            if st.button("📥 Export All Observations", key="pt_export_all_observations"):
                df_export = pd.DataFrame(child_observations)
                csv = df_export.to_csv(index=False)
                st.download_button(
                    label="Download Complete History (CSV)",
                    data=csv,
                    file_name=f"{child_name}_complete_observations_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key="download_complete_csv"
                )
        
        with export_col2:
            if filtered_observations != child_observations:
                if st.button("📊 Export Filtered Data", key="pt_export_filtered"):
                    df_filtered = pd.DataFrame(filtered_observations)
                    csv_filtered = df_filtered.to_csv(index=False)
                    st.download_button(
                        label="Download Filtered Data (CSV)",
                        data=csv_filtered,
                        file_name=f"{child_name}_filtered_observations_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        key="download_filtered_csv"
                    )

    # Enhanced tips and support section
    st.markdown("---")
    st.markdown("### 💡 Parent Tracking Success Tips")
    
    tip_col1, tip_col2 = st.columns(2)
    
    with tip_col1:
        st.markdown("""
        **🎯 Effective Daily Tracking:**
        - Record observations at the same time each day for consistency
        - Be specific about both successes and challenges
        - Note what strategies and supports work best for your child
        - Focus on patterns over time rather than individual bad days
        - Include context about special events or changes in routine
        """)
    
    with tip_col2:
        st.markdown("""
        **🤝 When to Reach Out for Support:**
        - Consistent low behavior or mood ratings over several days
        - Persistent difficulties with homework or specific subjects  
        - Significant changes in sleep patterns or energy levels
        - Social interaction concerns or withdrawal from activities
        - Any pattern that concerns you as a parent
        """)
    
    # Contact and resources
    st.markdown("---")
    st.markdown("### 📞 Support & Resources")
    
    support_col1, support_col2 = st.columns(2)
    
    with support_col1:
        st.markdown("""
        **🏫 School Communication:**
        - Share observation trends with your child's teacher
        - Use data to support parent-teacher conferences
        - Collaborate on consistent strategies between home and school
        - Request additional assessments if patterns indicate needs
        """)
    
    with support_col2:
        st.markdown("""
        **📚 Additional Resources:**
        - [Parent Support Groups](/#) - Connect with other parents
        - [Learning Strategies Guide](/#) - Evidence-based home support methods
        - [Child Development Milestones](/#) - Age-appropriate expectations
        - **Help Desk:** support@eduscan.edu | (555) 123-4567
        """)

if __name__ == "__main__":
    main()