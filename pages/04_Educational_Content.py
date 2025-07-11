# pages/04_Educational_Content.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
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
    get_school_icon, get_family_icon, get_admin_icon, get_student_icon
)

# IMPORTANT: Page config MUST be the first Streamlit command for this page
st.set_page_config(
    page_title="EduScan Educational Content",
    page_icon=get_material_icon_html("menu_book"), # Replaced emoji with Material Icon HTML
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

def main():
    # Authentication check for the page
    if not is_authenticated():
        st.warning("Please log in to access Educational Content.")
        st.switch_page("app.py")
        return

    # Render main app header with dynamic content
    render_exact_page_header(get_material_icon_html('book_4'), 'educational_content', 'building_educational_excellence', language)
    
    # Single centered Lottie animation for educational excellence
    st.markdown(f"### {get_text('educational_excellence_in_action', language)}")
    
    col_center1, col_center2, col_center3 = st.columns([1, 2, 1])
    
    with col_center2:
        if LOTTIE_AVAILABLE:
            # Educational research animation
            education_url = "https://lottie.host/15c1c3e6-35bf-4933-bc7e-193fa1580efe/iwAfN5Qwfz.json"
            education_json = load_lottie_url(education_url)
            education_json = remove_lottie_background(education_json)
            
            if education_json:
                st.markdown("**Building Educational Excellence**")
                st_lottie(
                    education_json, 
                    height=250,
                    key="educational_excellence_animation",
                    speed=1,
                    loop=True,
                    quality="high",
                    # renderer="canvas"
                )
                st.markdown("Research-based strategies and evidence-driven practices for inclusive education")
    
    # Research showcase section with gradient cards
    st.markdown(f"""
    <div class="content-section">
        <h2 class="highlight-text">{get_text('building_educational_excellence', language)}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Replace image cards with gradient cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; margin-bottom: 1rem;">
            <h3>🌍 Global Best Practices</h3>
            <p>International standards and evidence-based approaches</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 12px; color: white; margin-bottom: 1rem;">
            <h3>🧠 Learning Science</h3>
            <p>Neuroscience and cognitive research insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 12px; color: white; margin-bottom: 1rem;">
            <h3>📊 Intervention Studies</h3>
            <p>Evidence-based intervention strategies</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); border-radius: 12px; color: white; margin-bottom: 1rem;">
            <h3>🤝 Cultural Adaptation</h3>
            <p>Implementing inclusive educational practices</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add educational impact showcase with gradient cards
    st.markdown(f"### {get_text('educational_research_impact', language)}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; color: white;">
            <h4>📈 Research Impact</h4>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 8px; color: white;">
            <h4>🎯 Student Success</h4>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 8px; color: white;">
            <h4>🎓 Learning Focus</h4>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); border-radius: 8px; color: white;">
            <h4>🏆 Achievement</h4>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"<h2 style='font-size:1.75rem; font-weight:700; color:var(--gray-900); margin-bottom:1.5rem; text-align:center;'>{get_material_icon_html('category', 'outlined')} {get_text('content_categories', language)}</h2>", unsafe_allow_html=True)
    content_type = st.selectbox(
        get_text('choose_content_type', language),
        [
            get_text('research_overview', language),
            get_text('types_learning_difficulties', language), 
            get_text('early_intervention', language),
            get_text('academic_resources', language),
            get_text('technology_tools', language),
            get_text('support_strategies', language)
        ],
        key="content_category_selector"
    )
    
    st.markdown(f"<h4 style='color:var(--gray-600); font-size:1rem; margin-top:1rem; margin-bottom:0.5rem;'>{get_text('target_audience', language)}</h4>", unsafe_allow_html=True)
    audience = st.selectbox(
        get_text('content_for', language),
        [get_text('teachers', language), get_text('parents', language), get_text('administrators', language), get_text('all', language)],
        key="audience_selector"
    )

    if content_type == get_text('research_overview', language):
        st.markdown(f"## {get_text('research_overview', language)}: {get_text('types_learning_difficulties', language)}")
        
        tab1, tab2, tab3 = st.tabs([get_text('statistics', language), get_text('neuroscience', language), get_text('impact_studies', language)])
        
        with tab1:
            st.markdown(f"### {get_text('Learning Difficulties Statistics', language)}")
            
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
                title="Prevalence of Learning Difficulties in School-Age Children"
            )
            st.plotly_chart(fig_prevalence, use_container_width=True)
            
            st.markdown("#### Detailed Statistics")
            stats_df = pd.DataFrame(prevalence_data)
            st.dataframe(stats_df, use_container_width=True)
            
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
            st.markdown("""
            #### **Brain-Based Understanding**
            
            Learning difficulties are neurobiological in origin, involving differences in brain structure and function:
            
            **Key Brain Areas Affected:**
            
            **1. Left Hemisphere Language Areas**
            - Broca's Area: Speech production and grammar
            - Wernicke's Area: Language comprehension
            - Angular Gyrus: Word recognition and reading
            
            **2. Phonological Processing Networks**
            - Difficulty connecting sounds to letters
            - Reduced activation in reading circuits
            - Compensatory right hemisphere activation
            
            **3. Working Memory Systems**
            - Prefrontal cortex involvement
            - Information processing speed
            - Attention and executive function
            """)
            
            st.markdown("""
            #### **Neuroplasticity and Intervention**
            
            **🌟 The Brain's Ability to Change:**
            - Intensive intervention can create new neural pathways
            - Earlier intervention leads to greater plasticity
            - Multi-sensory approaches enhance brain connectivity
            - Practice strengthens neural networks
            
            **Research Evidence:**
            - fMRI studies show brain changes after intervention
            - Increased activation in reading networks
            - Improved connectivity between brain regions
            - Long-term structural brain changes possible
            """)
            
            st.markdown("#### ⏰ Critical Intervention Periods")
            
            timeline_data = {
                "Age Range": ["3-5 years", "6-8 years", "9-12 years", "13+ years"],
                "Brain Plasticity": ["Highest", "High", "Moderate", "Lower"],
                "Intervention Impact": ["Maximum", "High", "Moderate", "Requires intensity"],
                "Key Focus": [
                    "Language development, phonological awareness",
                    "Reading foundation, basic skills",
                    "Reading fluency, comprehension",
                    "Compensation strategies, technology"
                ]
            }
            
            timeline_df = pd.DataFrame(timeline_data)
            st.dataframe(timeline_df, use_container_width=True)
        
        with tab3:
            st.markdown("""
            #### **Major Research Findings**
            
            **National Reading Panel (2000)**
            - Systematic phonics instruction is essential
            - Phonemic awareness training improves reading
            - Guided oral reading builds fluency
            - Vocabulary instruction enhances comprehension
            
            **Meta-Analysis Studies**
            - Intensive intervention shows large effect sizes (0.8+)
            - Early intervention prevents reading failure
            - Multi-component approaches most effective
            - Technology tools can enhance traditional methods
            """)
            
            intervention_data = {
                "Intervention Type": [
                    "Phonics Instruction",
                    "Reading Fluency",
                    "Comprehension Strategies", 
                    "Vocabulary Training",
                    "Multi-sensory Approaches",
                    "Technology-Assisted"
                ],
                "Effect Size": [0.86, 0.71, 0.68, 0.62, 0.75, 0.58],
                "Grade Levels": ["K-3", "2-5", "3-8", "K-8", "K-8", "K-12"]
            }
            
            fig_effectiveness = px.bar(
                intervention_data,
                x="Effect Size",
                y="Intervention Type",
                orientation='h',
                title="Intervention Effectiveness (Effect Sizes from Research)"
            )
            st.plotly_chart(fig_effectiveness, use_container_width=True)
            
            st.markdown("""
            #### **Longitudinal Study Results**
            
            **Connecticut Longitudinal Study (Shaywitz et al.)**
            - Followed 445 children from kindergarten to grade 12
            - Reading difficulties persist without intervention
            - Early identification and intervention crucial
            - Brain imaging shows intervention changes neural pathways
            - Self-esteem and motivation significantly improve
            """)

    elif content_type == get_text('types_learning_difficulties', language):
        st.markdown("## 🧩 Types of Learning Difficulties")
        
        difficulty_type = st.selectbox(
            "Select learning difficulty:",
            ["Dyslexia", "Dyscalculia", "Dysgraphia", "ADHD", "Language Processing", "Executive Function"],
            key="difficulty_type_selector_page4"
        )
        
        if difficulty_type == "Dyslexia":
            st.markdown("""
            #### **Definition and Characteristics**
            Dyslexia is a neurobiological condition affecting reading and language processing despite adequate intelligence and instruction.
            
            **Core Characteristics:**
            - Difficulty with accurate and/or fluent word recognition
            - Poor spelling and decoding abilities
            - Challenges with phonological processing
            - Reading comprehension may be affected
            
            ** Observable Signs by Age:**
            """)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                **Ages 3-5:**
                - Delayed speech development
                - Difficulty rhyming
                - Problems learning alphabet
                - Trouble following directions
                """)
            
            with col2:
                st.markdown("""
                **Ages 6-8:**
                - Slow reading progress
                - Difficulty sounding out words
                - Confusing similar words
                - Avoiding reading activities
                """)
            
            with col3:
                st.markdown("""
                **Ages 9+:**
                - Reading below grade level
                - Difficulty with comprehension
                - Poor spelling despite instruction
                - Avoiding written work
                """)
            
            st.markdown("""
            #### **Brain Neurological Basis**
            - Differences in left hemisphere language areas
            - Reduced connectivity in reading networks
            - Phonological processing deficits
            - Working memory challenges
            
            #### **Effective Interventions**
            - Systematic, explicit phonics instruction
            - Multi-sensory reading programs (Orton-Gillingham, Wilson)
            - Structured literacy approaches
            - Assistive technology support
            """)
        
        elif difficulty_type == "Dyscalculia":
            st.markdown("""
            #### **Definition and Characteristics**
            Dyscalculia is a specific learning difficulty affecting mathematical understanding and computation.
            
            **Core Characteristics:**
            - Difficulty understanding number concepts
            - Problems with mathematical reasoning
            - Challenges with calculation and computation
            - Difficulty understanding mathematical symbols
            
            **Chart Common Manifestations:**
            """)
            
            manifestations = {
                "Area": [
                    "Number Sense",
                    "Calculation",
                    "Problem Solving",
                    "Mathematical Reasoning"
                ],
                "Difficulties": [
                    "Understanding quantity, comparing numbers, number line concepts",
                    "Basic arithmetic facts, multi-step calculations, algorithms",
                    "Word problems, mathematical language, applying concepts",
                    "Patterns, relationships, abstract mathematical thinking"
                ],
                "Support Strategies": [
                    "Visual number representations, manipulatives, number lines",
                    "Break down steps, provide algorithms, use calculators",
                    "Graphic organizers, key word strategies, real-world connections",
                    "Concrete examples, visual models, step-by-step instruction"
                ]
            }
            
            manifestations_df = pd.DataFrame(manifestations)
            st.dataframe(manifestations_df, use_container_width=True)
        
        elif difficulty_type == "Dysgraphia":
            st.markdown("""
            #### **Definition and Characteristics**
            Dysgraphia is a neurological condition affecting written expression and fine motor skills.
            
            **Core Characteristics:**
            - Difficulty with handwriting and written expression
            - Poor spelling and grammar usage
            - Challenges with organizing thoughts on paper
            - Fine motor coordination difficulties
            
            **Observable Signs by Age:**
            """)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                **Ages 3-5:**
                - Difficulty holding crayons/pencils
                - Problems with drawing shapes
                - Resistance to writing activities
                - Poor letter formation
                """)
            
            with col2:
                st.markdown("""
                **Ages 6-8:**
                - Illegible handwriting
                - Slow writing speed
                - Difficulty copying from board
                - Spacing problems between words
                """)
            
            with col3:
                st.markdown("""
                **Ages 9+:**
                - Avoiding writing tasks
                - Fatigue from writing
                - Difficulty organizing ideas
                - Poor written expression
                """)
            
            st.markdown("""
            #### **Effective Interventions**
            - Occupational therapy for fine motor skills
            - Keyboarding and assistive technology
            - Graphic organizers for planning
            - Alternative assessment methods
            """)

    elif content_type == get_text('early_intervention', language):
        st.markdown("## 🚀 Early Intervention Strategies")
        
        intervention_focus = st.selectbox(
            "Intervention focus:",
            ["Pre-Reading Skills", "Early Math", "Language Development", "Social-Emotional"],
            key="intervention_focus_selector_page4"
        )
        
        if intervention_focus == "Pre-Reading Skills":
            st.markdown("""
            #### **Essential Pre-Reading Components**
            
            **1. Phonological Awareness**
            - Recognizing and manipulating sounds in spoken language
            - Foundation for reading success
            - Can be developed before formal reading instruction
            """)
            
            # Phonological awareness progression
            progression_data = {
                "Skill Level": [
                    "Word Awareness",
                    "Syllable Awareness", 
                    "Onset-Rime",
                    "Phoneme Awareness"
                ],
                "Age Range": ["3-4 years", "4-5 years", "5-6 years", "6-7 years"],
                "Activities": [
                    "Counting words in sentences, recognizing word boundaries",
                    "Clapping syllables, syllable deletion and addition",
                    "Recognizing rhymes, identifying word families",
                    "Sound isolation, blending, segmentation, manipulation"
                ],
                "Assessment": [
                    "Can identify separate words in spoken sentences",
                    "Can clap and count syllables in words",
                    "Can identify rhyming words and word patterns",
                    "Can manipulate individual sounds in words"
                ]
            }
            
            progression_df = pd.DataFrame(progression_data)
            st.dataframe(progression_df, use_container_width=True)
            
            st.markdown("""
            #### **🎵 Effective Pre-Reading Activities**
            
            **Phonological Awareness Games:**
            - Sound matching and identification games
            - Rhyming songs and poems
            - Syllable clapping activities
            - Sound blending and segmentation
            
            **Print Awareness Activities:**
            - Environmental print exploration
            - Book handling and orientation
            - Letter recognition games
            - Name writing practice
            """)
        
        elif intervention_focus == "Early Math":
            st.markdown("""
            #### **Number Sense Development**
            
            **Foundation Skills (Ages 3-5):**
            - Counting with one-to-one correspondence
            - Understanding "more" and "less"
            - Recognizing numerals
            - Simple pattern recognition
            
            **Advanced Skills (Ages 5-7):**
            - Understanding number relationships
            - Basic addition and subtraction concepts
            - Place value understanding
            - Mathematical problem-solving
            """)
            
            # Early math milestones
            milestone_data = {
                "Age": ["3-4 years", "4-5 years", "5-6 years", "6-7 years"],
                "Counting": [
                    "Counts to 5-10",
                    "Counts to 20, understands cardinality",
                    "Counts to 100, skip counting by 10s",
                    "Counts by 2s, 5s, 10s; understands odd/even"
                ],
                "Number Recognition": [
                    "Recognizes numerals 1-5",
                    "Recognizes numerals 1-10",
                    "Recognizes numerals 1-20",
                    "Recognizes numerals to 100"
                ],
                "Operations": [
                    "Understands 'more' and 'less'",
                    "Simple addition with objects",
                    "Addition/subtraction within 10",
                    "Addition/subtraction within 20"
                ]
            }
            
            milestone_df = pd.DataFrame(milestone_data)
            st.dataframe(milestone_df, use_container_width=True)

    elif content_type == get_text('academic_resources', language):
        st.markdown("## Academic Resource Library")
        
        resource_category = st.selectbox(
            "Resource category:",
            ["Research Articles", "Best Practice Guides", "Intervention Programs", "Assessment Tools"],
            key="academic_resource_category_selector_page4"
        )
        
        if resource_category == "Research Articles":
            st.markdown("### Key Research Articles")
            
            articles = [
                {
                    "Title": "The Science of Reading: A Handbook",
                    "Author": "Snowling, M. J. & Hulme, C.",
                    "Year": "2021",
                    "Key Findings": "Comprehensive review of reading research, emphasizing structured literacy approaches",
                    "Relevance": "Essential for understanding evidence-based reading instruction",
                    "Citation": "Snowling, M. J., & Hulme, C. (2021). The science of reading: A handbook. Wiley."
                },
                {
                    "Title": "Preventing Reading Difficulties in Young Children",
                    "Author": "Snow, C. E., Burns, M. S., & Griffin, P.",
                    "Year": "1998",
                    "Key Findings": "Identifies predictors of reading success and failure; emphasizes early intervention",
                    "Relevance": "Foundational text for early literacy intervention",
                    "Citation": "Snow, C. E., Burns, M. S., & Griffin, P. (1998). Preventing reading difficulties in young children. National Academy Press."
                },
                {
                    "Title": "Mathematical Learning Disabilities: Current Issues and Future Directions",
                    "Author": "Gersten, R. & Chard, D.",
                    "Year": "2019",
                    "Key Findings": "Reviews effective interventions for mathematical learning difficulties",
                    "Relevance": "Guidelines for math intervention and support",
                    "Citation": "Gersten, R., & Chard, D. (2019). Mathematical learning disabilities. Journal of Learning Disabilities, 52(3), 123-145."
                }
            ]
            
            for article in articles:
                with st.expander(f"🔧 {article['Title']} ({article['Year']})"):
                    st.write(f"**Author(s):** {article['Author']}")
                    st.write(f"**Key Findings:** {article['Key Findings']}")
                    st.write(f"**Relevance:** {article['Relevance']}")
                    st.write(f"**Citation:** {article['Citation']}")
        
        elif resource_category == "Best Practice Guides":
            st.markdown("### List Best Practice Implementation Guides")
            
            practice_areas = ["Structured Literacy", "Multi-Tiered Support", "Universal Design", "Family Engagement"]
            
            selected_practice = st.selectbox("Select practice area:", practice_areas, key="best_practice_area_selector_page4")
            
            if selected_practice == "Structured Literacy":
                st.markdown("""
                #### 🏗️ Structured Literacy Implementation
                
                **Core Components:**
                
                **1. Systematic and Cumulative**
                - Skills taught in logical order
                - Each lesson builds on previous learning
                - Regular review and reinforcement
                
                **2. Explicit Instruction**
                - Direct teaching of concepts and skills
                - Clear explanations and modeling
                - Guided practice before independence
                
                **3. Diagnostic and Responsive**
                - Regular assessment of student progress
                - Instruction adjusted based on data
                - Individualized support as needed
                
                **Implementation Steps:**
                """)
                
                implementation_steps = [
                    "Assess current literacy curriculum and practices",
                    "Provide professional development for teachers",
                    "Select evidence-based curriculum materials",
                    "Establish assessment and progress monitoring systems",
                    "Create support structures for struggling students",
                    "Monitor implementation and student outcomes"
                ]
                
                for i, step in enumerate(implementation_steps, 1):
                    st.write(f"{i}. {step}")

    elif content_type == get_text('technology_tools', language):
        st.markdown("## Technology Tools for Learning Support")
        
        tool_category = st.selectbox(
            "Tool category:",
            ["Reading Support", "Writing Assistance", "Math Tools", "Organization Apps", "Communication Aids"],
            key="tool_category_selector_page4"
        )
        
        if tool_category == "Reading Support":
            
            reading_tools = [
                {
                    "Tool": "Text-to-Speech Software",
                    "Examples": "NaturalReader, Voice Dream Reader, Read&Write",
                    "Benefits": "Helps with decoding, comprehension, and accessing grade-level content",
                    "Implementation": "Start with short texts, teach controls, practice daily"
                },
                {
                    "Tool": "Digital Highlighters",
                    "Examples": "Kami, Hypothesis, Adobe Reader",
                    "Benefits": "Helps with focus, note-taking, and text organization",
                    "Implementation": "Teach color-coding system, practice with short passages"
                },
                {
                    "Tool": "Reading Comprehension Apps",
                    "Examples": "Epic!, Reading A-Z, Lexia Core5",
                    "Benefits": "Adaptive practice, immediate feedback, engaging content",
                    "Implementation": "Set appropriate levels, monitor progress, supplement instruction"
                }
            ]
            
            for tool in reading_tools:
                with st.expander(f"🔧 {tool['Tool']}"):
                    st.write(f"**Examples:** {tool['Examples']}")
                    st.write(f"**Benefits:** {tool['Benefits']}")
                    st.write(f"**Implementation:** {tool['Implementation']}")
        
        elif tool_category == "Writing Assistance":
            writing_tools_data = {
                "Tool Type": [
                    "Word Prediction",
                    "Grammar Checkers", 
                    "Graphic Organizers",
                    "Speech-to-Text"
                ],
                "Examples": [
                    "Co:Writer, WordQ, Ginger",
                    "Grammarly, ProWritingAid, Ginger",
                    "Inspiration, Kidspiration, MindMeister",
                    "Dragon Naturally Speaking, Google Voice Typing"
                ],
                "Primary Benefits": [
                    "Reduces spelling errors, improves vocabulary",
                    "Identifies grammar and punctuation errors",
                    "Helps organize thoughts and ideas",
                    "Bypasses handwriting difficulties"
                ]
            }
            
            writing_tools_df = pd.DataFrame(writing_tools_data)
            st.dataframe(writing_tools_df, use_container_width=True)

    else:  # Support Strategies
        st.markdown("## 🤝 Support Strategies for Different Stakeholders")
        
        stakeholder = st.selectbox(
            "Select stakeholder group:",
            [get_text('teachers', language), get_text('parents', language), get_text('administrators', language), get_text('students', language)],
            key="stakeholder_selector_page4"
        )
        
        if stakeholder == get_text('teachers', language):
            st.markdown("""
            #### **Classroom Implementation**
            
            **Daily Practices:**
            - Use explicit instruction methods
            - Provide multiple means of representation
            - Offer choice in how students demonstrate learning
            - Implement regular progress monitoring
            
            **Lesson Planning:**
            - Include universal design principles
            - Plan for differentiated instruction
            - Prepare accommodations and modifications
            - Build in multiple practice opportunities
            """)
            
            st.markdown("#### Daily Teaching Checklist")
            
            checklist_items = [
                "Clear learning objectives posted and explained",
                "Multi-sensory instruction techniques used",
                "Students given choice in activities or materials",
                "Progress monitored and feedback provided",
                "Accommodations implemented as needed",
                "Positive reinforcement and encouragement given",
                "Instructions broken into manageable steps",
                "Visual supports and graphic organizers available"
            ]
            
            for item in checklist_items:
                st.checkbox(item, key=f"teacher_{item}_page4")
        
        elif stakeholder == get_text('parents', language):
            st.markdown("""
            #### **Home Support Techniques**
            
            **Creating a Supportive Environment:**
            - Establish consistent routines and expectations
            - Provide a quiet, organized homework space
            - Celebrate effort and progress, not just achievement
            - Maintain open communication with teachers
            - Implement home-based learning activities
            
            **Academic Support:**
            - Break homework into manageable chunks
            - Use visual schedules and reminders
            - Practice skills in fun, game-like ways
            - Read together daily, regardless of child's reading level
            """)
            
            st.markdown("#### Recommended Parent Resources")
            
            parent_resources = [
                {
                    "Resource": "International Dyslexia Association",
                    "Type": "Website",
                    "Description": "Comprehensive information about dyslexia and reading difficulties",
                    "Link": "https://dyslexiaida.org"
                },
                {
                    "Resource": "Understood.org",
                    "Type": "Website", 
                    "Description": "Resources for learning and thinking differences",
                    "Link": "https://understood.org"
                },
                {
                    "Resource": "Learning Disabilities Association",
                    "Type": "Organization",
                    "Description": "Support and advocacy for individuals with learning disabilities",
                    "Link": "https://ldaamerica.org"
                }
            ]
            
            for resource in parent_resources:
                with st.expander(f"🔧 {resource['Resource']}"):
                    st.write(f"**Type:** {resource['Type']}")
                    st.write(f"**Description:** {resource['Description']}")
                    st.write(f"**Link:** {resource['Link']}")
        
        elif stakeholder == get_text('administrators', language):
            st.markdown("""
            #### **Systemic Support:**
            - Allocate resources for professional development in inclusive education.
            - Foster a school-wide culture of collaboration between general and special education teachers.
            - Ensure availability of evidence-based intervention programs and tools.
            - Implement data-driven decision-making for student support and interventions.
            
            #### **Policy and Leadership:**
            - Develop and enforce inclusive policies that support diverse learners.
            - Advocate for funding and resources to meet student needs.
            - Promote parent and community engagement in school initiatives.
            - Lead by example in promoting a positive and supportive school environment.
            """)
        
        elif stakeholder == get_text('students', language):
            st.markdown("""
            #### **Empowering Students:**
            - Teach students to understand their own learning profiles and strengths.
            - Encourage students to communicate their needs to teachers and parents.
            - Develop self-monitoring and self-regulation skills.
            - Foster a growth mindset and resilience in facing learning challenges.
            
            #### **Tools for Independence:**
            - Introduce assistive technologies that support their learning style.
            - Teach organizational strategies (e.g., planners, digital tools).
            - Promote goal-setting and self-reflection on their progress.
            - Encourage participation in peer support networks.
            """)

    st.markdown("---")
    st.markdown(f"### {get_material_icon_html('quick_reference')} Quick Resources", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Reading Strategies", use_container_width=True, key="quick_link_reading_footer_page4"):
            st.info("Comprehensive reading support strategies loaded above!")
    
    with col2:
        if st.button("Math Support", use_container_width=True, key="quick_link_math_footer_page4"):
            st.info("Mathematics intervention techniques displayed above!")
    
    with col3:
        if st.button("Writing Help", use_container_width=True, key="quick_link_writing_footer_page4"):
            st.info("Writing differentiation strategies shown above!")
    
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Behavior Tips", use_container_width=True, key="quick_link_behavior_footer_page4"):
        st.info("Behavioral intervention strategies provided above!")

if __name__ == "__main__":
    main()