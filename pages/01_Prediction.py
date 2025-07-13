# pages/01_Prediction.py - Enhanced with Improved Animations and UI
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
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

from utils.model_utils import load_model, make_prediction
from utils.data_utils import save_prediction_data, load_student_data
from utils.image_base64 import get_base64_images
from utils.language_utils import get_text, load_app_settings, save_app_settings
from utils.exact_ui import (
    add_exact_ui_styles,
    render_exact_sidebar,
    render_exact_page_header,
    create_exact_metric_card,
    create_exact_chart_container,
    get_b64_image_html
)
from utils.auth_utils import is_authenticated, render_login_page, logout_user, get_user_role
from utils.icon_utils import get_material_icon_html

# Page config
st.set_page_config(
    page_title="EduScan Prediction",
    page_icon="🔍",
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

def render_lottie(url, height=200, key=None, fallback_icon="school", fallback_text="Loading..."):
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

def get_risk_animation_url(prediction_prob):
    """Get appropriate animation URL based on risk level"""
    if prediction_prob < 0.3:
        return "https://lottie.host/4d42d6a6-8290-4b13-b3ab-2a10a490e6db/9oJrI4pj1F.json"  # Success/celebration
    elif prediction_prob < 0.7:
        return "https://lottie.host/8a1c9f65-4b8d-4e2f-9a3c-7f6e5d4c3b2a/M4X8jK9wR5.json"  # Warning/attention
    else:
        return "https://lottie.host/6c3d8e9f-2a1b-4c5d-8e7f-9g8h7i6j5k4l/P7Y3nM2qL8.json"  # Alert/intervention

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
    """Create enhanced visualization for risk assessment"""
    
    # Determine colors based on risk level
    if prediction_prob < 0.3:
        gauge_color = "#10b981"  # Green
        bar_color = "#059669"
    elif prediction_prob < 0.7:
        gauge_color = "#f59e0b"  # Orange  
        bar_color = "#d97706"
    else:
        gauge_color = "#ef4444"  # Red
        bar_color = "#dc2626"
    
    # Enhanced risk gauge chart
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=prediction_prob * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Learning Risk Assessment (%)", 'font': {'size': 16, 'color': '#374151'}},
        delta={'reference': 30, 'increasing': {'color': "#ef4444"}, 'decreasing': {'color': "#10b981"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#6b7280"},
            'bar': {'color': bar_color, 'thickness': 0.3},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e5e7eb",
            'steps': [
                {'range': [0, 30], 'color': "#dcfdf7"},
                {'range': [30, 70], 'color': "#fef3c7"},
                {'range': [70, 100], 'color': "#fee2e2"}
            ],
            'threshold': {
                'line': {'color': "#dc2626", 'width': 3},
                'thickness': 0.8,
                'value': 70
            }
        }
    ))
    
    fig_gauge.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#374151', 'family': 'Inter'},
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # Enhanced performance radar chart
    categories = ['Math Score', 'Reading Score', 'Writing Score', 'Attendance', 'Behavior×20', 'Literacy×10']
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
        name='Student Performance',
        line_color=gauge_color,
        fillcolor=f'rgba({int(gauge_color[1:3], 16)}, {int(gauge_color[3:5], 16)}, {int(gauge_color[5:7], 16)}, 0.3)'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="#e5e7eb",
                tickfont={'size': 10, 'color': '#6b7280'}
            ),
            angularaxis=dict(
                tickfont={'size': 11, 'color': '#374151'}
            )
        ),
        showlegend=False,
        title={'text': "Performance Profile", 'font': {'size': 16, 'color': '#374151'}},
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter'},
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig_gauge, fig_radar

def display_recommendations(risk_level, student_data):
    """Display personalized recommendations based on risk level"""
    
    if "Low" in risk_level:
        st.markdown(f"✅ **Low Risk** - Continue current support strategies", unsafe_allow_html=True)
        recommendations = [
            "Maintain current learning pace and methods",
            "Continue regular progress monitoring",
            "Encourage continued engagement in all subjects",
            "Consider enrichment activities to challenge the student"
        ]
        color = "#10b981"
    elif "Medium" in risk_level:
        st.markdown(f"⚠️ **Medium Risk** - Targeted interventions recommended", unsafe_allow_html=True)
        recommendations = [
            "Implement targeted interventions in lower-performing areas",
            "Increase frequency of progress monitoring",
            "Consider additional support in specific subjects",
            "Engage parents in home-based learning activities",
            "Explore different teaching methods and materials"
        ]
        color = "#f59e0b"
    else:
        st.markdown(f"🚨 **High Risk** - Intensive intervention required", unsafe_allow_html=True)
        recommendations = [
            "Initiate comprehensive assessment by learning specialists",
            "Implement intensive intervention strategies",
            "Consider individualized education plan (IEP)",
            "Increase collaboration between teachers and parents",
            "Explore assistive technologies and adaptive methods",
            "Regular monitoring and adjustment of intervention strategies"
        ]
        color = "#ef4444"
    
    st.markdown("### 💡 Personalized Recommendations")
    for i, rec in enumerate(recommendations, 1):
        st.write(f"{i}. {rec}")

def main():
    # Authentication check
    if not is_authenticated():
        st.warning("Please log in to access the Prediction page.")
        st.switch_page("app.py")
        return
    
    # Header
    render_exact_page_header(
        get_material_icon_html('search'), 
        'Prediction', 
        'AI-Powered Student Evaluation System', 
        language
    )
    
    # Enhanced hero section with multiple animations
    st.markdown("### 🌟 Empowering Student Success Through Data-Driven Assessment")
    
    # Three-column animation layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📊 Data Analysis**")
        render_lottie(
            "https://lottie.host/c5d32643-1965-4071-981e-d2ab6e40f0f7/cIUo7cX9X9.json",
            height=180,
            key="data_analysis",
            fallback_icon="analytics",
            fallback_text="Comprehensive Data Analysis"
        )
        st.caption("Advanced analytics for student assessment")
    
    with col2:
        st.markdown("**🎯 Learning Success**")
        render_lottie(
            "https://lottie.host/c5dfa88a-8138-4928-9a9c-8f810f30419c/v5EB8t0KVf.json",
            height=180,
            key="learning_success",
            fallback_icon="school",
            fallback_text="Student Achievement"
        )
        st.caption("Celebrating educational achievements")
    
    with col3:
        st.markdown("**🔬 Evidence-Based Methods**")
        render_lottie(
            "https://lottie.host/687a0991-917f-4d7b-92f6-d9ecaa0780b7/D75iWs83gn.json",
            height=180,
            key="evidence_methods",
            fallback_icon="science",
            fallback_text="Research-Based Approach"
        )
        st.caption("Scientific approach to learning assessment")

    # Enhanced sidebar for prediction options
    with st.sidebar:
        st.markdown("### 🎯 Assessment Options")
        
        available_prediction_types = ["Individual Student Assessment", "Batch Student Upload", "Historical Data Analysis"]
        user_role = get_user_role()
        
        prediction_type = st.selectbox(
            "Choose assessment type:",
            available_prediction_types,
            key="prediction_type_selector"
        )
        
        # Enhanced model information panel
        st.markdown("### 🤖 AI Model Information")
        st.info("""
        **Assessment Model Details**
        
        - **Type**: Random Forest Classifier
        - **Input Features**: 6 key learning indicators  
        - **Data Processing**: Standardized scoring
        - **Optimization**: Grid search validated
        - **Status**: ✅ Ready for assessments
        """)
        
        # Show model features with icons
        st.markdown("**📋 Assessment Criteria:**")
        features = [
            "📊 Mathematics Score (0-100%)",
            "📖 Reading Comprehension (0-100%)", 
            "✍️ Writing Skills (0-100%)",
            "📅 School Attendance Rate (%)",
            "🎭 Classroom Behavior (1-5 scale)",
            "📚 Literacy Development (1-10 scale)"
        ]
        for feature in features:
            st.markdown(f"• {feature}")
            
        st.success("✅ AI model ready for student assessments")
        
        uploaded_file = None
        if "Batch" in prediction_type:
            st.markdown("#### 📁 Upload Student Data")
            uploaded_file = st.file_uploader(
                "Upload CSV file with student data",
                type=['csv'],
                help="CSV must include: math_score, reading_score, writing_score, attendance, behavior, literacy",
                key="prediction_batch_uploader"
            )

    # Main content based on prediction type
    if prediction_type == "Individual Student Assessment":
        reset_counter = st.session_state.get('reset_counter', 0)
        
        st.markdown("""
        <div class="input-section section-animated-text">
            <h2 class="highlight-text">Student Learning Assessment Form</h2>
            <p style="font-size: 1.1em; margin-bottom: 2rem; color: var(--gray-700);">
                Complete this comprehensive evaluation to assess learning risk factors and receive personalized recommendations
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="input-section">
                <h3 class="highlight-text">📊 Academic Performance Scores</h3>
            </div>
            """, unsafe_allow_html=True)
            math_score = st.number_input("Mathematics Score (%)", min_value=0, max_value=100, value=75, step=1, 
                                       help="Student's current mathematics performance level", key=f"math_score_input_{reset_counter}")
            reading_score = st.number_input("Reading Comprehension Score (%)", min_value=0, max_value=100, value=80, step=1, 
                                          help="Student's reading and comprehension ability", key=f"reading_score_input_{reset_counter}")
            writing_score = st.number_input("Writing Skills Score (%)", min_value=0, max_value=100, value=70, step=1, 
                                          help="Student's written expression and composition skills", key=f"writing_score_input_{reset_counter}")
            
        with col2:
            st.markdown("""
            <div class="input-section">
                <h3 class="highlight-text">🎭 Behavioral & Social Indicators</h3>
            </div>
            """, unsafe_allow_html=True)
            attendance = st.slider("School Attendance Rate (%)", 0, 100, 85, 
                                  help="Percentage of school days attended this term", key=f"attendance_slider_{reset_counter}")
            behavior_options = ["1 - Poor", "2 - Below Average", "3 - Average", "4 - Good", "5 - Excellent"]
            behavior_selection = st.select_slider("Classroom Behavior Rating", options=behavior_options, value="3 - Average", 
                                                help="Rate the student's typical classroom behavior and cooperation", key=f"behavior_slider_{reset_counter}")
            behavior = int(behavior_selection.split(' ')[0])
            literacy_options = [f'{i} - {"Beginner" if i <= 3 else "Developing" if i <= 6 else "Advanced"}' for i in range(1, 11)]
            literacy_selection = st.select_slider("Overall Literacy Level", options=literacy_options, value="6 - Developing",
                                                help="Assess the student's reading and literacy development stage", key=f"literacy_slider_{reset_counter}")
            literacy = int(literacy_selection.split(' ')[0])
        
        st.markdown("""
        <div class="input-section">
            <h3 class="highlight-text">👤 Student Information</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            student_name = st.text_input("Student Name", help="Enter the student's full name for record keeping", key=f"student_name_input_{reset_counter}")
            grade_level = st.selectbox("Current Grade Level", ["Pre-K", "K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], key=f"grade_level_select_{reset_counter}")
        
        with col4:
            notes = st.text_area("Additional Notes", placeholder="Any relevant observations, special circumstances, or additional context...", 
                                help="Include any relevant observations about the student", height=100, key=f"teacher_notes_input_{reset_counter}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            predict_button = st.button("🧠 Analyze Learning Risk", type="primary", use_container_width=True)
        
        with col2:
            reset_button = st.button("🔄 Clear All Fields", use_container_width=True)
        
        with col3:
            save_button = st.button("💾 Save Assessment Data", use_container_width=True)
        
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
                st.error("❌ Please correct the following errors:")
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
                    
                    # Enhanced results display
                    st.markdown("""
                    <div class="results-section">
                        <h2 class="highlight-text">AI Assessment Results</h2>
                        <p style="font-size: 1.2em; text-align: center; color: var(--gray-700); margin-bottom: 2rem;">
                            <strong>Comprehensive learning assessment completed</strong>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Determine risk level and display
                    if prediction_prob < 0.3:
                        risk_level = "Low Risk"
                        risk_color = "#10b981"
                        risk_icon = "✅"
                    elif prediction_prob < 0.7:
                        risk_level = "Medium Risk"
                        risk_color = "#f59e0b"
                        risk_icon = "⚠️"
                    else:
                        risk_level = "High Risk"
                        risk_color = "#ef4444"
                        risk_icon = "🚨"
                    
                    # Risk level display with animation
                    st.markdown(f"""
                    <div style="text-align: center; background: linear-gradient(135deg, {risk_color}20, {risk_color}30); 
                         padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border: 2px solid {risk_color}40;">
                        <h3 style="color: {risk_color}; margin-bottom: 0.5rem;">{risk_icon} Learning Risk Level: {risk_level}</h3>
                        <p style="color: {risk_color}; font-size: 1.1em; margin: 0;">AI Confidence Score: {prediction_prob:.1%}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Display appropriate risk-level animation
                    animation_col = st.columns([1, 2, 1])
                    with animation_col[1]:
                        animation_url = get_risk_animation_url(prediction_prob)
                        
                        if prediction_prob < 0.3:
                            st.markdown("**🎉 Excellent Progress - Continue Current Path**")
                        elif prediction_prob < 0.7:
                            st.markdown("**⚠️ Attention Needed - Targeted Support Recommended**")
                        else:
                            st.markdown("**🚨 Immediate Action - Comprehensive Intervention Required**")
                        
                        render_lottie(
                            animation_url,
                            height=250,
                            key=f"risk_result_{prediction_prob}",
                            fallback_icon="psychology" if prediction_prob >= 0.7 else "warning" if prediction_prob >= 0.3 else "celebration",
                            fallback_text=f"{risk_level} Assessment Result"
                        )
                    
                    # Enhanced visualizations
                    fig_gauge, fig_radar = create_risk_visualization(prediction_prob, student_data)
                    
                    viz_col1, viz_col2 = st.columns(2)
                    with viz_col1:
                        st.plotly_chart(fig_gauge, use_container_width=True)
                    with viz_col2:
                        st.plotly_chart(fig_radar, use_container_width=True)
                    
                    # Recommendations
                    display_recommendations(risk_level, student_data)
                    
                    # Assessment summary
                    st.markdown("### 📋 Complete Assessment Summary")
                    summary_data = {
                        "Assessment Area": ["Mathematics", "Reading Comprehension", "Writing Skills", "School Attendance", 
                                          "Classroom Behavior", "Literacy Development", "Overall Risk Level", "AI Confidence"],
                        "Score/Rating": [f"{math_score}%", f"{reading_score}%", f"{writing_score}%", f"{attendance}%", 
                                       f"{behavior}/5", f"{literacy}/10", risk_level, f"{prediction_prob:.1%}"]
                    }
                    st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
                    
                    if st.button("💾 Save This Assessment", key=f"save_button_after_predict_{reset_counter}"):
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
                        st.success("✅ Assessment saved successfully to database!")
                
                except Exception as e:
                    st.error(f"❌ Error processing assessment: {str(e)}")
                    st.info("ℹ️ Note: Using demonstration model. Please ensure your trained model file is properly configured.")

    elif prediction_type == "Batch Student Upload":
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ Successfully uploaded file with {len(df)} student records")
                
                required_columns = ['math_score', 'reading_score', 'writing_score', 'attendance', 'behavior', 'literacy']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
                    st.info("💡 Required columns: math_score, reading_score, writing_score, attendance, behavior, literacy")
                else:
                    st.markdown("### 📊 Data Preview")
                    st.dataframe(df.head())
                    
                    if st.button("🚀 Process Batch Assessments", key="process_batch_predictions_button"):
                        progress_bar = st.progress(0)
                        st.markdown("**Processing student assessments...**")
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
                                    'Risk_Assessment': risk_level,
                                    'Confidence_Score': f"{prediction_prob:.1%}",
                                    **row.to_dict()
                                })
                                
                                progress_bar.progress((idx + 1) / len(df))
                            
                            except Exception as e:
                                st.error(f"❌ Error processing student {idx + 1}: {str(e)}")
                        
                        results_df = pd.DataFrame(results)
                        st.markdown("### 📈 Batch Assessment Results")
                        st.dataframe(results_df)
                        
                        # Enhanced visualization
                        risk_counts = results_df['Risk_Assessment'].value_counts()
                        fig_pie = px.pie(values=risk_counts.values, names=risk_counts.index, 
                                         title="Student Risk Level Distribution",
                                         color_discrete_map={'Low Risk': '#10B981', 'Medium Risk': '#F59E0B', 'High Risk': '#EF4444'})
                        st.plotly_chart(fig_pie, use_container_width=True)
                        
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Assessment Results",
                            data=csv,
                            file_name=f"student_risk_assessments_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            key="download_batch_results_button"
                        )
            
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
                st.info("💡 Please ensure your CSV file is properly formatted with the required columns.")
        else:
            st.info("📁 Please upload a CSV file to begin batch processing")
            
            # Show sample CSV format
            st.markdown("### 📋 Sample CSV Format")
            sample_data = pd.DataFrame({
                'math_score': [85, 72, 93],
                'reading_score': [78, 65, 89],
                'writing_score': [82, 70, 91],
                'attendance': [95, 88, 97],
                'behavior': [4, 3, 5],
                'literacy': [7, 6, 9]
            })
            st.dataframe(sample_data)
    
    else:  # Historical Data Analysis
        st.markdown("### 📊 Historical Assessment Analysis")
        historical_data = load_student_data()
        
        if historical_data:
            df_historical = pd.DataFrame(historical_data)
            df_historical['timestamp'] = pd.to_datetime(df_historical['timestamp'])
            
            # Enhanced analysis options
            analysis_col1, analysis_col2 = st.columns(2)
            
            with analysis_col1:
                analysis_type = st.selectbox(
                    "Select analysis type:",
                    ["Risk Trends Over Time", "Performance Correlation Analysis", "Individual Student Progress", "Intervention Effectiveness"],
                    key="historical_analysis_type_selector"
                )
            
            with analysis_col2:
                time_range = st.selectbox(
                    "Time range:",
                    ["Last 30 Days", "Last 90 Days", "Last 6 Months", "All Time"],
                    key="time_range_selector"
                )
            
            # Filter data based on time range
            now = datetime.now()
            if time_range == "Last 30 Days":
                cutoff = now - pd.Timedelta(days=30)
            elif time_range == "Last 90 Days":
                cutoff = now - pd.Timedelta(days=90)
            elif time_range == "Last 6 Months":
                cutoff = now - pd.Timedelta(days=180)
            else:
                cutoff = df_historical['timestamp'].min()
            
            filtered_data = df_historical[df_historical['timestamp'] >= cutoff]
            
            if analysis_type == "Risk Trends Over Time":
                st.markdown("#### 📈 Risk Level Trends Analysis")
                
                if 'risk_level' in filtered_data.columns:
                    daily_risks = filtered_data.groupby([filtered_data['timestamp'].dt.date, 'risk_level']).size().unstack(fill_value=0)
                    
                    fig_trend = px.line(daily_risks, title="Risk Level Trends Over Time",
                                       color_discrete_map={'Low Risk': '#10B981', 'Medium Risk': '#F59E0B', 'High Risk': '#EF4444'})
                    fig_trend.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Number of Students",
                        height=400
                    )
                    st.plotly_chart(fig_trend, use_container_width=True)
                    
                    # Summary statistics
                    total_assessments = len(filtered_data)
                    risk_distribution = filtered_data['risk_level'].value_counts()
                    
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    with metric_col1:
                        st.metric("Total Assessments", total_assessments)
                    with metric_col2:
                        low_risk_pct = (risk_distribution.get('Low Risk', 0) / total_assessments * 100) if total_assessments > 0 else 0
                        st.metric("Low Risk Students", f"{low_risk_pct:.1f}%")
                    with metric_col3:
                        medium_risk_pct = (risk_distribution.get('Medium Risk', 0) / total_assessments * 100) if total_assessments > 0 else 0
                        st.metric("Medium Risk Students", f"{medium_risk_pct:.1f}%")
                    with metric_col4:
                        high_risk_pct = (risk_distribution.get('High Risk', 0) / total_assessments * 100) if total_assessments > 0 else 0
                        st.metric("High Risk Students", f"{high_risk_pct:.1f}%")
                else:
                    st.warning("⚠️ No risk level data available for trend analysis")
            
            elif analysis_type == "Performance Correlation Analysis":
                st.markdown("#### 🔗 Academic Performance Correlation Matrix")
                
                numeric_cols = ['math_score', 'reading_score', 'writing_score', 'attendance', 'behavior', 'literacy']
                available_cols = [col for col in numeric_cols if col in filtered_data.columns]
                
                if len(available_cols) >= 2:
                    corr_matrix = filtered_data[available_cols].corr()
                    
                    fig_heatmap = px.imshow(corr_matrix, 
                                          text_auto=True, 
                                          title="Performance Indicators Correlation",
                                          color_continuous_scale="RdBu_r",
                                          aspect="auto")
                    fig_heatmap.update_layout(height=500)
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                    
                    # Insights
                    st.markdown("#### 💡 Key Insights")
                    strong_correlations = []
                    for i in range(len(corr_matrix.columns)):
                        for j in range(i+1, len(corr_matrix.columns)):
                            corr_val = corr_matrix.iloc[i, j]
                            if abs(corr_val) > 0.6:
                                strong_correlations.append({
                                    'Factor 1': corr_matrix.columns[i],
                                    'Factor 2': corr_matrix.columns[j],
                                    'Correlation': f"{corr_val:.3f}",
                                    'Strength': 'Strong' if abs(corr_val) > 0.8 else 'Moderate'
                                })
                    
                    if strong_correlations:
                        st.dataframe(pd.DataFrame(strong_correlations), hide_index=True)
                    else:
                        st.info("No strong correlations (>0.6) found between performance indicators")
                else:
                    st.warning("⚠️ Insufficient numeric data for correlation analysis")
            
            elif analysis_type == "Individual Student Progress":
                st.markdown("#### 👤 Individual Student Progress Tracking")
                
                if 'student_name' in filtered_data.columns:
                    student_names = filtered_data['student_name'].dropna().unique()
                    
                    if len(student_names) > 0:
                        selected_student = st.selectbox("Select student:", student_names, key="student_progress_tracking_selector")
                        
                        if selected_student:
                            student_progress = filtered_data[filtered_data['student_name'] == selected_student].sort_values('timestamp')
                            
                            if len(student_progress) > 1:
                                # Progress over time
                                fig_progress = px.line(student_progress, x='timestamp', y='probability', 
                                                     title=f"Learning Risk Trend for {selected_student}",
                                                     markers=True)
                                fig_progress.update_layout(
                                    xaxis_title="Assessment Date",
                                    yaxis_title="Risk Probability",
                                    height=400
                                )
                                st.plotly_chart(fig_progress, use_container_width=True)
                                
                                # Performance comparison
                                if len(student_progress) >= 2:
                                    latest = student_progress.iloc[-1]
                                    previous = student_progress.iloc[-2]
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        risk_change = latest['probability'] - previous['probability']
                                        trend = "📈 Increasing" if risk_change > 0.05 else "📉 Decreasing" if risk_change < -0.05 else "➡️ Stable"
                                        st.metric("Risk Trend", trend, f"{risk_change:+.1%}")
                                    
                                    with col2:
                                        days_between = (latest['timestamp'] - previous['timestamp']).days
                                        st.metric("Days Since Last Assessment", f"{days_between} days")
                                
                                # Detailed progress table
                                st.markdown("#### 📊 Assessment History")
                                progress_display = student_progress[['timestamp', 'math_score', 'reading_score', 'writing_score', 'attendance', 'behavior', 'literacy', 'risk_level', 'probability']].copy()
                                progress_display['timestamp'] = progress_display['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
                                progress_display['probability'] = progress_display['probability'].apply(lambda x: f"{x:.1%}")
                                st.dataframe(progress_display, hide_index=True)
                            else:
                                st.info("📊 Only one assessment available. Multiple assessments needed for trend analysis.")
                    else:
                        st.warning("⚠️ No student names found in the data")
                else:
                    st.warning("⚠️ Student name data not available")
            
            else:  # Intervention Effectiveness
                st.markdown("#### 🎯 Intervention Effectiveness Analysis")
                
                if 'risk_level' in filtered_data.columns and len(filtered_data) > 10:
                    # Analyze risk level changes over time
                    monthly_data = filtered_data.groupby([filtered_data['timestamp'].dt.to_period('M'), 'risk_level']).size().unstack(fill_value=0)
                    
                    if len(monthly_data) > 1:
                        fig_monthly = px.bar(monthly_data, title="Monthly Risk Level Distribution",
                                           color_discrete_map={'Low Risk': '#10B981', 'Medium Risk': '#F59E0B', 'High Risk': '#EF4444'})
                        fig_monthly.update_layout(
                            xaxis_title="Month",
                            yaxis_title="Number of Students",
                            height=400
                        )
                        st.plotly_chart(fig_monthly, use_container_width=True)
                        
                        # Effectiveness metrics
                        st.markdown("#### 📈 Intervention Impact Metrics")
                        
                        total_students = len(filtered_data['student_name'].unique()) if 'student_name' in filtered_data.columns else len(filtered_data)
                        high_risk_students = len(filtered_data[filtered_data['risk_level'] == 'High Risk'])
                        intervention_rate = (high_risk_students / total_students * 100) if total_students > 0 else 0
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Students Assessed", total_students)
                        with col2:
                            st.metric("High Risk Identified", f"{intervention_rate:.1f}%")
                        with col3:
                            avg_math_score = filtered_data['math_score'].mean() if 'math_score' in filtered_data.columns else 0
                            st.metric("Average Math Score", f"{avg_math_score:.1f}%")
                    else:
                        st.info("📊 Insufficient data for monthly trend analysis")
                else:
                    st.warning("⚠️ Insufficient data for intervention effectiveness analysis")
        else:
            st.info("📊 No historical data available. Complete some assessments first to enable analysis!")
            
            # Show sample of what analysis would look like
            st.markdown("### 🔮 Available After Assessments")
            st.markdown("""
            Once you've completed student assessments, you'll be able to:
            
            - **📈 Track Risk Trends**: Monitor how student risk levels change over time
            - **🔗 Analyze Correlations**: Understand relationships between different performance factors  
            - **👤 Individual Progress**: Follow specific students' learning journeys
            - **🎯 Measure Impact**: Evaluate the effectiveness of interventions
            """)

    # Enhanced tips section
    st.markdown("---")
    st.markdown("### 💡 Assessment Best Practices")
    
    tip_col1, tip_col2 = st.columns(2)
    
    with tip_col1:
        st.markdown("""
        **🎯 For Accurate Assessments:**
        - Gather data from multiple sources and timeframes
        - Consider external factors affecting performance
        - Update assessments regularly (monthly recommended)
        - Include qualitative observations in notes
        """)
    
    with tip_col2:
        st.markdown("""
        **📊 Using Results Effectively:**
        - Use assessments as starting points for deeper evaluation
        - Combine AI insights with professional judgment
        - Track progress over time, not just single assessments
        - Share results with educational support teams
        """)
    
    # Add help and support section
    st.markdown("---")
    st.markdown("### 🤝 Need Help?")
    
    help_col1, help_col2 = st.columns(2)
    
    with help_col1:
        st.markdown("""
        **📚 Resources:**
        - [Assessment Guidelines](/#) - Best practices for student evaluation
        - [Interpretation Guide](/#) - Understanding risk levels and recommendations  
        - [Intervention Strategies](/#) - Evidence-based support methods
        """)
    
    with help_col2:
        st.markdown("""
        **📞 Support:**
        - Email: support@eduscan.edu
        - Phone: (555) 123-4567
        - Live Chat: Available 8 AM - 6 PM
        """)

if __name__ == "__main__":
    main()