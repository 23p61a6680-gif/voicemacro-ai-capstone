import streamlit as st

def apply_custom_theme():
    """Applies a crazy, futuristic custom CSS for a premium AI dashboard look."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=Space+Grotesk:wght@500;700&display=swap');

        /* Global Font Settings */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif !important;
        }

        /* Crazy Gradient Headers */
        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif !important;
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700 !important;
            letter-spacing: 1px;
            margin-bottom: 20px !important;
        }

        /* Glassmorphism Containers */
        .stExpander {
            background: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 15px !important;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1) !important;
            transition: all 0.3s ease;
        }
        
        .stExpander:hover {
            border-color: rgba(0, 210, 255, 0.3) !important;
            box-shadow: 0 8px 32px rgba(0, 210, 255, 0.1) !important;
        }

        /* Futuristic Primary Buttons */
        button[kind="primary"] {
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
            color: #0F111A !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 10px 25px !important;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.4) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }

        button[kind="primary"]:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 0 25px rgba(0, 210, 255, 0.7) !important;
        }
        
        /* Secondary Buttons Hover Effect */
        button[kind="secondary"] {
            border-radius: 50px !important;
            transition: all 0.3s ease !important;
        }
        button[kind="secondary"]:hover {
            border-color: #00d2ff !important;
            color: #00d2ff !important;
        }

        /* Glowing Code Blocks */
        .stCodeBlock {
            background: #0d0f17 !important;
            border: 1px solid rgba(0, 210, 255, 0.2) !important;
            border-radius: 10px !important;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5) !important;
        }
        
        /* Info Boxes */
        div[data-testid="stCallout"] {
            background: rgba(0, 210, 255, 0.05) !important;
            border-left: 5px solid #00d2ff !important;
            border-radius: 0 10px 10px 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
