# pages/02_Teacher_Resources.py - Enhanced with Multiple Animations
import streamlit as st
import pandas as pd
import json
from datetime import datetime
import random
import sys
import os

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
    page_title="EduScan Teacher Resources",
    page_icon="👩‍🏫",
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

def generate_activity(difficulty_type, grade_level):
    """Generate a random educational activity based on difficulty type and grade level"""
    
    activities = {
        "reading": {
            "K-2": [
                "Picture book discussion with visual cues",
                "Letter sound matching games",
                "Simple word building with letter tiles",
                "Reading comprehension with picture support",
                "Phonics songs and rhyming activities"
            ],
            "3-5": [
                "Graphic organizer for story elements",
                "Vocabulary word maps with illustrations",
                "Partner reading with guided questions",
                "Reading response journals with prompts",
                "Text-to-self connection activities"
            ],
            "6-8": [
                "Literature circles with differentiated roles",
                "Character analysis using graphic organizers",
                "Compare and contrast essays with templates",
                "Research projects with structured guidelines",
                "Reading strategy instruction (summarizing, questioning)"
            ]
        },
        "math": {
            "K-2": [
                "Hands-on counting with manipulatives",
                "Visual number line activities",
                "Shape recognition through real-world objects",
                "Simple addition/subtraction with pictures",
                "Math story problems with visual supports"
            ],
            "3-5": [
                "Fraction circles and visual representations",
                "Word problem solving with step-by-step guides",
                "Math journals for problem-solving strategies",
                "Multiplication games with visual arrays",
                "Real-world math applications (cooking, shopping)"
            ],
            "6-8": [
                "Algebra tiles for equation solving",
                "Geometric constructions with technology",
                "Data analysis projects with real data",
                "Mathematical modeling activities",
                "Peer tutoring for complex problem solving"
            ]
        },
        "writing": {
            "K-2": [
                "Picture prompts for creative writing",
                "Sentence frames for structured writing",
                "Interactive writing with teacher support",
                "Story sequencing activities",
                "Simple poetry with repetitive patterns"
            ],
            "3-5": [
                "Graphic organizer for essay planning",
                "Peer editing with specific checklists",
                "Multi-step writing process instruction",
                "Genre studies with mentor texts",
                "Writing conferences with guided feedback"
            ]
        },
        "behavior": {
            "All": [
                "Positive behavior reinforcement system",
                "Clear classroom expectations with visual reminders",
                "Break cards for self-regulation",
                "Mindfulness and breathing exercises",
                "Social skills practice through role-play",
                "Sensory break activities",
                "Peer mentoring programs",
                "Goal-setting and progress tracking",
                "Conflict resolution strategies",
                "Emotional regulation techniques"
            ]
        }
    }
    
    if difficulty_type == "behavior":
        return random.choice(activities[difficulty_type]["All"])
    else:
        grade_group = "K-2" if grade_level in ["K", "1", "2"] else "3-5" if grade_level in ["3", "4", "5"] else "6-8"
        return random.choice(activities[difficulty_type].get(grade_group, activities[difficulty_type]["3-5"]))

def main():
    # Authentication check
    if not is_authenticated():
        st.warning("Please log in to access Teacher Resources.")
        st.switch_page("app.py")
        return

    # Role-based access control
    user_role = get_user_role()
    if user_role == 'parent':
        st.error("Access Denied: Parents cannot view Teacher Resources.")
        st.info("Redirecting you to Parent Tracker...")
        st.switch_page("pages/03_Parent_Tracker.py")
        return
        
    # Header
    render_exact_page_header(
        get_material_icon_html('school'), 
        'Teacher Resources', 
        'Comprehensive Tools for Effective Student Support', 
        language
    )
    
    # Enhanced hero section with multiple animations
    st.markdown("### 🌟 Professional Excellence in Education")
    
    # Two-column layout for animations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👥 Teacher Collaboration**")
        render_lottie(
            "https://lottie.host/9dbf9a0f-b1fd-4b92-8215-e595745178d6/iFNBmCDQ5Z.json",
            height=250,
            key="teacher_collaboration",
            fallback_icon="groups",
            fallback_text="Collaborative Teaching Excellence"
        )
        st.caption("Building professional learning communities and collaborative support systems")
    
    with col2:
        st.markdown("**📚 Innovative Teaching Methods**")
        render_lottie(
            "https://lottie.host/62286ecf-6779-4781-90a0-c747f05d5f8a/giBjeAZ9o4.json",
            height=250,
            key="innovative_teaching",
            fallback_icon="lightbulb",
            fallback_text="Innovative Learning Strategies"
        )
        st.caption("Implementing research-based strategies for diverse learners and inclusive classrooms")

    # Quick Assessment Tools
    st.markdown("---")
    st.markdown("### 🔍 Quick Assessment Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Student Risk Assessment")
        student_name = st.text_input("Student Name", key="teacher_student_name")
        risk_indicators = st.multiselect(
            "Observed Risk Indicators",
            ["Low attendance", "Poor academic performance", "Behavioral issues", 
             "Social difficulties", "Learning disabilities", "Language barriers"],
            key="risk_indicators"
        )
        
        if st.button("Submit Assessment", key="assess_student_btn"):
            if student_name and risk_indicators:
                st.success(f"✅ Assessment recorded for {student_name}")
                risk_level = "High" if len(risk_indicators) >= 3 else "Medium" if len(risk_indicators) >= 2 else "Low"
                st.info(f"Recommended Risk Level: **{risk_level}**")
            else:
                st.warning("Please enter student name and select risk indicators")
    
    with col2:
        st.markdown("#### Intervention Planning")
        intervention_type = st.selectbox(
            "Intervention Type",
            ["Academic Support", "Behavioral Intervention", "Social Skills", "Family Engagement"],
            key="intervention_type"
        )
        
        duration = st.selectbox(
            "Duration",
            ["2 weeks", "1 month", "2 months", "Semester"],
            key="intervention_duration"
        )
        
        if st.button("Submit Plan", key="create_plan_btn"):
            st.success("✅ Intervention plan created successfully!")
            
            # Show sample intervention plan
            st.markdown("**Suggested Intervention Plan:**")
            if intervention_type == "Academic Support":
                st.markdown("""
                - **Daily**: 15-minute focused skill practice
                - **Weekly**: Progress assessment and adjustment
                - **Resources**: Differentiated worksheets, educational games
                - **Support**: Peer tutoring, teacher check-ins
                """)
            elif intervention_type == "Behavioral Intervention":
                st.markdown("""
                - **Daily**: Behavior tracking chart
                - **Weekly**: Positive reinforcement system review
                - **Resources**: Social stories, self-regulation tools
                - **Support**: Counselor collaboration, parent communication
                """)

    # Resource categories with enhanced animations
    st.markdown("---")
    st.markdown("### 📚 Evidence-Based Intervention Strategies")
    
    # Two animations for intervention strategies section
    intervention_col1, intervention_col2 = st.columns(2)
    
    with intervention_col1:
        st.markdown("**🎯 Targeted Intervention Strategies**")
        render_lottie(
            "https://lottie.host/687a0991-917f-4d7b-92f6-d9ecaa0780b7/D75iWs83gm.json",
            height=280,
            key="intervention_strategies",
            fallback_icon="psychology",
            fallback_text="Evidence-Based Interventions"
        )
        st.caption("Research-proven strategies for supporting diverse learning needs")
    
    with intervention_col2:
        st.markdown("**📊 Data-Driven Assessment**")
        render_lottie(
            "https://lottie.host/8a1c9f65-4b8d-4e2f-9a3c-7f6e5d4c3b2a/M4X8jK9wR5.json",
            height=280,
            key="data_assessment",
            fallback_icon="analytics",
            fallback_text="Progress Monitoring & Assessment"
        )
        st.caption("Continuous monitoring and data-driven decision making for student success")

    # Strategy categories
    strategy_tabs = st.tabs(["📖 Reading Support", "🔢 Math Interventions", "✍️ Writing Help", "🎭 Behavioral Strategies"])
    
    with strategy_tabs[0]:  # Reading Support
        st.markdown("#### Proven Reading Intervention Techniques")
        
        strategies = [
            {
                "title": "Phonemic Awareness Training",
                "description": "Systematic instruction in sound-letter relationships",
                "duration": "15-20 minutes daily",
                "materials": "Letter cards, sound games, word building activities"
            },
            {
                "title": "Guided Reading Groups",
                "description": "Small group instruction with leveled texts",
                "duration": "20-30 minutes, 3x weekly",
                "materials": "Leveled readers, comprehension questions, vocabulary cards"
            },
            {
                "title": "Repeated Reading Practice",
                "description": "Multiple readings of the same text to build fluency",
                "duration": "10-15 minutes daily",
                "materials": "High-interest passages, timing charts, recording sheets"
            }
        ]
        
        for strategy in strategies:
            with st.expander(f"📖 {strategy['title']}"):
                st.markdown(f"**Description:** {strategy['description']}")
                st.markdown(f"**Duration:** {strategy['duration']}")
                st.markdown(f"**Materials:** {strategy['materials']}")
    
    with strategy_tabs[1]:  # Math Interventions
        st.markdown("#### Mathematics Support Strategies")
        
        math_strategies = [
            {
                "title": "Concrete-Representational-Abstract (CRA)",
                "description": "Three-stage approach using manipulatives, pictures, then symbols",
                "duration": "25-30 minutes per lesson",
                "materials": "Math manipulatives, visual models, worksheets"
            },
            {
                "title": "Number Sense Development",
                "description": "Building foundational understanding of numbers and operations",
                "duration": "15-20 minutes daily",
                "materials": "Number lines, counting materials, number games"
            }
        ]
        
        for strategy in math_strategies:
            with st.expander(f"🔢 {strategy['title']}"):
                st.markdown(f"**Description:** {strategy['description']}")
                st.markdown(f"**Duration:** {strategy['duration']}")
                st.markdown(f"**Materials:** {strategy['materials']}")
    
    with strategy_tabs[2]:  # Writing Help
        st.markdown("#### Writing Development Support")
        
        writing_strategies = [
            {
                "title": "Structured Writing Framework",
                "description": "Step-by-step approach to paragraph and essay writing",
                "duration": "30-40 minutes per session",
                "materials": "Graphic organizers, sentence starters, rubrics"
            },
            {
                "title": "Interactive Writing",
                "description": "Collaborative writing with teacher guidance",
                "duration": "20-25 minutes",
                "materials": "Chart paper, markers, editing checklists"
            }
        ]
        
        for strategy in writing_strategies:
            with st.expander(f"✍️ {strategy['title']}"):
                st.markdown(f"**Description:** {strategy['description']}")
                st.markdown(f"**Duration:** {strategy['duration']}")
                st.markdown(f"**Materials:** {strategy['materials']}")
    
    with strategy_tabs[3]:  # Behavioral Strategies
        st.markdown("#### Behavioral Support Techniques")
        
        behavioral_strategies = [
            {
                "title": "Positive Behavior Support",
                "description": "Proactive approach focusing on teaching appropriate behaviors",
                "duration": "Ongoing implementation",
                "materials": "Behavior charts, reward systems, social stories"
            },
            {
                "title": "Self-Regulation Training",
                "description": "Teaching students to monitor and control their own behavior",
                "duration": "15-20 minutes, 2x weekly",
                "materials": "Emotion cards, breathing exercises, reflection journals"
            }
        ]
        
        for strategy in behavioral_strategies:
            with st.expander(f"🎭 {strategy['title']}"):
                st.markdown(f"**Description:** {strategy['description']}")
                st.markdown(f"**Duration:** {strategy['duration']}")
                st.markdown(f"**Materials:** {strategy['materials']}")

    # Progress Monitoring Tools
    st.markdown("---")
    st.markdown("### 📊 Progress Monitoring & Documentation")
    
    monitor_col1, monitor_col2 = st.columns(2)
    
    with monitor_col1:
        st.markdown("#### Weekly Progress Tracker")
        
        tracking_student = st.text_input("Student Name", key="tracking_student")
        tracking_week = st.date_input("Week Starting", key="tracking_week")
        
        # Progress indicators
        academic_progress = st.slider("Academic Progress", 1, 5, 3, key="academic_progress")
        behavioral_progress = st.slider("Behavioral Progress", 1, 5, 3, key="behavioral_progress")
        engagement_level = st.slider("Engagement Level", 1, 5, 3, key="engagement_level")
        
        notes = st.text_area("Weekly Notes", key="weekly_notes", 
                            placeholder="Observations, challenges, successes...")
        
        if st.button("Save Progress Report", key="save_progress"):
            if tracking_student:
                st.success("✅ Progress report saved successfully!")
                
                # Display summary
                st.markdown("**Weekly Summary:**")
                st.markdown(f"- **Student:** {tracking_student}")
                st.markdown(f"- **Week:** {tracking_week}")
                st.markdown(f"- **Academic Progress:** {academic_progress}/5")
                st.markdown(f"- **Behavioral Progress:** {behavioral_progress}/5")
                st.markdown(f"- **Engagement:** {engagement_level}/5")
            else:
                st.warning("Please enter student name")
    
    with monitor_col2:
        st.markdown("#### Resource Library")
        
        st.markdown("""
        **📁 Downloadable Resources:**
        - Intervention planning templates
        - Progress monitoring forms
        - Parent communication templates
        - Student goal-setting worksheets
        
        **🔗 External Links:**
        - Research-based intervention databases
        - Professional development resources
        - Collaboration tools for educators
        """)
        
        if st.button("📥 Download Resource Pack", key="download_resources"):
            st.info("📦 Resource pack would be downloaded in a real implementation")

    # Interactive Learning Activities Generator
    st.markdown("---")
    st.markdown("### 🎮 Interactive Learning Activities Generator")
    
    # Two animations for activity generation section
    activity_anim_col1, activity_anim_col2 = st.columns(2)
    
    with activity_anim_col1:
        st.markdown("**🎲 Activity Generation Engine**")
        render_lottie(
            "https://lottie.host/5940ae0a-4ef4-4f79-a517-abce94639765/H8tXMAPaUk.json",
            height=250,
            key="activity_generator",
            fallback_icon="extension",
            fallback_text="Interactive Activity Ideas"
        )
        st.caption("Generate customized learning activities for any subject and grade level")
    
    with activity_anim_col2:
        st.markdown("**🧩 Adaptive Learning Tools**")
        render_lottie(
            "https://lottie.host/15c1c3e6-35bf-4933-bc7e-193fa1580efe/iwAfN5QwfZ.json",
            height=250,
            key="adaptive_tools",
            fallback_icon="tune",
            fallback_text="Personalized Learning Solutions"
        )
        st.caption("Adaptive tools and resources that adjust to individual student learning needs")

    activity_col1, activity_col2 = st.columns(2)
    
    with activity_col1:
        difficulty_type_act = st.selectbox("Select area of focus:",
                                         ["reading", "math", "writing", "behavior"], 
                                         key="act_difficulty_type")
        grade_level_act = st.selectbox("Select grade level:",
                                     ["K", "1", "2", "3", "4", "5", "6", "7", "8"], 
                                     key="act_grade_level")
    
    with activity_col2:
        group_size_act = st.selectbox("Group size:",
                                     ["Individual", "Small Group (2-4)", "Large Group (5+)", "Whole Class"], 
                                     key="act_group_size")
        time_available_act = st.selectbox("Time available:",
                                         ["5-10 minutes", "15-20 minutes", "30+ minutes", "Full lesson"], 
                                         key="act_time_available")

    if st.button("🎯 Generate Custom Activity", key="gen_act_btn", type="primary"):
        activity = generate_activity(difficulty_type_act, grade_level_act)
        
        st.markdown("### 🎉 Generated Activity")
        st.info(f"**Activity**: {activity}")
        
        # Customize materials and objectives based on activity type
        materials = ["Whiteboard", "Markers", "Flashcards", "Worksheets"]
        objectives = ["Skill practice", "Concept reinforcement"]
        
        if difficulty_type_act == "reading":
            materials = ["Leveled books", "Graphic organizers", "Vocabulary cards", "Audio recordings"]
            objectives = ["Improve decoding skills", "Enhance comprehension", "Build vocabulary", "Increase fluency"]
        elif difficulty_type_act == "math":
            materials = ["Manipulatives", "Calculator", "Graph paper", "Visual aids"]
            objectives = ["Build number sense", "Improve problem-solving", "Practice facts", "Understand concepts"]
        elif difficulty_type_act == "writing":
            materials = ["Graphic organizers", "Word banks", "Sentence frames", "Editing checklists"]
            objectives = ["Improve organization", "Build vocabulary", "Practice mechanics", "Enhance creativity"]
        elif difficulty_type_act == "behavior":
            materials = ["Visual cues", "Timer", "Reward system", "Calm down area"]
            objectives = ["Self-regulation", "Social skills", "Focus attention", "Follow directions"]

        col_mat, col_obj = st.columns(2)
        with col_mat:
            st.markdown("**📋 Materials Needed:**")
            for material in materials:
                st.write(f"• {material}")
        with col_obj:
            st.markdown("**🎯 Learning Objectives:**")
            for obj in objectives:
                st.write(f"• {obj}")

    # Help and Support
    st.markdown("---")
    st.markdown("""
    ### 💡 Need Additional Support?
    
    **Contact Information:**
    - 📧 Email: support@eduscan.edu
    - 📞 Phone: (555) 123-4567
    - 💬 Chat: Available 8 AM - 5 PM
    
    **Training Resources:**
    - Weekly webinars on intervention strategies
    - Professional learning communities
    - Implementation guides and tutorials
    """)

if __name__ == "__main__":
    main()