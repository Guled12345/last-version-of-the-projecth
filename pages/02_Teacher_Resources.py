# pages/02_Teacher_Resources.py
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

from utils.image_base64 import get_base64_images # Only need this for the image dict
from utils.language_utils import get_text, load_app_settings, save_app_settings

# Corrected: All UI functions now imported from utils.exact_ui
from utils.exact_ui import (
    add_exact_ui_styles,
    render_exact_sidebar,
    render_exact_page_header,
    create_exact_metric_card,
    create_exact_chart_container,
    get_b64_image_html
)
from utils.auth_utils import is_authenticated, render_login_page, logout_user, get_user_role
from utils.icon_utils import ( # Import for specific Material Icons in content
    get_material_icon_html, get_lightbulb_icon, get_rocket_icon, get_puzzle_icon, get_brain_icon,
    get_ruler_icon, get_gamepad_icon, get_book_icon, get_laptop_icon, get_handshake_icon,
    get_school_icon
)

# IMPORTANT: Page config MUST be the first Streamlit command for this page
st.set_page_config(
    page_title="EduScan Teacher Resources",
    page_icon=get_material_icon_html("school"), # Replaced emoji with Material Icon HTML
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
    # Authentication check for the page
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
        
    # Render main app header with dynamic content
    st.markdown(f'<div class="section-animated-text">', unsafe_allow_html=True)
    render_exact_page_header(get_material_icon_html('school'), 'teacher_resources', 'empowering_teachers', language)
    st.markdown(f'</div>', unsafe_allow_html=True)
    
    # Enhanced header for teacher resources
    
    # Teacher showcase section with Lottie animation
    st.markdown(f"""
    <div class="resource-section">
    </div>
    """, unsafe_allow_html=True)
    
    # Single centered Lottie animation
    col_center1, col_center2, col_center3 = st.columns([1, 2, 1])
    
    with col_center2:
        if LOTTIE_AVAILABLE:
            # Teacher collaboration animation
            collaboration_url = "https://lottie.host/9dbf9a0f-b1fd-4b92-8215-e595745178d6/iFNBmCDQ5Z.json"
            collaboration_json = load_lottie_url(collaboration_url)
            collaboration_json = remove_lottie_background(collaboration_json)
            
            if collaboration_json:
                st.markdown("**Professional Excellence in Education**")
                st_lottie(
                    collaboration_json, 
                    height=250,
                    key="teacher_excellence_animation",
                    speed=1,
                    loop=True,
                    quality="high",
                    # renderer="canvas"
                )
                st.markdown("Empowering teachers with research-based strategies and collaborative support systems for student success")

    # Resource categories - improved styling
    st.markdown(f"<h2 style='font-size:1.75rem; font-weight:700; color:var(--gray-900); margin-bottom:1.5rem; text-align:center;'>{get_material_icon_html('category', 'outlined')} {get_text('resource_categories', language)}</h2>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs([get_text('teaching_strategies', language), get_text('learning_activities', language), get_text('assessment_tools', language)])
    
    with tab1:
        st.subheader(f"🎯 {get_text('differentiated_learning_strategies', language)}")
        
        difficulty_level = st.selectbox(get_text('target_difficulty', language), 
                                         ["Beginner", "Intermediate", "Advanced"], key="res_diff_lvl_teacher_page")
        subject_area = st.selectbox(get_text('subject_area', language), 
                                     ["Mathematics", "Language Arts", "Science", "Social Studies"], key="res_subj_area_teacher_page")
        
        if st.button(get_text('generate_teaching_strategy', language), key="gen_strat_btn_teacher_page"):
            strategies = {
                "Mathematics": [
                    "Use visual aids and manipulatives for concrete learning",
                    "Implement peer tutoring and collaborative problem solving",
                    "Break complex problems into smaller, manageable steps",
                    "Use real-world applications to make math relevant"
                ],
                "Language Arts": [
                    "Implement guided reading with level-appropriate texts",
                    "Use graphic organizers for writing structure",
                    "Encourage creative storytelling and expression",
                    "Practice phonics through interactive games"
                ],
                "Science": [
                    "Conduct hands-on experiments and demonstrations",
                    "Use scientific method for structured learning",
                    "Integrate technology for virtual lab experiences",
                    "Connect science concepts to everyday life"
                ],
                "Social Studies": [
                    "Use maps and timelines for visual learning",
                    "Implement role-playing historical scenarios",
                    "Encourage cultural exchange and discussion",
                    "Connect historical events to current events"
                ]
            }
            
            if subject_area in strategies:
                st.markdown( # Replaced st.success with st.markdown
                    f"<div style='background-color: #d4edda; color: #155724; padding: 1em; border-radius: 0.5em;'>"
                    f"{get_material_icon_html('check_circle')} {get_text('strategy_generated', language)}"
                    f"</div>",
                    unsafe_allow_html=True
                )
                for i, strategy in enumerate(strategies[subject_area][:3], 1):
                    st.write(f"• {strategy}")
            else:
                st.info(f"{get_material_icon_html('info')} No specific strategies found for this subject. Please select a different one.", unsafe_allow_html=True)
        
        st.markdown("""
        #### **Universal Design for Learning (UDL) Principles:**
        
        **Multiple Means of Representation**
        - Present information in various formats (visual, auditory, hands-on)
        - Use multimedia resources
        - Provide background knowledge activation
        - Offer multiple examples and non-examples
        
        **⚡ Multiple Means of Engagement**
        - Offer choices in topics, tools, and learning environment
        - Connect to student interests and cultural backgrounds
        - Provide appropriate challenges for all learners
        - Foster collaboration and community
        
        **🛠️ Multiple Means of Expression**
        - Allow various ways to demonstrate knowledge
        - Provide options for physical action and movement
        - Support planning and strategy development
        - Use assistive technologies as needed
        """)

        # Inclusive Classroom Tips
        st.markdown(f"### {get_material_icon_html('lightbulb')} {get_text('inclusive_classroom_tips', language)}", unsafe_allow_html=True)
        st.markdown("""
        **🌈 Creating an Inclusive Environment**
        - Flexible seating options (standing desks, stability balls, quiet corners)
        - Clear visual schedules and expectations posted
        - Sensory-friendly spaces for breaks
        - Well-organized materials with visual labels
        - Adequate lighting and minimal distractions
        
        **🤝 Collaboration Strategies**
        - Regular co-planning sessions with special education teachers
        - Consistent communication with parents about student progress
        - Joint problem-solving for challenges
        """)
        
        with st.expander("Daily Inclusive Practices Checklist"):
            st.markdown("""
            - [ ] Provided multiple ways to access content today?
            - [ ] Offered choices in how students demonstrated learning?
            - [ ] Checked in with students who needed extra support?
            - [ ] Celebrated diverse contributions and perspectives?
            """)

    with tab2: # Learning Activities Tab
        st.subheader(f"🎮 {get_text('interactive_learning_activities', language)}")
        
        difficulty_type_act = st.selectbox("Select area of difficulty for activity:",
                                             ["reading", "math", "writing", "behavior"], key="act_difficulty_type_teacher_page_tab2")
        grade_level_act = st.selectbox("Select grade level for activity:",
                                         ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], key="act_grade_level_teacher_page_tab2")
        group_size_act = st.selectbox("Group size for activity:",
                                         ["Individual", "Small Group (2-4)", "Large Group (5+)", "Whole Class"], key="act_group_size_teacher_page_tab2")
        time_available_act = st.selectbox("Time available for activity:",
                                             ["5-10 minutes", "15-20 minutes", "30+ minutes", "Full lesson"], key="act_time_available_teacher_page_tab2")

        if st.button(get_text('generate_activity_ideas', language), key="gen_act_btn_teacher_page_tab2_unique"):
            activity = generate_activity(difficulty_type_act, grade_level_act)
            
            st.markdown("### Generated Activity")
            st.info(f"**Activity**: {activity}")
            
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
                st.markdown("**Materials Needed:**")
                for material in materials:
                    st.write(f"- {material}")
            with col_obj:
                st.markdown("**Learning Objectives:**")
                for obj in objectives:
                    st.write(f"- {obj}")

            st.markdown("### Adaptation Suggestions")
            adaptations = {
                "Individual": "Provide one-on-one support and immediate feedback.",
                "Small Group (2-4)": "Encourage peer collaboration and shared learning.",
                "Large Group (5+)": "Use cooperative learning structures and assign clear roles.",
                "Whole Class": "Implement universal supports and offer multiple participation pathways."
            }
            time_adaptations = {
                "5-10 minutes": "Focus on a single specific skill or concept with quick, targeted practice.",
                "15-20 minutes": "Include brief instruction, guided practice, and a quick reflection.",
                "30+ minutes": "Allow for deeper exploration, modeling, guided practice, and independent application.",
                "Full lesson": "Design a complete learning cycle from introduction to assessment and extension."
            }
            st.write(f"**Group Adaptation**: {adaptations.get(group_size_act, 'General adaptation applies.')}")
            st.write(f"**Time Adaptation**: {time_adaptations.get(time_available_act, 'General adaptation applies.')}")

    with tab3: # Assessment Tools Tab
        st.subheader(f"📝 {get_text('assessment_tools', language)}")
        
        assessment_type = st.selectbox(get_text('assessment_type', language), 
                                         ["Formative", "Summative", "Diagnostic"], key="assess_type_select_teacher_page_tab3")
        
        if st.button(get_text('create_assessment', language), key="create_assess_btn_teacher_page_tab3_unique"):
            st.markdown( # Replaced st.success with st.markdown
                f"<div style='background-color: #d4edda; color: #155724; padding: 1em; border-radius: 0.5em;'>"
                f"{get_material_icon_html('assignment_add')} {get_text('assessment_template_created', language)}"
                f"</div>",
                unsafe_allow_html=True
            )
            st.write(f"• {get_text('clear_learning_objectives', language)}")
            st.write(f"• {get_text('multiple_question_formats', language)}")
            st.write(f"• {get_text('rubric_provided', language)}")
            st.write(f"• {get_text('differentiated_difficulty', language)}")

        # Intervention Techniques Section
        st.markdown("---")
        st.subheader("Intervention Techniques")
        intervention_area_main = st.selectbox(
            "Select intervention focus:",
            ["Reading Interventions", "Math Interventions", "Behavioral Interventions", "Executive Function Support"],
            key="intervention_area_main_teacher_page"
        )
        
        if intervention_area_main == "Reading Interventions":
            st.markdown("""
            #### **Systematic Phonics Interventions**
            - **Orton-Gillingham Approach**: Multi-sensory phonics instruction
            - **Wilson Reading System**: Structured literacy program
            - **REWARDS**: Reading strategies for older students
            - **Duration**: 30-45 minutes daily, 12-16 weeks minimum
            
            #### **Fluency Interventions**
            - **Repeated Reading**: Practice with the same text multiple times
            - **Paired Reading**: Student and tutor read together
            - **Reader's Theater**: Performance-based fluency practice
            - **Goal**: Increase words per minute and expression
            
            #### **Comprehension Interventions**
            - **Reciprocal Teaching**: Students take turns leading discussions
            - **Graphic Organizers**: Visual supports for understanding
            - **Question-Answer Relationships**: Teaching question types
            - **Think-Alouds**: Modeling comprehension strategies
            """)
            
            # Interactive intervention tracker
            st.markdown(f"#### {get_material_icon_html('track_changes')} Intervention Progress Tracker", unsafe_allow_html=True)
            
            with st.form("reading_intervention_form_teacher_page"):
                student_name_track = st.text_input("Student Name", key="read_int_student_name")
                intervention_type_track = st.selectbox("Intervention Type", 
                    ["Phonics", "Fluency", "Comprehension", "Vocabulary"], key="read_int_type")
                baseline_score_track = st.number_input("Baseline Score", min_value=0, max_value=100, key="read_int_baseline")
                current_score_track = st.number_input("Current Score", min_value=0, max_value=100, key="read_int_current")
                weeks_elapsed_track = st.number_input("Weeks of Intervention", min_value=1, max_value=52, key="read_int_weeks")
                notes_track = st.text_area("Progress Notes", key="read_int_notes")
                
                if st.form_submit_button("Track Progress"):
                    progress = current_score_track - baseline_score_track
                    rate = progress / weeks_elapsed_track if weeks_elapsed_track > 0 else 0
                    
                    st.markdown( # Replaced st.success with st.markdown
                        f"<div style='background-color: #d4edda; color: #155724; padding: 1em; border-radius: 0.5em;'>"
                        f"{get_material_icon_html('check_circle')} Progress tracked for {student_name_track}"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    st.metric("Score Improvement", f"{progress} points", f"{rate:.1f} pts/week")
        
        elif intervention_area_main == "Math Interventions":
            st.markdown("""
            #### **Number Sense Interventions**
            - **Number Worlds**: Comprehensive number sense program
            - **TouchMath**: Multi-sensory approach to basic facts
            - **Number Line Activities**: Visual representation of number relationships
            - **Subitizing Practice**: Quick recognition of small quantities
            
            #### **Fact Fluency Interventions**
            - **Math Facts in a Flash**: Systematic fact practice
            - **Rocket Math**: Timed practice with progression
            - **Computer-Based Programs**: Adaptive fact practice
            - **Goal**: Automatic recall of basic facts
            
            #### **Problem-Solving Interventions**
            - **Schema-Based Instruction**: Teaching problem types
            - **Concrete-Representational-Abstract**: Gradual release model
            - **Math Talk**: Verbalization of thinking processes
            - **Error Analysis**: Learning from mistakes
            """)
        
        elif intervention_area_main == "Behavioral Interventions":
            st.markdown("""
            #### **Positive Behavior Interventions and Supports (PBIS)**
            - **Tier 1**: Universal classroom management
            - **Tier 2**: Targeted group interventions
            - **Tier 3**: Intensive individual supports
            - **Focus**: Prevention and positive reinforcement
            
            #### **Self-Regulation Strategies**
            - **Zones of Regulation**: Emotional awareness and control
            - **Mindfulness Practices**: Breathing and centering techniques
            - **Break Cards**: Self-advocacy for regulation needs
            - **Goal Setting**: Student-directed behavior goals
            
            #### **Social Skills Interventions**
            - **Social Stories**: Narrative-based skill instruction
            - **Role Playing**: Practice in safe environments
            - **Peer Mediation**: Student-led conflict resolution
            - **Circle Time**: Community building and problem-solving
            """)
        
        else:  # Executive Function Support
            st.markdown("""
            #### **Organization Strategies**
            - **Color-Coding Systems**: Different subjects, different colors
            - **Checklists and Templates**: Step-by-step guidance
            - **Digital Organization Tools**: Apps and platforms
            - **Clean Desk Policy**: Minimize distractions
            
            #### **Time Management Support**
            - **Visual Schedules**: Picture or text-based daily schedules
            - **Timer Use**: Breaking tasks into manageable chunks
            - **Transition Warnings**: 5-minute, 2-minute notices
            - **Priority Ranking**: Teaching importance vs. urgency
            
            #### **Working Memory Support**
            - **Chunking Information**: Breaking into smaller parts
            - **Rehearsal Strategies**: Repetition and practice
            - **External Memory Aids**: Notes, recordings, visuals
            - **Reduce Cognitive Load**: Simplify instructions
            """)
    
    # Footer with quick links
    st.markdown("---")
    st.markdown(f"### {get_material_icon_html('quick_reference')} Quick Resources", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Reading Strategies", use_container_width=True, key="quick_link_reading_teacher_page_footer"):
            st.info("Comprehensive reading support strategies loaded above!")
    
    with col2:
        if st.button("Math Support", use_container_width=True, key="quick_link_math_teacher_page_footer"):
            st.info("Mathematics intervention techniques displayed above!")
    
    with col3:
        if st.button("Writing Help", use_container_width=True, key="quick_link_writing_teacher_page_footer"):
            st.info("Writing differentiation strategies shown above!")
    
    with col4: # Wrapped in a column to maintain grid structure, even if it's the last one
        if st.button("Behavior Tips", use_container_width=True, key="quick_link_behavior_teacher_page_footer"):
            st.info("Behavioral intervention strategies provided above!")

if __name__ == "__main__":
    main()