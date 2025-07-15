import streamlit as st
import time
import random
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
   # st.info("✅ Environment variables loaded from .env file")
except ImportError:
    st.warning("⚠️ python-dotenv not installed. Install with: pip install python-dotenv")
except Exception as e:
    st.warning(f"⚠️ Could not load .env file: {str(e)}")

# Set Streamlit page configuration
st.set_page_config(
    page_title="TonePilot – Emotionally Aware AI",
    page_icon="✨",
    layout="centered"
)

# Simple styling - no complex CSS
st.markdown("""
<style>
.main {
    text-align: center;
    color: #f5f5dc;
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 0.1rem;
}
.main-subtitle {
    text-align: center;
    color: #5a6c7d;
    font-size: 2.0rem;
    margin-bottom: 1.5rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# App title with logo
# Add the logo image
try:
    # Try different possible paths
    import os
    possible_paths = [
        "src/logo.png",
        "./src/logo.png", 
        "logo.png",
        os.path.join("src", "logo.png")
    ]
    
    logo_loaded = False
    for path in possible_paths:
        if os.path.exists(path):
            # Use Streamlit columns to center the logo
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.image(path, width=150, use_container_width=False)
            st.markdown("<br>", unsafe_allow_html=True)
            logo_loaded = True
            break
    
    if not logo_loaded:
        # Show current working directory for debugging
        current_dir = os.getcwd()
        st.error(f"Logo not found. Current directory: {current_dir}")
        # Center the fallback emoji
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown("<div style='text-align: center; font-size: 4rem; margin-bottom: 10px;'>🧠🤖</div>", unsafe_allow_html=True)
        
except Exception as e:
    # Show the actual error for debugging
    st.error(f"Error loading logo: {str(e)}")
    # Center the fallback emoji
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='text-align: center; font-size: 4rem; margin-bottom: 10px;'>🧠🤖</div>", unsafe_allow_html=True)

st.markdown('<h1 class="main">TonePilot–Emotionally Aware AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">An emotionally intelligent prompt generator for human-like responses</p>', unsafe_allow_html=True)

# Initialize TonePilot engine with lazy loading
engine = None

def initialize_tonepilot():
    """Lazy load TonePilot only when needed"""
    global engine
    
    if engine is not None:
        return engine
    
    try:
        from tonepilot.core.tonepilot import TonePilotEngine
        
        # Try simple initialization
        st.info("🔄 Initializing TonePilot engine...")
        engine = TonePilotEngine(mode='gemini', respond=True)
        st.success("✅ TonePilot engine initialized successfully!")
        return engine
        
    except Exception as e:
        st.error(f"❌ Failed to initialize TonePilot: {str(e)}")
        st.info("💡 Make sure your .env file contains the required API keys")
        return None

# Demo mode function for testing
def demo_analysis(text):
    """Demo function that simulates TonePilot output"""
    import hashlib
    
    text_hash = int(hashlib.md5(text.encode()).hexdigest(), 16)
    emotions = ["curious", "excited", "confident", "worried", "happy"]
    personalities = ["empathetic_listener", "direct_ally", "supportive_friend"]
    
    emotion1 = emotions[text_hash % len(emotions)]
    emotion2 = emotions[(text_hash + 1) % len(emotions)]
    personality = personalities[text_hash % len(personalities)]
    
    return {
        "input_tags": {
            emotion1: (text_hash % 50 + 30) / 100,
            emotion2: (text_hash % 30 + 10) / 100
        },
        "response_tags": {
            personality: True
        },
        "final_prompt": f"Demo prompt for: {text[:50]}...",
        "response_text": f"This is a demo response for: '{text[:100]}...'"
    }

# Sample prompts for randomization
SAMPLE_PROMPTS = [
    "I'm feeling overwhelmed with my workload and don't know how to prioritize my tasks.",
    "I just got a promotion at work and I'm excited but also nervous about the new responsibilities.",
    "I had a disagreement with my friend and I'm not sure how to approach them about it.",
    "I'm struggling to find motivation to exercise regularly and stay healthy.",
    "I received constructive feedback at work and I'm unsure how to implement the changes.",
    "I'm planning a surprise party for my partner and I want everything to be perfect.",
    "I'm considering a career change but I'm worried about the financial implications.",
    "I just moved to a new city and I'm feeling lonely and disconnected.",
    "I'm trying to learn a new skill but I keep getting frustrated with my progress.",
    "I want to have a difficult conversation with my family about boundaries.",
    "Can you help me come up with a unique birthday message for my best friend?",
    "What are some high-protein vegetarian foods I can add to my diet?",
    "Explain the concept of transformers in AI in simple, beginner-friendly terms.",
    "Suggest a few side hustle ideas for someone good at writing and tech.",
    "How do I stop procrastinating and stay focused while working from home?",
    "Give me a 3-day meal plan for healthy weight loss with Indian vegetarian recipes.",

"Help me write a professional but friendly follow-up email after a job interview.",

"Why do I get muscle soreness two days after a workout instead of the next day?",

"Can you generate some creative Instagram captions for travel photos?",

"What are some emotionally intelligent ways to handle passive-aggressive coworkers?",
]

# Update text area to use session state
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# User input - full width
user_input = st.text_area("Enter your text here:", height=150, value=st.session_state.user_input, key="input_text")

# Both buttons centered on the same line
col1, col2, col3, col4, col5 = st.columns([2, 1, 0.5, 1, 2])

with col2:
    if st.button("🎲 Random", help="Fill with a random sample prompt", type="primary", use_container_width=True):
        random_prompt = random.choice(SAMPLE_PROMPTS)
        st.session_state.user_input = random_prompt
        st.rerun()

with col4:
    generate_button = st.button("🚀 Generate", type="primary", use_container_width=True)

if generate_button:
    if user_input:
        with st.spinner("Processing..."):
            # Try to initialize TonePilot
            engine = initialize_tonepilot()
            
            if engine:
                try:
                    result = engine.run(user_input)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("🎭 Running in demo mode...")
                    result = demo_analysis(user_input)
            else:
                st.info("🎭 Running in demo mode...")
                result = demo_analysis(user_input)
            
            if result:
                st.markdown("---")
                
                # Display results with simple formatting
                st.subheader("🏷️ Detected Emotion Tags")
                emotion_tags = result.get("input_tags", {})
                for emotion, score in emotion_tags.items():
                    st.write(f"**{emotion.replace('_', ' ').title()}**: {score:.1%}")
                    st.progress(float(score))

                st.subheader("🎭 Response Personality Tags")
                personality_tags = result.get("response_tags", {})
                active_traits = [trait for trait, active in personality_tags.items() if active]
                for trait in active_traits:
                    st.write(f"✓ **{trait.replace('_', ' ').title()}**")

                st.subheader("🧾 Generated Prompt Instruction")
                st.write(result.get("final_prompt", "-"))

                st.subheader("💬 Response")
                st.write(result.get("response_text", "-"))
            else:
                st.error("❌ No result returned")
    else:
        st.warning("⚠️ Please enter some text before generating.")
# Add a footer with a link to the TonePilot GitHub repository
st.markdown("---")
st.markdown("Powered by [TonePilot](https://github.com/sdurgi/tonepilot)")
st.markdown("PyPI: https://pypi.org/project/tonepilot")
st.markdown("LinkedIn: https://www.linkedin.com/in/srivanidurgi")
