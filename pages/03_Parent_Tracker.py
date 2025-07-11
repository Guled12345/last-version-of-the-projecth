# pages/03_Parent_Tracker.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
import json
import os
import sys

# Add streamlit-lottie import
try:
    from streamlit_lottie import st_lottie
    import requests
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False
    st.warning("streamlit-lottie not installed. Install with: pip install streamlit-lottie")

# Append parent directory to sys.path to enable importing from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_utils import save_parent_observation, load_parent_observations
from utils.image_base64 import get_base64_images # Only need this for the image dict
from utils.language_utils import get_text, load_app_settings, save_app_settings

# Corrected: All UI functions now imported from utils.exact_ui
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
from utils.icon_utils import get_material_icon_html # NEW: Import for specific Material Icons in content

# IMPORTANT: Page config MUST be the first Streamlit command for this page
st.set_page_config(
    page_title="EduScan Parent Tracker",
    page_icon=get_material_icon_html("family_restroom"), # Replaced emoji with Material Icon HTML
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply modern UI styles - CRITICAL to be at the top of the script
add_exact_ui_styles()

# Initialize language and theme in session state (these are usually inherited from app.py)
if 'app_language' not in st.session_state:
    settings = load_app_settings()
    st.session_state['app_language'] = settings.get('language', 'English')
if 'app_theme' not in st.session_state:
    settings = load_app_settings()
    st.session_state['app_theme'] = settings.get('theme', 'Light')
if 'offline_mode' not in st.session_state:
    settings = load_app_settings()
    st.session_state['offline_mode'] = settings.get('offline_mode', False)

# Get current language
language = st.session_state.get('app_language', 'English')
current_theme = st.session_state.get('app_theme', 'Light')

# Apply theme-specific body attribute via JavaScript (important for dynamic theme changes)
st.markdown(f"""
    <script>
        document.body.setAttribute('data-theme', '{current_theme}');
    </script>
""", unsafe_allow_html=True)

# Render the sidebar for this page (from utils.exact_ui). This is called only once per rerun.
render_exact_sidebar()

def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    if not LOTTIE_AVAILABLE:
        return None
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def remove_lottie_background(lottie_json):
    """Remove background from Lottie JSON"""
    if not lottie_json:
        return None
    
    # Method 1: Remove solid background layers
    if 'layers' in lottie_json:
        # Filter out solid color layers (backgrounds)
        lottie_json['layers'] = [
            layer for layer in lottie_json['layers'] 
            if layer.get('ty') != 1  # ty=1 is solid layer type
        ]
        
        # Also remove any layers with solid fills that cover the entire composition
        lottie_json['layers'] = [
            layer for layer in lottie_json['layers']
            if not (layer.get('ty') == 4 and  # shape layer
                   any(shape.get('ty') == 'fl' for shape in layer.get('shapes', [])))  # fill shape
        ]
    
    # Method 2: Set background color to transparent
    if 'bg' in lottie_json:
        del lottie_json['bg']
    
    # Method 3: Remove background color property
    lottie_json['bg'] = None
    
    return lottie_json

def create_progress_chart(data, metric):
    """Create progress chart for specific metric"""
    df = pd.DataFrame(data)
    if df.empty:
        return None
    
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    fig = px.line(df, x='date', y=metric, 
                    title=f"{metric.replace('_', ' ').title()} Progress Over Time",
                    markers=True)
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=metric.replace('_', ' ').title(),
        height=400
    )
    
    return fig

def create_weekly_summary(data):
    """Create weekly summary visualization"""
    if not data:
        return None, None
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.to_period('W')
    
    # Calculate weekly averages
    weekly_avg = df.groupby('week')[['homework_completion', 'behavior_rating', 'sleep_hours', 'mood_rating']].mean()
    
    # Create summary chart
    fig = go.Figure()
    
    colors = ['var(--primary-purple)', 'var(--warning-orange)', 'var(--success-green)', 'var(--info-blue)'] # Use CSS variables
    metrics_map = {
        'homework_completion': get_text('homework_completion_label', st.session_state.app_language),
        'behavior_rating': get_text('behavior_rating_label', st.session_state.app_language),
        'sleep_hours': get_text('sleep_hours_label', st.session_state.app_language),
        'mood_rating': get_text('mood_rating_label', st.session_state.app_language),
    }
    
    for i, metric in enumerate(['homework_completion', 'behavior_rating', 'sleep_hours', 'mood_rating']):
        fig.add_trace(go.Scatter(
            x=weekly_avg.index.astype(str),
            y=weekly_avg[metric],
            mode='lines+markers',
            name=metrics_map[metric], # Use translated labels
            line=dict(color=colors[i])
        ))
    
    fig.update_layout(
        title="Weekly Progress Summary",
        xaxis_title=get_text('week', st.session_state.app_language), # Translated
        yaxis_title=get_text('score', st.session_state.app_language), # Translated
        height=400
    )
    
    return fig, weekly_avg

def main():
    # Authentication check for the page
    if not is_authenticated():
        custom_alert("Please log in to access the Parent Tracker page.", alert_type="warning")
        st.switch_page("app.py")
        return

    # Role-based access control
    user_role = get_user_role()
    if user_role == 'teacher':
        st.error("Access Denied: Teachers cannot view Parent Resources.")
        st.info("Redirecting you to Teacher Resources...")
        st.switch_page("pages/02_Teacher_Resources.py")
        return
        
    # Render main app header with dynamic content
    render_exact_page_header(get_material_icon_html('family_restroom'), 'parent_tracker', 'supporting_childs_learning', language)
    
    # Single centered Lottie animation for family support
    st.markdown(f"### {get_text('supporting_childs_learning', language)}")
    
    col_center1, col_center2, col_center3 = st.columns([1, 2, 1])
    
    with col_center2:
        if LOTTIE_AVAILABLE:
            # Family support animation
            family_url = "https://lottie.host/ed479bf5-36af-4dd8-84f2-f5893f0687f9/Tgc64kKeCO.json"
            family_json = load_lottie_url(family_url)
            family_json = remove_lottie_background(family_json)
            
            if family_json:
                st.markdown("**Strengthening Home-School Connections**")
                st_lottie(
                    family_json, 
                    height=250,
                    key="family_support_animation",
                    speed=1,
                    loop=True,
                    quality="high",
                    # renderer="canvas"
                )
                st.markdown("Empowering families with tools to track, support, and celebrate their child's learning journey")
    
    # Family showcase section with decorated text instead of images
    st.markdown(f"""
    <div class="family-section">
        <h2 class="highlight-text">Supporting Every Family Connection</h2>
        <div class="family-showcase">
            <div class="family-card">
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; margin-bottom: 1rem;">
                    <h3>📊 Daily Tracking</h3>
                </div>
                <h4>{get_text('daily_tracking', language).replace('_', ' ').title()}</h4>
                <p>{get_text('monitor_child_progress', language)}</p>
            </div>
            <div class="family-card">
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 12px; color: white; margin-bottom: 1rem;">
                    <h3>💪 Parent Empowerment</h3>
                </div>
                <h4>{get_text('parent_empowerment', language)}</h4>
                <p>{get_text('gain_insights_strategies', language)}</p>
            </div>
            <div class="family-card">
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 12px; color: white; margin-bottom: 1rem;">
                    <h3>🤝 School Partnership</h3>
                </div>
                <h4>{get_text('school_partnership', language).replace('_', ' ').title()}</h4>
                <p>{get_text('build_communication_bridges', language)}</p>
            </div>
            <div class="family-card">
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); border-radius: 12px; color: white; margin-bottom: 1rem;">
                    <h3>🎉 Student Success</h3>
                </div>
                <h4>{get_text('student_success', language)}</h4>
                <p>{get_text('celebrate_achievements', language)}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add student progress gallery with decorated text
    st.markdown(f"### {get_text('student_progress_stories', language)}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; margin-bottom: 1rem;">
            <h3>📈 Academic Progress</h3>
            <p>Tracking growth in learning</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 12px; color: white; margin-bottom: 1rem;">
            <h3>😊 Learning Joy</h3>
            <p>Celebrating happy moments</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 12px; color: white; margin-bottom: 1rem;">
            <h3>🎯 Study Focus</h3>
            <p>Building concentration skills</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar for child selection and navigation
    with st.sidebar:
        st.markdown(f"### {get_text('child_selection', language)}")
        child_name = st.text_input(get_text('child_name', language), placeholder="Enter child's name", key="pt_child_name_input")
        
        if child_name:
            st.success(f"Tracking: {child_name}")
        
        st.markdown(f"### {get_text('dashboard_options', language)}")
        dashboard_view = st.selectbox(
            get_text('choose_view', language),
            [get_text('daily_entry', language), get_text('progress_tracking', language), get_text('weekly_summary', language), get_text('observations_log', language)],
            key="pt_dashboard_view_selector"
        )
        
        # Date range for analysis
        if dashboard_view in [get_text('progress_tracking', language), get_text('weekly_summary', language)]:
            st.markdown("### Date Range")
            end_date = st.date_input("End Date", value=date.today(), key="pt_end_date_input")
            start_date = st.date_input("Start Date", value=end_date - timedelta(days=30), key="pt_start_date_input")

    if not child_name:
        custom_alert(
        message=get_text('please_enter_child_name', language),
        icon_html=get_material_icon_html('info', style='fill'),
        alert_type="warning"
    )
        st.stop()

    if dashboard_view == get_text('daily_entry', language):
        st.markdown(f"## {get_text('daily_observation_entry', language)}")
        st.markdown(f"{get_text('recording_observations_for', language)} **{child_name}** {get_text('on', language)} {date.today().strftime('%B %d, %Y')}")
        
        # Create form for daily entry
        with st.form("daily_observation_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"### {get_text('academic_observations', language)}")
                
                homework_completion = st.slider(
                    get_text('homework_completion', language).replace('_', ' ').title(), 
                    0, 100, 75,
                    help="Percentage of assigned homework completed",
                    key="pt_homework_completion_input"
                )
                
                reading_time = st.number_input(
                    get_text('reading_time', language).replace('_', ' ').title(), 
                    min_value=0, max_value=180, value=20,
                    help="Minutes spent reading independently",
                    key="pt_reading_time_input"
                )
                
                focus_level = st.select_slider(
                    get_text('focus_level', language).replace('_', ' ').title(),
                    options=[get_text('poor'), get_text('below_average'), get_text('average'), get_text('good'), get_text('excellent')],
                    value=get_text('good'),
                    key="pt_focus_level_input"
                )
                
                subjects_struggled = st.multiselect(
                    get_text('subjects_struggled', language).replace('_', ' ').title(),
                    ["Math", "Reading", "Writing", "Science", "Social Studies", "Other"],
                    help="Select subjects where child struggled today",
                    key="pt_subjects_struggled_input"
                )
            
            with col2:
                st.markdown(f"### {get_text('behavioral_emotional', language)}")
                
                behavior_options_map = {
                    f"1 - {get_text('poor', language)}": 1,
                    f"2 - {get_text('below_average', language)}": 2,
                    f"3 - {get_text('average', language)}": 3,
                    f"4 - {get_text('good', language)}": 4,
                    f"5 - {get_text('excellent', language)}": 5,
                }
                behavior_rating_display_options = list(behavior_options_map.keys())
                
                behavior_rating = st.select_slider(
                    get_text('behavior_rating', language).replace('_', ' ').title(), 
                    options=behavior_rating_display_options,
                    value=f"3 - {get_text('average', language)}",
                    help="Select your child's overall behavior today",
                    key="pt_behavior_rating_input"
                )
                behavior_value = behavior_options_map[behavior_rating]
                
                mood_options_map = {
                    f"1 - {get_text('very_low', language)}": 1,
                    f"2 - {get_text('low', language)}": 2,
                    f"3 - {get_text('normal', language)}": 3,
                    f"4 - {get_text('high', language)}": 4,
                    f"5 - {get_text('very_high', language)}": 5,
                }
                mood_rating_display_options = list(mood_options_map.keys())

                mood_rating = st.select_slider(
                    get_text('mood_rating', language).replace('_', ' ').title(), 
                    options=mood_rating_display_options,
                    value=f"3 - {get_text('normal', language)}",
                    help="How was your child's mood today?",
                    key="pt_mood_rating_input"
                )
                mood_value = mood_options_map[mood_rating]
                
                sleep_hours = st.number_input(
                    get_text('sleep_hours', language).replace('_', ' ').title(), 
                    min_value=4.0, max_value=12.0, value=8.0, step=0.5,
                    help="Total hours of sleep last night",
                    key="pt_sleep_hours_input"
                )
                
                energy_level_options = [get_text('very_low', language), get_text('low', language), get_text('normal', language), get_text('high', language), get_text('very_high', language)]
                energy_level = st.select_slider(
                    get_text('energy_level', language).replace('_', ' ').title(),
                    options=energy_level_options,
                    value=get_text('normal', language),
                    key="pt_energy_level_input"
                )
            
            st.markdown("### Additional Observations")
            
            col3, col4 = st.columns(2)
            
            with col3:
                social_interactions = st.text_area(
                    "Social Interactions",
                    placeholder="How did your child interact with siblings, friends, or family today?",
                    height=100,
                    key="pt_social_interactions_input"
                )
                
                learning_wins = st.text_area(
                    get_text('learning_wins', language).replace('_', ' ').title(),
                    placeholder="What went well today? Any breakthroughs or positive moments?",
                    height=100,
                    key="pt_learning_wins_input"
                )
            
            with col4:
                challenges_faced = st.text_area(
                    get_text('challenges_faced', language).replace('_', ' ').title(),
                    placeholder="What was difficult today? Any specific struggles or concerns?",
                    height=100,
                    key="pt_challenges_faced_input"
                )
                
                strategies_used = st.text_area(
                    "Strategies That Helped",
                    placeholder="What strategies or supports helped your child today?",
                    height=100,
                    key="pt_strategies_used_input"
                )
            
            st.markdown("### Home Environmental Factors")
            
            col5, col6 = st.columns(2)
            
            with col5:
                screen_time = st.number_input(
                    "Screen Time (hours)", 
                    min_value=0.0, max_value=12.0, value=2.0, step=0.5,
                    key="pt_screen_time_input"
                )
                
                physical_activity = st.number_input(
                    "Physical Activity (minutes)", 
                    min_value=0, max_value=300, value=60,
                    key="pt_physical_activity_input"
                )
            
            with col6:
                medication_taken = st.checkbox("Medication taken as prescribed", key="pt_medication_taken_checkbox")
                
                special_events = st.text_input(
                    "Special Events/Changes",
                    placeholder="Any unusual events, schedule changes, or disruptions?",
                    key="pt_special_events_input"
                )
            
            submitted = st.form_submit_button(get_text('save_observation', language), type="primary")
            
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
                    "social_interactions": social_interactions,
                    "learning_wins": learning_wins,
                    "challenges_faced": challenges_faced,
                    "strategies_used": strategies_used,
                    "screen_time": screen_time,
                    "physical_activity": physical_activity,
                    "medication_taken": medication_taken,
                    "special_events": special_events,
                    "timestamp": datetime.now().isoformat()
                }
                
                save_parent_observation(observation_data)
                st.success(" Observation saved successfully!")
                st.balloons()

    elif dashboard_view == get_text('progress_tracking', language):
        st.markdown(f"## {get_text('progress_tracking', language)}")
        st.markdown(f"Analyzing progress for **{child_name}** from {start_date} to {end_date}")
        
        all_observations = load_parent_observations()
        child_observations = [obs for obs in all_observations 
                                if obs.get('child_name') == child_name 
                                and start_date <= date.fromisoformat(obs['date']) <= end_date]
        
        if not child_observations:
            custom_alert(
            message=f"{get_text('no_observations_recorded', language)}. {get_text('start_by_adding_daily_observations', language)}",
            icon_html=get_material_icon_html('info', style='fill'),
            alert_type="warning"
        )

            return
        
        tab1, tab2, tab3, tab4 = st.tabs(["Academic", "Behavioral", "Emotional", "Health"])
        
        with tab1:
            st.markdown("### Academic Progress")
            
            col1, col2 = st.columns(2)
            
            with col1:
                homework_fig = create_progress_chart(child_observations, 'homework_completion')
                if homework_fig:
                    st.plotly_chart(homework_fig, use_container_width=True)
            
            with col2:
                reading_fig = create_progress_chart(child_observations, 'reading_time')
                if reading_fig:
                    st.plotly_chart(reading_fig, use_container_width=True)
            
            st.markdown("#### Chart Subject Difficulty Analysis")
            
            all_subjects = []
            for obs in child_observations:
                all_subjects.extend(obs.get('subjects_struggled', []))
            
            if all_subjects:
                subject_counts = pd.Series(all_subjects).value_counts()
                fig_subjects = px.bar(x=subject_counts.index, y=subject_counts.values,
                                       title="Subjects with Most Difficulties",
                                       labels={'x': 'Subject', 'y': 'Number of Days'})
                st.plotly_chart(fig_subjects, use_container_width=True)
            else:
                st.info(f"{get_material_icon_html('check_circle', style='fill')} Great news! No subject difficulties recorded in this period.", unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### Behavioral Progress")
            
            behavior_fig = create_progress_chart(child_observations, 'behavior_rating')
            if behavior_fig:
                st.plotly_chart(behavior_fig, use_container_width=True)
            
            df = pd.DataFrame(child_observations)
            if not df.empty:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_behavior = df['behavior_rating'].mean()
                    st.metric("Average Behavior Rating", f"{avg_behavior:.1f}/5")
                
                with col2:
                    good_days = len(df[df['behavior_rating'] >= 4])
                    st.metric("Good Behavior Days", f"{good_days}/{len(df)}")
                
                with col3:
                    improvement = df['behavior_rating'].diff().mean()
                    st.metric("Trend", f"{improvement:+.2f}", delta=f"{improvement:.2f}")
        
        with tab3:
            st.markdown("### Emotional Well-being")
            
            mood_fig = create_progress_chart(child_observations, 'mood_rating')
            if mood_fig:
                st.plotly_chart(mood_fig, use_container_width=True)
            
            df = pd.DataFrame(child_observations)
            if not df.empty:
                mood_dist = df['mood_rating'].value_counts().sort_index()
                fig_mood_dist = px.pie(values=mood_dist.values, names=[f"Mood {i}" for i in mood_dist.index],
                                       title="Mood Distribution")
                st.plotly_chart(fig_mood_dist, use_container_width=True)
        
        with tab4:
            st.markdown("### Health & Lifestyle")
            
            col1, col2 = st.columns(2)
            
            with col1:
                sleep_fig = create_progress_chart(child_observations, 'sleep_hours')
                if sleep_fig:
                    st.plotly_chart(sleep_fig, use_container_width=True)
            
            with col2:
                activity_fig = create_progress_chart(child_observations, 'physical_activity')
                if activity_fig:
                    st.plotly_chart(activity_fig, use_container_width=True)
            
            df = pd.DataFrame(child_observations)
            if not df.empty:
                st.markdown("#### Chart Health Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    avg_sleep = df['sleep_hours'].mean()
                    st.metric("Average Sleep", f"{avg_sleep:.1f} hrs")
                
                with col2:
                    avg_activity = df['physical_activity'].mean()
                    st.metric("Average Activity", f"{avg_activity:.0f} min")
                
                with col3:
                    avg_screen = df['screen_time'].mean()
                    st.metric("Average Screen Time", f"{avg_screen:.1f} hrs")
                
                with col4:
                    med_compliance = df['medication_taken'].mean() * 100
                    st.metric("Medication Compliance", f"{med_compliance:.0f}%")

    elif dashboard_view == get_text('weekly_summary', language):
        st.markdown(f"## {get_text('weekly_summary', language)}")
        st.markdown(f"Weekly analysis for **{child_name}**")
        
        all_observations = load_parent_observations()
        child_observations = [obs for obs in all_observations 
                                if obs.get('child_name') == child_name 
                                and start_date <= date.fromisoformat(obs['date']) <= end_date]
        
        if not child_observations:
            custom_alert(
            message=get_text('no_observations_recorded', language),
            icon_html=get_material_icon_html('info', style='fill'),
            alert_type="warning"
        )

            return
        
        weekly_fig, weekly_data = create_weekly_summary(child_observations)
        
        if weekly_fig:
            st.plotly_chart(weekly_fig, use_container_width=True)
            
            st.markdown("### 💡 Weekly Insights")
            
            if weekly_data is not None and not weekly_data.empty:
                latest_week = weekly_data.iloc[-1]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### This Week's Highlights")
                    
                    if latest_week['homework_completion'] >= 80:
                        st.success(f"{get_material_icon_html('check_circle', style='fill')} Great homework completion!", unsafe_allow_html=True)
                    elif latest_week['homework_completion'] >= 60:
                        custom_alert(
                        message="Homework completion needs attention",
                        icon_html=get_material_icon_html('warning', style='fill'),
                        alert_type="warning"
                    )
                    else:
                        st.error(f"{get_material_icon_html('error', style='fill')} Homework completion is concerning", unsafe_allow_html=True)
                    
                    if latest_week['behavior_rating'] >= 4:
                        st.success(f"{get_material_icon_html('check_circle', style='fill')} Excellent behavior this week!", unsafe_allow_html=True)
                    elif latest_week['behavior_rating'] >= 3:
                        st.info(f"{get_material_icon_html('info', style='fill')} Good behavior overall", unsafe_allow_html=True)
                    else:
                        custom_alert(
                        message="Behavior needs support",
                        icon_html=get_material_icon_html('warning', style='fill'),
                        alert_type="warning"
                    )
                
                with col2:
                    st.markdown("#### Growth Areas of Growth")
                    
                    if len(weekly_data) > 1:
                        prev_week = weekly_data.iloc[-2]
                        
                        homework_change = latest_week['homework_completion'] - prev_week['homework_completion']
                        behavior_change = latest_week['behavior_rating'] - prev_week['behavior_rating']
                        mood_change = latest_week['mood_rating'] - prev_week['mood_rating']
                        
                        if homework_change > 5:
                            st.success(f"{get_material_icon_html('arrow_upward')} Homework completion improved!", unsafe_allow_html=True)
                        if behavior_change > 0.2:
                            st.success(f"{get_material_icon_html('arrow_upward')} Behavior rating improved!", unsafe_allow_html=True)
                        if mood_change > 0.2:
                            st.success(f"{get_material_icon_html('arrow_upward')} Mood has improved!", unsafe_allow_html=True)

    else:
        st.markdown(f"## {get_text('observations_log', language)}")
        st.markdown(f"Complete observation history for **{child_name}**")
        
        all_observations = load_parent_observations()
        child_observations = [obs for obs in all_observations if obs.get('child_name') == child_name]
        
        if not child_observations:
            custom_alert(
            message=f"{get_text('no_observations_recorded', language)}. {get_text('start_by_adding_daily_observations', language)}",
            icon_html=get_material_icon_html('info', style='fill'),
            alert_type="warning"
            )
            return
        
        child_observations.sort(key=lambda x: x['date'], reverse=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            date_filter = st.date_input("Filter by date (optional)", key="pt_log_date_filter")
        
        with col2:
            show_detailed = st.checkbox("Show detailed observations", value=False, key="pt_log_show_detailed")
        
        for obs in child_observations[:20]:
            obs_date = date.fromisoformat(obs['date'])
            
            if date_filter and obs_date != date_filter:
                continue
            
            with st.expander(f"{obs_date.strftime('%B %d, %Y')} - Rating: {obs['behavior_rating']}/5"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Academic**")
                    st.write(f"Homework: {obs['homework_completion']}%")
                    st.write(f"Reading: {obs['reading_time']} min")
                    st.write(f"Focus: {obs.get('focus_level', 'N/A')}")
                    if obs.get('subjects_struggled'):
                        st.write(f"Struggled with: {', '.join(obs['subjects_struggled'])}")
                
                with col2:
                    st.markdown("**Behavioral**")
                    st.write(f"Behavior: {obs['behavior_rating']}/5")
                    st.write(f"Mood: {obs['mood_rating']}/5")
                    st.write(f"Energy: {obs.get('energy_level', 'N/A')}")
                
                with col3:
                    st.markdown("**Health**")
                    st.write(f"Sleep: {obs['sleep_hours']} hrs")
                    st.write(f"Activity: {obs['physical_activity']} min")
                    st.write(f"Screen time: {obs['screen_time']} hrs")
                
                if show_detailed:
                    if obs.get('learning_wins'):
                        st.markdown(f"**{get_material_icon_html('military_tech')} Learning Wins:**", unsafe_allow_html=True)
                        st.write(obs['learning_wins'])
                    
                    if obs.get('challenges_faced'):
                        st.markdown(f"**{get_material_icon_html('gpp_bad')} Challenges:**", unsafe_allow_html=True)
                        st.write(obs['challenges_faced'])
                    
                    if obs.get('strategies_used'):
                        st.markdown(f"**{get_material_icon_html('handyman')} Helpful Strategies:**", unsafe_allow_html=True)
                        st.write(obs['strategies_used'])
                    
                    if obs.get('social_interactions'):
                        st.markdown(f"**{get_material_icon_html('groups')} Social Interactions:**", unsafe_allow_html=True)
                        st.write(obs['social_interactions'])
        
        if st.button("📥 Export Observations", key="pt_export_observations_button"):
            df_export = pd.DataFrame(child_observations)
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{child_name}_observations_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

    st.markdown("---")
    st.markdown(f"### {get_material_icon_html('lightbulb_circle', style='fill')} Parent Tracking Tips", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Effective Tracking:**
        - Record observations consistently each day
        - Be specific about challenges and successes
        - Note what strategies work best
        - Track patterns over time, not just individual days
        """)
    
    with col2:
        st.markdown(f"""
        **{get_material_icon_html('phone_in_talk', style='fill')} When to Seek Help:**""", unsafe_allow_html=True)
        st.markdown("""
        - Consistent low behavior/mood ratings
        - Persistent homework struggles
        - Sleep or health concerns
        - Significant changes in patterns
        """)

if __name__ == "__main__":
    main()