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

# Function to encode background image
@st.cache_data
def get_background_image():
    """Load and encode background image as base64"""
    import base64
    try:
        possible_paths = [
            "src/background.png",
            "./src/background.png", 
            "background.png",
            os.path.join("src", "background.png"),
            os.path.join(os.path.dirname(__file__), "background.png")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, "rb") as img_file:
                    encoded = base64.b64encode(img_file.read()).decode()
                    return f"data:image/png;base64,{encoded}"
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

# Get background image
background_image = get_background_image()

# Modern CSS styling with improved responsiveness and better colors
st.markdown("""
<style>
/* Content container with subtle glassmorphism effect */
.main .block-container {
    background: rgba(255, 255, 255, 0.75);
    border-radius: 15px;
    padding: 2rem;
    margin-top: 1rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}
.main-title {
    text-align: center;
    color: #1f1f1f;
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
    color: #1f2937;
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

# Add background image if available
if background_image:
    st.markdown(f"""
    <style>
    .stApp {{
        background: url('{background_image}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        min-height: 100vh;
    }}
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
st.markdown('<p class="main-subtitle">open-source AI library for Emotionally Aware Human-like Responses</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Initialize TonePilot engine with improved error handling
@st.cache_resource
def initialize_tonepilot():
    """Initialize TonePilot with caching for better performance"""
    # Check for API key first
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    if not api_key:
        return None, "No API key found! Please set GOOGLE_API_KEY or GEMINI_API_KEY in your environment variables"
    
    try:
        from tonepilot.core.tonepilot import TonePilotEngine
        
        # Initialize with improved configuration
        engine = TonePilotEngine(mode='gemini', respond=True)
        return engine, "TonePilot engine initialized successfully!"
        
    except ImportError as e:
        return None, "TonePilot library not available. Install with: pip install tonepilot"
    except Exception as e:
        return None, f"Failed to initialize TonePilot: {str(e)}"

# Add cache clearing option in sidebar
with st.sidebar:
    st.markdown("---")
    if st.button("🗑️ Clear Cache & Restart"):
        initialize_tonepilot.clear()
        get_background_image.clear()
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Cache cleared! Please refresh the page.")
        st.rerun()

# Sample prompts organized by category
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
            all_prompts = [prompt for prompts in SAMPLE_PROMPTS.values() for prompt in prompts]
            random_prompt = random.choice(all_prompts)
            st.session_state.user_input = random_prompt
            st.rerun()
    
    with subcol2:
        generate_button = st.button("🚀 Generate", type="secondary", use_container_width=True)

# Processing and results
if generate_button:
    if user_input.strip():
        # Initialize TonePilot
        engine, message = initialize_tonepilot()
        
        if not engine:
            st.error(f"❌ {message}")
            if "API key" in message:
                st.info("💡 For Streamlit Cloud: Go to your app settings → Secrets → Add your API key")
        else:
            # Removed the success message as requested
            
            # Process with progress indication
            with st.spinner("🤖 TonePilot is analyzing your input..."):
                try:
                    result = engine.run(user_input)
                    st.session_state.last_result = result
                except Exception as e:
                    st.error(f"❌ Processing Error: {str(e)}")
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