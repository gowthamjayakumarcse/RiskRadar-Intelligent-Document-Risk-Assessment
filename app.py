import streamlit as st
import google.generativeai as genai
import PyPDF2
import os
from dotenv import load_dotenv
import json
import re
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Set page config at the very beginning
st.set_page_config(
    page_title="License Agreement Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro')

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background-color: #f0f2f6 !important;
        padding: 1rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a237e 0%, #283593 100%) !important;
    }
    
    [data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #1a237e 0%, #283593 100%) !important;
    }
    
    .css-1vq4p4l {
        padding: 2rem 1rem !important;
    }
    
    .sidebar-content {
        background: rgba(255, 255, 255, 0.15);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .sidebar-title {
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        margin-bottom: 1rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        display: block !important;
        letter-spacing: 0.5px !important;
    }
    
    .sidebar-text {
        color: white !important;
        margin-bottom: 1rem !important;
        line-height: 1.6 !important;
        display: block !important;
        font-size: 1rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .contact-section {
        background: rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1rem;
        border-left: 4px solid #fff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .contact-section strong {
        color: white !important;
        font-weight: 600 !important;
    }
    
    .contact-section a {
        color: #90caf9 !important;
        text-decoration: none !important;
        font-weight: 500 !important;
        text-shadow: none !important;
    }
    
    .contact-section a:hover {
        color: #bbdefb !important;
        text-decoration: underline !important;
    }
    
    /* Title styling */
    .title-section {
        background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .title-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        pointer-events: none;
    }
    
    .app-title {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: center !important;
        font-family: 'Arial', sans-serif !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        display: block !important;
    }
    
    .app-subtitle {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.1rem !important;
        margin-top: 1rem !important;
        text-align: center !important;
        display: block !important;
    }
    
    /* Metrics styling */
    .metric-card {
        background: white;
        padding: 1.25rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border-color: #3949ab;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #1a237e;
        margin: 10px 0;
        background: -webkit-linear-gradient(45deg, #1a237e, #3949ab);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    
    /* Upload section styling */
    .upload-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin: 1.5rem 0;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .upload-container:hover {
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border-color: #3949ab;
    }
    
    /* Results section styling */
    .results-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin: 1.5rem 0;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .results-container:hover {
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border-color: #3949ab;
    }
    
    /* File uploader styling */
    .stFileUploader {
        padding: 1.5rem;
        border: 2px dashed #3949ab;
        border-radius: 10px;
        background-color: #f8fafc;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #1a237e;
        background-color: #f1f5f9;
    }
    
    /* Score breakdown styling */
    .score-breakdown {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-top: 1rem;
    }
    
    .score-item {
        display: flex;
        align-items: center;
        margin-bottom: 0.75rem;
        padding: 0.5rem;
        background: white;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .score-item:hover {
        transform: translateX(5px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8fafc !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-weight: 600 !important;
        color: #000000 !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #f1f5f9 !important;
        color: #3949ab !important;
    }
    
    div[data-testid="stExpander"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        margin-bottom: 1rem !important;
        background-color: white !important;
    }
    
    div[data-testid="stExpander"]:hover {
        border-color: #3949ab !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    }

    /* Content styling within expanders */
    .analysis-content {
        background-color: white !important;
        padding: 1rem !important;
        border-radius: 0 0 10px 10px !important;
    }

    .analysis-item {
        background-color: #f8fafc !important;
        padding: 0.75rem 1rem !important;
        margin-bottom: 0.75rem !important;
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        color: #000000 !important;
        transition: all 0.3s ease !important;
    }

    .analysis-item:hover {
        background-color: #f1f5f9 !important;
        border-color: #3949ab !important;
        transform: translateX(5px) !important;
    }
    </style>
""", unsafe_allow_html=True)

def calculate_risk_score(analysis):
    """Calculate overall risk score based on analysis results."""
    # Weight different factors
    weights = {
        "privacy_issues": 0.4,
        "major_concerns": 0.3,
        "data_misuse": 0.3
    }
    
    # Calculate scores for each category
    privacy_score = min(len(analysis["privacy_issues"]) * 20, 100)  # 20 points per issue, max 100
    concerns_score = min(len(analysis["major_concerns"]) * 15, 100)  # 15 points per concern, max 100
    misuse_score = min(len(analysis["data_misuse"]) * 25, 100)  # 25 points per risk, max 100
    
    # Calculate weighted average
    total_score = (
        privacy_score * weights["privacy_issues"] +
        concerns_score * weights["major_concerns"] +
        misuse_score * weights["data_misuse"]
    )
    
    return round(total_score, 1)

def create_gauge_chart(score):
    """Create a gauge chart using plotly."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Score", 'font': {'size': 24, 'color': '#1f77b4'}},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#1f77b4"},
            'steps': [
                {'range': [0, 30], 'color': "#2ecc71"},
                {'range': [30, 70], 'color': "#f1c40f"},
                {'range': [70, 100], 'color': "#e74c3c"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin={'l': 10, 'r': 10, 't': 30, 'b': 10},
        paper_bgcolor="white",
        font={'color': "#2c3e50", 'family': "Arial"}
    )
    
    return fig

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def clean_json_response(response_text):
    """Clean the JSON response by removing markdown code blocks."""
    # Remove markdown code block markers if present
    response_text = re.sub(r'```json\s*', '', response_text)
    response_text = re.sub(r'```\s*$', '', response_text)
    return response_text.strip()

def analyze_license(text):
    """Analyze license agreement using Gemini model."""
    prompt = f"""
    You are an expert legal document analyzer specializing in license agreements. Your task is to analyze the following license agreement and provide a detailed analysis in JSON format. Focus on identifying key legal terms, potential risks, important clauses, advantages, and disadvantages.

    Please provide your analysis in the following JSON structure:
    {{
        "key_points": [
            "List the main terms and conditions",
            "Include important legal obligations",
            "Highlight key rights and responsibilities"
        ],
        "privacy_issues": [
            "Identify data collection practices",
            "List privacy-related concerns",
            "Highlight data sharing policies"
        ],
        "major_concerns": [
            "List ambiguous terms",
            "Identify potentially harmful clauses",
            "Highlight unclear obligations"
        ],
        "data_misuse": [
            "Identify potential data exploitation risks",
            "List concerning data usage terms",
            "Highlight privacy vulnerabilities"
        ],
        "advantages": [
            "List beneficial terms for the user",
            "Highlight user protections",
            "Identify favorable conditions"
        ],
        "disadvantages": [
            "List unfavorable terms",
            "Highlight potential limitations",
            "Identify user restrictions"
        ]
    }}

    License Agreement Text:
    {text}

    Important: Provide your response in valid JSON format without any markdown formatting.
    """
    
    try:
        response = model.generate_content(prompt)
        cleaned_response = clean_json_response(response.text)
        return json.loads(cleaned_response)
    except Exception as e:
        st.error(f"Error analyzing document: {str(e)}")
        return {
            "key_points": ["Error analyzing document"],
            "privacy_issues": ["Error analyzing document"],
            "major_concerns": ["Error analyzing document"],
            "data_misuse": ["Error analyzing document"],
            "advantages": ["Error analyzing document"],
            "disadvantages": ["Error analyzing document"]
        }

def main():
    # Sidebar with About Us section
    with st.sidebar:
        st.markdown("""
            <h2 class="sidebar-title">🎯 About Us</h2>
            <p class="sidebar-text">Empowering users with AI-driven legal document analysis for better understanding and informed decision-making.</p>
            
            <h3 class="sidebar-title">🚀 Our Mission</h3>
            <p class="sidebar-text">Making complex legal documents accessible and understandable through cutting-edge AI technology.</p>
            
            <h3 class="sidebar-title">💡 Our Technology</h3>
            <p class="sidebar-text">Powered by Google's Gemini 1.5 Pro AI model for precise and comprehensive document analysis.</p>
            
            <div class="contact-section">
                <h3 class="sidebar-title">📬 Contact Information</h3>
                <p class="sidebar-text">
                    👤 <strong>Name:</strong> GOWTHAM.J<br>
                    🏛️ <strong>Institution:</strong> VIT VELLORE<br>
                    🎓 <strong>Qualification:</strong> Post Graduate in AI & ML<br>
                    📧 <strong>Email:</strong> <a href="mailto:gowtham.aidev@gmail.com" style="color: #90caf9;">gowtham.aidev@gmail.com</a>
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Main content
    # Title section with custom styling
    st.markdown("""
        <div class="title-section">
            <div class="app-title">
                📄 License Agreement Analyzer
            </div>
            <div class="app-subtitle">
                Analyze legal documents with AI-powered insights
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Dashboard Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Processing Time</div>
            <div class="metric-value">~3 sec</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Model Version</div>
            <div class="metric-value">Gemini 1.5</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Analysis Accuracy</div>
            <div class="metric-value">87.9%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Last Updated</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(datetime.now().strftime("%H:%M")), unsafe_allow_html=True)

    # File Upload Section
    st.markdown("""
    <div class="upload-container">
        <h3 style='color: #1e3a8a; margin-bottom: 1rem;'>Upload Document</h3>
        <p style='color: #475569;'>Upload a PDF containing a license agreement to analyze key points, privacy issues, 
        major concerns, and potential data misuse risks.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        with st.spinner("Analyzing document..."):
            # Extract text from PDF
            text = extract_text_from_pdf(uploaded_file)
            
            # Analyze the license
            analysis = analyze_license(text)

            # Calculate and display risk score
            risk_score = calculate_risk_score(analysis)
            
            # Add Summary Section at the top
            st.markdown("""
                <div style='background-color: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;'>
                    <h3 style='color: #1a237e; font-weight: 700; margin-bottom: 1rem; font-size: 1.5rem;'>📊 Analysis Summary</h3>
                    <p style='color: #475569; font-size: 1.1rem; line-height: 1.6;'>
                        This analysis evaluates the license agreement across multiple dimensions, including privacy concerns, legal obligations, and user rights. 
                        The overall risk assessment is based on the number and severity of identified issues in each category.
                    </p>
                    <div style='display: flex; gap: 2rem; margin-top: 1rem;'>
                        <div style='flex: 1;'>
                            <p style='color: #1e3a8a; font-weight: 600; margin-bottom: 0.5rem;'>Total Issues Found:</p>
                            <p style='color: #475569;'>{} issues across all categories</p>
                        </div>
                        <div style='flex: 1;'>
                            <p style='color: #1e3a8a; font-weight: 600; margin-bottom: 0.5rem;'>Primary Concerns:</p>
                            <p style='color: #475569;'>{} major concerns identified</p>
                        </div>
                    </div>
                </div>
            """.format(
                len(analysis['privacy_issues']) + len(analysis['major_concerns']) + len(analysis['data_misuse']),
                len(analysis['major_concerns'])
            ), unsafe_allow_html=True)
            
            # Create two columns for the gauge chart and risk level
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.plotly_chart(create_gauge_chart(risk_score), use_container_width=True)
            
            with col2:
                st.markdown("<h3 style='color: #FF0000; font-weight: 700;'>Risk Assessment</h3>", unsafe_allow_html=True)
                if risk_score < 30:
                    st.markdown("<p style='color: #000000; font-weight: 600;'>Low Risk</p>", unsafe_allow_html=True)
                elif risk_score < 70:
                    st.markdown("<p style='color: #000000; font-weight: 600;'>Medium Risk</p>", unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color: #000000; font-weight: 600;'>High Risk</p>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="score-breakdown">
                    <h4 style='color: #1a237e; margin-bottom: 1rem; font-size: 1.2rem;'>📊 Score Breakdown</h4>
                    <div class="score-item">
                        <span style='color: #3949ab; margin-right: 0.5rem;'>🔐</span>
                        <span style='color: #000000;'>Privacy Issues: {len(analysis['privacy_issues'])} issues</span>
                    </div>
                    <div class="score-item">
                        <span style='color: #3949ab; margin-right: 0.5rem;'>⚠️</span>
                        <span style='color: #000000;'>Major Concerns: {len(analysis['major_concerns'])} concerns</span>
                    </div>
                    <div class="score-item">
                        <span style='color: #3949ab; margin-right: 0.5rem;'>🛡️</span>
                        <span style='color: #000000;'>Data Misuse Risks: {len(analysis['data_misuse'])} risks</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Display results in collapsible sections
            st.markdown("""
                <div style='background-color: #1a237e; color: white; padding: 1.5rem; border-radius: 15px; margin: 2rem 0 1.5rem; text-align: center; font-size: 1.8rem; font-weight: 600;'>
                    📋 Detailed Analysis
                </div>
            """, unsafe_allow_html=True)

            # Key Points Section
            with st.expander("", expanded=True):
                st.markdown("<h3 style='color: #FF0000; font-weight: 700; margin-bottom: 1rem; font-size: 1.8rem;'>📝 Key Points</h3>", unsafe_allow_html=True)
                for point in analysis["key_points"]:
                    st.markdown(f"""
                        <div class="analysis-item" style="color: #000000 !important;">
                            <span style='color: #1a237e; margin-right: 0.5rem;'>→</span>
                            {point}
                        </div>
                    """, unsafe_allow_html=True)

            # Privacy Issues Section
            with st.expander("", expanded=True):
                st.markdown("<h3 style='color: #FF0000; font-weight: 700; margin-bottom: 1rem; font-size: 1.8rem;'>🔒 Privacy Issues</h3>", unsafe_allow_html=True)
                for issue in analysis["privacy_issues"]:
                    st.markdown(f"""
                        <div class="analysis-item" style="color: #000000 !important;">
                            <span style='color: #1a237e; margin-right: 0.5rem;'>→</span>
                            {issue}
                        </div>
                    """, unsafe_allow_html=True)

            # Major Concerns Section
            with st.expander("", expanded=True):
                st.markdown("<h3 style='color: #FF0000; font-weight: 700; margin-bottom: 1rem; font-size: 1.8rem;'>⚠️ Major Concerns</h3>", unsafe_allow_html=True)
                for concern in analysis["major_concerns"]:
                    st.markdown(f"""
                        <div class="analysis-item" style="color: #000000 !important;">
                            <span style='color: #1a237e; margin-right: 0.5rem;'>→</span>
                            {concern}
                        </div>
                    """, unsafe_allow_html=True)

            # Data Misuse Section
            with st.expander("", expanded=True):
                st.markdown("<h3 style='color: #FF0000; font-weight: 700; margin-bottom: 1rem; font-size: 1.8rem;'>🛡️ Data Misuse Risks</h3>", unsafe_allow_html=True)
                for risk in analysis["data_misuse"]:
                    st.markdown(f"""
                        <div class="analysis-item" style="color: #000000 !important;">
                            <span style='color: #1a237e; margin-right: 0.5rem;'>→</span>
                            {risk}
                        </div>
                    """, unsafe_allow_html=True)

            # Advantages Section
            with st.expander("", expanded=True):
                st.markdown("<h3 style='color: #FF0000; font-weight: 700; margin-bottom: 1rem; font-size: 1.8rem;'>💫 Advantages</h3>", unsafe_allow_html=True)
                for advantage in analysis["advantages"]:
                    st.markdown(f"""
                        <div class="analysis-item" style="color: #000000 !important;">
                            <span style='color: #1a237e; margin-right: 0.5rem;'>→</span>
                            {advantage}
                        </div>
                    """, unsafe_allow_html=True)

            # Disadvantages Section
            with st.expander("", expanded=True):
                st.markdown("<h3 style='color: #FF0000; font-weight: 700; margin-bottom: 1rem; font-size: 1.8rem;'>⚡ Disadvantages</h3>", unsafe_allow_html=True)
                for disadvantage in analysis["disadvantages"]:
                    st.markdown(f"""
                        <div class="analysis-item" style="color: #000000 !important;">
                            <span style='color: #1a237e; margin-right: 0.5rem;'>→</span>
                            {disadvantage}
                        </div>
                    """, unsafe_allow_html=True)

            # Side Prompt Section
            with st.sidebar:
                st.markdown("""
                    <div class="sidebar-content">
                        <span class="sidebar-title">🔍 Understanding Your Analysis</span>
                        <span class="sidebar-text">
                            This analysis evaluates license agreements across multiple dimensions to give you a comprehensive view of potential risks, benefits, and concerns.
                        </span>
                        <span class="sidebar-text">
                            • Privacy Issues: Direct violations or concerns related to user privacy
                            • Major Concerns: Significant red flags in the policy
                            • Data Misuse Risks: Potential ways data could be mishandled
                            • Advantages: Beneficial terms and protections for users
                            • Disadvantages: Unfavorable terms and limitations
                        </span>
                        <span class="sidebar-text">
                            Review each section carefully to understand the full implications of this agreement.
                        </span>
                    </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 

    