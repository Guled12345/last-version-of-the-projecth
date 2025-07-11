# utils/exact_ui.py
import streamlit as st
import os
import base64
# Import ALL necessary icon utilities. SVG functions will ONLY be used for non-interactive display (like stat cards).
from utils.icon_utils import (
    get_dashboard_icon, get_assessment_icon, get_teacher_icon,
    get_parent_icon, get_research_icon, get_checkmark_icon,
    get_warning_icon, get_error_icon, get_settings_icon,
    get_total_students_icon, get_on_track_icon, get_at_risk_icon, get_intervention_icon,
    get_material_icon_html, # NEW: Import the Material Icons HTML generator
    get_lightbulb_icon, get_rocket_icon, get_puzzle_icon, get_brain_icon,
    get_chart_line_icon, get_chart_pie_icon, get_table_icon, get_ruler_icon,
    get_gamepad_icon, get_book_icon, get_laptop_icon, get_handshake_icon,
    get_school_icon
)
# Import ALL necessary language utilities
from utils.language_utils import get_text, save_app_settings, load_app_settings
from utils.auth_utils import is_authenticated, logout_user, get_user_role # Import auth utilities
from utils.image_base64 import get_base64_images # Import to access the b64 image dictionary

def custom_alert(message, icon_html="", alert_type="info"):
    colors = {
        "info": "#fff3cd",     # Yellow
        "success": "#d4edda",   # Green
        "warning": "#fff3cd",   # Yellow
        "error": "#f8d7da"      # Red
    }
    borders = {
        "info": "#ffeeba",
        "success": "#c3e6cb",
        "warning": "#ffeeba",
        "error": "#f5c6cb"
    }
    st.markdown(
        f"""
        <div style='background-color:{colors[alert_type]}; border-left: 6px solid {borders[alert_type]}; padding: 1rem; border-radius: 0.5rem;'>
            {icon_html} {message}
        </div>
        """,
        unsafe_allow_html=True
    )

def add_exact_ui_styles():
    """Add modern, mobile-first CSS styles for Streamlit"""
    # Load background image from get_base64_images() in image_base64.py
    b64_images = get_base64_images()
    background_image_b64 = b64_images.get('image_83d859', '')

    bg_image_css = f"url('{background_image_b64}')" if background_image_b64 else "none"
    bg_color_fallback = "#f9fafb" # Light background color if image fails

    st.markdown(f"""
    <style>
        /* Import Inter font (if not already handled by a global setup) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        /* NEW: Import Google Material Symbols font */
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Sharp:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
        
        :root {{
            /* Define brand colors */
            --primary-purple: #8b5cf6;
            --secondary-blue: #3b82f6;
            --success-green: #10b981;
            --warning-orange: #f59e0b;
            --danger-red: #ef4444;
            --info-blue: #3b82f6;

            /* Grayscale colors */
            --gray-900: #111827;
            --gray-800: #1f2937;
            --gray-700: #374151;
            --gray-600: #4b5563;
            --gray-500: #6b7280;
            --gray-400: #9ca3af;
            --gray-300: #d1d5db;
            --gray-200: #e5e7eb;
            --gray-100: #f3f4f6;
            --gray-50: #f9fafb;
            --white: #ffffff;

            /* Shadows */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);

            /* Transitions */
            --transition-ease: all 0.3s ease;
        }}

        /* Dark mode variables */
        body[data-theme="Dark"] {{
            --primary-purple: #a78bfa;
            --secondary-blue: #60a5fa;
            --success-green: #34d399;
            --warning-orange: #fbbf24;
            --danger-red: #f87171;
            --info-blue: #60a5fa;

            --gray-900: #f9fafb;
            --gray-800: #e0e0e0;
            --gray-700: #d1d5db;
            --gray-600: #9ca3af;
            --gray-500: #6b7280; /* Text color for muted elements */
            --gray-400: #4b5563;
            --gray-300: #374151;
            --gray-200: #2a3038; /* Lighter dark backgrounds */
            --gray-100: #1f2937; /* Even lighter dark backgrounds */
            --gray-50: #111827; /* Main dark background */
            --white: #1f2937; /* Card background in dark mode */
        }}

        /* Reset and base styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html, body {{
            font-family: 'Inter', sans-serif !important;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-rendering: optimizeLegibility;
            line-height: 1.6;
            color: var(--gray-700);
            background-color: var(--gray-50); /* Main app background */
            height: 100vh;
            width: 100vw;
            overflow-x: hidden;
        }}

        /* Global background image setup (transparent overlay on top) */
        body {{
            background-image: {bg_image_css} !important;
            background-size: cover !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            background-position: center center !important;
            background-color: var(--gray-50) !important; /* Fallback color */
        }}
        .stApp, .main {{
            background-color: transparent !important; /* Make Streamlit's base divs transparent */
            font-family: 'Inter', sans-serif !important; 
            color: var(--gray-700); 
            min-height: 100vh;
            position: relative;
            z-index: 0;
        }}
        .stApp::before, .main::before {{ /* Semi-transparent overlay over background image */
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(240,242,245,0.9) !important; /* Increased opacity for more blur */
            backdrop-filter: blur(5px); /* Add blur effect */
            z-index: -1; 
        }}
        body[data-theme="Dark"] .stApp::before, body[data-theme="Dark"] .main::before {{
            background: rgba(17,24,39,0.9) !important; /* Dark overlay */
            backdrop-filter: blur(5px); /* Add blur effect */
        }}

        /* Hide Streamlit default elements */
        #MainMenu, footer, header, .stDeployButton, .stDecoration {{ display: none !important; }}

        /* Hamburger menu icon color */
        .stSidebar .st-emotion-cache-eq8clt, /* Hamburger menu */
        .stSidebar .st-emotion-cache-1cypcdb > div > button /* Expander button */ {{
            color: var(--primary-purple) !important;
            opacity: 1 !important;
        }}

        /* Material Symbols general styling */
        .material-symbols-outlined, .material-symbols-rounded, .material-symbols-sharp, .material-symbols-fill {{
            font-family: 'Material Symbols Outlined'; /* Use outlined as default for non-filled */
            font-weight: normal;
            font-style: normal;
            font-size: 24px; /* Default size, override with specific classes */
            display: inline-block;
            line-height: 1;
            text-transform: none;
            letter-spacing: normal;
            word-wrap: normal;
            white-space: nowrap;
            direction: ltr;
            -webkit-font-feature-settings: 'liga';
            -webkit-font-smoothing: antialiased;
            vertical-align: middle; /* Align with text */
        }}
        .material-symbols-rounded {{ font-family: 'Material Symbols Rounded'; }}
        .material-symbols-sharp {{ font-family: 'Material Symbols Sharp'; }}
        .material-symbols-fill {{ font-family: 'Material Symbols Outlined'; font-variation-settings: 'FILL' 1; }} /* For filled style, still use outlined font and apply fill settings */


        /* Main content area structure */
        .main .block-container {{
            background: var(--white); /* Card background, lighter shade in dark mode */
            border-radius: 12px; 
            padding: clamp(1rem, 4vw, 2rem) !important; /* Responsive padding */
            margin: 1rem auto !important;
            max-width: 1200px;
            width: 100%;
            box-shadow: var(--shadow-lg);
            transition: var(--transition-ease);
        }}
        
        /* Sidebar Styling */
        .css-1d391kg, .css-1cypcdb, section[data-testid="stSidebar"] {{
            background: var(--white) !important;
            border-right: 1px solid var(--gray-200) !important;
            box-shadow: var(--shadow-md);
            width: 280px !important;
            min-width: 280px !important;
            max-width: 280px !important;
            padding: 0 !important;
            transition: var(--transition-ease);
        }}
        div[data-testid="stSidebarNav"] {{ display: none !important; }} /* Hide default nav */
        .css-1d391kg > div:first-child > div[data-testid="stVerticalBlock"] {{
            padding: 1.5rem !important;
            display: flex;
            flex-direction: column;
            height: 100vh; /* Full viewport height */
            gap: 1.5rem;
        }}

        /* Sidebar Brand */
        .sidebar-brand {{
            display: flex;
            align-items: center;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--gray-200);
            margin-bottom: 1.5rem;
        }}
        .sidebar-logo {{
            width: 48px; height: 48px;
            background: linear-gradient(135deg, var(--primary-purple), var(--secondary-blue));
            border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            color: white; font-weight: 700; font-size: 18px; margin-right: 12px;
            box-shadow: var(--shadow-sm);
            flex-shrink: 0;
        }}
        .sidebar-title {{ font-size: 20px; font-weight: 800; color: var(--gray-900); line-height: 1.2; }}
        .sidebar-subtitle {{ font-size: 14px; color: var(--gray-500); line-height: 1.3; margin-top: 2px; }}

        /* Sidebar Navigation Links */
        .nav-section-header {{
            font-size: 12px; font-weight: 600; color: var(--gray-400); text-transform: uppercase;
            letter-spacing: 0.05em; margin: 0.5rem 0; padding-left: 4px;
        }}
        div[data-testid^="stPageLink"] {{
            margin-bottom: 0.5rem;
            border-radius: 12px;
            overflow: hidden;
            transition: var(--transition-ease);
        }}
        div[data-testid^="stPageLink"] > a {{
            padding: 12px 16px; border-radius: 12px; text-decoration: none;
            color: var(--gray-600); font-weight: 500; font-size: 14px;
            display: flex; align-items: center; gap: 12px; width: 100%; min-height: 48px;
            border: 1px solid transparent; transition: var(--transition-ease);
        }}
        div[data-testid^="stPageLink"] > a:hover {{
            background: var(--gray-50); color: var(--gray-700); transform: translateX(4px);
            border-color: var(--gray-200);
        }}
        div[data-testid^="stPageLink"] > a[aria-current="page"] {{
            background: linear-gradient(135deg, var(--primary-purple), var(--secondary-blue)) !important;
            color: white !important; font-weight: 600 !important;
            box-shadow: 0 4px 6px -1px rgba(139, 92, 246, 0.3) !important;
            border-color: transparent !important;
            transform: translateX(0); /* Reset transform for active */
        }}
        /* Style the actual HTML icon within st.page_link (which are spans with Material Symbols font) */
        div[data-testid^="stPageLink"] > a .material-symbols-outlined, .material-symbols-rounded, .material-symbols-sharp {{
            font-size: 20px; /* Adjust size for nav icons */
            color: var(--gray-500); /* Default icon color */
            transition: var(--transition-ease);
            font-variation-settings: 'wght' 400; /* Regular weight for nav icons */
        }}
        div[data-testid^="stPageLink"] > a:hover .material-symbols-outlined,
        div[data-testid^="stPageLink"] > a[aria-current="page"] .material-symbols-outlined {{
            color: white !important; /* White icon on hover/active for contrast */
        }}


        /* Sidebar Settings Section */
        .settings-section {{
            margin-top: auto; /* Push to bottom */
            padding-top: 1.5rem; border-top: 1px solid var(--gray-200);
        }}
        /* Custom labels for settings */
        .settings-label {{
            font-weight: 600; color: var(--gray-700); font-size: 14px; margin-bottom: 0.5rem; display: block;
            text-align: left; /* Ensure alignment */
        }}


        /* Form Control Overrides (Selectbox, Radio, Checkbox) */
        /* Target Streamlit's internal label for collapsed label alignment */
        div[data-testid="stSelectbox"] > label[data-testid="stWidgetLabel"] {{
            display: none; /* Hide default label when custom label is used */
        }}
        /* Actual selectbox input control */
        .stSelectbox > div[data-testid="stSelectbox"] > div:first-child > div {{
            background: var(--gray-50) !important; 
            border: 1px solid var(--gray-300) !important;
            border-radius: 8px !important; 
            padding: 8px 12px !important; 
            color: var(--gray-700) !important;
            font-size: 14px !important; 
            transition: var(--transition-ease); 
            box-shadow: var(--shadow-sm);
            width: 100%; /* Ensure it fills container */
        }}
        .stSelectbox > div[data-testid="stSelectbox"] > div:first-child > div:hover {{ background: var(--white) !important; border-color: var(--gray-400) !important; }}
        .stSelectbox > div[data-testid="stSelectbox"] > div:first-child > div:focus-within {{
            border-color: var(--primary-purple) !important; 
            box-shadow: 0 0 0 3px rgba(var(--primary-purple-rgb), 0.1) !important;
            outline: none !important;
        }}
        /* Ensure dropdown icon is colored */
        .stSelectbox .st-bv .st-dg svg {{ color: var(--gray-500); }}


        /* Radio buttons for theme selection */
        div[data-testid="stRadio"] > label[data-testid="stWidgetLabel"] {{
            display: none; /* Hide default label when custom label is used */
        }}
        .stRadio div[role="radiogroup"] {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-top: 8px; }} /* Changed to 2 columns for Light/Dark/System */
        .stRadio div[data-testid="stRadio"] label {{
            background: var(--gray-50); border: 1px solid var(--gray-300); border-radius: 8px;
            padding: 8px 12px; cursor: pointer; transition: var(--transition-ease);
            font-weight: 500; color: var(--gray-600); text-align: center; font-size: 12px;
            min-height: 36px; display: flex; align-items: center; justify-content: center;
        }}
        .stRadio div[data-testid="stRadio"] label:hover {{ background: var(--gray-100); border-color: var(--gray-400); }}
        .stRadio div[data-testid="stRadio"] input:checked + div {{
            background: linear-gradient(135deg, var(--primary-purple), var(--secondary-blue)) !important;
            color: white !important; border-color: transparent !important; box-shadow: var(--shadow-md) !important;
        }}


        /* Modern toggle switch for Offline Mode */
        .stCheckbox > label[data-testid="stWidgetLabel"] {{ /* Target the default label for Streamlit checkbox */
            display: none; /* Hide default label */
        }}
        /* The visual checkbox control */
        .stCheckbox span.st-emotion-cache-ch5f2v {{
            position: relative; width: 44px; height: 24px; appearance: none;
            background: var(--gray-300); border-radius: 12px; transition: var(--transition-ease);
            cursor: pointer; flex-shrink: 0;
        }}
        .stCheckbox input[type="checkbox"]:checked + span.st-emotion-cache-ch5f2v {{ background: linear-gradient(135deg, var(--primary-purple), var(--secondary-blue)); }}
        .stCheckbox input[type="checkbox"]::before {{
            content: ''; position: absolute; top: 2px; left: 2px;
            width: 20px; height: 20px; background: white; border-radius: 50%;
            transition: var(--transition-ease); box-shadow: var(--shadow-sm);
        }}
        .stCheckbox input[type="checkbox"]:checked + span.st-emotion-cache-ch5f2v::before {{ transform: translateX(20px); }}
        /* For the text next to the checkbox, often automatically generated by Streamlit */
        .stCheckbox > label > div > p {{
            font-weight: 600; color: var(--gray-700); font-size: 14px; /* Ensure text matches custom labels */
        }}
        /* Adjust alignment for the checkbox item itself */
        div[data-testid="stCheckbox"] {{
            margin-top: 1rem; /* Space below theme radio */
        }}
        div[data-testid="stCheckbox"] > label {{
            display: flex; /* Make the label itself a flex container */
            justify-content: space-between; /* Push checkbox to end */
            align-items: center;
            width: 100%;
        }}


        /* Status indicator (at the bottom of sidebar) */
        .status-indicator {{
            display: flex; align-items: center; justify-content: space-between;
            padding: 12px 16px; background: var(--gray-50); border-radius: 12px;
            border: 1px solid var(--gray-200); margin-top: 1rem;
        }}
        .status-dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }}
        .status-online {{ background-color: var(--success-green); }}
        .status-offline {{ background-color: var(--warning-orange); }}

        /* Main Page Header */
        .page-header {{
            background: var(--white); border-bottom: 1px solid var(--gray-200);
            padding: 2rem; margin-bottom: 2rem; border-radius: 16px;
            box-shadow: var(--shadow-sm); transition: var(--transition-ease);
            display: flex; flex-direction: column; align-items: flex-start;
        }}
        .page-title {{
            font-size: 2.25rem; font-weight: 800;
            background-image: linear-gradient(135deg, var(--primary-purple), var(--secondary-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-fill-color: transparent;
            margin-bottom: 0.5rem; line-height: 1.2;
            animation: fadeIn 1s ease-out; /* Added animation */
        }}
        /* Style the actual HTML icon within the page title */
        .page-title .material-symbols-outlined, .page-title .material-symbols-rounded {{
            font-size: 36px; /* Larger icon for page title */
            vertical-align: middle;
            margin-right: 8px;
            color: var(--primary-purple); /* Color the icon */
            font-variation-settings: 'wght' 600; /* Make it bolder */
            -webkit-text-fill-color: var(--primary-purple); /* Ensure icon color is not transparent */
        }}
        .page-subtitle {{
            font-size: 1.125rem; color: var(--gray-500);
            margin-bottom: 1rem; line-height: 1.5;
            animation: slideInDown 1s ease-out; /* Added animation */
        }}
        .status-badge {{
            display: inline-flex; align-items: center;
            padding: 6px 12px; background: #dcfdf7; color: #065f46;
            border-radius: 20px; font-size: 14px; font-weight: 500;
            border: 1px solid #a7f3d0;
        }}
        .status-badge.offline {{
            background: #fef3c7; color: #92400e; border-color: #fcd34d;
        }}

        /* Metric Cards */
        .metric-card {{
            background: var(--white); border-radius: 16px; padding: 1.5rem;
            box-shadow: var(--shadow-sm); border: 1px solid var(--gray-200);
            transition: var(--transition-ease); height: 100%; display: flex;
            flex-direction: column; justify-content: space-between;
        }}
        .metric-card:hover {{
            transform: translateY(-4px); box-shadow: var(--shadow-md);
            border-color: var(--gray-300);
        }}
        .metric-header {{
            display: flex; justify-content: space-between; align-items: flex-start;
            margin-bottom: 1rem;
        }}
        .metric-label {{ font-size: 14px; font-weight: 500; color: var(--gray-600); line-height: 1.4; }}
        .metric-icon {{
            width: 48px; height: 48px; border-radius: 12px; display: flex;
            align-items: center; justify-content: center; color: white;
            font-size: 20px; flex-shrink: 0;
        }}
        .metric-icon .material-symbols-outlined, .metric-icon .material-symbols-rounded {{
            font-size: 28px; /* Larger icons for metric cards */
            color: white;
            font-variation-settings: 'wght' 500; /* Adjust weight for icons */
        }}
        .metric-icon.total {{ background: linear-gradient(135deg, var(--primary-purple), var(--secondary-blue)); box-shadow: var(--shadow-sm); }}
        .metric-icon.on-track {{ background: linear-gradient(135deg, var(--success-green), #059669); box-shadow: var(--shadow-sm); }}
        .metric-icon.at-risk {{ background: linear-gradient(135deg, var(--warning-orange), #d97706); box-shadow: var(--shadow-sm); }}
        .metric-icon.intervention {{ background: linear-gradient(135deg, var(--danger-red), #dc2626); box-shadow: var(--shadow-sm); }}
        .metric-number {{ font-size: 2.5rem; font-weight: 800; color: var(--gray-900); line-height: 1; margin-bottom: 0.5rem; }}
        .metric-change {{ font-size: 14px; font-weight: 500; color: var(--gray-500); display: flex; align-items: center; gap: 4px; }}
        .metric-change.positive {{ color: var(--success-green); }}
        .metric-change.negative {{ color: var(--danger-red); }}

        /* Chart Containers */
        .chart-container {{
            background: var(--white); border-radius: 16px; padding: 1.5rem;
            box-shadow: var(--shadow-sm); border: 1px solid var(--gray-200);
            transition: var(--transition-ease); margin-bottom: 2rem;
        }}
        .chart-container:hover {{ transform: translateY(-4px); box-shadow: var(--shadow-md); border-color: var(--gray-300); }}
        .chart-title {{ font-size: 1.25rem; font-weight: 700; color: var(--gray-900); margin-bottom: 0.5rem; }}
        .chart-subtitle {{ font-size: 14px; color: var(--gray-500); margin-bottom: 1.5rem; }}

        /* New Glassy Container Style */
        .glassy-container {{
            background: rgba(var(--white-rgb), 0.7); /* Semi-transparent white */
            backdrop-filter: blur(10px); /* Glass effect */
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: var(--shadow-lg);
            border: 1px solid rgba(var(--gray-200-rgb), 0.3); /* Lighter border for glassy look */
            transition: var(--transition-ease);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%; /* Ensure it fills parent height */
            text-align: center;
            color: var(--gray-800);
            position: relative;
            overflow: hidden; /* Important for plotly charts inside */
        }}
        body[data-theme="Dark"] .glassy-container {{
            background: rgba(var(--gray-800-rgb), 0.7);
            border: 1px solid rgba(var(--gray-700-rgb), 0.3);
            color: var(--gray-100);
        }}
        .glassy-container .plotly-container {{
            width: 100%;
            height: 100%;
        }}
        .glassy-container .modebar {{
            background: transparent !important; /* Make plotly modebar transparent */
        }}

        /* Data Tables */
        .stDataFrame {{ border-radius: 12px; overflow: hidden; box-shadow: var(--shadow-sm); }}
        .stDataFrame table {{ border-collapse: separate; border-spacing: 0; }}
        .stDataFrame th {{ background: var(--gray-50); color: var(--gray-700); font-weight: 600; font-size: 14px; padding: 12px 16px; border-bottom: 1px solid var(--gray-200); }}
        .stDataFrame td {{ padding: 12px 16px; border-bottom: 1px solid var(--gray-100); font-size: 14px; }}
        .stDataFrame tbody tr:hover {{ background: var(--gray-50); }}

        /* Modern Buttons */
        .stButton button {{
            background: linear-gradient(135deg, var(--primary-purple), var(--secondary-blue));
            color: white; border: none; border-radius: 12px; padding: 12px 24px;
            font-weight: 600; font-size: 14px; cursor: pointer;
            transition: var(--transition-ease); box-shadow: var(--shadow-md);
        }}
        .stButton button:hover {{ transform: translateY(-2px); box-shadow: var(--shadow-lg); }}
        .stButton button:active {{ transform: translateY(0); box-shadow: var(--shadow-sm); }}

        /* Modern Text Inputs / Text Areas / Number Inputs */
        div[data-testid="stTextInput"] label p, div[data-testid="stTextArea"] label p, div[data-testid="stNumberInput"] label p,
        div[data-testid="stSlider"] label p, div[data-testid="stSelectbox"] label p, div[data-testid="stRadio"] label p,
        div[data-testid="stMultiselect"] label p, div[data-testid="stDateInput"] label p {{
            font-weight: 600; /* Ensure all labels are bold for clarity */
            color: var(--gray-700);
            font-size: 14px;
            margin-bottom: 0.5rem;
        }}
        body[data-theme="Dark"] div[data-testid="stTextInput"] label p, body[data-theme="Dark"] div[data-testid="stTextArea"] label p, body[data-theme="Dark"] div[data-testid="stNumberInput"] label p,
        body[data-theme="Dark"] div[data-testid="stSlider"] label p, body[data-theme="Dark"] div[data-testid="stSelectbox"] label p, body[data-theme="Dark"] div[data-testid="stRadio"] label p,
        body[data-theme="Dark"] div[data-testid="stMultiselect"] label p, body[data-theme="Dark"] div[data-testid="stDateInput"] label p {{
            color: var(--gray-400); /* Dark mode label color */
        }}


        div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stNumberInput"] input {{
            background: var(--gray-50) !important;
            border: 1px solid var(--gray-300) !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            font-size: 1em !important;
            color: var(--gray-800) !important;
            transition: var(--transition-ease) !important;
            box-shadow: inset var(--shadow-sm);
        }}
        div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus, div[data-testid="stNumberInput"] input:focus {{
            border-color: var(--primary-purple) !important;
            box-shadow: 0 0 0 3px rgba(var(--primary-purple-rgb), 0.15) !important;
            outline: none !important;
        }}
        
        /* Sliders */
        div[data-testid="stSlider"] {{
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        /* div[data-testid="stSlider"] label {{ /* Moved to general label styling above */
        /* }} */
        .stSlider .st-fx {{ /* Track */
            background: var(--gray-300);
            height: 6px;
            border-radius: 3px;
        }}
        .stSlider .st-fy {{ /* Filled track */
            background: linear-gradient(to right, var(--secondary-blue), var(--primary-purple));
            height: 6px;
            border-radius: 3px;
        }}
        .stSlider .st-fz {{ /* Thumb */
            background: white;
            border: 2px solid var(--primary-purple);
            width: 20px;
            height: 20px;
            border-radius: 50%;
            box-shadow: var(--shadow-sm);
            transition: var(--transition-ease);
        }}
        .stSlider .st-fz:hover {{
            box-shadow: 0 0 0 8px rgba(var(--primary-purple-rgb), 0.1);
        }}

        /* Expander */
        button[data-testid="stExpanderToggleIcon"] svg {{
            color: var(--primary-purple);
            transition: var(--transition-ease);
        }}
        button[data-testid="stExpanderToggleIcon"]:hover svg {{
            transform: scale(1.1);
        }}
        div[data-testid="stExpander"] {{
            border: 1px solid var(--gray-200);
            border-radius: 12px;
            box-shadow: var(--shadow-sm);
            transition: var(--transition-ease);
        }}
        div[data-testid="stExpander"]:hover {{
            box-shadow: var(--shadow-md);
            border-color: var(--gray-300);
        }}
        div[data-testid="stExpander"] div[data-testid="stVerticalBlock"] {{
            padding: 1rem;
        }}
        div[data-testid="stExpander"] > div > div > div > p {{
            font-weight: 600;
            color: var(--gray-800);
        }}


        /* --- Image container responsiveness --- */
        /* Base container for images with controlled aspect ratio */
        .image-aspect-ratio-container {{
            position: relative;
            width: 100%;
            padding-bottom: 56.25%; /* Default 16:9 aspect ratio */
            overflow: hidden;
            border-radius: 8px;
            display: flex; /* For centering fallback text */
            justify-content: center;
            align-items: center;
            background: var(--gray-100); /* Fallback background for container - prevents white overlays */
            transition: var(--transition-ease);
        }}
        /* Specific aspect ratios */
        .image-aspect-ratio-container.aspect-4-3 {{ padding-bottom: 75%; }}
        .image-aspect-ratio-container.aspect-1-1 {{ padding-bottom: 100%; }}

        .image-aspect-ratio-container img {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: contain; /* Default: ensures entire image is visible without cropping */
            border-radius: 8px;
            transition: var(--transition-ease);
        }}
        /* Class to apply for images that should fill the container, even if cropped */
        .image-aspect-ratio-container.object-fit-cover-mode img {{
            object-fit: cover; 
        }}
        /* Fallback text styling */
        .image-aspect-ratio-container span {{
            position: absolute; color: var(--gray-500); text-align: center; font-size: 0.8em; padding: 10px;
        }}
        /* Animated fallback for removed images (now dynamic text animation) */
        .image-aspect-ratio-container.animated-fallback {{
            background: linear-gradient(45deg, var(--gray-200), var(--gray-300));
            animation: pulseBackground 2s infinite alternate;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-size: 1.2em;
            color: var(--gray-600);
            text-align: center;
            padding: 1rem;
        }}
        .image-aspect-ratio-container.animated-fallback .material-symbols-outlined {{
            font-size: 3em;
            margin-bottom: 0.5rem;
            color: var(--primary-purple);
            animation: bounceIn 1s ease-out;
        }}
        /* Add text animation for titles/subtitles in specific sections */
        .section-animated-text h1, .section-animated-text h2, .section-animated-text h3, .section-animated-text p {{
            animation: textFadeInUp 0.8s ease-out forwards;
            opacity: 0;
            transform: translateY(20px);
        }}
        .section-animated-text h1 {{ animation-delay: 0.1s; }}
        .section-animated-text h2 {{ animation-delay: 0.2s; }}
        .section-animated-text h3 {{ animation-delay: 0.3s; }}
        .section-animated-text p {{ animation-delay: 0.4s; }}

        @keyframes textFadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* New 3D-like hover effects for cards */
        .teacher-card:hover, .family-card:hover, .research-card:hover {{
            transform: translateY(-8px) rotateX(5deg) rotateY(-5deg) scale(1.02); /* More pronounced 3D effect */
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
            border-color: var(--primary-purple); /* Highlight border */
        }}


        @keyframes pulseBackground {{
            0% {{ background-position: 0% 50%; }}
            100% {{ background-position: 100% 50%; }}
        }}
        @keyframes bounceIn {{
            0%, 20%, 40%, 60%, 80%, 100% {{ transition-timing-function: cubic-bezier(0.215, 0.610, 0.355, 1.000); }}
            0% {{ opacity: 0; transform: scale3d(.3, .3, .3); }}
            20% {{ transform: scale3d(1.1, 1.1, 1.1); }}
            40% {{ transform: scale3d(.9, .9, .9); }}
            60% {{ opacity: 1; transform: scale3d(1.03, 1.03, 1.03); }}
            80% {{ transform: scale3d(.97, .97, .97); }}
            100% {{ opacity: 1; transform: scale3d(1, 1, 1); }}
        }}


        /* Responsive Image Grids (e.g., student-showcase, teacher-showcase, family-showcase) */
        /* These classes are applied to the parent div that holds the image cards */
        .student-showcase, .teacher-showcase, .family-showcase, .image-gallery-grid, .research-showcase {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); /* Min width for cards, auto-fit to columns */
            gap: 1rem; /* Spacing between cards */
            margin-bottom: 1.5rem;
        }}

        /* Ensure cards within these grids take full height of their grid cell */
        /* .student-card, .teacher-card, .family-card, .research-card {{ Removed individual styles as they are now in the combined .teacher-card, .family-card, .research-card selector above}} */

        /* Images within these cards (now using the image-aspect-ratio-container) */
        .student-card .image-aspect-ratio-container,  
        .teacher-card .image-aspect-ratio-container,  
        .family-card .image-aspect-ratio-container,
        .research-card .image-aspect-ratio-container {{
            padding-bottom: 66.66%; /* Consistent 3:2 aspect ratio for card images */
            margin-bottom: 0.5rem;
            height: auto; /* Let padding-bottom control height */
        }}
        
        /* Header Image Container (for smaller images with headings like Academic Performance) */
        .header-image-container {{
            display: block; width: 100%; height: 120px; /* Consistent fixed height for header images */
            overflow: hidden; border-radius: 8px; margin-top: 0.5rem; /* Space from heading */
            margin-bottom: 1rem; /* Space below header image */
            background: var(--gray-100); /* Fallback background for container */
            text-align: center; /* Center image horizontally */
        }}
        .header-image-container .image-aspect-ratio-container {{
            height: 100%; padding-bottom: 0; /* Make the aspect ratio container fill its explicit height */
            background: transparent; /* No background here, just let image fill */
        }}
        .header-image-container .image-aspect-ratio-container img {{
            object-fit: contain; /* Ensure full image is visible, no cropping for headers */
        }}

        /* Hero Image Container (for large banners at the top of pages) */
        .hero-image-container {{
            width: 100%;
            padding-bottom: 35%; /* Example: ~2.8:1 aspect ratio for a wide hero */
            overflow: hidden;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            background: var(--gray-100); /* Fallback background */
        }}
        .hero-image-container .image-aspect-ratio-container {{
            padding-bottom: 0; /* Fixed height for hero if container explicitly sized */
            height: 100%;
        }}
        .hero-image-container .image-aspect-ratio-container img {{
            object-fit: cover; /* Hero images usually cover, some cropping is okay */
        }}

        /* Login Container Specific Styling */
        .login-container {{
            max-width: 450px; /* Constrain width */
            margin: 50px auto; /* Center horizontally, add top/bottom margin */
            padding: 30px;
            background: white;
            border-radius: 12px;
            box-shadow: var(--shadow-lg);
            text-align: center;
        }}
        .login-container h1 {{
            color: var(--primary-purple); /* Match brand color */
            font-size: 2.2em;
            margin-bottom: 15px;
        }}
        .login-container .stMarkdown p {{
            color: var(--gray-700);
            font-size: 1.1em;
            margin-bottom: 25px;
        }}
        .login-container .stForm {{
            padding: 0; /* Remove default form padding */
            border: none; /* Remove default form border */
        }}
        .login-container .stTextInput label,
        .login-container .stSelectbox label,
        .login-container .stRadio label,
        .login-container .stCheckbox label {{
            font-weight: 500;
            color: var(--gray-700);
            text-align: left;
            display: block;
            margin-bottom: 5px;
        }}
        .login-container .stTextInput div[data-testid="stInputContainer"] input {{
            border-radius: 8px;
            border: 1px solid var(--gray-300);
            padding: 10px 14px;
            font-size: 1em;
            color: var(--gray-800);
        }}
        .login-container .stButton button {{
            width: 100%;
            padding: 12px 20px;
            font-size: 1.1em;
            font-weight: 600;
            border-radius: 8px;
            margin-top: 20px;
        }}
        .login-container hr {{
            margin-top: 30px;
            margin-bottom: 20px;
        }}
        .login-container h3 {{
            color: var(--gray-600);
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        .login-container ul {{
            list-style: none;
            padding: 0;
            margin: 0;
            color: var(--gray-500);
            font-size: 0.95em;
        }}
        .login-container ul li {{
            margin-bottom: 5px;
        }}


        /* Theme-specific CSS overrides (basic example) */
        body[data-theme="Dark"] {{
            background-color: var(--gray-900) !important;
            color: var(--gray-100) !important;
        }}
        body[data-theme="Dark"] .stApp::before, body[data-theme="Dark"] .main::before {{
            background: rgba(var(--gray-900-rgb),0.9) !important; /* Increased opacity for more blur */
        }}
        body[data-theme="Dark"] .main .block-container,
        body[data-theme="Dark"] .metric-card,
        body[data-theme="Dark"] .section-card,
        body[data-theme="Dark"] .chart-container, /* Changed from .chart-section */
        body[data-theme="Dark"] .css-1d391kg, body[data-theme="Dark"] .css-1cypcdb,
        body[data-theme="Dark"] .login-container
        {{
            background: var(--gray-800) !important;
            color: var(--gray-100) !important;
            border-color: var(--gray-700) !important;
            box-shadow: var(--shadow-xl) !important;
        }}
        body[data-theme="Dark"] .page-title, .metric-number, .chart-title {{
            color: var(--gray-100) !important;
        }}
        body[data-theme="Dark"] .page-subtitle, .metric-label, .chart-subtitle,
        body[data-theme="Dark"] .stSelectbox label, .stRadio > label, .stCheckbox > label,
        body[data-theme="Dark"] .sidebar-subtitle, .status-indicator span,
        body[data-theme="Dark"] .login-container .stMarkdown p,
        body[data-theme="Dark"] .login-container h3,
        body[data-theme="Dark"] .login-container ul li
        {{
            color: var(--gray-400) !important;
        }}

        body[data-theme="Dark"] .stButton button {{
            background: linear-gradient(135deg, var(--primary-purple), var(--secondary-blue)) !important;
            color: white !important;
            border-color: var(--primary-purple) !important;
            box-shadow: 0 4px 12px rgba(var(--primary-purple-rgb), 0.4) !important;
        }}
        body[data-theme="Dark"] .stButton button:hover {{ background: linear-gradient(135deg, #9b6cff, #4a94ff) !important; }}
        body[data-theme="Dark"] .metric-icon.total {{ background: linear-gradient(135deg, var(--primary-purple), var(--secondary-blue)); }}
        body[data-theme="Dark"] .metric-icon.on-track {{ background: linear-gradient(135deg, var(--success-green), #27a27b); }}
        body[data-theme="Dark"] .metric-icon.at-risk {{ background: linear-gradient(135deg, var(--warning-orange), #c26703); }}
        body[data-theme="Dark"] .metric-icon.intervention {{ background: linear-gradient(135deg, var(--danger-red), #b61c1c); }}
        body[data-theme="Dark"] .metric-change.positive {{ color: var(--success-green); }}
        body[data-theme="Dark"] .metric-change.negative {{ color: var(--danger-red); }}

        body[data-theme="Dark"] .status-badge.online {{ background: rgba(52, 211, 153, 0.2) !important; color: var(--success-green) !important; border-color: var(--success-green) !important; }}
        body[data-theme="Dark"] .status-badge.offline {{ background: rgba(251, 191, 36, 0.2) !important; color: var(--warning-orange) !important; border-color: var(--warning-orange) !important; }}

        /* Dark mode inputs */
        body[data-theme="Dark"] div[data-testid="stTextInput"] input, body[data-theme="Dark"] div[data-testid="stTextArea"] textarea, div[data-testid="stNumberInput"] input,
        body[data-theme="Dark"] .stSelectbox > div[data-testid="stSelectbox"] > div:first-child > div,
        body[data-theme="Dark"] .stRadio div[data-testid="stRadio"] label,
        body[data-theme="Dark"] .stCheckbox input[type="checkbox"]
        {{
            background: var(--gray-700) !important;
            border-color: var(--gray-600) !important;
            color: var(--gray-100) !important;
        }}
        body[data-theme="Dark"] .stSelectbox > div[data-testid="stSelectbox"] > div:first-child > div:hover {{ background: var(--gray-600) !important; }}
        body[data-theme="Dark"] .stRadio div[data-testid="stRadio"] label:hover {{ background: var(--gray-600) !important; }}
        body[data-theme="Dark"] .stSlider .st-fx {{ background: var(--gray-600); }}
        body[data-theme="Dark"] .stSlider .st-fy {{ background: linear-gradient(to right, var(--secondary-blue), var(--primary-purple)); }}
        body[data-theme="Dark"] .stSlider .st-fz {{ background: var(--gray-900); border-color: var(--primary-purple); }}

        body[data-theme="Dark"] .stDataFrame th {{ background: var(--gray-700) !important; color: var(--gray-300) !important; border-bottom-color: var(--gray-600) !important; }}
        body[data-theme="Dark"] .stDataFrame td {{ border-bottom-color: var(--gray-700) !important; }}
        body[data-theme="Dark"] .stDataFrame tbody tr:hover {{ background: var(--gray-700); }}

        /* Image Containers Dark Mode */
        body[data-theme="Dark"] .image-aspect-ratio-container,
        body[data-theme="Dark"] .hero-image-container,
        body[data-theme="Dark"] .header-image-container {{
            background: var(--gray-700); /* Darker background for contained images */
        }}
        body[data-theme="Dark"] .image-aspect-ratio-container span {{
            color: var(--gray-500); /* Darker fallback text */
        }}


        /* --- Responsive Design --- */
        /* Tablet (>= 768px and < 1200px) */
        @media (max-width: 1200px) and (min-width: 768px) {{
            .main .block-container {{
                margin-left: 1rem !important;
                margin-right: 1rem !important;
                width: calc(100% - 2rem) !important;
                padding: clamp(1rem, 3vw, 1.5rem) !important;
            }}
            
            div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {{
                flex-wrap: wrap;
                gap: 1rem;
                align-items: stretch;
            }}
            
            div[data-testid="stColumn"] {{
                min-width: 280px !important;
                flex-basis: calc(50% - 0.5rem) !important;
                width: auto !important;
                padding: 0 !important;
            }}
            
            .metric-card, .section-card, .chart-container, .glassy-container {{
                width: 100% !important;
                margin-bottom: 0 !important;
            }}
            
            .app-header-section {{
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }}
            .app-main-title, .app-subtitle-tagline, .app-status-tag {{
                flex-basis: 100%;
            }}
            .header-buttons {{
                width: 100%; justify-content: flex-start; flex-wrap: wrap; gap: 0.5rem;
            }}
            .stButton button {{ flex-grow: 1; min-width: unset; }}

            .hero-image-container {{ height: 200px; padding-bottom: 0; }}
            .image-gallery-grid .image-aspect-ratio-container {{ padding-bottom: 75%; height: auto; }}
            .header-image-container {{ height: 100px; }}
            .login-container {{ max-width: 70% !important; }}
            
            .glassy-chart-col {{ /* Specific styling for prediction charts */
                height: 400px; /* Fixed height for consistency on tablet */
                margin-bottom: 1rem;
            }}
            .stPlotlyChart {{ /* Ensure plotly chart fills its container */
                height: 100% !important;
            }}
        }}

        /* Mobile devices (max-width: 767px) */
        @media (max-width: 767px) {{
            .css-1d391kg, .css-1cypcdb {{ display: none !important; }}
            .main .block-container {{ margin-left: 0.5rem !important; margin-right: 0.5rem !important; width: calc(100% - 1rem) !important; padding: 1rem !important; }}
            
            .app-header-section {{ flex-direction: column; align-items: flex-start; margin-bottom: 1rem; text-align: left; }}
            .app-main-title {{ font-size: 1.5rem !important; margin-bottom: 0.5rem; }}
            .app-subtitle-tagline {{ font-size: 0.8rem !important; margin-bottom: 0.5rem; }}
            .app-status-tag {{ font-size: 0.7rem !important; padding: 3px 6px; margin-bottom: 1rem; }}
            .header-buttons {{ width: 100%; justify-content: flex-start; margin-top: 0; flex-wrap: wrap; gap: 0.5rem; }}
            .stButton button {{ flex: 1 1 auto; min-width: 120px; padding: 8px 12px; font-size: 0.8rem !important; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
            
            div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {{ flex-direction: column !important; gap: 1rem; }}
            div[data-testid="stColumn"] {{ width: 100% !important; flex-basis: auto !important; max-width: none !important; padding: 0 !important; margin: 0 !important; }}
            
            .metric-card, .section-card, .chart-container, .glassy-container {{ padding: 15px !important; margin-bottom: 1rem; width: 100% !important; }}
            
            .list-item {{ flex-wrap: wrap; align-items: flex-start; padding: 10px 0; }}
            .list-item .item-meta {{ flex-direction: column; align-items: flex-start; gap: 4px; width: 100%; margin-top: 0.5rem; }}
            .list-item .item-time {{ font-size: 0.7rem !important; }}
            .risk-badge {{ font-size: 0.6rem !important; padding: 2px 6px !important; }}
            
            .stSelectbox, .stRadio, .stCheckbox {{ margin-bottom: 1rem; }}
            .stSelectbox > div[data-testid="stSelectbox"] > div:first-child > div {{ padding: 10px 12px !important; font-size: 0.9rem !important; }}
            
            .stat-number {{ font-size: 2rem !important; margin-bottom: 0.3rem; }}
            .stat-label {{ font-size: 0.8rem !important; line-height: 1.2; }}
            .stat-subtitle {{ font-size: 0.75rem !important; line-height: 1.3; margin-top: 0.3rem; }}
            
            .hero-image-container {{ height: 120px; padding-bottom: 0; }}
            .image-gallery-grid .image-aspect-ratio-container {{ padding-bottom: 0; height: 80px; }}
            .header-image-container {{ height: 60px; }}
            .login-container {{ max-width: 90% !important; padding: 20px !important; }}
            
            .glassy-chart-col {{ /* Specific styling for prediction charts */
                height: 350px; /* Adjusted fixed height for mobile */
                margin-bottom: 1rem;
            }}
            .stPlotlyChart {{ /* Ensure plotly chart fills its container */
                height: 100% !important;
            }}
        }}

        /* Extra small devices (max-width: 480px) */
        @media (max-width: 480px) {{
            .main .block-container {{ margin: 0.25rem !important; width: calc(100% - 0.5rem) !important; padding: 0.75rem !important; border-radius: 8px !important; }}
            .app-main-title {{ font-size: 1.3rem !important; line-height: 1.1; }}
            .app-subtitle-tagline {{ font-size: 0.75rem !important; }}
            .metric-card, .section-card, .chart-container, .glassy-container {{ padding: 12px !important; border-radius: 8px !important; }}
            .stat-number {{ font-size: 1.8rem !important; }}
            .stButton button {{ padding: 6px 10px !important; font-size: 0.75rem !important; min-height: 36px !important; }}
            
            .sidebar-title, .sidebar-subtitle, .app-main-title, .app-subtitle-tagline, .stat-label, .stat-subtitle, .list-item .item-title, .list-item .item-subtitle {{
                word-break: break-word; overflow-wrap: anywhere; hyphens: auto;
            }}
            .hero-image-container {{ height: 80px; }}
            .image-gallery-grid .image-aspect-ratio-container {{ height: 50px; }}
            .header-image-container {{ height: 40px; }}
            
            .glassy-chart-col {{ /* Specific styling for prediction charts */
                height: 300px; /* Further adjusted fixed height for extra small mobile */
            }}
        }}

        /* Animations */
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        @keyframes slideInDown {{ from {{ opacity: 0; transform: translateY(-20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        @keyframes slideInRight {{ from {{ opacity: 0; transform: translateX(-10px); }} to {{ opacity: 1; transform: translateX(0); }} }}
        @keyframes pulseDot {{ 0% {{ transform: scale(1); opacity: 1; }} 50% {{ transform: scale(1.1); opacity: 0.7; }} 100% {{ transform: scale(1); opacity: 1; }} }}
        @keyframes scaleIn {{ from {{ opacity: 0; transform: scale(0.9); }} to {{ opacity: 1; transform: scale(1); }} }}
    </style>
    """, unsafe_allow_html=True)


def render_exact_sidebar(): # This function remains as the main sidebar renderer
    """Render the modern sidebar with improved styling"""
    with st.sidebar:
        # Modern brand section
        st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-logo">ES</div>
            <div>
                <div class="sidebar-title">EduScan</div>
                <div class="sidebar-subtitle">Learning Assessment Tool</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation section
        st.markdown('<div class="nav-section-header">Navigation</div>', unsafe_allow_html=True)
        
        # Get user role for conditional navigation
        user_role = st.session_state.get("role") # Use session state directly
        language = st.session_state.get('app_language', 'English')
        
        # Navigation links (using st.page_link for Streamlit's MPA routing)
        st.page_link("app.py", label=get_text('dashboard', language), icon=":material/dashboard:")
        st.page_link("pages/01_Prediction.py", label=get_text('prediction', language), icon=":material/search:")

        if user_role in ['teacher', 'admin']:
            st.page_link("pages/02_Teacher_Resources.py", label=get_text('teacher_resources', language), icon=":material/school:")
        if user_role in ['parent', 'admin']:
            st.page_link("pages/03_Parent_Tracker.py", label=get_text('parent_tracker', language), icon=":material/family_restroom:")
            
        st.page_link("pages/04_Educational_Content.py", label=get_text('educational_content', language), icon=":material/menu_book:")
        
        st.markdown("<hr>", unsafe_allow_html=True) # Separator below navigation

        # --- Settings Section in Sidebar ---
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        st.markdown('<div class="nav-section-header">Settings</div>', unsafe_allow_html=True)

        # Language selector
        st.markdown('<p class="settings-label">Language</p>', unsafe_allow_html=True) # Custom label for better alignment
        current_language = st.session_state.get('app_language', 'English')
        languages = {'English': 'English', 'Somali': 'Somali', 'Arabic': 'Arabic'}
        selected_language = st.selectbox(
            "Select Language", # Streamlit label, will be collapsed
            list(languages.keys()),
            index=list(languages.keys()).index(current_language),
            key="sidebar_lang_select_all_pages",
            label_visibility="collapsed" # Hide default Streamlit label
        )

        if selected_language != current_language:
            st.session_state['app_language'] = selected_language
            settings = load_app_settings()
            settings['language'] = selected_language
            save_app_settings(settings)
            st.rerun()

        # Theme selector
        st.markdown('<p class="settings-label">Theme</p>', unsafe_allow_html=True) # Custom label
        current_theme = st.session_state.get('app_theme', 'Light')
        themes = ['Light', 'Dark', 'System'] # Changed 'EduScan Theme' to 'System' for consistency with OS preference
        selected_theme = st.radio(
            "Choose Theme", # Streamlit label, will be collapsed
            themes,
            index=themes.index(current_theme),
            key="sidebar_theme_select_all_pages",
            horizontal=True,
            label_visibility="collapsed" # Hide default Streamlit label
        )

        if selected_theme != current_theme:
            st.session_state['app_theme'] = selected_theme
            settings = load_app_settings()
            settings['theme'] = selected_theme
            save_app_settings(settings)
            st.markdown(f"""
                <script>
                    document.body.setAttribute('data-theme', '{selected_theme}');
                </script>
            """, unsafe_allow_html=True)
            st.rerun()

        # Offline mode toggle
        st.markdown('<p class="settings-label">Connection</p>', unsafe_allow_html=True) # Custom label
        current_offline = st.session_state.get('offline_mode', False)
        # Use a more explicit label for the checkbox itself, but keep it as a Streamlit widget.
        offline_mode = st.checkbox(
            "Offline Mode", # Actual label visible
            value=current_offline,
            key="sidebar_offline_toggle_all_pages",
        )

        if offline_mode != current_offline:
            st.session_state['offline_mode'] = offline_mode
            settings = load_app_settings()
            settings['offline_mode'] = offline_mode
            save_app_settings(settings)
            st.rerun()

        # Status indicator
        is_offline_status = st.session_state.get('offline_mode', False)
        status_text = get_text('offline_mode', language) if is_offline_status else get_text('online_mode', language)
        status_dot_class = "status-offline" if is_offline_status else "status-online"
        
        st.markdown(f"""
        <div class="status-indicator">
            <div style="display: flex; align-items: center;">
                <div class="status-dot {status_dot_class}"></div>
                <span style="font-size: 14px; font-weight: 500;">Status: {status_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True) # Close settings-section

        # Logout button (only if authenticated)
        if is_authenticated():
            st.markdown("---")
            if st.button(":material/logout: Logout", use_container_width=True, key="sidebar_logout_button"): # Added Material Icon
                logout_user()

def render_exact_page_header(icon_html, title_key, subtitle_key, language): # Changed icon_emoji to icon_html
    """Render modern page header"""
    is_offline = st.session_state.get('offline_mode', False)
    status_class = "status-badge offline" if is_offline else "status-badge"
    status_text = get_text('offline_mode', language) if is_offline else get_text('online_mode', language)
    
    st.markdown(f"""
    <div class="page-header section-animated-text">
        <h1 class="page-title">{icon_html} {get_text(title_key, language)}</h1>
        <p class="page-subtitle">{get_text(subtitle_key, language)}</p>
        <div class="{status_class}">
            <div class="status-dot {'status-offline' if is_offline else 'status-online'}"></div>
            {status_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_exact_metric_card(label_key, number, change_text, icon_html, icon_class, change_type="positive"): # Renamed from create_modern_metric_card
    """Create a modern metric card"""
    change_class = f"metric-change {change_type}"
    language = st.session_state.get('app_language', 'English')
    
    return f"""
    <div class="metric-card">
        <div class="metric-header">
            <div class="metric-label">{get_text(label_key, language)}</div>
            <div class="metric-icon {icon_class}">{icon_html}</div>
        </div>
        <div class="metric-number">{number}</div>
        <div class="{change_class}">{change_text}</div>
    </div>
    """

def create_exact_chart_container(title, subtitle, content_html=""): # Renamed from create_modern_chart_container
    """Create a modern chart container"""
    # content_html is expected to be raw HTML that will be placed inside
    return f"""
    <div class="chart-container">
        <h3 class="chart-title">{title}</h3>
        <p class="chart-subtitle">{subtitle}</p>
        {content_html}
    </div>
    """

def get_b64_image_html(base64_data, alt_text, aspect_ratio="16/9", cover_mode=False):
    """
    Generates HTML for a base64 image, wrapped in an aspect-ratio-controlled container.
    If base64_data is empty, it renders an animated fallback.
    
    Args:
        base64_data (str): The base64 encoded image string (e.g., "data:image/jpeg;base64,...").
        alt_text (str): Alt text for the image.
        aspect_ratio (str): Aspect ratio as "width/height" (e.g., "16/9", "4/3", "1/1").
        cover_mode (bool): If True, object-fit is 'cover'. If False, 'contain'.
    Returns:
        str: HTML string for the image container.
    """
    object_fit_class = "object-fit-cover-mode" if cover_mode else ""
    
    # Calculate padding-bottom for aspect ratio trick
    padding_bottom_percentage = "56.25%" # Default to 16:9
    if aspect_ratio == "4/3":
        padding_bottom_percentage = "75%"
    elif aspect_ratio == "1/1":
        padding_bottom_percentage = "100%"
    elif aspect_ratio == "3/2": # Common for card images
        padding_bottom_percentage = "66.66%"
    elif aspect_ratio == "2.5/1": # Common for hero images
        padding_bottom_percentage = "40%"
    elif aspect_ratio == "2/1": # Common for header images
        padding_bottom_percentage = "50%"
    elif aspect_ratio == "3/1": # For very wide banners
        padding_bottom_percentage = "33.33%"
    else:
        try:
            w, h = map(int, aspect_ratio.split('/'))
            padding_bottom_percentage = f"{(h/w * 100):.2f}%"
        except ValueError:
            pass # Keep default if custom aspect_ratio is invalid

    if not base64_data:
        # Animated fallback div if image not found
        # Use a relevant Material Icon based on alt_text or a generic one
        icon_name = "visibility_off" # Default if no specific icon applies
        if "Academic" in alt_text or "Learning" in alt_text or "Student" in alt_text:
            icon_name = "school"
        elif "Teacher" in alt_text:
            icon_name = "person_add"
        elif "Parent" in alt_text or "Family" in alt_text:
            icon_name = "family_restroom"
        elif "Research" in alt_text or "Science" in alt_text:
            icon_name = "science"
        elif "Assessment" in alt_text:
            icon_name = "quiz"
        elif "Math" in alt_text:
            icon_name = "calculate"
        elif "Reading" in alt_text:
            icon_name = "book_4"
        elif "Writing" in alt_text:
            icon_name = "edit"
        elif "Behavioral" in alt_text:
            icon_name = "sentiment_satisfied"
        
        return f"""
        <div class="image-aspect-ratio-container animated-fallback" style="padding-bottom: {padding_bottom_percentage};">
            <span class="material-symbols-outlined">{icon_name}</span>
            <span>{alt_text}</span>
        </div>
        """
    
    return f"""
    <div class="image-aspect-ratio-container {object_fit_class}" style="padding-bottom: {padding_bottom_percentage};">
        <img src="{base64_data}" alt="{alt_text}">
    </div>
    """