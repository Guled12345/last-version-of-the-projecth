"""
Educational image utility functions for EduScan Somalia
Provides diverse educational SVG images and graphics
"""

def get_classroom_scene():
    """Classroom learning scene SVG"""
    return """
    <svg width="300" height="200" viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg">
        <!-- Classroom background -->
        <rect width="300" height="200" fill="#f0f9ff"/>
        <!-- Blackboard -->
        <rect x="20" y="30" width="80" height="50" fill="#2d3748" rx="4"/>
        <text x="60" y="50" text-anchor="middle" fill="white" font-size="12">Math</text>
        <text x="60" y="65" text-anchor="middle" fill="white" font-size="10">2 + 3 = 5</text>
        
        <!-- Students -->
        <g id="student1">
            <circle cx="150" cy="100" r="15" fill="#8B4513"/>
            <rect x="145" y="115" width="10" height="25" fill="#4CAF50"/>
            <circle cx="145" cy="130" r="3" fill="#FFD700"/>
            <circle cx="155" cy="130" r="3" fill="#FFD700"/>
        </g>
        
        <g id="student2">
            <circle cx="200" cy="100" r="15" fill="#DEB887"/>
            <rect x="195" y="115" width="10" height="25" fill="#2196F3"/>
            <circle cx="195" cy="130" r="3" fill="#FFD700"/>
            <circle cx="205" cy="130" r="3" fill="#FFD700"/>
        </g>
        
        <!-- Teacher -->
        <g id="teacher">
            <circle cx="60" cy="90" r="18" fill="#A0522D"/>
            <rect x="52" y="108" width="16" height="30" fill="#800080"/>
            <rect x="75" y="95" width="8" height="15" fill="#8B4513"/>
        </g>
        
        <!-- Books and supplies -->
        <rect x="250" y="140" width="20" height="15" fill="#FF4444" rx="2"/>
        <rect x="270" y="135" width="20" height="15" fill="#44FF44" rx="2"/>
        <circle cx="230" cy="160" r="8" fill="#4444FF"/>
        
        <text x="150" y="190" text-anchor="middle" fill="#FF6B35" font-weight="bold" font-size="14">Engaged Learning</text>
    </svg>
    """

def get_student_success():
    """Student achievement SVG"""
    return """
    <svg width="300" height="200" viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg">
        <!-- Background gradient -->
        <defs>
            <linearGradient id="successGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#FFE4B5;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#F0E68C;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect width="300" height="200" fill="url(#successGrad)"/>
        
        <!-- Trophy -->
        <ellipse cx="150" cy="70" rx="25" ry="30" fill="#FFD700"/>
        <rect x="140" y="100" width="20" height="20" fill="#FFD700"/>
        <rect x="135" y="120" width="30" height="10" fill="#CD853F"/>
        
        <!-- Stars around trophy -->
        <polygon points="100,50 102,56 108,56 103,60 105,66 100,62 95,66 97,60 92,56 98,56" fill="#FFD700"/>
        <polygon points="200,50 202,56 208,56 203,60 205,66 200,62 195,66 197,60 192,56 198,56" fill="#FFD700"/>
        <polygon points="120,30 122,36 128,36 123,40 125,46 120,42 115,46 117,40 112,36 118,36" fill="#FFD700"/>
        <polygon points="180,30 182,36 188,36 183,40 185,46 180,42 175,46 177,40 172,36 178,36" fill="#FFD700"/>
        
        <!-- Student celebrating -->
        <circle cx="150" cy="130" r="20" fill="#DEB887"/>
        <rect x="140" y="150" width="20" height="35" fill="#4CAF50"/>
        <!-- Arms raised -->
        <rect x="125" y="140" width="15" height="8" fill="#DEB887" transform="rotate(-30 132 144)"/>
        <rect x="160" y="140" width="15" height="8" fill="#DEB887" transform="rotate(30 167 144)"/>
        
        <text x="150" y="195" text-anchor="middle" fill="#FF6B35" font-weight="bold" font-size="14">Academic Excellence</text>
    </svg>
    """

def get_learning_progress():
    """Learning progress chart SVG"""
    return """
    <svg width="300" height="200" viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg">
        <!-- Background -->
        <rect width="300" height="200" fill="#f8fafc"/>
        
        <!-- Chart axes -->
        <line x1="50" y1="150" x2="250" y2="150" stroke="#333" stroke-width="2"/>
        <line x1="50" y1="150" x2="50" y2="50" stroke="#333" stroke-width="2"/>
        
        <!-- Progress bars -->
        <rect x="70" y="130" width="30" height="20" fill="#4CAF50"/>
        <rect x="110" y="110" width="30" height="40" fill="#2196F3"/>
        <rect x="150" y="90" width="30" height="60" fill="#FF9800"/>
        <rect x="190" y="70" width="30" height="80" fill="#9C27B0"/>
        
        <!-- Labels -->
        <text x="85" y="170" text-anchor="middle" font-size="10">Week 1</text>
        <text x="125" y="170" text-anchor="middle" font-size="10">Week 2</text>
        <text x="165" y="170" text-anchor="middle" font-size="10">Week 3</text>
        <text x="205" y="170" text-anchor="middle" font-size="10">Week 4</text>
        
        <!-- Y-axis labels -->
        <text x="45" y="155" text-anchor="end" font-size="10">0</text>
        <text x="45" y="130" text-anchor="end" font-size="10">25</text>
        <text x="45" y="105" text-anchor="end" font-size="10">50</text>
        <text x="45" y="80" text-anchor="end" font-size="10">75</text>
        <text x="45" y="55" text-anchor="end" font-size="10">100</text>
        
        <!-- Title -->
        <text x="150" y="30" text-anchor="middle" fill="#FF6B35" font-weight="bold" font-size="16">Learning Progress</text>
        <text x="150" y="190" text-anchor="middle" fill="#666" font-size="12">Continuous Improvement</text>
    </svg>
    """

def get_teacher_resources():
    """Teacher resources SVG"""
    return """
    <svg width="300" height="200" viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg">
        <!-- Background -->
        <rect width="300" height="200" fill="#fff8e1"/>
        
        <!-- Books stack -->
        <rect x="50" y="130" width="60" height="8" fill="#FF5722"/>
        <rect x="50" y="122" width="60" height="8" fill="#2196F3"/>
        <rect x="50" y="114" width="60" height="8" fill="#4CAF50"/>
        <rect x="50" y="106" width="60" height="8" fill="#FF9800"/>
        
        <!-- Computer/tablet -->
        <rect x="150" y="110" width="80" height="50" fill="#333" rx="4"/>
        <rect x="155" y="115" width="70" height="40" fill="#87CEEB"/>
        <circle cx="190" cy="135" r="15" fill="#FFD700"/>
        <text x="190" y="140" text-anchor="middle" font-size="10" fill="#333">AI</text>
        
        <!-- Teaching materials -->
        <circle cx="260" cy="120" r="20" fill="#9C27B0"/>
        <rect x="252" y="112" width="16" height="16" fill="white"/>
        <line x1="256" y1="116" x2="268" y2="128" stroke="#9C27B0" stroke-width="2"/>
        <line x1="256" y1="128" x2="268" y2="116" stroke="#9C27B0" stroke-width="2"/>
        
        <!-- Ruler -->
        <rect x="120" y="80" width="60" height="6" fill="#8B4513"/>
        <line x1="125" y1="80" x2="125" y2="86" stroke="white"/>
        <line x1="135" y1="80" x2="135" y2="86" stroke="white"/>
        <line x1="145" y1="80" x2="145" y2="86" stroke="white"/>
        <line x1="155" y1="80" x2="155" y2="86" stroke="white"/>
        <line x1="165" y1="80" x2="165" y2="86" stroke="white"/>
        <line x1="175" y1="80" x2="175" y2="86" stroke="white"/>
        
        <text x="150" y="30" text-anchor="middle" fill="#FF6B35" font-weight="bold" font-size="16">Teaching Excellence</text>
        <text x="150" y="190" text-anchor="middle" fill="#666" font-size="12">Professional Resources</text>
    </svg>
    """

def get_parent_support():
    """Parent support scene SVG"""
    return """
    <svg width="300" height="200" viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg">
        <!-- Background -->
        <rect width="300" height="200" fill="#f0f8e8"/>
        
        <!-- House outline -->
        <polygon points="150,50 100,90 200,90" fill="#8B4513"/>
        <rect x="120" y="90" width="60" height="60" fill="#DEB887"/>
        <rect x="140" y="110" width="20" height="40" fill="#654321"/>
        <rect x="130" y="100" width="12" height="12" fill="#87CEEB"/>
        <rect x="158" y="100" width="12" height="12" fill="#87CEEB"/>
        
        <!-- Parent and child -->
        <!-- Parent -->
        <circle cx="100" cy="130" r="15" fill="#A0522D"/>
        <rect x="92" y="145" width="16" height="25" fill="#4CAF50"/>
        
        <!-- Child -->
        <circle cx="80" cy="140" r="12" fill="#DEB887"/>
        <rect x="74" y="152" width="12" height="20" fill="#FF4444"/>
        
        <!-- Book between them -->
        <rect x="85" y="135" width="8" height="12" fill="#2196F3"/>
        
        <!-- Hearts showing love/support -->
        <polygon points="120,110 122,108 126,108 123,111 124,115 120,113 116,115 117,111 114,108 118,108" fill="#FF69B4"/>
        <polygon points="200,120 202,118 206,118 203,121 204,125 200,123 196,125 197,121 194,118 198,118" fill="#FF69B4"/>
        
        <!-- Learning materials on ground -->
        <circle cx="240" cy="160" r="8" fill="#FFD700"/>
        <rect x="220" y="155" width="15" height="10" fill="#9C27B0"/>
        <rect x="260" y="150" width="12" height="15" fill="#FF5722"/>
        
        <text x="150" y="30" text-anchor="middle" fill="#FF6B35" font-weight="bold" font-size="16">Family Learning</text>
        <text x="150" y="190" text-anchor="middle" fill="#666" font-size="12">Home Support System</text>
    </svg>
    """

def get_assessment_tools():
    """Assessment tools SVG"""
    return """
    <svg width="300" height="200" viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg">
        <!-- Background -->
        <rect width="300" height="200" fill="#fef7f0"/>
        
        <!-- Clipboard -->
        <rect x="100" y="50" width="80" height="100" fill="#F5F5DC" stroke="#333" stroke-width="2"/>
        <rect x="110" y="40" width="60" height="20" fill="#333"/>
        <circle cx="140" cy="50" r="3" fill="white"/>
        
        <!-- Checklist items -->
        <rect x="115" y="70" width="8" height="8" fill="#4CAF50"/>
        <text x="128" y="78" font-size="10">Math Skills</text>
        <line x1="116" y1="74" x2="122" y2="76" stroke="white" stroke-width="2"/>
        
        <rect x="115" y="85" width="8" height="8" fill="#4CAF50"/>
        <text x="128" y="93" font-size="10">Reading</text>
        <line x1="116" y1="89" x2="122" y2="91" stroke="white" stroke-width="2"/>
        
        <rect x="115" y="100" width="8" height="8" fill="#FF9800"/>
        <text x="128" y="108" font-size="10">Writing</text>
        
        <rect x="115" y="115" width="8" height="8" fill="#F44336"/>
        <text x="128" y="123" font-size="10">Attention</text>
        
        <!-- Magnifying glass -->
        <circle cx="220" cy="100" r="20" fill="none" stroke="#333" stroke-width="3"/>
        <line x1="235" y1="115" x2="250" y2="130" stroke="#333" stroke-width="3"/>
        
        <!-- Brain icon in magnifying glass -->
        <circle cx="220" cy="100" r="12" fill="#FF69B4"/>
        <path d="M220,95 Q215,90 220,88 Q225,90 220,95" fill="#FF1493"/>
        <path d="M220,105 Q215,110 220,112 Q225,110 220,105" fill="#FF1493"/>
        
        <text x="150" y="30" text-anchor="middle" fill="#FF6B35" font-weight="bold" font-size="16">Assessment Tools</text>
        <text x="150" y="190" text-anchor="middle" fill="#666" font-size="12">Comprehensive Evaluation</text>
    </svg>
    """

def get_brain_development():
    """Brain development SVG"""
    return """
    <svg width="300" height="200" viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg">
        <!-- Background -->
        <rect width="300" height="200" fill="#fff0f5"/>
        
        <!-- Brain outline -->
        <ellipse cx="150" cy="100" rx="60" ry="40" fill="#FFB6C1" stroke="#FF69B4" stroke-width="2"/>
        
        <!-- Neural networks -->
        <g stroke="#FF1493" stroke-width="1" fill="none">
            <!-- Network connections -->
            <line x1="120" y1="80" x2="140" y2="90"/>
            <line x1="140" y1="90" x2="160" y2="85"/>
            <line x1="160" y1="85" x2="180" y2="95"/>
            <line x1="140" y1="90" x2="155" y2="110"/>
            <line x1="155" y1="110" x2="170" y2="105"/>
            <line x1="120" y1="120" x2="140" y2="110"/>
            <line x1="170" y1="105" x2="185" y2="115"/>
        </g>
        
        <!-- Neural nodes -->
        <circle cx="120" cy="80" r="3" fill="#FF1493"/>
        <circle cx="140" cy="90" r="3" fill="#FF1493"/>
        <circle cx="160" cy="85" r="3" fill="#FF1493"/>
        <circle cx="180" cy="95" r="3" fill="#FF1493"/>
        <circle cx="155" cy="110" r="3" fill="#FF1493"/>
        <circle cx="170" cy="105" r="3" fill="#FF1493"/>
        <circle cx="120" cy="120" r="3" fill="#FF1493"/>
        <circle cx="185" cy="115" r="3" fill="#FF1493"/>
        
        <!-- Learning symbols around brain -->
        <text x="80" y="70" font-size="16">📚</text>
        <text x="220" y="70" font-size="16">🧮</text>
        <text x="80" y="130" font-size="16">✏️</text>
        <text x="220" y="130" font-size="16">🎨</text>
        
        <!-- Growth arrows -->
        <polygon points="100,50 105,45 110,50 105,40 105,55" fill="#4CAF50"/>
        <polygon points="200,50 205,45 210,50 205,40 205,55" fill="#4CAF50"/>
        
        <text x="150" y="30" text-anchor="middle" fill="#FF6B35" font-weight="bold" font-size="16">Cognitive Development</text>
        <text x="150" y="180" text-anchor="middle" fill="#666" font-size="12">Neural Growth & Learning</text>
    </svg>
    """

def get_diverse_educational_images():
    """Returns a dictionary of diverse educational SVG images"""
    return {
        'classroom_scene': get_classroom_scene(),
        'student_success': get_student_success(),
        'learning_progress': get_learning_progress(),
        'teacher_resources': get_teacher_resources(),
        'parent_support': get_parent_support(),
        'assessment_tools': get_assessment_tools(),
        'brain_development': get_brain_development()
    }