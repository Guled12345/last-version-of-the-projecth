# pages/04_Educational_Content.py - Enhanced with Material Icons

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys
import os

# Enhanced Lottie import
try:
    from streamlit_lottie import st_lottie
    import requests
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

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
    page_title="EduScan Educational Content",
    page_icon="📚",
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

def main():
    # Authentication check
    if not is_authenticated():
        st.warning("Please log in to access Educational Content.")
        st.switch_page("app.py")
        return

    # Header
    render_exact_page_header(
        get_material_icon_html('menu_book'), 
        'Educational Content', 
        'Curated Learning Materials for Student Success', 
        language
    )
    
    # Enhanced hero section with multiple animations
    st.markdown(f"### {get_material_icon_html('star')} Educational Excellence in Action", unsafe_allow_html=True)
    
    # Three-column animation layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**{get_material_icon_html('library_books')} Learning Excellence**", unsafe_allow_html=True)
        render_lottie(
            "https://lottie.host/5940ae0a-4ef4-4f79-a517-abce94639765/H8tXMAPaUK.json",
            height=200,
            key="learning_excellence_edu",
            fallback_icon="school",
            fallback_text="Evidence-based strategies"
        )
        st.caption("Research-based educational strategies and methodologies")
    
    with col2:
        st.markdown(f"**{get_material_icon_html('science')} Research Innovation**", unsafe_allow_html=True)
        render_lottie(
            "https://lottie.host/687a0991-917f-4d7b-92f6-d9ecaa0780b7/D75iWs83gn.json",
            height=200,
            key="research_innovation_edu",
            fallback_icon="science",
            fallback_text="Cutting-edge research"
        )
        st.caption("Cutting-edge educational research and development")
    
    with col3:
        st.markdown(f"**{get_material_icon_html('target')} Student Success**", unsafe_allow_html=True)
        render_lottie(
            "https://lottie.host/4e1ac443-9c90-4a25-b20d-c918d5a0290f/pa2Qd9xE5l.json",
            height=200,
            key="student_success_edu",
            fallback_icon="emoji_events",
            fallback_text="Student achievements"
        )
        st.caption("Empowering every learner to reach their potential")

    # Enhanced educational impact showcase
    st.markdown("---")
    st.markdown(f"### {get_material_icon_html('analytics')} Educational Impact & Research", unsafe_allow_html=True)
    
    impact_col1, impact_col2 = st.columns(2)
    
    with impact_col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
             border-radius: 16px; color: white; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s ease;"
             onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
            <h3>{get_material_icon_html('public')} Global Best Practices</h3>
            <p>International standards and evidence-based approaches for inclusive education</p>
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-top: 1rem;">
                <strong>{get_material_icon_html('analytics')} 150+ Research Studies | {get_material_icon_html('public')} 25+ Countries</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
             border-radius: 16px; color: white; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s ease;"
             onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
            <h3>{get_material_icon_html('analytics')} Intervention Studies</h3>
            <p>Evidence-based intervention strategies with measurable outcomes</p>
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-top: 1rem;">
                <strong>{get_material_icon_html('trending_up')} 85% Success Rate | {get_material_icon_html('groups')} 10,000+ Students</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with impact_col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
             border-radius: 16px; color: white; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s ease;"
             onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
            <h3>{get_material_icon_html('psychology')} Learning Science</h3>
            <p>Neuroscience and cognitive research insights for optimal learning</p>
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-top: 1rem;">
                <strong>{get_material_icon_html('science')} 200+ Studies | {get_material_icon_html('biotech')} 50+ Experiments</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
             border-radius: 16px; color: white; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s ease;"
             onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
            <h3>{get_material_icon_html('handshake')} Cultural Adaptation</h3>
            <p>Implementing inclusive educational practices across diverse communities</p>
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-top: 1rem;">
                <strong>{get_material_icon_html('public')} 40+ Cultures | {get_material_icon_html('library_books')} 100+ Adaptations</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Enhanced content selection
    st.markdown("---")
    st.markdown(f"### {get_material_icon_html('target')} Explore Educational Content", unsafe_allow_html=True)
    
    content_col1, content_col2 = st.columns(2)

    with content_col1:
        content_type = st.selectbox(
            "Content Category",
            [
                "Research Overview",
                "Types of Learning Difficulties", 
                "Early Intervention Strategies",
                "Academic Resources Library",
                "Technology Tools & Platforms",
                "Support Strategies & Best Practices"
            ],
            key="content_category_selector"
        )

    with content_col2:
        audience = st.selectbox(
            "Target Audience",
            [
                "Teachers",
                "Parents",
                "Administrators",
                "All Stakeholders"
            ],
            key="audience_selector"
        )


    # Enhanced content sections
    if content_type == f"Research Overview":
        st.markdown(f"## {get_material_icon_html('analytics')} Research Overview: Learning Difficulties", unsafe_allow_html=True)
        
        # Add research-focused animation
        research_col = st.columns([1, 2, 1])
        with research_col[1]:
            st.markdown(f"**{get_material_icon_html('science')} Data-Driven Research Excellence**", unsafe_allow_html=True)
            render_lottie(
                "https://lottie.host/8a1c9f65-4b8d-4e2f-9a3c-7f6e5d4c3b2a/M4X8jK9wR6.json",
                height=250,
                key="research_data_overview",
                fallback_icon="analytics",
                fallback_text="Comprehensive Research Analysis"
            )
            st.caption("Evidence-based research driving educational innovation")
        
        tab1, tab2, tab3 = st.tabs([f"Statistics", f"Neuroscience", f"Impact Studies"])
        
        with tab1:
            st.markdown("### Learning Difficulties Statistics")
            
            prevalence_data = {
                "Type": ["Dyslexia", "ADHD", "Dyscalculia", "Dysgraphia", "Language Disorders", "Other"],
                "Prevalence (%)": [5.0, 11.0, 3.5, 4.0, 7.0, 2.5],
                "Description": [
                    "Reading and language processing difficulties",
                    "Attention deficit hyperactivity disorder", 
                    "Mathematical learning difficulties",
                    "Writing and fine motor difficulties",
                    "Spoken language comprehension issues",
                    "Other specific learning disabilities"
                ]
            }
            
            fig_prevalence = px.pie(
                prevalence_data, 
                values="Prevalence (%)", 
                names="Type",
                title="Prevalence of Learning Difficulties in School-Age Children",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_prevalence.update_layout(height=500)
            st.plotly_chart(fig_prevalence, use_container_width=True)
            
            # Enhanced metrics display
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Students Affected", "15-20%", "of all students")
            with col2:
                st.metric("Early Identification", "< 30%", "before age 8")
            with col3:
                st.metric("Gender Ratio", "2:1", "Male to Female")
            with col4:
                st.metric("Improvement Rate", "80%", "with intervention")
        
        with tab2:
            st.markdown(f"""
            #### **{get_material_icon_html('psychology')} Brain-Based Understanding of Learning Difficulties**
            
            Learning difficulties are neurobiological in origin, involving differences in brain structure and function:
            
            **{get_material_icon_html('psychology')} Key Brain Areas Affected:**
            
            **1. Left Hemisphere Language Areas**
            - **Broca's Area**: Speech production and grammar processing
            - **Wernicke's Area**: Language comprehension and meaning
            - **Angular Gyrus**: Word recognition and reading integration
            
            **2. Phonological Processing Networks**
            - Difficulty connecting sounds to letters (phoneme-grapheme correspondence)
            - Reduced activation in reading circuits during phonological tasks
            - Compensatory right hemisphere activation in skilled readers with dyslexia
            
            **3. Working Memory Systems**
            - Prefrontal cortex involvement in executive function
            - Information processing speed and capacity limitations
            - Attention and cognitive control challenges
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            #### **{get_material_icon_html('star')} Neuroplasticity and Intervention**
            
            **The Brain's Remarkable Ability to Change:**
            - Intensive, structured intervention can create new neural pathways
            - Earlier intervention leads to greater neuroplastic changes
            - Multi-sensory approaches enhance connectivity between brain regions
            - Consistent practice strengthens and stabilizes new neural networks
            
            **{get_material_icon_html('science')} Research Evidence:**
            - fMRI studies demonstrate measurable brain changes after intensive intervention
            - Increased activation in left hemisphere reading networks post-intervention
            - Improved white matter connectivity between language areas
            - Long-term structural brain changes possible with sustained intervention
            """, unsafe_allow_html=True)
            
            st.markdown(f"#### {get_material_icon_html('schedule')} Critical Intervention Periods", unsafe_allow_html=True)
            
            timeline_data = {
                "Age Range": ["3-5 years", "6-8 years", "9-12 years", "13+ years"],
                "Brain Plasticity": ["Highest", "High", "Moderate", "Lower but significant"],
                "Intervention Impact": ["Maximum potential", "High effectiveness", "Moderate with intensity", "Requires sustained effort"],
                "Key Focus Areas": [
                    "Language development, phonological awareness, pre-literacy skills",
                    "Reading foundation, phonics, basic academic skills",
                    "Reading fluency, comprehension strategies, content learning",
                    "Compensation strategies, assistive technology, self-advocacy"
                ]
            }
            
            timeline_df = pd.DataFrame(timeline_data)
            st.dataframe(timeline_df, use_container_width=True, hide_index=True)
        
        with tab3:
            st.markdown(f"""
            #### **{get_material_icon_html('emoji_events')} Major Research Findings & Evidence**
            
            **National Reading Panel (2000) - Landmark Study**
            - Systematic phonics instruction is essential for beginning readers
            - Phonemic awareness training significantly improves reading outcomes
            - Guided oral reading builds fluency more effectively than silent reading
            - Vocabulary instruction enhances reading comprehension across grades
            
            **{get_material_icon_html('analytics')} Meta-Analysis Studies (Multiple Reviews)**
            - Intensive intervention shows large effect sizes (Cohen's d > 0.8)
            - Early intervention prevents reading failure in 75-85% of at-risk students
            - Multi-component approaches outperform single-strategy interventions
            - Technology tools can enhance but not replace systematic instruction
            """, unsafe_allow_html=True)
            
            intervention_data = {
                "Intervention Type": [
                    "Systematic Phonics",
                    "Reading Fluency Training",
                    "Comprehension Strategies", 
                    "Vocabulary Instruction",
                    "Multi-sensory Approaches",
                    "Technology-Enhanced Learning"
                ],
                "Effect Size": [0.86, 0.71, 0.68, 0.62, 0.75, 0.58],
                "Grade Levels": ["K-3", "2-5", "3-8", "K-8", "K-8", "K-12"],
                "Implementation Time": ["30-45 min daily", "15-20 min daily", "20-30 min", "15-20 min", "45-60 min", "20-40 min"]
            }
            
            fig_effectiveness = px.bar(
                intervention_data,
                x="Effect Size",
                y="Intervention Type",
                orientation='h',
                title="Research-Proven Intervention Effectiveness",
                color="Effect Size",
                color_continuous_scale="Viridis"
            )
            fig_effectiveness.update_layout(height=400)
            st.plotly_chart(fig_effectiveness, use_container_width=True)
            
            st.markdown(f"""
            #### **{get_material_icon_html('trending_up')} Longitudinal Study Insights**
            
            **Connecticut Longitudinal Study (Shaywitz et al.) - 20+ Year Follow-up**
            - Tracked 445 children from kindergarten through high school
            - Reading difficulties persist without targeted intervention
            - Early identification and intervention absolutely crucial for long-term success
            - Brain imaging reveals intervention literally changes neural pathways
            - Self-esteem and academic motivation significantly improve with effective support
            - Students receiving intensive early intervention show normalized brain activation patterns
            """, unsafe_allow_html=True)

    elif content_type == f"Types of Learning Difficulties":
        st.markdown(f"## {get_material_icon_html('extension')} Understanding Different Learning Difficulties", unsafe_allow_html=True)
        
        # Add learning types animation
        types_col = st.columns([1, 2, 1])
        with types_col[1]:
            st.markdown(f"**{get_material_icon_html('extension')} Learning Differences & Strengths**", unsafe_allow_html=True)
            render_lottie(
                "https://lottie.host/15c1c3e6-35bf-4933-bc7e-193fa1580efe/iwAfN5QwfZ.json",
                height=250,
                key="learning_types_overview",
                fallback_icon="psychology",
                fallback_text="Understanding Learning Differences"
            )
            st.caption("Every learner is unique - understanding leads to empowerment")
        
        difficulty_type = st.selectbox(
            "Select learning difficulty to explore:",
            ["Dyslexia", "Dyscalculia", "Dysgraphia", "ADHD", "Language Processing Disorders", "Executive Function Challenges"],
            key="difficulty_type_selector"
        )
        
        if difficulty_type == "Dyslexia":
            st.markdown(f"""
            #### **{get_material_icon_html('menu_book')} Dyslexia: Understanding Reading Challenges**
            
            Dyslexia is a neurobiological learning difference that affects reading and language processing, 
            despite adequate intelligence and educational opportunities.
            
            **{get_material_icon_html('target')} Core Characteristics:**
            - Difficulty with accurate and/or fluent word recognition
            - Challenges with spelling and decoding unfamiliar words
            - Problems with phonological processing (sound-letter connections)
            - Reading comprehension may be affected secondary to decoding difficulties
            - Often accompanied by significant strengths in reasoning, creativity, and big-picture thinking
            
            **{get_material_icon_html('bolt')} Strengths Often Associated with Dyslexia:**
            - Enhanced creative thinking and problem-solving abilities
            - Strong spatial reasoning and 3D visualization skills
            - Excellent big-picture perspective and strategic thinking
            - High levels of empathy and interpersonal skills
            - Innovative approaches to challenges
            """, unsafe_allow_html=True)
            
            st.markdown(f"#### {get_material_icon_html('schedule')} Observable Signs by Developmental Stage", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                **{get_material_icon_html('child_care')} Early Years (Ages 3-5):**
                - Delayed speech development or unclear speech
                - Difficulty learning nursery rhymes or rhyming games
                - Problems learning alphabet letters and sounds
                - Trouble following multi-step directions
                - Family history of reading or learning difficulties
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                **{get_material_icon_html('library_books')} Elementary (Ages 6-8):**
                - Slow progress in learning to read
                - Difficulty sounding out words or blending sounds
                - Confusing similar-looking words (was/saw, on/no)
                - Avoiding reading activities or expressing reading anxiety
                - Strong listening comprehension vs. reading comprehension gap
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                **{get_material_icon_html('school')} Older Students (Ages 9+):**
                - Reading significantly below grade level expectations
                - Difficulty with reading comprehension of complex texts
                - Poor spelling despite extensive instruction and practice
                - Avoiding written assignments or taking much longer to complete
                - Fatigue after reading for short periods
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            #### **{get_material_icon_html('psychology')} Neurological Understanding**
            - Differences in left hemisphere language processing areas
            - Reduced connectivity in reading-specific neural networks
            - Phonological processing deficits at the neurological level
            - Working memory challenges affecting reading fluency
            - Often compensated by enhanced right-hemisphere processing
            
            #### **{get_material_icon_html('build')} Evidence-Based Interventions**
            - **Structured Literacy Approaches**: Systematic, explicit instruction in phonology, morphology, and syntax
            - **Multi-sensory Programs**: Orton-Gillingham, Wilson Reading System, Barton Reading & Spelling
            - **Assistive Technology**: Text-to-speech, speech-to-text, audiobooks, reading apps
            - **Accommodations**: Extended time, alternative formats, reduced reading load
            - **Strength-Based Learning**: Leveraging visual, spatial, and creative abilities
            """, unsafe_allow_html=True)
        
        elif difficulty_type == "Dyscalculia":
            st.markdown(f"""
            #### **{get_material_icon_html('calculate')} Dyscalculia: Mathematical Learning Challenges**
            
            Dyscalculia is a specific learning difficulty that affects mathematical understanding, 
            number sense, and mathematical reasoning abilities.
            
            **{get_material_icon_html('target')} Core Characteristics:**
            - Difficulty understanding number concepts and relationships
            - Problems with mathematical reasoning and problem-solving
            - Challenges with calculation, computation, and math facts
            - Difficulty understanding mathematical symbols and operations
            - Trouble with time, money, and measurement concepts
            """, unsafe_allow_html=True)
            
            st.markdown(f"#### {get_material_icon_html('analytics')} Common Areas of Difficulty", unsafe_allow_html=True)
            
            manifestations = {
                "Mathematical Area": [
                    "Number Sense & Quantity",
                    "Calculation & Computation",
                    "Mathematical Problem Solving",
                    "Mathematical Reasoning"
                ],
                "Specific Difficulties": [
                    "Understanding quantity, comparing numbers, number line concepts, subitizing",
                    "Basic arithmetic facts, multi-step calculations, algorithms, mental math",
                    "Word problems, mathematical language, applying concepts to real situations",
                    "Patterns, relationships, abstract mathematical thinking, logical sequences"
                ],
                "Effective Support Strategies": [
                    "Visual number representations, manipulatives, number lines, counting tools",
                    "Breaking down steps, providing algorithms, allowing calculators, visual aids",
                    "Graphic organizers, keyword strategies, real-world connections, collaborative solving",
                    "Concrete examples, visual models, step-by-step instruction, pattern games"
                ],
                "Assistive Technologies": [
                    "Virtual manipulatives, number line apps, visual math tools",
                    "Calculator apps, math fact practice programs, step-by-step solvers",
                    "Problem-solving apps, graphic organizer tools, math journals",
                    "Pattern recognition software, logic games, visual reasoning tools"
                ]
            }
            
            manifestations_df = pd.DataFrame(manifestations)
            st.dataframe(manifestations_df, use_container_width=True, hide_index=True)
            
            st.markdown(f"""
            #### **{get_material_icon_html('lightbulb')} Strengths Often Present:**
            - Strong language and verbal reasoning abilities
            - Excellent memory for stories, facts, and information
            - Creative problem-solving in non-mathematical areas
            - Strong social and interpersonal skills
            """, unsafe_allow_html=True)

    elif content_type == f"Early Intervention Strategies":
        st.markdown(f"## {get_material_icon_html('rocket_launch')} Early Intervention: The Foundation of Success", unsafe_allow_html=True)
        
        # Add early intervention animation
        early_col = st.columns([1, 2, 1])
        with early_col[1]:
            st.markdown(f"**{get_material_icon_html('eco')} Early Intervention Excellence**", unsafe_allow_html=True)
            render_lottie(
                "https://lottie.host/4d42d6a6-8290-4b13-b3ab-2a10a490e6db/9oJrI4pj1f.json",
                height=250,
                key="early_intervention_focus",
                fallback_icon="child_care",
                fallback_text="Building Strong Foundations"
            )
            st.caption("The earlier the intervention, the greater the impact on learning outcomes")
        
        intervention_focus = st.selectbox(
            f"Select intervention focus area:",
            ["Pre-Reading & Literacy Foundations", "Early Mathematical Concepts", "Language Development", "Social-Emotional Learning"],
            key="intervention_focus_selector"
        )
        
        if intervention_focus == "Pre-Reading & Literacy Foundations":
            st.markdown(f"""
            #### **{get_material_icon_html('library_books')} Building Essential Pre-Reading Skills**
            
            **{get_material_icon_html('key')} Core Foundation: Phonological Awareness**
            Early phonological awareness is the strongest predictor of later reading success and can be developed 
            before formal reading instruction begins.
            
            **Why It Matters:**
            - Children who struggle with phonological awareness are at high risk for reading difficulties
            - These skills can be taught and improved with targeted practice
            - Early intervention in this area prevents later reading failure in 75-85% of at-risk children
            """, unsafe_allow_html=True)
            
            # Enhanced phonological awareness progression
            progression_data = {
                "Developmental Level": [
                    f"Word Awareness",
                    f"Syllable Awareness", 
                    f"Onset-Rime Recognition",
                    f"Phoneme Awareness"
                ],
                "Typical Age Range": ["3-4 years", "4-5 years", "5-6 years", "6-7 years"],
                "Key Skills & Activities": [
                    "Counting words in sentences, recognizing word boundaries, word games",
                    "Clapping syllables, syllable deletion/addition, rhythm activities",
                    "Recognizing rhymes, identifying word families, rhyming games",
                    "Sound isolation, blending, segmentation, manipulation activities"
                ],
                "Assessment Indicators": [
                    "Can identify and count separate words in spoken sentences",
                    "Can clap and count syllables accurately in multisyllabic words",
                    "Can identify rhyming words and generate rhymes independently",
                    "Can isolate, blend, and manipulate individual sounds in words"
                ],
                "Red Flags for Intervention": [
                    "Cannot identify words as separate units by age 4",
                    "Difficulty with syllable awareness by kindergarten entry",
                    "No rhyming ability by age 5-6",
                    "Cannot blend or segment sounds by end of kindergarten"
                ]
            }
            
            progression_df = pd.DataFrame(progression_data)
            st.dataframe(progression_df, use_container_width=True, hide_index=True)
            
            st.markdown(f"""
            #### **{get_material_icon_html('games')} Effective Pre-Reading Activities by Category**
            
            **{get_material_icon_html('music_note')} Phonological Awareness Games:**
            - **Sound Scavenger Hunts**: Find objects that start with target sounds
            - **Rhyme Time**: Daily rhyming songs, poems, and word play
            - **Syllable Clapping**: Rhythmic activities with names, words, and songs
            - **Sound Substitution Games**: Change beginning sounds to make new words
            - **Listening Games**: Identify and discriminate environmental and speech sounds
            
            **{get_material_icon_html('menu_book')} Print Awareness Activities:**
            - **Environmental Print Exploration**: Road signs, food labels, store names
            - **Book Handling Skills**: Proper orientation, page turning, print direction
            - **Letter Recognition Games**: Alphabet songs, letter hunts, tactile letters
            - **Name Writing Practice**: Starting with child's own name as meaningful text
            - **Print-Rich Environment**: Labels, charts, and books throughout the space
            
            **{get_material_icon_html('edit')} Early Writing Development:**
            - **Scribbling and Drawing**: Developing fine motor control and print concepts
            - **Letter Formation Practice**: Multi-sensory approaches to letter shapes
            - **Story Dictation**: Child tells stories while adult writes them down
            - **Interactive Writing**: Shared writing experiences with adult support
            """, unsafe_allow_html=True)

    elif content_type == f"Academic Resources Library":
        st.markdown(f"## {get_material_icon_html('library_books')} Comprehensive Academic Resource Library", unsafe_allow_html=True)
        
        # Add academic resources animation
        resources_col = st.columns([1, 2, 1])
        with resources_col[1]:
            st.markdown(f"**{get_material_icon_html('library_books')} Evidence-Based Resource Collection**", unsafe_allow_html=True)
            render_lottie(
                "https://lottie.host/687a0991-917f-4d7b-92f6-d9ecaa0780b7/D75iWs83gn.json",
                height=250,
                key="academic_resources_focus",
                fallback_icon="library_books",
                fallback_text="Comprehensive Resource Library"
            )
            st.caption("Curated collection of research-based educational materials and tools")
        
        resource_category = st.selectbox(
            f"Select resource category:",
            [f"Research Articles & Studies", f"Best Practice Implementation Guides", f"Intervention Programs & Curricula", f"Assessment Tools & Instruments"],
            key="academic_resource_category_selector"
        )
        
        if resource_category == f"{get_material_icon_html('article')} Research Articles & Studies":
            st.markdown(f"### {get_material_icon_html('science')} Essential Research Articles & Studies", unsafe_allow_html=True)
            
            articles = [
                {
                    "Title": "The Science of Reading: A Handbook",
                    "Author": "Snowling, M. J. & Hulme, C.",
                    "Year": "2021",
                    "Key Findings": "Comprehensive review of reading research, emphasizing structured literacy approaches and multi-tiered intervention systems",
                    "Relevance": "Essential for understanding current evidence-based reading instruction methodologies",
                    "Citation": "Snowling, M. J., & Hulme, C. (2021). The science of reading: A handbook. Wiley-Blackwell.",
                    "Impact Factor": "High",
                    "Access": "University libraries, academic databases"
                },
                {
                    "Title": "Preventing Reading Difficulties in Young Children",
                    "Author": "Snow, C. E., Burns, M. S., & Griffin, P.",
                    "Year": "1998",
                    "Key Findings": "Identifies key predictors of reading success and failure; emphasizes critical importance of early intervention",
                    "Relevance": "Foundational text for early literacy intervention and prevention programs",
                    "Citation": "Snow, C. E., Burns, M. S., & Griffin, P. (1998). Preventing reading difficulties in young children. National Academy Press.",
                    "Impact Factor": "Foundational",
                    "Access": "Free PDF available from National Academy Press"
                },
                {
                    "Title": "Mathematical Learning Disabilities: Current Issues and Future Directions",
                    "Author": "Gersten, R. & Chard, D.",
                    "Year": "2019",
                    "Key Findings": "Comprehensive review of effective interventions for mathematical learning difficulties and dyscalculia",
                    "Relevance": "Current guidelines for math intervention design and implementation",
                    "Citation": "Gersten, R., & Chard, D. (2019). Mathematical learning disabilities. Journal of Learning Disabilities, 52(3), 123-145.",
                    "Impact Factor": "High",
                    "Access": "Academic journals, research databases"
                },
                {
                    "Title": "Executive Function and Self-Regulation Skills: Building the Foundation for Academic Success",
                    "Author": "Diamond, A. & Lee, K.",
                    "Year": "2020",
                    "Key Findings": "Demonstrates how executive function skills impact academic achievement and can be improved through targeted interventions",
                    "Relevance": "Critical for understanding cognitive foundations of learning and developing executive function interventions",
                    "Citation": "Diamond, A., & Lee, K. (2020). Executive function and self-regulation. Annual Review of Psychology, 71, 487-518.",
                    "Impact Factor": "Very High",
                    "Access": "Psychology journals, university databases"
                }
            ]
            
            for article in articles:
                with st.expander(f"{article['Title']} ({article['Year']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Authors:** {article['Author']}")
                        st.write(f"**Publication Year:** {article['Year']}")
                        st.write(f"**Impact Level:** {article['Impact Factor']}")
                        st.write(f"**Access:** {article['Access']}")
                    
                    with col2:
                        st.write(f"**Key Findings:** {article['Key Findings']}")
                        st.write(f"**Relevance to Practice:** {article['Relevance']}")
                    
                    st.write(f"**Full Citation:** {article['Citation']}")

    elif content_type == f"Technology Tools & Platforms":
        st.markdown(f"## {get_material_icon_html('computer')} Technology Tools for Learning Support", unsafe_allow_html=True)
        
        # Add technology tools animation
        tech_col = st.columns([1, 2, 1])
        with tech_col[1]:
            st.markdown(f"**{get_material_icon_html('computer')} Educational Technology Solutions**", unsafe_allow_html=True)
            render_lottie(
                "https://lottie.host/5940ae0a-4ef4-4f79-a517-abce94639765/H8tXMAPaUk.json",
                height=250,
                key="tech_tools_focus",
                fallback_icon="computer",
                fallback_text="Innovative Learning Technologies"
            )
            st.caption("Cutting-edge tools to enhance learning and accessibility")
        
            tool_category = st.selectbox(
                "Select technology category:",
                [
                    "Reading Support Tools",
                    "Writing Assistance Software",
                    "Mathematics Applications",
                    "Organization & Executive Function Apps",
                    "Communication & Language Tools"
                ],
                key="tool_category_selector"
            )

        
        if tool_category == f"{get_material_icon_html('menu_book')} Reading Support Tools":
            st.markdown(f"#### {get_material_icon_html('menu_book')} Advanced Reading Support Technologies", unsafe_allow_html=True)
            
            reading_tools = [
                {
                    "Tool": "Text-to-Speech Software",
                    "Examples": "NaturalReader, Voice Dream Reader, Read&Write Gold, Immersive Reader",
                    "Benefits": "Supports decoding difficulties, improves comprehension, provides access to grade-level content",
                    "Implementation": "Start with familiar texts, teach interface controls, gradually increase complexity, daily practice sessions",
                    "Cost": "Free to $200/year",
                    "Platforms": "Windows, Mac, iOS, Android, Web browsers"
                },
                {
                    "Tool": "Digital Annotation & Highlighting Tools",
                    "Examples": "Kami, Hypothesis, Adobe Acrobat Reader, Microsoft OneNote",
                    "Benefits": "Enhances active reading, supports note-taking, improves text organization and comprehension",
                    "Implementation": "Teach color-coding systems, practice with short passages, integrate with assignments",
                    "Cost": "Free to $50/year",
                    "Platforms": "Cross-platform compatibility"
                },
                {
                    "Tool": "Adaptive Reading Comprehension Platforms",
                    "Examples": "Epic!, Reading A-Z, Lexia Core5, Reading Plus, NewsELA",
                    "Benefits": "Personalized practice, immediate feedback, progress tracking, engaging multimedia content",
                    "Implementation": "Set appropriate reading levels, monitor progress weekly, supplement classroom instruction",
                    "Cost": "$100-500/year per student",
                    "Platforms": "Web-based, tablet applications"
                },
                {
                    "Tool": "Audiobook and Digital Library Access",
                    "Examples": "Audible, Learning Ally, Bookshare, OverDrive, Hoopla",
                    "Benefits": "Access to literature, vocabulary development, comprehension through listening",
                    "Implementation": "Pair with physical books, use for research projects, encourage independent exploration",
                    "Cost": "Free (libraries) to $15/month",
                    "Platforms": "Mobile apps, web browsers, dedicated devices"
                }
            ]
            
            for tool in reading_tools:
                with st.expander(f"{tool['Tool']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Popular Examples:** {tool['Examples']}")
                        st.write(f"**Cost Range:** {tool['Cost']}")
                        st.write(f"**Platforms:** {tool['Platforms']}")
                    
                    with col2:
                        st.write(f"**Key Benefits:** {tool['Benefits']}")
                        st.write(f"**Implementation Strategy:** {tool['Implementation']}")

    else:  # Support Strategies & Best Practices
        st.markdown(f"## {get_material_icon_html('handshake')} Support Strategies for Educational Stakeholders", unsafe_allow_html=True)
        
        # Add support strategies animation
        support_col = st.columns([1, 2, 1])
        with support_col[1]:
            st.markdown(f"**{get_material_icon_html('handshake')} Collaborative Support Strategies**", unsafe_allow_html=True)
            render_lottie(
                "https://lottie.host/15c1c3e6-35bf-4933-bc7e-193fa1580efe/iwAfN5Qwfz.json",
                height=250,
                key="support_strategies_focus",
                fallback_icon="groups",
                fallback_text="Collaborative Support Networks"
            )
            st.caption("Building strong support systems for every learner's success")
        
            stakeholder = st.selectbox(
                "Select stakeholder group:",
                [
                    "Teachers & Educators",
                    "Parents & Families",
                    "Administrators & Leaders",
                    "Students & Self-Advocacy"
                ],
                key="stakeholder_selector"
            )

        
        if stakeholder == f"{get_material_icon_html('school')} Teachers & Educators":
            st.markdown(f"""
            #### **{get_material_icon_html('target')} Classroom Implementation Strategies**
            
            **{get_material_icon_html('library_books')} Daily Teaching Practices:**
            - **Universal Design for Learning (UDL)**: Provide multiple means of representation, engagement, and expression
            - **Explicit Instruction Model**: Clear learning objectives, systematic teaching, guided practice, independent application
            - **Multi-sensory Teaching Approaches**: Incorporate visual, auditory, kinesthetic, and tactile learning modalities
            - **Differentiated Instruction**: Adjust content, process, product, and learning environment based on student needs
            - **Regular Progress Monitoring**: Use frequent, brief assessments to track student learning and adjust instruction
            
            **{get_material_icon_html('checklist')} Lesson Planning Essentials:**
            - Incorporate evidence-based teaching strategies and interventions
            - Plan for various learning styles and ability levels within the same lesson
            - Prepare accommodations and modifications in advance
            - Build in multiple opportunities for practice and reinforcement
            - Include both formative and summative assessment opportunities
            """, unsafe_allow_html=True)
            
            st.markdown(f"#### {get_material_icon_html('check_circle')} Daily Teaching Excellence Checklist", unsafe_allow_html=True)
            
            checklist_categories = {
                f"Learning Objectives & Instruction": [
                    "Clear, measurable learning objectives posted and explained to students",
                    "Multi-sensory instruction techniques incorporated into lessons",
                    "Explicit instruction model followed (I do, We do, You do)",
                    "Real-world connections and relevance established"
                ],
                f"Student Engagement & Support": [
                    "Students given meaningful choices in activities, materials, or demonstration methods",
                    "Progress monitored and specific feedback provided to students",
                    "Accommodations and modifications implemented seamlessly",
                    "Positive reinforcement and encouragement given frequently"
                ],
                f"Instructional Delivery": [
                    "Instructions broken into clear, manageable steps",
                    "Visual supports and graphic organizers available and utilized",
                    "Multiple opportunities for practice and application provided",
                    "Student understanding checked frequently throughout lesson"
                ],
                f"Classroom Environment": [
                    "Inclusive, supportive classroom culture maintained",
                    "Student strengths highlighted and celebrated",
                    "Mistakes treated as learning opportunities",
                    "Collaborative learning opportunities provided"
                ]
            }
            
            for category, items in checklist_categories.items():
                st.markdown(f"**{category}**")
                for item in items:
                    st.checkbox(item, key=f"teacher_checklist_{item}")
        
        elif stakeholder == f"{get_material_icon_html('family_restroom')} Parents & Families":
            st.markdown(f"""
            #### **{get_material_icon_html('home')} Creating a Supportive Home Learning Environment**
            
            **{get_material_icon_html('star')} Foundation Strategies:**
            - **Consistent Routines**: Establish predictable daily schedules for homework, reading, and family time
            - **Organized Learning Space**: Create a quiet, well-lit, distraction-free area for studying and homework
            - **Growth Mindset Culture**: Celebrate effort, progress, and learning from mistakes rather than just final outcomes
            - **Open Communication**: Maintain regular, positive communication with teachers and school staff
            - **Strength-Based Approach**: Identify and build upon your child's unique talents and interests
            
            **{get_material_icon_html('menu_book')} Academic Support at Home:**
            - **Reading Together**: Make daily reading a family priority, regardless of your child's independent reading level
            - **Homework Support**: Break assignments into manageable chunks, provide breaks, use visual timers
            - **Learning Through Play**: Use games, cooking, and everyday activities to reinforce academic concepts
            - **Technology Balance**: Set appropriate limits on recreational screen time while leveraging educational technology
            - **Real-World Learning**: Connect school learning to everyday experiences and family activities
            """, unsafe_allow_html=True)
            
            st.markdown(f"#### {get_material_icon_html('library_books')} Evidence-Based Parent Resources", unsafe_allow_html=True)
            
            parent_resources = [
                {
                    "Resource": "International Dyslexia Association (IDA)",
                    "Type": "Professional Organization & Website",
                    "Description": "Comprehensive, research-based information about dyslexia, reading difficulties, and evidence-based interventions",
                    "Website": "https://dyslexiaida.org",
                    "Key Features": "Fact sheets, webinars, local branch networks, professional development"
                },
                {
                    "Resource": "Understood.org",
                    "Type": "Educational Platform & Community",
                    "Description": "Expert-reviewed resources for learning and thinking differences, practical strategies for home and school",
                    "Website": "https://understood.org",
                    "Key Features": "Interactive tools, parent community, expert advice, accommodation guides"
                },
                {
                    "Resource": "Learning Disabilities Association of America (LDA)",
                    "Type": "Advocacy Organization",
                    "Description": "Support, advocacy, and resources for individuals with learning disabilities and their families",
                    "Website": "https://ldaamerica.org",
                    "Key Features": "State affiliates, conferences, policy advocacy, educational resources"
                },
                {
                    "Resource": "Center for Parent Information and Resources",
                    "Type": "Federal Resource Center",
                    "Description": "Information about disabilities, special education, and resources for children with disabilities",
                    "Website": "https://www.parentcenterhub.org",
                    "Key Features": "State-specific resources, IEP guidance, transition planning, multilingual materials"
                }
            ]
            
            for resource in parent_resources:
                with st.expander(f"{resource['Resource']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Type:** {resource['Type']}")
                        st.write(f"**Website:** {resource['Website']}")
                    
                    with col2:
                        st.write(f"**Description:** {resource['Description']}")
                        st.write(f"**Key Features:** {resource['Key Features']}")

    # Enhanced help and support section
    st.markdown("---")
    st.markdown(f"### {get_material_icon_html('lightbulb')} Additional Resources & Support", unsafe_allow_html=True)
    
    support_col1, support_col2 = st.columns(2)
    
    with support_col1:
        st.markdown(f"""
        **{get_material_icon_html('link')} Professional Development & Training:**
        - [Orton-Gillingham Training](/#) - Structured literacy certification programs
        - [Wilson Language Training](/#) - Multi-sensory reading program certification
        - [International Literacy Association](/#) - Research-based literacy resources
        - [Council for Exceptional Children](/#) - Special education professional development
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        **{get_material_icon_html('analytics')} Assessment & Screening Tools:**
        - [DIBELS Assessment](/#) - Dynamic Indicators of Basic Early Literacy Skills
        - [AIMSweb Screening](/#) - Universal screening and progress monitoring
        - [STAR Assessments](/#) - Computer-adaptive reading and math assessments
        - [Phonological Awareness Literacy Screening (PALS)](/#) - Comprehensive literacy assessment
        """, unsafe_allow_html=True)
    
    with support_col2:
        st.markdown(f"""
        **{get_material_icon_html('school')} Educational Organizations & Resources:**
        - [National Center on Improving Literacy](/#) - Federal literacy research center
        - [What Works Clearinghouse](/#) - Evidence-based education practices
        - [Center on Multi-Tiered System of Supports](/#) - MTSS implementation resources
        - [National Association of Elementary School Principals](/#) - Leadership resources
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        **{get_material_icon_html('phone')} Technical Support & Assistance:**
        - **Help Desk:** support@eduscan.edu
        - **Phone Support:** (555) 123-4567
        - **Live Chat:** Available Monday-Friday, 8 AM - 6 PM EST
        - **Training Webinars:** Weekly sessions on implementation strategies
        """, unsafe_allow_html=True)
    
    # What's new section
    st.markdown("---")
    st.markdown(f"### {get_material_icon_html('new_releases')} Latest Updates & Additions", unsafe_allow_html=True)
    
    updates_col1, updates_col2 = st.columns(2)
    
    with updates_col1:
        st.markdown(f"""
        **{get_material_icon_html('science')} Recently Added Research:**
        - Updated meta-analysis on reading intervention effectiveness (March 2024)
        - New studies on executive function development and academic achievement
        - Latest findings on technology-enhanced learning for students with disabilities
        - Cultural and linguistic diversity in special education research updates
        """, unsafe_allow_html=True)
    
    with updates_col2:
        st.markdown(f"""
        **{get_material_icon_html('build')} New Tools & Resources:**
        - Enhanced digital accessibility toolkit for educators
        - Updated parent communication templates and guides
        - New professional development modules on trauma-informed practices
        - Expanded multilingual resources for diverse families
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
         border-radius: 16px; color: white; margin: 2rem 0;">
        <h3>{get_material_icon_html('rocket_launch')} Ready to Make a Difference?</h3>
        <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">
            Join thousands of educators, parents, and administrators using evidence-based practices 
            to support every learner's success.
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem 1.5rem; border-radius: 8px;">
                <strong>{get_material_icon_html('mail')} Newsletter Signup</strong>
            </div>
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem 1.5rem; border-radius: 8px;">
                <strong>{get_material_icon_html('school')} Professional Development</strong>
            </div>
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem 1.5rem; border-radius: 8px;">
                <strong>{get_material_icon_html('handshake')} Community Forum</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()