# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
import json
import os
import pickle
import random

# Import utilities
from utils.language_utils import get_text, load_app_settings, save_app_settings
from utils.data_utils import load_student_data
from utils.auth_utils import is_authenticated, render_login_page, logout_user, get_user_role
from utils.image_base64 import get_base64_images # Import get_base64_images for its dictionary

# Corrected: All UI functions now imported from utils.exact_ui
from utils.exact_ui import (
    add_exact_ui_styles, # Apply overall app styles
    render_exact_sidebar, # Sidebar structure and fixed content, including settings
    render_exact_page_header, # Global header rendering function (without settings button)
    create_exact_metric_card, # Helper for individual stat cards (used on Dashboard)
    create_exact_chart_container, # Helper for chart containers
    get_b64_image_html # Helper for rendering base64 images within HTML
)
from utils.icon_utils import ( # Icons are used within metric cards
    get_total_students_icon, get_on_track_icon,
    get_at_risk_icon, get_intervention_icon,
    get_material_icon_html # NEW: Import for specific Material Icons in header
)

# IMPORTANT: Page config MUST be the first Streamlit command
st.set_page_config(
    page_title="EduScan - Learning Assessment Dashboard", # More readable title
    page_icon=get_material_icon_html("school"), # Replaced emoji with Material Icon HTML
    layout="wide",
    initial_sidebar_state="expanded" # Default state (can be 'collapsed' for production)
)

# Apply modern UI styles - CRITICAL to be at the top
add_exact_ui_styles()

# Initialize session state for settings
if 'app_language' not in st.session_state:
    settings = load_app_settings()
    st.session_state['app_language'] = settings.get('language', 'English')
if 'offline_mode' not in st.session_state:
    settings = load_app_settings()
    st.session_state['offline_mode'] = settings.get('offline_mode', False)
if 'app_theme' not in st.session_state:
    settings = load_app_settings()
    st.session_state['app_theme'] = settings.get('theme', 'Light') # Default theme

# Get current language
language = st.session_state.get('app_language', 'English')

# Apply theme-specific body attribute via JavaScript to allow CSS targeting
current_theme = st.session_state.get('app_theme', 'Light')
st.markdown(f"""
    <script>
        document.body.setAttribute('data-theme', '{current_theme}');
    </script>
""", unsafe_allow_html=True)


# --- Dashboard Content Rendering Function ---
def render_dashboard_page_content():
    """Renders the main content of the Dashboard page."""
    
    # Top Header Section with improved readability
    render_exact_page_header(get_material_icon_html("dashboard"), 'Educational Assessment Dashboard', 'Comprehensive Learning Analytics Platform', language)

    st.markdown("<h3 style='font-size:1.5rem; font-weight:600; color:var(--gray-900); margin-bottom:1.5rem;'>System Overview</h3>", unsafe_allow_html=True)
    
    # --- Fetch actual data for dashboard stats ---
    all_student_data = load_student_data()
    df_students = pd.DataFrame(all_student_data)

    total_students = len(df_students)
    
    # Calculate new students this month (example: last 30 days)
    new_this_month = 0
    if not df_students.empty:
        df_students['timestamp'] = pd.to_datetime(df_students['timestamp'])
        one_month_ago = datetime.now() - timedelta(days=30)
        new_this_month = df_students[df_students['timestamp'] >= one_month_ago].shape[0]

    on_track_count = 0
    at_risk_count = 0
    intervention_count = 0
    
    if not df_students.empty:
        # Assuming 'risk_level' is stored as 'Low Risk', 'Medium Risk', 'High Risk'
        on_track_count = df_students[df_students['risk_level'] == 'Low Risk'].shape[0]
        at_risk_count = df_students[df_students['risk_level'] == 'Medium Risk'].shape[0]
        intervention_count = df_students[df_students['risk_level'] == 'High Risk'].shape[0]

    on_track_percentage = (on_track_count / total_students * 100) if total_students > 0 else 0
    at_risk_percentage = (at_risk_count / total_students * 100) if total_students > 0 else 0
    
    # Render Stat Cards with readable labels
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(create_exact_metric_card('Total Students', total_students, f"↑ {new_this_month} new this month", get_total_students_icon(), 'total'), unsafe_allow_html=True)
    with col2:
        st.markdown(create_exact_metric_card('Students On Track', on_track_count, f"↑ {on_track_percentage:.0f}% performing well", get_on_track_icon(), 'on-track'), unsafe_allow_html=True)
    with col3:
        st.markdown(create_exact_metric_card('Students At Risk', at_risk_count, f"↑ {at_risk_percentage:.0f}% need support", get_at_risk_icon(), 'at-risk', change_type="negative"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_exact_metric_card('Need Intervention', intervention_count, f"↑ {(intervention_count / total_students * 100):.0f}% urgent attention" if total_students > 0 else "↑ 0% urgent attention", get_intervention_icon(), 'intervention', change_type="negative"), unsafe_allow_html=True)
    
    # --- Performance Charts with readable titles ---
    st.markdown("<h3 style='font-size:1.5rem; font-weight:600; color:var(--gray-900); margin-top:2.5rem; margin-bottom:1.5rem;'>Performance Insights</h3>", unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        subjects = ['Mathematics', 'Reading', 'Writing', 'Science', 'Social Studies']
        
        if not df_students.empty and all(col in df_students.columns for col in ['math_score', 'reading_score', 'writing_score']):
            df_students_copy = df_students.copy()
            if 'science_score' not in df_students_copy.columns:
                df_students_copy['science_score'] = df_students_copy[['math_score', 'reading_score', 'writing_score']].mean(axis=1) * 1.05
            if 'social_studies_score' not in df_students_copy.columns:
                df_students_copy['social_studies_score'] = df_students_copy[['math_score', 'reading_score', 'writing_score']].mean(axis=1) * 1.02

            avg_scores = df_students_copy[['math_score', 'reading_score', 'writing_score', 'science_score', 'social_studies_score']].mean().to_dict()
            
            scores_display = [
                avg_scores.get('math_score', 0),
                avg_scores.get('reading_score', 0),
                avg_scores.get('writing_score', 0),
                avg_scores.get('science_score', 0),
                avg_scores.get('social_studies_score', 0)
            ]
        else:
            scores_display = [75, 82, 70, 78, 80]

        # Use px.bar and map subjects to color for distinct colors
        fig_bar = px.bar(
            x=subjects,
            y=scores_display,
            title="",
            labels={'x': 'Subjects', 'y': 'Average Score (%)'},
            # Use a categorical color mapping for distinct colors
            color=subjects, # Map colors by subject name
            color_discrete_sequence=px.colors.qualitative.Plotly # Or choose another palette like 'Pastel', 'Set1', etc.
        )
        
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='var(--gray-700)'),
            showlegend=False, # We don't need a legend if colors are tied to x-axis labels
            margin=dict(l=0, r=0, t=20, b=0),
            height=350,
            xaxis=dict(gridcolor='var(--gray-200)', showgrid=True),
            yaxis=dict(gridcolor='var(--gray-200)', showgrid=True, range=[0,100])
        )
        
        st.markdown(create_exact_chart_container(
            f"{get_material_icon_html('trending_up', 'outlined')} <span style='color: var(--gray-900); font-weight: 600;'>Academic Performance by Subject</span>",
            "<span style='color: var(--gray-800);'>Average scores across all core academic subjects</span>",
        ), unsafe_allow_html=True)
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        risk_labels = ['Students On Track', 'Students At Risk', 'Need Intervention']
        risk_values = [on_track_count, at_risk_count, intervention_count]
        risk_colors = ['var(--success-green)', 'var(--warning-orange)', 'var(--danger-red)']
        
        filtered_labels = [label for i, label in enumerate(risk_labels) if risk_values[i] > 0]
        filtered_values = [value for value in risk_values if value > 0]
        filtered_colors = [risk_colors[i] for i, value in enumerate(risk_values) if value > 0]

        if not filtered_values:
            fig_pie = go.Figure(data=[go.Pie(labels=['No Data Available'], values=[1], marker_colors=['var(--gray-400)'], hole=.4, textinfo='label')])
        else:
            fig_pie = go.Figure(data=[go.Pie(
                labels=filtered_labels,
                values=filtered_values,
                marker_colors=filtered_colors,
                hole=.4,
                textinfo='percent+label',
                insidetextorientation='radial',
                pull=[0.1 if 'Intervention' in label else 0 for label in filtered_labels]
            )])
        
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='var(--gray-700)'),
            showlegend=True,
            margin=dict(l=0, r=0, t=20, b=0),
            height=350,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(size=10)
            )
        )
        fig_pie.update_traces(
            textfont_color="white",
            textfont_size=14,
            marker=dict(line=dict(color='var(--white)', width=1))
        )
        
        st.markdown(create_exact_chart_container(
            f"{get_material_icon_html('pie_chart')} <span style='color: var(--gray-900); font-weight: 600;'>Student Risk Assessment Distribution</span>",
            "<span style='color: var(--gray-800);'>Overview of student learning risk levels</span>",
        ), unsafe_allow_html=True)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Recent assessments table with readable headers
    st.markdown(create_exact_chart_container(
        f"{get_material_icon_html('grading')} <span style='color: var(--gray-900); font-weight: 600;'>Recent Assessment Results</span>",
        "<span style='color: var(--gray-800);'>Latest student assessment data and risk evaluations</span>"
    ), unsafe_allow_html=True)
    
    if not df_students.empty:
        df_recent = df_students.sort_values(by='timestamp', ascending=False).head(5)
        display_columns = ['student_name', 'grade_level', 'math_score', 'reading_score', 'risk_level']
        
        for col in display_columns:
            if col not in df_recent.columns:
                df_recent[col] = np.nan
        
        df_display = df_recent[display_columns].copy()
        df_display.columns = ['Student Name', 'Grade Level', 'Math Score (%)', 'Reading Score (%)', 'Risk Assessment']
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        sample_data = {
            'Student Name': ['No assessment data available yet'],
            'Grade Level': ['N/A'],
            'Math Score (%)': [0],
            'Reading Score (%)': [0],
            'Risk Assessment': ['N/A']
        }
        st.dataframe(pd.DataFrame(sample_data), use_container_width=True, hide_index=True)

    # Performance trends chart with better description
    st.markdown(create_exact_chart_container(
        f"{get_material_icon_html('analytics')} <span style='color: var(--gray-900); font-weight: 600;'>Monthly Performance Trends</span>",
        "<span style='color: var(--gray-800);'>Track average subject performance changes over time</span>"
    ), unsafe_allow_html=True)
    
    if not df_students.empty:
        df_students['month_year'] = df_students['timestamp'].dt.to_period('M').astype(str)
        monthly_avg = df_students.groupby('month_year')[['math_score', 'reading_score']].mean().reset_index()
        monthly_avg.columns = ['Month-Year', 'Mathematics Average', 'Reading Average']
        monthly_avg = monthly_avg.sort_values(by='Month-Year')

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=monthly_avg['Month-Year'], y=monthly_avg['Mathematics Average'],
            mode='lines+markers',
            name='Mathematics',
            line=dict(color='var(--primary-purple)', width=3),
            marker=dict(size=8)
        ))
        fig_line.add_trace(go.Scatter(
            x=monthly_avg['Month-Year'], y=monthly_avg['Reading Average'],
            mode='lines+markers',
            name='Reading',
            line=dict(color='var(--success-green)', width=3),
            marker=dict(size=8)
        ))
    else:
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
        math_trend = [72, 74, 76, 79, 78, 81, 85]
        reading_trend = [75, 76, 78, 80, 82, 80, 78]
        
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=months, y=math_trend,
            mode='lines+markers',
            name='Mathematics',
            line=dict(color='var(--primary-purple)', width=3),
            marker=dict(size=8)
        ))
        fig_line.add_trace(go.Scatter(
            x=months, y=reading_trend,
            mode='lines+markers',
            name='Reading',
            line=dict(color='var(--success-green)', width=3),
            marker=dict(size=8)
        ))
    
    fig_line.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='var(--gray-700)'),
        showlegend=True,
        margin=dict(l=60, r=40, t=40, b=60),  # Increased margins for full visibility
        height=450,  # Increased height for better display
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",  # Center the legend
            x=0.5
        ),
        xaxis=dict(
            gridcolor='var(--gray-200)', 
            showgrid=True, 
            title="Time Period",
            title_font=dict(size=14, color='var(--gray-700)'),
            tickfont=dict(size=12, color='var(--gray-600)'),
            showline=True,
            linecolor='var(--gray-300)',
            mirror=True
        ),
        yaxis=dict(
            gridcolor='var(--gray-200)', 
            showgrid=True, 
            range=[65,90], 
            title="Average Score (%)",
            title_font=dict(size=14, color='var(--gray-700)'),
            tickfont=dict(size=12, color='var(--gray-600)'),
            showline=True,
            linecolor='var(--gray-300)',
            mirror=True
        ),
        # Add hover styling
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='white',
            font_size=12,
            font_family='Inter'
        )
    )
    
    st.plotly_chart(fig_line, use_container_width=True)

def main():
    """Main application function"""
    # Render sidebar
    render_exact_sidebar()

    # Check authentication
    if not is_authenticated():
        render_login_page()
        return
    
    # Render dashboard
    render_dashboard_page_content()

if __name__ == "__main__":
    main()