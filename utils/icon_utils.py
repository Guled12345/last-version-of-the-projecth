# utils/icon_utils.py
"""
Material Symbols icons for EduScan application.
"""

def get_material_icon_html(icon_name, style="outlined"):
    """
    Returns HTML for a Material Symbol icon.
    'style' can be 'outlined', 'rounded', 'sharp', 'filled'.
    """
    if style == "filled":
        # Filled style uses a different class
        return f'<span class="material-symbols-fill">{icon_name}</span>'
    return f'<span class="material-symbols-{style}">{icon_name}</span>'

# Dashboard Icons
def get_dashboard_icon(): return get_material_icon_html("dashboard")
def get_assessment_icon(): return get_material_icon_html("quiz") # Or "assessment"
def get_teacher_icon(): return get_material_icon_html("school")
def get_parent_icon(): return get_material_icon_html("family_restroom")
def get_research_icon(): return get_material_icon_html("science")

# Status Icons
def get_checkmark_icon(): return get_material_icon_html("check_circle")
def get_warning_icon(): return get_material_icon_html("warning")
def get_error_icon(): return get_material_icon_html("error")
def get_settings_icon(): return get_material_icon_html("settings")

# Metric Card Icons (Specific to Dashboard)
def get_total_students_icon(): return get_material_icon_html("group")
def get_on_track_icon(): return get_material_icon_html("track_changes") # Or "trending_up"
def get_at_risk_icon(): return get_material_icon_html("priority_high") # Or "warning"
def get_intervention_icon(): return get_material_icon_html("crisis_alert") # Or "support_agent"

# Other commonly used icons in content
def get_lightbulb_icon(): return get_material_icon_html("lightbulb")
def get_rocket_icon(): return get_material_icon_html("rocket_launch")
def get_puzzle_icon(): return get_material_icon_html("extension")
def get_brain_icon(): return get_material_icon_html("psychology")
def get_chart_line_icon(): return get_material_icon_html("monitoring")
def get_chart_pie_icon(): return get_material_icon_html("pie_chart")
def get_table_icon(): return get_material_icon_html("table_chart")
def get_ruler_icon(): return get_material_icon_html("straighten") # For assessment tools/strategies
def get_gamepad_icon(): return get_material_icon_html("gamepad") # For interactive activities
def get_book_icon(): return get_material_icon_html("book_4") # For educational content/reading
def get_laptop_icon(): return get_material_icon_html("laptop_mac") # For technology tools
def get_handshake_icon(): return get_material_icon_html("handshake") # For support strategies
def get_school_icon(): return get_material_icon_html("school")
def get_family_icon(): return get_material_icon_html("family_restroom")
def get_admin_icon(): return get_material_icon_html("manage_accounts") # Or "admin_panel_settings"
def get_student_icon(): return get_material_icon_html("person")