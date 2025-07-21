import streamlit as st
import time
import random
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    # Removed the info message as requested
except ImportError:
    st.warning("⚠️ python-dotenv not installed. Install with: pip install python-dotenv")
    pass
except Exception as e:
    st.warning(f"⚠️ Could not load .env file: {str(e)}")

# Function to encode background image (cloud optimized)
@st.cache_data(ttl=3600)  # Cache for 1 hour to prevent memory buildup
def get_background_image():
    """Load and encode background image as base64 (cloud optimized)"""
    import base64
    try:
        # Cloud-optimized path detection
        if RUNNING_ON_CLOUD:
            possible_paths = ["src/background.png"]  # Simplified for cloud
        else:
            possible_paths = ["src/background.png", "background.png"]
        
        for path in possible_paths:
            try:
                if os.path.exists(path):
                    file_size = os.path.getsize(path)
                    # More conservative size limit for cloud
                    max_size = 3 * 1024 * 1024 if RUNNING_ON_CLOUD else 5 * 1024 * 1024
                    if file_size > max_size:
                        return None
                    
                    with open(path, "rb") as img_file:
                        encoded = base64.b64encode(img_file.read()).decode()
                        return f"data:image/png;base64,{encoded}"
            except (OSError, IOError):
                # Skip files that can't be read (common on cloud)
                continue
        return None
    except Exception as e:
        return None

# Set Streamlit page configuration with modern options
st.set_page_config(
    page_title="TonePilot – Emotionally Aware AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/sdurgi/tonepilot',
        'Report a bug': 'https://github.com/sdurgi/tonepilot/issues',
        'About': "TonePilot - An emotionally intelligent prompt generator for human-like responses"
    }
)

# Detect if running on Streamlit Cloud and optimize accordingly
RUNNING_ON_CLOUD = os.getenv('STREAMLIT_SHARING_MODE') or '/mount/src' in os.getcwd()

if RUNNING_ON_CLOUD:
    # Reduce file watching on cloud to prevent inotify issues
    os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'

# Get background image
background_image = get_background_image()

# Modern CSS styling with improved responsiveness and better colors
st.markdown("""
<style>
/* Content container with optimized styling for performance */
.main .block-container {
    background: rgba(0, 0, 0, 0.7);
    border-radius: 15px;
    padding: 2rem;
    margin-top: 1rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #ffffff;
}

/* Mobile-optimized styles with dark theme */
@media (max-width: 768px) {
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 0.5rem;
        box-shadow: 0 4px 20px rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .main-title {
        font-size: 2rem !important;
        margin-bottom: 0.25rem !important;
    }
    
    .main-subtitle {
        font-size: 1.5rem !important;
        margin-top: -0.5rem !important;
        margin-bottom: 0.25rem !important;
    }
    
    .header-container {
        margin-bottom: 0.25rem !important;
    }
    
    .stButton > button {
        height: 2.5rem !important;
        min-height: 2.5rem !important;
        font-size: 0.9rem !important;
        padding: 0.4rem 0.8rem !important;
        background: linear-gradient(135deg, #06b6d4, #0891b2) !important;
        border: 1px solid #0284c7 !important;
        color: white !important;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 8px !important;
        font-size: 14px !important;
    }
}

/* Ultra-sleek mobile styles for very small screens */
@media (max-width: 480px) {
    .main .block-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 15px;
        padding: 1.25rem;
        margin-top: 0.5rem;
        box-shadow: 0 6px 25px rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .main-title {
        font-size: 1.75rem !important;
    }
    
    .main-subtitle {
        font-size: 1.75rem !important;
        line-height: 1.3 !important;
    }
    
    .stButton > button {
        height: 2.25rem !important;
        font-size: 0.85rem !important;
        padding: 0.3rem 0.6rem !important;
        background: linear-gradient(135deg, #06b6d4, #0891b2) !important;
        border: 1px solid #0284c7 !important;
        color: white !important;
    }
}
.main-title {
    text-align: center;
    color: #ffffff !important;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    background: linear-gradient(90deg, #2dd4bf, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.main-subtitle {
    text-align: center;
    color: #ffffff !important;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    margin-top: -1rem;
    font-weight: 600;
    background: linear-gradient(135deg, #2563eb, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.header-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 100%;
    margin-bottom: 0.25rem;
    padding-bottom: 0rem;
}
.logo-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 0rem;
    margin-top: 0rem;
    width: 100%;
    text-align: center;
}
.logo-wrapper img {
    display: block;
    margin: 0 auto;
    filter: brightness(1.1) contrast(1.1) saturate(0.9);
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.centered-emoji {
    font-size: 4rem;
    margin-bottom: 0rem;
    margin-top: 0rem;
    text-align: center;
    width: 100%;
    display: block;
    filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.1));
}
.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.3s ease;
    height: 2.75rem;
    min-height: 2.75rem;
    padding: 0.5rem 1rem;
    white-space: nowrap;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #e0f2fe, #b3e5fc);
    border: 1px solid #0891b2;
    color: #0c4a6e;
    box-shadow: 0 2px 4px rgba(8, 145, 178, 0.2);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #b3e5fc, #81d4fa);
    box-shadow: 0 4px 8px rgba(8, 145, 178, 0.3);
    transform: translateY(-1px);
    border-color: #0284c7;
}
.stTextArea > div > div > textarea {
    border-radius: 12px;
    font-size: 16px;
}
.result-section {
    margin-top: 1rem;
    padding: 1.5rem;
    border-radius: 12px;
    background: #fafafa;
    border: 1px solid #e5e7eb;
}
.metric-card {
    background: white;
}

/* AGGRESSIVE TEXT FORCING - OVERRIDE ALL STREAMLIT DEFAULTS */
* {
    color: #ffffff !important;
}

body, html, div, p, span, h1, h2, h3, h4, h5, h6, label {
    color: #ffffff !important;
}

.stApp, .stApp *, .main *, .block-container * {
    color: #ffffff !important;
}

.stMarkdown, .stMarkdown *, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    color: #ffffff !important;
}

.stMarkdown p, .stMarkdown span, .stMarkdown div, .stMarkdown li {
    color: #ffffff !important;
}

/* Force all text elements */
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] * {
    color: #ffffff !important;
}

/* Input and form styling - keep readable */
.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    color: #1f2937 !important;
    background-color: rgba(255, 255, 255, 0.95) !important;
}

.stSelectbox label, .stTextInput label, .stTextArea label {
    color: #ffffff !important;
}

/* Button text override - dark text for light button backgrounds */
.stButton > button, .stButton > button * {
    color: #1f2937 !important;
}

/* Links */
a, .stMarkdown a {
    color: #60a5fa !important;
    text-decoration: underline;
}

/* Sidebar styling */
.css-1d391kg, .css-1d391kg p, .css-1d391kg span {
    color: #ffffff !important;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin: 0.5rem 0;
}
/* Fix for expander behavior - auto close after selection */
.streamlit-expanderHeader {
    background-color: transparent !important;
}
/* Remove extra white space */
.block-container {
    padding-top: 0.25rem;
    padding-bottom: 0.5rem;
}
/* Center the entire app content */
.main .block-container {
    max-width: 800px;
    margin: 0 auto;
}
/* Force image centering */
.stImage {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}
.stImage > div {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Add background image if available with mobile optimization
if background_image:
    st.markdown(f"""
    <style>
    /* Desktop background with WHITE text for dark background */
    .stApp {{
        background: url('{background_image}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        min-height: 100vh;
        color: #ffffff;
    }}
    
    /* Desktop text styling - WHITE for dark background */
    @media (min-width: 769px) {{
        .stApp {{
            color: #ffffff !important;
        }}
        .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            color: #ffffff !important;
        }}
        .stSelectbox label, .stTextInput label, .stTextArea label {{
            color: #ffffff !important;
        }}
    }}
    
    /* ONLY mobile gets black background */
    @media (max-width: 768px) {{
        .stApp {{
            background: linear-gradient(135deg, #000000, #1a1a1a) !important;
            background-attachment: scroll !important;
            color: #ffffff !important;
        }}
    }}
    
    /* Deep black for very small screens */
    @media (max-width: 480px) {{
        .stApp {{
            background: #000000 !important;
            color: #ffffff !important;
        }}
    }}
    
    </style>
    
    <script>
    if (window.innerWidth <= 768) {{
        document.body.classList.add('mobile-device');
        // Disable animations on mobile for better performance
        document.documentElement.style.setProperty('--animation-duration', '0s');
        
        // Send mobile detection to Streamlit
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: {{mobile_detected: true}}
        }}, '*');
    }}
    </script>
    """, unsafe_allow_html=True)
else:
    # Fallback styling when no background image is available
    st.markdown("""
    <style>
    /* Desktop fallback - dark theme to match */
    .stApp {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        min-height: 100vh;
        color: #ffffff;
    }
    
    /* Desktop text styling for fallback */
    @media (min-width: 769px) {
        .stApp {
            color: #ffffff !important;
        }
        .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #ffffff !important;
        }
        .stSelectbox label, .stTextInput label, .stTextArea label {
            color: #ffffff !important;
        }
    }
    
    /* ONLY mobile gets black theme */
    @media (max-width: 768px) {
        .stApp {
            background: linear-gradient(135deg, #000000, #1a1a1a) !important;
            color: #ffffff !important;
        }
    }
    
    @media (max-width: 480px) {
        .stApp {
            background: #000000 !important;
            color: #ffffff !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state 
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'last_result' not in st.session_state:
    st.session_state.last_result = None

# App header with perfectly aligned logo and title
st.markdown('<div class="header-container">', unsafe_allow_html=True)

try:
    possible_paths = [
        "src/logo.png",
        "./src/logo.png", 
        "logo.png",
        os.path.join("src", "logo.png"),
        os.path.join(os.path.dirname(__file__), "logo.png")
    ]
    
    logo_loaded = False
    for path in possible_paths:
        if os.path.exists(path):
            st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
            # Use columns to center the image
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.image(path, width=200, use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
            logo_loaded = True
            break
    
    if not logo_loaded:
        st.markdown('<div class="centered-emoji">🧠🤖</div>', unsafe_allow_html=True)
        
except Exception as e:
    st.markdown('<div class="centered-emoji">🧠🤖</div>', unsafe_allow_html=True)

# Title and subtitle in the same container for perfect alignment
st.markdown('<p class="main-subtitle">Open-Source AI library for Emotionally Aware Human-like Responses</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Initialize TonePilot engine with simple, effective caching
@st.cache_resource
def get_tonepilot_engine():
    """Get cached TonePilot engine - only loads once per session"""
    try:
        from tonepilot.core.tonepilot import TonePilotEngine
        # Simple initialization without complex memory management that breaks caching
        engine = TonePilotEngine(mode='gemini', respond=True)
        return engine
    except Exception as e:
        # Return None if initialization fails - let calling code handle errors
        return None

def initialize_tonepilot():
    """Initialize TonePilot with proper error handling but simple caching"""
    # Check for API key first
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    if not api_key:
        return None, "No API key found! Please set GOOGLE_API_KEY or GEMINI_API_KEY in your environment variables"
    
    # Get cached engine
    engine = get_tonepilot_engine()
    
    if engine is None:
        return None, "TonePilot library not available. Install with: pip install tonepilot"
    
    return engine, "TonePilot engine initialized successfully!"

# Add cache clearing and memory management in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🛠️ App Controls")
    
    # Mobile mode toggle
    mobile_mode = st.toggle("📱 Mobile Mode (Demo Only)", 
                           value=st.session_state.get('mobile_mode', False),
                           help="Enable to use pre-written responses instead of loading the full model")
    st.session_state.mobile_mode = mobile_mode
    
    if mobile_mode:
        st.info("🚀 **Mobile Mode Active:** Using sample responses for faster performance!")
    
    if st.button("🗑️ Clear Cache & Restart"):
        get_tonepilot_engine.clear()
        get_background_image.clear()
        st.cache_data.clear()
        st.cache_resource.clear()
        # Clear session state to free memory
        for key in list(st.session_state.keys()):
            if key not in ['user_input', 'mobile_mode']:  # Keep user input and mobile mode
                del st.session_state[key]
        st.success("Cache cleared! Please refresh the page.")
        st.rerun()
    

        
    # Cache status and memory info
    st.markdown("💾 **Cache Info:**")
    
    # Show current mode and environment
    mobile_mode = st.session_state.get('mobile_mode', False)
    if mobile_mode:
        st.markdown("📱 Mode: Mobile Demo (No AI model)")
    else:
        st.markdown("🖥️ Mode: Full AI Model")
    
    if RUNNING_ON_CLOUD:
        st.markdown("☁️ Environment: Streamlit Cloud")
        st.markdown("🔧 File watching: Disabled")
    else:
        st.markdown("💻 Environment: Local")
        
    st.markdown("🖼️ Background: Auto-cached (1hr)")
    st.markdown("🧠 AI Model: Cached when used")
    
    st.markdown("**Performance Tips:**")
    if RUNNING_ON_CLOUD:
        st.markdown("- Cloud optimized for file watching issues")
        st.markdown("- Use Mobile Mode for best cloud performance")
        st.markdown("- Black theme on mobile for better performance")
    else:
        st.markdown("- Use Mobile Mode for instant responses")
        st.markdown("- AI model loads once and stays cached")
        st.markdown("- Clear cache only if issues occur")
    
    # Mobile optimization info
    st.markdown("📱 **Mobile Optimized:**")
    st.markdown("- Sleek black background on mobile")
    st.markdown("- Enhanced contrast and visibility")
    st.markdown("- Sample responses for demo")
    st.markdown("- Optimized buttons for dark theme")

# Mobile sample responses (pre-written to avoid loading model)
MOBILE_SAMPLE_RESPONSES = {
    "I'm feeling overwhelmed with my workload and don't know how to prioritize my tasks.": {
        "input_tags": {"overwhelmed": 0.85, "stressed": 0.72, "anxious": 0.68},
        "response_tags": {"empathetic_listener": True, "nurturing_teacher": True, "supportive": True},
        "final_prompt": "Respond with deep empathy and understanding. Acknowledge their feelings of being overwhelmed and provide gentle, practical guidance for prioritization. Use a warm, supportive tone that makes them feel heard and validated.",
        "response_text": "I can really hear how overwhelmed you're feeling right now, and that's completely understandable. When everything feels urgent, it's natural to feel paralyzed about where to start.\n\nLet's take this step by step together. First, take a deep breath - you've got this. Try writing down all your tasks, then ask yourself: 'What absolutely must be done today?' Focus on just 2-3 priority items.\n\nRemember, you don't have to tackle everything at once. Sometimes the most productive thing you can do is give yourself permission to do less, but do it well. You're handling more than you realize, and it's okay to take things one task at a time."
    },
    "I just got a promotion at work and I'm excited but also nervous about the new responsibilities.": {
        "input_tags": {"excited": 0.78, "nervous": 0.65, "anticipatory": 0.71},
        "response_tags": {"confident_mentor": True, "encouraging": True, "celebratory": True},
        "final_prompt": "Respond with enthusiasm for their promotion while acknowledging their nervousness. Provide confident, encouraging guidance that builds their self-belief. Use an uplifting, mentoring tone.",
        "response_text": "Congratulations! This is such exciting news, and you should be incredibly proud of this achievement. The fact that you were chosen for this promotion says everything about your capabilities and potential.\n\nThose nervous butterflies? They're completely normal and actually a good sign - they show you care and want to succeed. Every great leader has felt exactly what you're feeling right now.\n\nYou already have the skills that got you here, and now you'll develop even more. Trust in the process, be patient with yourself as you learn, and remember - your organization believes in you, and so do I. You're going to do amazing things in this new role!"
    },
    "I had a disagreement with my friend and I'm not sure how to approach them about it.": {
        "input_tags": {"conflicted": 0.73, "uncertain": 0.68, "concerned": 0.65},
        "response_tags": {"diplomatic_advisor": True, "thoughtful": True, "relationship_focused": True},
        "final_prompt": "Provide thoughtful, diplomatic advice for resolving the friendship conflict. Focus on understanding, communication, and preserving the relationship. Use a caring but wise tone.",
        "response_text": "Friendship disagreements can feel really heavy on the heart, and it's clear you value this relationship deeply. The fact that you're thinking carefully about how to approach this shows what a caring friend you are.\n\nWhen you're ready, consider reaching out with something simple like, 'I've been thinking about our conversation, and I really value our friendship. Could we talk?' Sometimes the hardest part is just taking that first step.\n\nApproach the conversation with curiosity rather than being right. Listen to understand their perspective, share yours openly, and remember that good friends can disagree and still care deeply for each other. This might even strengthen your bond in the long run."
    }
}

# Function to detect mobile device
def is_mobile_device():
    """Detect if user is on mobile device"""
    try:
        # Simple check based on screen width detection
        if 'mobile_detected' not in st.session_state:
            st.session_state.mobile_detected = False
        return st.session_state.mobile_detected
    except:
        return False

# Memory-optimized sample prompts (reduced size for cloud deployment)
SAMPLE_PROMPTS = {
    "Personal Growth": [
        "I'm feeling overwhelmed with my workload and don't know how to prioritize my tasks.",
        "I received constructive feedback at work and I'm unsure how to implement the changes.",
        "How do I stop procrastinating and stay focused while working from home?",
        "I'm trying to learn a new skill but I keep getting frustrated with my progress."
    ],
    "Relationships": [
        "I had a disagreement with my friend and I'm not sure how to approach them about it.",
        "I want to have a difficult conversation with my family about boundaries.",
        "What are some emotionally intelligent ways to handle passive-aggressive coworkers?",
        "Can you help me come up with a unique birthday message for my best friend?"
    ],
    "Career & Goals": [
        "I just got a promotion at work and I'm excited but also nervous about the new responsibilities.",
        "I'm considering a career change but I'm worried about the financial implications.",
        "Help me write a professional but friendly follow-up email after a job interview.",
        "Suggest a few side hustle ideas for someone good at writing and tech."
    ],
    "Health & Lifestyle": [
        "I'm struggling to find motivation to exercise regularly and stay healthy.",
        "What are some high-protein vegetarian foods I can add to my diet?",
        "Give me a 3-day meal plan for healthy weight loss with Indian vegetarian recipes.",
        "Why do I get muscle soreness two days after a workout instead of the next day?"
    ],
    "Creative & Learning": [
        "Explain the concept of transformers in AI in simple, beginner-friendly terms.",
        "Can you generate some creative Instagram captions for travel photos?",
        "I just moved to a new city and I'm feeling lonely and disconnected.",
        "I'm planning a surprise party for my partner and I want everything to be perfect."
    ]
}

# Mobile mode indicator
mobile_mode = st.session_state.get('mobile_mode', False)
if mobile_mode:
    st.success("📱 **Mobile Demo Mode Active** - Using optimized sample responses for better performance! Toggle off in sidebar to use full AI model.")

# User input section with better layout
st.markdown('<div style="margin-top: 0.5rem;"><h3 style="margin-bottom: 0.25rem;">💭 Enter Your Prompt</h3></div>', unsafe_allow_html=True)
user_input = st.text_area(
    "What's on your mind?", 
    height=120, 
    value=st.session_state.user_input, 
    key="input_text",
    placeholder="Type your thoughts, questions, or scenarios here..."
)



# Action buttons with improved spacing
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    subcol1, subcol2 = st.columns(2)
    
    with subcol1:
        if st.button("🎲 Random Sample", type="secondary", use_container_width=True):
            # Include mobile sample prompts if mobile mode is enabled
            mobile_mode = st.session_state.get('mobile_mode', False)
            if mobile_mode:
                mobile_prompts = list(MOBILE_SAMPLE_RESPONSES.keys())
                all_prompts = [prompt for prompts in SAMPLE_PROMPTS.values() for prompt in prompts] + mobile_prompts
            else:
                all_prompts = [prompt for prompts in SAMPLE_PROMPTS.values() for prompt in prompts]
            
            random_prompt = random.choice(all_prompts)
            st.session_state.user_input = random_prompt
            st.rerun()
    
    with subcol2:
        generate_button = st.button("🚀 Generate", type="secondary", use_container_width=True)

# Processing and results
if generate_button:
    if user_input.strip():
        # Check if mobile mode is enabled
        mobile_mode = st.session_state.get('mobile_mode', False)
        
        if mobile_mode:
            # Use pre-written sample responses for mobile
            with st.spinner("🤖 TonePilot is analyzing your input..."):
                time.sleep(1)  # Small delay for realistic feel
                
                # Check if input matches any sample responses
                result = None
                for sample_input, sample_result in MOBILE_SAMPLE_RESPONSES.items():
                    if user_input.lower() in sample_input.lower() or sample_input.lower() in user_input.lower():
                        result = sample_result
                        break
                
                # If no match, create a generic response
                if not result:
                    result = {
                        "input_tags": {"curious": 0.65, "thoughtful": 0.58, "engaged": 0.72},
                        "response_tags": {"supportive": True, "informative": True, "encouraging": True},
                        "final_prompt": "Respond with warmth and understanding. Provide thoughtful, encouraging guidance that shows empathy and offers practical support.",
                        "response_text": "Thank you for sharing that with me. I can sense the thoughtfulness behind your words, and I appreciate you opening up about this.\n\nWhile everyone's situation is unique, what often helps is taking a step back and approaching things with both compassion for yourself and curiosity about what might work best for you. Sometimes the answers we're looking for are already within us - we just need the right space and support to discover them.\n\nRemember, it's okay to take things one step at a time. You don't have to have all the answers right now. What matters is that you're being thoughtful about your situation and seeking understanding."
                    }
                
                st.session_state.last_result = result
                
        else:
            # Initialize TonePilot for full mode
            engine, message = initialize_tonepilot()
            
            if not engine:
                st.error(f"❌ {message}")
                if "API key" in message:
                    st.info("💡 For Streamlit Cloud: Go to your app settings → Secrets → Add your API key")
                st.info("💡 **Try Mobile Mode** in the sidebar for a demo without requiring API keys!")
                result = None
            else:
                # Process with progress indication
                with st.spinner("🤖 TonePilot is analyzing your input..."):
                    try:
                        result = engine.run(user_input)
                        st.session_state.last_result = result
                        
                    except MemoryError as e:
                        st.error("❌ Memory limit exceeded. Try Mobile Mode in the sidebar for better performance.")
                        result = None
                    except Exception as e:
                        error_msg = str(e)
                        if "memory" in error_msg.lower() or "oom" in error_msg.lower():
                            st.error("❌ Memory issue detected. Try Mobile Mode in the sidebar for better performance.")
                        else:
                            st.error(f"❌ Processing Error: {error_msg}")
                        result = None
            
            # Display results with improved layout - no extra white space
            if result:
                st.markdown("---")
                
                # Emotion Analysis
                st.markdown("### 🏷️ Detected Emotions")
                emotion_tags = result.get("input_tags", {})
                
                if emotion_tags:
                    # Display emotions in a grid
                    emotion_cols = st.columns(min(3, len(emotion_tags)))
                    for i, (emotion, score) in enumerate(emotion_tags.items()):
                        with emotion_cols[i % 3]:
                            st.metric(
                                label=emotion.replace('_', ' ').title(),
                                value=f"{score:.1%}",
                                delta=None
                            )
                            st.progress(float(score))

                # Personality Traits
                st.markdown("### 🎭 Response Personality")
                personality_tags = result.get("response_tags", {})
                active_traits = [trait for trait, active in personality_tags.items() if active]
                
                if active_traits:
                    trait_cols = st.columns(min(4, len(active_traits)))
                    for i, trait in enumerate(active_traits):
                        with trait_cols[i % 4]:
                            st.success(f"✨ {trait.replace('_', ' ').title()}")

                # Generated Prompt
                st.markdown("### 🧾 Generated Prompt Instruction")
                if result.get("final_prompt"):
                    st.code(result.get("final_prompt"), language="text")

                # AI Response
                st.markdown("### 💬 AI Response")
                if result.get("response_text"):
                    st.markdown(result.get("response_text"))
            else:
                st.error("❌ No result returned from TonePilot")
    else:
        st.warning("⚠️ Please enter some text before generating.")

# Footer with modern styling
st.markdown("---")
footer_cols = st.columns([1, 1, 1])

with footer_cols[0]:
    st.markdown("**Powered by**")
    st.markdown("[🔗 TonePilot](https://github.com/sdurgi/tonepilot)")

with footer_cols[1]:
    st.markdown("**Package**")
    st.markdown("[📦 PyPI](https://pypi.org/project/tonepilot)")

with footer_cols[2]:
    st.markdown("**Developer**")
    st.markdown("[👤 LinkedIn](https://www.linkedin.com/in/srivanidurgi)")

# Add version info in sidebar for debugging
with st.sidebar:
    st.markdown("### 🔧 App Info")
    st.markdown(f"**Streamlit**: {st.__version__}")
    try:
        import tonepilot
        st.markdown(f"**TonePilot**: {tonepilot.__version__}")
    except:
        st.markdown("**TonePilot**: Not available") 