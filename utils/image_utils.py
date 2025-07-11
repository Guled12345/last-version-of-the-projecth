import streamlit as st
import base64
import os
from PIL import Image
import io

def load_image_as_base64(image_path):
    """Load an image file and convert it to base64 string"""
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
        return None
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None

def get_image_html(image_path, alt_text="Student Image", width="100%", height="auto", border_radius="15px"):
    """Generate HTML for displaying an image with styling"""
    base64_image = load_image_as_base64(image_path)
    if base64_image:
        return f"""
        <img src="data:image/jpeg;base64,{base64_image}" 
             alt="{alt_text}"
             style="width: {width}; 
                    height: {height}; 
                    border-radius: {border_radius};
                    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
                    margin: 1rem 0;
                    object-fit: cover;
                    transition: transform 0.3s ease;"
             onmouseover="this.style.transform='scale(1.02)'"
             onmouseout="this.style.transform='scale(1)'">
        """
    else:
        return f"""
        <div style="width: {width}; 
                    height: 200px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: {border_radius};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 1.2rem;
                    margin: 1rem 0;">
            {alt_text}
        </div>
        """

def create_image_gallery(image_paths, alt_texts, columns=3):
    """Create a gallery of images in columns"""
    cols = st.columns(columns)
    
    for i, (image_path, alt_text) in enumerate(zip(image_paths, alt_texts)):
        with cols[i % columns]:
            base64_image = load_image_as_base64(image_path)
            if base64_image:
                st.markdown(f"""
                <div style="text-align: center; margin: 1rem 0;">
                    <img src="data:image/jpeg;base64,{base64_image}" 
                         alt="{alt_text}"
                         style="width: 100%; 
                                height: 200px; 
                                border-radius: 15px;
                                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
                                object-fit: cover;
                                transition: transform 0.3s ease;"
                         onmouseover="this.style.transform='scale(1.05)'"
                         onmouseout="this.style.transform='scale(1)'">
                    <p style="margin-top: 0.5rem; font-weight: 500; color: #2c3e50;">{alt_text}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="text-align: center; margin: 1rem 0;">
                    <div style="width: 100%; 
                                height: 200px; 
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                border-radius: 15px;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                color: white;
                                font-size: 1.2rem;">
                        {alt_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)

def get_student_images():
    """Get paths to all student images including new authentic Somali student photos"""
    return {
        # New authentic Somali student images
        'classroom_girls': 'attached_assets/ph_20447_72936_1751965339103.jpg',
        'happy_young_students': 'attached_assets/20220420_Slaight Preprimary Education_Garowe_Hill (6)_1751965339106.jpg',
        'teacher_with_students': 'attached_assets/image_2_1751965339106.jpg',
        'boys_in_classroom': 'attached_assets/somalia-children-in-class_1751965339107.jpg',
        
        # Original images as backup
        'exam_students': 'data/Exam-Students_1751918889656.jpg',
        'focused_student': 'data/Ez0BdyeWUAQeFjt_1751918889659.jpg', 
        'happy_students': 'data/IMG_340E6A-360708-5A7F82-28A32F-B00A0B-5C1E93_1751918889660.jpg',
        'student_portrait': 'data/thumbnail_1751918889660.jpg'
    }