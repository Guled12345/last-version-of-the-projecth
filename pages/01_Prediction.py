import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
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

from utils.model_utils import load_model, make_prediction
from utils.data_utils import save_prediction_data, load_student_data
from utils.image_base64 import get_base64_images # Only need this for the image dict
from utils.language_utils import get_text, load_app_settings, save_app_settings

# Corrected: All UI functions now imported from utils.exact_ui
from utils.exact_ui import (
    add_exact_ui_styles, # Apply overall app styles
    render_exact_sidebar, # Sidebar structure and fixed content, including settings
    render_exact_page_header, # Global header rendering function (without settings button)
    create_exact_metric_card, # Helper for individual stat cards (used on Dashboard)
    create_exact_chart_container, # Helper for chart containers
    get_b64_image_html # Helper for rendering base64 images within HTML
)
from utils.auth_utils import is_authenticated, render_login_page, logout_user, get_user_role # Import auth utilities
from utils.icon_utils import get_material_icon_html # NEW: Import for specific Material Icons in content


# IMPORTANT: Page config MUST be the first Streamlit command for this page
st.set_page_config(
    page_title="EduScan Prediction - Learning Risk Assessment",
    page_icon=get_material_icon_html("search"), # Replaced emoji with Material Icon HTML
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



def validate_inputs(math_score, reading_score, writing_score, attendance, behavior, literacy):
    """Validate all input parameters"""
    errors = []
    
    if not (0 <= math_score <= 100):
        errors.append("Math score must be between 0 and 100")
    if not (0 <= reading_score <= 100):
        errors.append("Reading score must be between 0 and 100")
    if not (0 <= writing_score <= 100):
        errors.append("Writing score must be between 0 and 100")
    if not (0 <= attendance <= 100):
        errors.append("Attendance must be between 0 and 100%")
    if not (1 <= behavior <= 5):
        errors.append("Behavior rating must be between 1 and 5")
    if not (1 <= literacy <= 10):
        errors.append("Literacy level must be between 1 and 10")
    
    return errors

def create_risk_visualization(prediction_prob, student_data):
    """Create visualization for risk assessment"""
    
    # Risk gauge chart
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = prediction_prob * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Learning Difficulty Risk Level (%)"},
        delta = {'reference': 30},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig_gauge.update_layout(height=300)
    
    # Performance radar chart
    categories = ['Math Score', 'Reading Score', 'Writing Score', 'Attendance', 'Behavior*20', 'Literacy*10']
    values = [
        student_data['math_score'],
        student_data['reading_score'], 
        student_data['writing_score'],
        student_data['attendance'],
        student_data['behavior'] * 20,
        student_data['literacy'] * 10
    ]
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Student Performance'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Student Performance Profile",
        height=400
    )
    
    return fig_gauge, fig_radar

def display_recommendations(risk_level, student_data):
    """Display personalized recommendations based on risk level"""
    
    if risk_level == get_text('low_risk', language):
        st.markdown(f" {get_material_icon_html('check_circle', style='fill')} **Low Risk** - {get_text('maintain_academic_support', language)}", unsafe_allow_html=True)
        recommendations = [
            "Maintain current learning pace and methods",
            "Continue regular progress monitoring",
            "Encourage continued engagement in all subjects",
            "Consider enrichment activities to challenge the student"
        ]
        color = "green"
    elif risk_level == get_text('medium_risk', language):
        st.markdown(f" {get_material_icon_html('warning', style='fill')} **Medium Risk** - {get_text('provide_targeted_interventions', language)} recommended", unsafe_allow_html=True)
        recommendations = [
            "Implement targeted interventions in lower-performing areas",
            "Increase frequency of progress monitoring",
            "Consider additional support in specific subjects",
            "Engage parents in home-based learning activities",
            "Explore different teaching methods and materials"
        ]
        color = "orange"
    else:
        st.markdown(f" {get_material_icon_html('error', style='fill')} **High Risk** - {get_text('implement_intensive_program', language)} required", unsafe_allow_html=True)
        recommendations = [
            "Initiate comprehensive assessment by learning specialists",
            "Implement intensive intervention strategies",
            "Consider individualized education plan (IEP)",
            "Increase collaboration between teachers and parents",
            "Explore assistive technologies and adaptive methods",
            "Regular monitoring and adjustment of intervention strategies"
        ]
        color = "red"
    
    st.markdown(f"### {get_text('recommendations', language)}")
    for i, rec in enumerate(recommendations, 1):
        st.write(f"• {rec}")


def main():
    # Authentication check for the page
    if not is_authenticated():
        st.warning("Please log in to access the Prediction page.")
        st.switch_page("app.py")
        return
    
    # Render main app header with dynamic content (from utils.exact_ui)
    st.markdown(f'<div class="section-animated-text">', unsafe_allow_html=True)
    render_exact_page_header(get_material_icon_html('search'), 'assessment_form', 'empowering_student_success', language)
    st.markdown(f'</div>', unsafe_allow_html=True)
    
    # Add Lottie animation for the hero section
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        if LOTTIE_AVAILABLE:
            # Load from lottiehost.com
            lottie_url = "https://lottie.host/4d42d6a6-8290-4b13-b3ab-2a10a490e6db/9oJrI4pj1F.json"
            lottie_json = load_lottie_url(lottie_url)
            
            # Remove background from the animation
            lottie_json = remove_lottie_background(lottie_json)
            
            if lottie_json:
                st_lottie(
                    lottie_json, 
                    height=300,
                    key="hero_animation",
                    speed=1,
                    reverse=False,
                    loop=True,
                    quality="high",
                    renderer="canvas"
                )

    
    # Student showcase section
    st.markdown(f"""
    <div class="input-section section-animated-text">
        <h2 class="highlight-text">{get_text('empowering_student_success', language)}</h2>
        <div class="student-showcase">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add student animation gallery
    col1, col2 = st.columns(2)
    
    with col1:
        if LOTTIE_AVAILABLE:
            # Learning Success Animation
            success_url = "https://lottie.host/687a0991-917f-4d7b-92f6-d9ecaa0780b7/D75iWs83gn.json"
            success_json = load_lottie_url(success_url)
            success_json = remove_lottie_background(success_json)
            
            if success_json:
                st.markdown("**Learning Success**")
                st_lottie(
                    success_json, 
                    height=200,
                    key="success_animation",
                    speed=1,
                    loop=True,
                    quality="high",
                    # renderer="canvas"
                )
    
    with col2:
        if LOTTIE_AVAILABLE:
            # Classroom Activity Animation
            classroom_url = "https://lottie.host/5940ae0a-4ef4-4f79-a517-abce94639765/H8tXMAPaUK.json"
            classroom_json = load_lottie_url(classroom_url)
            classroom_json = remove_lottie_background(classroom_json)
            
            if classroom_json:
                st.markdown("**Classroom Activity**")
                st_lottie(
                    classroom_json, 
                    height=200,
                    key="classroom_animation",
                    speed=1,
                    loop=True,
                    quality="high",
                    # renderer="canvas"
                )

    # Sidebar for prediction options
    with st.sidebar:
        st.markdown("### Prediction Options")
        
        available_prediction_types = ["Single Student", "Batch Upload", "Historical Analysis"] # Reordered for clarity
        user_role = get_user_role()
        # Keep conditional insertion for Batch Upload if not already in list for some reason
        if "Batch Upload" not in available_prediction_types and user_role in ['teacher', 'admin']:
            available_prediction_types.insert(1, "Batch Upload") 
            
        prediction_type = st.selectbox(
            "Choose prediction type:",
            available_prediction_types,
            key="prediction_type_selector"
        )
        
        # Model information panel
        st.markdown("### Model Information")
        st.info("""
        **Your Trained Model Active**
        
        - **Type**: RandomForest Classifier
        - **Features**: 6 key metrics
        - **Normalization**: StandardScaler
        - **Training**: GridSearchCV optimized
        - **Status**: Ready for predictions
        """)
        
        # Show model features
        st.markdown("**Input Features:**")
        features = [
            "Math Score (0-100)",
            "Reading Score (0-100)", 
            "Writing Score (0-100)",
            "Attendance Rate (%)",
            "Behavior Score (1-5)",
            "Literacy Level (1-10)"
        ]
        for feature in features:
            st.markdown(f"• {feature}")
            
        # Performance note
        st.success("Model loaded successfully from your notebook specifications")
        
        uploaded_file = None
        if prediction_type == "Batch Upload":
            st.markdown("#### Upload CSV File")
            uploaded_file = st.file_uploader(
                "Upload student data (CSV)",
                type=['csv'],
                help="CSV should contain columns: math_score, reading_score, writing_score, attendance, behavior, literacy",
                key="prediction_batch_uploader"
            )


    # --- Content for Prediction Page based on prediction_type ---
    if prediction_type == "Single Student":
        reset_counter = st.session_state.get('reset_counter', 0)
        
        st.markdown(f"""
        <div class="input-section section-animated-text">
            <h2 class="highlight-text">{get_text('assessment_form', language)}</h2>
            <p style="font-size: 1.1em; margin-bottom: 2rem; color: var(--gray-700);">
                {get_text('comprehensive_assessment', language)}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        b64_images = get_base64_images() # Not used for placeholders anymore, only for retained AI results images

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="input-section">
                <h3 class="highlight-text">Academic Performance</h3>
            </div>
            """, unsafe_allow_html=True)
            math_score = st.number_input(get_text('math_score', language).replace('_', ' ').title(), min_value=0, max_value=100, value=75, step=1, key=f"math_score_input_{reset_counter}")
            reading_score = st.number_input(get_text('reading_score', language).replace('_', ' ').title(), min_value=0, max_value=100, value=80, step=1, key=f"reading_score_input_{reset_counter}")
            writing_score = st.number_input(get_text('writing_score', language).replace('_', ' ').title(), min_value=0, max_value=100, value=70, step=1, key=f"writing_score_input_{reset_counter}")
            
        with col2:
            st.markdown(f"""
            <div class="input-section">
                <h3 class="highlight-text">Behavioral & Social Indicators</h3>
            </div>
            """, unsafe_allow_html=True)
            attendance = st.slider(get_text('attendance', language).replace('_', ' ').title(), 0, 100, 85, help="Percentage of school days attended", key=f"attendance_slider_{reset_counter}")
            behavior_options = [f"1 - {get_text('poor', language)}", f"2 - {get_text('below_average', language)}", f"3 - {get_text('average', language)}", f"4 - {get_text('good', language)}", f"5 - {get_text('excellent', language)}"]
            behavior_selection = st.select_slider(get_text('behavior_rating', language).replace('_', ' ').title(), options=behavior_options, value=f"3 - {get_text('average', language)}", 
                                                    help="Select the student's typical classroom behavior", key=f"behavior_slider_{reset_counter}")
            behavior = int(behavior_selection.split(' ')[0])
            literacy_options = [f'{i} - {"Beginner" if i <= 3 else "Developing" if i <= 6 else "Advanced"}' for i in range(1, 11)]
            literacy_selection = st.select_slider(get_text('literacy_level', language).replace('_', ' ').title(), options=literacy_options, value="6 - Developing",
                                                    help="Select the student's reading and literacy level", key=f"literacy_slider_{reset_counter}")
            literacy = int(literacy_selection.split(' ')[0])
        
        st.markdown(f"""
        <div class="input-section">
            <h3 class="highlight-text">Student Information</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            student_name = st.text_input(get_text('student_name', language).replace('_', ' ').title(), help="For record keeping and tracking purposes", key=f"student_name_input_{reset_counter}")
            grade_level = st.selectbox(get_text('grade_level', language).replace('_', ' ').title(), ["Pre-K", "K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], key=f"grade_level_select_{reset_counter}")
        
        with col4:
            notes = st.text_area("Teacher Notes", placeholder="Teacher notes…", help="Any relevant observations", height=100, key=f"teacher_notes_input_{reset_counter}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            predict_button = st.button(get_text('analyze_learning_risk', language), type="primary", use_container_width=True)
        
        with col2:
            reset_button = st.button(get_text('clear_form', language), use_container_width=True)
        
        with col3:
            save_button = st.button("Save Data", use_container_width=True)
        
        if reset_button:
            all_keys = list(st.session_state.keys())
            
            keys_to_keep = ['app_language', 'app_theme', 'offline_mode', 'authenticated', 'username', 'role']
            
            for key in all_keys:
                if key not in keys_to_keep:
                    del st.session_state[key]
            
            if 'reset_counter' not in st.session_state:
                st.session_state['reset_counter'] = 0
            st.session_state['reset_counter'] += 1
            
            st.success("✅ Form completely reset! Ready for new student assessment.")
            st.rerun()
        
        show_results = st.session_state.get('show_prediction_results', False)
        
        if predict_button:
            errors = validate_inputs(math_score, reading_score, writing_score, attendance, behavior, literacy)
            
            if errors:
                st.error(f"{get_material_icon_html('error', style='fill')} {get_text('please_correct_errors', language)}", unsafe_allow_html=True)
                for error in errors:
                    st.write(f"• {error}")
            else:
                student_data = {
                    'math_score': math_score,
                    'reading_score': reading_score,
                    'writing_score': writing_score,
                    'attendance': attendance,
                    'behavior': behavior,
                    'literacy': literacy
                }
                
                try:
                    prediction, prediction_prob = make_prediction(student_data) 
                    
                    st.session_state['show_prediction_results'] = True
                    st.session_state['current_prediction_data'] = {
                        'prediction': prediction,
                        'prediction_prob': prediction_prob,
                        'student_data': student_data,
                        'student_name': student_name,
                        'grade_level': grade_level,
                        'notes': notes
                    }
                    
                    st.markdown(f"""
                    <div class="results-section">
                        <h2 class="highlight-text">{get_text('assessment_results', language)}</h2>
                        <div class="image-gallery-grid">
                            <div class="image-aspect-ratio-container" style="background-color: transparent;">{get_b64_image_html(b64_images.get('exam_students', ''), "Exam Students", aspect_ratio="4/3", cover_mode=True)}</div>
                            <div class="image-aspect-ratio-container" style="background-color: transparent;">{get_b64_image_html(b64_images.get('student_writing', ''), "Student Writing", aspect_ratio="4/3", cover_mode=True)}</div>
                            <div class="image-aspect-ratio-container" style="background-color: transparent;">{get_b64_image_html(b64_images.get('student_portrait', ''), "Student Portrait", aspect_ratio="4/3", cover_mode=True)}</div>
                        </div>
                        <p style="font-size: 1.2em; text-align: center; color: var(--gray-700); margin-bottom: 2rem;">
                            <strong>{get_text('comprehensive_assessment', language)} {student_name if student_name else "the student"}</strong>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if prediction_prob < 0.3:
                        risk_level = get_text('low_risk', language)
                        risk_color = "var(--success-green)"
                        risk_icon_html = get_material_icon_html('check_circle', style='fill')
                    elif prediction_prob < 0.7:
                        risk_level = get_text('medium_risk', language)
                        risk_color = "var(--warning-orange)"
                        risk_icon_html = get_material_icon_html('warning', style='fill')
                    else:
                        risk_level = get_text('high_risk', language)
                        risk_color = "var(--danger-red)"
                        risk_icon_html = get_material_icon_html('error', style='fill')
                    
                    st.markdown(f"""
                    <div style="text-align: center; background: linear-gradient(135deg, {risk_color}20, {risk_color}30); padding: 1rem; border-radius: 8px; margin-bottom: 1rem; color: {risk_color};">
                        <h3>{risk_icon_html} {get_text('risk_level', language)}: {risk_level}</h3>
                        <p>{get_text('confidence', language)}: {prediction_prob:.1%}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    fig_gauge, fig_radar = create_risk_visualization(prediction_prob, student_data)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f'<div class="glassy-container" style="height:400px;">', unsafe_allow_html=True)
                        st.plotly_chart(fig_gauge, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'<div class="glassy-container" style="height:400px;">', unsafe_allow_html=True)
                        st.plotly_chart(fig_radar, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Image removed from here, replaced with animated fallback in previous iteration
                    st.markdown(f"""
                    <div class="results-section section-animated-text">
                        <h3 class="highlight-text">{get_text('Personalized Intervention Recommendations', language)}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    display_recommendations(risk_level, student_data)
                    
                    st.markdown(f"""
                    <div class="results-section">
                        <h3 class="highlight-text">{get_text('assessment_summary', language)}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    summary_data = {
                        "Assessment Area": ["Mathematics", "Reading", "Writing", "Attendance", "Behavior", "Literacy", "Overall Risk", "AI Confidence"],
                        "Score/Rating": [f"{math_score}%", f"{reading_score}%", f"{writing_score}%", f"{attendance}%", f"{behavior}/5", f"{literacy}/10", risk_level, f"{prediction_prob:.1%}"]
                    }
                    st.table(pd.DataFrame(summary_data))
                    
                    if save_button or st.button(" Save This Prediction", key=f"save_button_after_predict_{reset_counter}"):
                        prediction_record = {
                            "timestamp": datetime.now().isoformat(),
                            "student_name": student_name,
                            "grade_level": grade_level,
                            "prediction": prediction,
                            "probability": prediction_prob,
                            "risk_level": risk_level,
                            "notes": notes,
                            **student_data
                        }
                        save_prediction_data(prediction_record)
                        st.success(" Prediction saved successfully!")
                
                except Exception as e:
                    st.error(f"{get_material_icon_html('error', style='fill')} Error making prediction: {str(e)}", unsafe_allow_html=True)
                    st.info("Note: Using sample prediction model. Replace with your trained model file.")
        
        if show_results and 'current_prediction_data' in st.session_state and not predict_button:
            pred_data = st.session_state['current_prediction_data']
            prediction = pred_data['prediction']
            prediction_prob = pred_data['prediction_prob']
            student_data = pred_data['student_data']
            student_name = pred_data['student_name']
            grade_level = pred_data['grade_level']
            notes = pred_data['notes']
            
            b64_images = get_base64_images()
            
            st.markdown(f"""
            <div class="results-section section-animated-text">
                <h2 class="highlight-text">{get_text('assessment_results', language)}</h2>
                <div class="image-gallery-grid">
                    <div class="image-aspect-ratio-container" style="background-color: transparent;">{get_b64_image_html(b64_images.get('exam_students', ''), "Exam Students", aspect_ratio="4/3", cover_mode=True)}</div>
                    <div class="image-aspect-ratio-container" style="background-color: transparent;">{get_b64_image_html(b64_images.get('student_writing', ''), "Student Writing", aspect_ratio="4/3", cover_mode=True)}</div>
                    <div class="image-aspect-ratio-container" style="background-color: transparent;">{get_b64_image_html(b64_images.get('student_portrait', ''), "Student Portrait", aspect_ratio="4/3", cover_mode=True)}</div>
                </div>
                <p style="font-size: 1.2em; text-align: center; color: var(--gray-700); margin-bottom: 2rem;">
                    <strong>{get_text('comprehensive_assessment', language)} {student_name if student_name else "the student"}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if prediction_prob < 0.3:
                risk_level = get_text('low_risk', language)
                risk_color = "var(--success-green)"
                risk_icon_html = get_material_icon_html('check_circle', style='fill')
            elif prediction_prob < 0.7:
                risk_level = get_text('medium_risk', language)
                risk_color = "var(--warning-orange)"
                risk_icon_html = get_material_icon_html('warning', style='fill')
            else:
                risk_level = get_text('high_risk', language)
                risk_color = "var(--danger-red)"
                risk_icon_html = get_material_icon_html('error', style='fill')
            
            st.markdown(f"""
            <div style="text-align: center; background: linear-gradient(135deg, {risk_color}20, {risk_color}30); padding: 1rem; border-radius: 8px; margin-bottom: 1rem; color: {risk_color};">
                <h3>{risk_icon_html} {get_text('risk_level', language)}: {risk_level}</h3>
                <p>{get_text('confidence', language)}: {prediction_prob:.1%}</p>
            </div>
            """, unsafe_allow_html=True)
            
            fig_gauge, fig_radar = create_risk_visualization(prediction_prob, student_data)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="glassy-container" style="height:400px;">', unsafe_allow_html=True)
                st.plotly_chart(fig_gauge, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="glassy-container" style="height:400px;">', unsafe_allow_html=True)
                st.plotly_chart(fig_radar, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Image removed, replaced by animated fallback
            st.markdown(f"""
            <div class="results-section section-animated-text">
                <h3 class="highlight-text">{get_text('Personalized Intervention Recommendations', language)}</h3
            </div>
            """, unsafe_allow_html=True)
            display_recommendations(risk_level, student_data)
            
            st.markdown(f"""
            <div class="results-section">
                <h3 class="highlight-text">{get_text('Assessment Summary', language)}</h3>
            </div>
            """, unsafe_allow_html=True)
            summary_data = {
                "Assessment Area": ["Mathematics", "Reading", "Writing", "Attendance", "Behavior", "Literacy", "Overall Risk", "AI Confidence"],
                "Score/Rating": [f"{student_data['math_score']}%", f"{student_data['reading_score']}%", f"{student_data['writing_score']}%", 
                                f"{student_data['attendance']}%", f"{student_data['behavior']}/5", f"{student_data['literacy']}/10", 
                                risk_level, f"{prediction_prob:.1%}"]
            }
            st.table(pd.DataFrame(summary_data))
            
            if save_button or st.button(" Save This Prediction", key=f"save_button_after_predict_rerun_{reset_counter}"):
                prediction_record = {
                    "timestamp": datetime.now().isoformat(),
                    "student_name": student_name,
                    "grade_level": grade_level,
                    "prediction": prediction,
                    "probability": prediction_prob,
                    "risk_level": risk_level,
                    "notes": notes,
                    **student_data
                }
                save_prediction_data(prediction_record)
                st.success(" Prediction saved successfully!")
    
    elif prediction_type == "Batch Upload":
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f" Uploaded file with {len(df)} students")
                
                required_columns = ['math_score', 'reading_score', 'writing_score', 'attendance', 'behavior', 'literacy']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    st.error(f"{get_material_icon_html('error', style='fill')} Missing required columns: {', '.join(missing_columns)}", unsafe_allow_html=True)
                else:
                    st.markdown("### Data Preview")
                    st.dataframe(df.head())
                    
                    if st.button("Process Batch Predictions", key="process_batch_predictions_button"):
                        progress_bar = st.progress(0)
                        results = []
                        
                        for idx, row in df.iterrows():
                            try:
                                prediction, prediction_prob = make_prediction(row.to_dict())
                                
                                if prediction_prob < 0.3:
                                    risk_level = "Low Risk"
                                elif prediction_prob < 0.7:
                                    risk_level = "Medium Risk"
                                else:
                                    risk_level = "High Risk"
                                
                                results.append({
                                    'Student_ID': idx + 1,
                                    'Risk_Level': risk_level,
                                    'Risk_Probability': f"{prediction_prob:.1%}",
                                    **row.to_dict()
                                })
                                
                                progress_bar.progress((idx + 1) / len(df))
                            
                            except Exception as e:
                                st.error(f"Error processing student {idx + 1}: {str(e)}")
                        
                        results_df = pd.DataFrame(results)
                        st.markdown("### Batch Prediction Results")
                        st.dataframe(results_df)
                        
                        risk_counts = results_df['Risk_Level'].value_counts()
                        fig_pie = px.pie(values=risk_counts.values, names=risk_counts.index, 
                                         title="Risk Level Distribution")
                        st.plotly_chart(fig_pie, use_container_width=True)
                        
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results",
                            data=csv,
                            file_name=f"learning_risk_predictions_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            key="download_batch_results_button"
                        )
            
            except Exception as e:
                st.error(f" {get_material_icon_html('error', style='fill')} Error reading file: {str(e)}", unsafe_allow_html=True)
        else:
            st.info("Please upload a CSV file to begin batch processing")
    
    else:
        st.markdown("### Historical Analysis")
        historical_data = load_student_data()
        
        if historical_data:
            df_historical = pd.DataFrame(historical_data)
            
            df_historical['timestamp'] = pd.to_datetime(df_historical['timestamp'])
            
            analysis_type = st.selectbox(
                "Select analysis type:",
                ["Risk Trends Over Time", "Performance Correlation", "Student Progress Tracking"],
                key="historical_analysis_type_selector"
            )
            
            if analysis_type == "Risk Trends Over Time":
                daily_risks = df_historical.groupby([df_historical['timestamp'].dt.date, 'risk_level']).size().unstack(fill_value=0)
                
                fig_trend = px.line(daily_risks, title="Risk Level Trends Over Time")
                st.plotly_chart(fig_trend, use_container_width=True)
            
            elif analysis_type == "Performance Correlation":
                numeric_cols = ['math_score', 'reading_score', 'writing_score', 'attendance', 'behavior', 'literacy', 'probability']
                if all(col in df_historical.columns for col in numeric_cols):
                    corr_matrix = df_historical[numeric_cols].corr()
                    fig_heatmap = px.imshow(corr_matrix, text_auto=True, title="Performance Correlation Matrix")
                    st.plotly_chart(fig_heatmap, use_container_width=True)
            
            elif analysis_type == "Student Progress Tracking":
                if 'student_name' in df_historical.columns:
                    student_names = df_historical['student_name'].dropna().unique()
                    selected_student = st.selectbox("Select student:", student_names, key="student_progress_tracking_selector")
                    
                    if selected_student:
                        student_progress = df_historical[df_historical['student_name'] == selected_student].sort_values('timestamp')
                        
                        if len(student_progress) > 1:
                            fig_progress = px.line(student_progress, x='timestamp', y='probability', 
                                                     title=f"Risk Probability Trend for {selected_student}")
                            st.plotly_chart(fig_progress, use_container_width=True)
                        else:
                            st.info("Not enough data points for trend analysis")
        else:
            st.info("No historical data available. Make some predictions first!")

    st.markdown("---")
    st.markdown(f"### {get_material_icon_html('lightbulb_circle', style='fill')} Tips for Accurate Predictions", unsafe_allow_html=True)
    st.markdown("""
    - **Regular Updates**: Update student data regularly for more accurate tracking
    - **Multiple Indicators**: Consider all factors, not just academic scores
    - **Context Matters**: Add relevant notes about external factors
    - **Follow-up**: Use predictions as starting points for deeper assessment
    """)

if __name__ == "__main__":
    main()