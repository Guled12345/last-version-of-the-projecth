# utils/image_base64.py
"""
Base64 encoded essential images for reliable display.
Removed most static images, keeping only background and AI result visuals.
"""
import base64
import os

def get_base64_images():
    """Get base64 encoded essential images (background and AI result visuals)."""
    
    def image_to_base64(filename):
        image_path = os.path.join(os.path.dirname(__file__), '..', 'pictures', filename)
        try:
            if os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    return base64.b64encode(img_file.read()).decode('utf-8')
            else:
                print(f"Warning: Image not found at {image_path}. Skipping base64 encoding.")
                return None
        except Exception as e:
            print(f"Error converting {image_path} to base64: {e}")
            return None
    
    # --- Only load essential images ---
    # 1. Main Background Image
    image_83d859_b64 = image_to_base64('image_83d859.jpg')

    # 2. AI Assessment Results Stage Images (as specifically requested to keep)
    academic_performance_b64 = image_to_base64('academic_performance.png') # Often used as exam/chart visual
    girl_reading_book_b64 = image_to_base64('girl reading book.jpg') # Can represent student writing/learning
    smiling_girl_b64 = image_to_base64('smiling girl.jpeg') # Can represent student portrait

    # 3. Specific request to keep 'somali-children-in-class.jpg' for recommendations section
    somali_children_in_class_b64 = image_to_base64('somali-children-in-class.jpg')

    return {
        'image_83d859': f'data:image/jpeg;base64,{image_83d859_b64}' if image_83d859_b64 else '',
        
        # AI Assessment Results specific images
        'academic_performance': f'data:image/png;base64,{academic_performance_b64}' if academic_performance_b64 else '',
        'exam_students': f'data:image/png;base64,{academic_performance_b64}' if academic_performance_b64 else '', # Reusing as a general "exam" visual
        'behavioral_social': f'data:image/png;base64,{academic_performance_b64}' if academic_performance_b64 else '', # Reusing for consistency
        'student_writing': f'data:image/jpeg;base64,{girl_reading_book_b64}' if girl_reading_book_b64 else '',
        'student_portrait': f'data:image/jpeg;base64,{smiling_girl_b64}' if smiling_girl_b64 else '',
        'somali_children_in_class': f'data:image/jpeg;base64,{somali_children_in_class_b64}' if somali_children_in_class_b64 else '',

        # Provide empty strings for keys that are no longer actively mapped to specific images,
        # but might still be referenced in old page code for safety during refactor.
        # This prevents KeyError but will show the 'Not Found' fallback.
        'abc_kids': '', 'girls_in_class': '', 'girls_in_white_hijab': '', 'girls_in_orange_hijab': '',
        'kindergarten': '', 'small_kids_and_teacher': '', 'three_somali_girls': '',
        'student_information_2': '', # Was a placeholder header image
        'daily_tracking': '', 'parent_empowerment': '', 'school_partnership': '',
        'educational_excellence_1': '', 'global_practices': '', 'learning_science': '', 'intervention_studies': '', 'cultural_adaptation': '',
        'teacher_with_students': '', 'happy_young_students': '', 'classroom_girls': '', 'boys_in_classroom': '',
        'engaging_strategies': '', 'assessment_innovation': '',
    }

def get_b64_image_html(base64_data, alt_text, aspect_ratio="16/9", cover_mode=False):
    """
    Generates HTML for a base64 image, wrapped in an aspect-ratio-controlled container.
    
    Args:
        base64_data (str): The base64 encoded image string (e.g., "data:image/jpeg;base64,...").
        alt_text (str): Alt text for the image.
        aspect_ratio (str): Aspect ratio as "width/height" (e.g., "16/9", "4/3", "1/1").
        cover_mode (bool): If True, object-fit is 'cover'. If False, 'contain'.
    Returns:
        str: HTML string for the image container.
    """
    object_fit_class = "object-fit-cover-mode" if cover_mode else ""
    
    padding_bottom_percentage = "56.25%" # Default to 16:9
    if aspect_ratio == "4/3": padding_bottom_percentage = "75%"
    elif aspect_ratio == "1/1": padding_bottom_percentage = "100%"
    else:
        try:
            w, h = map(int, aspect_ratio.split('/'))
            padding_bottom_percentage = f"{(h/w * 100):.2f}%"
        except ValueError: pass

    if not base64_data:
        # Fallback div if image not found (now with transparent background by default)
        return f"""
        <div class="image-aspect-ratio-container" style="padding-bottom: {padding_bottom_percentage}; background: transparent;">
            <span style="color: var(--gray-500); text-align:center; font-size:0.8em; padding:10px;">Image:<br>{alt_text}<br>(Not Found)</span>
        </div>
        """
    
    return f"""
    <div class="image-aspect-ratio-container {object_fit_class}" style="padding-bottom: {padding_bottom_percentage};">
        <img src="{base64_data}" alt="{alt_text}">
    </div>
    """