"""
Main entry point for Streamlit Cloud deployment
"""
import sys
import os

# Add backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Run the Streamlit dashboard
if __name__ == "__main__":
    import streamlit.cli
    import sys
    sys.argv = ["streamlit", "run", "backend/streamlit_app/dashboard.py"]
    streamlit.cli.main()