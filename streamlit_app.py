"""
TonePilot Streamlit App
Main entry point for Streamlit Community Cloud
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main app
import tonepilot_streamlit_app 