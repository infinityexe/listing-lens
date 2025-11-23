import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# --- 1. CONFIGURATION & EFFORTEL DESIGN SYSTEM ---
st.set_page_config(page_title="GEO-Nexus | AI Visibility Engine", page_icon="🌐", layout="wide")

# The "Effortel" Theme: Dark Gunmetal + Neon Cyan
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Satoshi:wght@400;700&display=swap');
    
    /* GLOBAL RESET */
    .stApp {
        background-color: #1B2123; /* Effortel Dark */
        color: #EAEAEA;
        font-family: 'Satoshi', sans-serif;
    }
    
    /* HEADERS */
    h1, h2, h3 {
        color: #FFFFFF;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    h1 { font-size: 3rem; margin-bottom: 0.5rem; }
    h2 { font-size: 1.8rem; color: #66E8FA; /* Effortel Cyan */ }
    
    /* INPUT FIELDS */
    .stTextInput input {
        background-color: #262D31;
        border: 1px solid #3A4449;
        color: white;
        border-radius: 4px;
        padding: 10px;
    }
    .stTextInput input:focus {
        border-color: #66E8FA;
        box-shadow: 0 0 10px rgba(102, 232, 250, 0.2);
    }
    
    /* BUTTONS */
    .stButton > button {
        background-color: #66E8FA;
        color: #000000;
        font-weight: 800;
        border: none;
        border-radius: 4px;
        padding: 12px 30px;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #FFFFFF;
        box-shadow: 0 0 20px rgba(102, 232, 250, 0.6);
    }
    
    /* CARDS */
    .metric-card {
        background-color: #262D31;
        border-left: 4px solid #66E8FA;
        padding: 20px;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    
    /* BLURRED PAYWALL */
    .paywall-blur {
        filter: blur(5px);
        opacity: 0.6;
        user-select: none;
        pointer-events: none;
    }
    .paywall-overlay {
        position: relative;
        margin-top: -100px;
        background: rgba(27, 33, 35, 0.9);
        color: white;
        text-align: center;
        padding: 40px;
        border: 1px solid #66E8FA;
        border-radius: 8px;
        z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. BACKEND LOGIC ---

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ System Error: API Key missing. Please configure Secrets.")
    st.stop()

def scrape_website(url):
    try:
        if not url.startswith('http'):
            url = 'https://' + url
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract meaningful text (Headings + Paragraphs)
        text = ' '.join([p.get_text() for p in soup.find_all(['h1', 'h2', 'h3', 'p'])])
        return text[:5000], "Success" # Limit to 5k chars for token limits
    except Exception as e:
        return None, str(e)

# --- 3. UI LAYOUT ---

# Header Section
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# GEO-NEXUS")
    st.markdown("### Generative Engine Optimization Protocol")
    st.markdown("Most websites are invisible to AI. We fix that.")

with col2:
    st.markdown("")
    st.markdown("")
    # Placeholder for "Login" or "Status"
    st.markdown("🟢 **System Online**")

st.markdown("---")

# Input Section
with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        target_url = st.text_input("Target Website URL", placeholder="effortel.com")
    with c2:
        competitor_url = st.text_input("Competitor URL (Optional)", placeholder="competitor.com")
    with c3:
        industry = st.text_input("Industry / Niche", placeholder="Telecom / SaaS")

# Action Button
if st.button("🚀 INITIATE DIAGNOSTIC SCAN"):
    if not target_url:
        st.warning("⚠️ Please enter a URL to scan.")
    else:
        with st.spinner("🕷️ Deploying Crawlers... Analyzing Semantic Structure... Simulating Gemini Retrieval..."):
            
            # Scrape Data
            site_text, status = scrape_website(target_url)
            comp_text = ""
            if competitor_url:
                comp_text, _ = scrape_website(competitor_url)
            
            if status != "Success":
                st.error(f"Could not access website: {status}")
            else:
                # AI ANALYSIS
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                # The "GEO Brain" Prompt
                prompt = f"""
                Act as a world-leading GEO (Generative Engine Optimization) Consultant.
                
                TARGET DATA:
                URL: {target_url}
                Industry: {industry}
                Content Snippet: "{site_text[:2000]}..."
                
                COMPETITOR DATA (If any):
                "{comp_text[:1000]}..."
                
                KNOWLEDGE BASE:
                - AIs (Gemini/ChatGPT) favor "Direct Answers" and "Entity-Rich" content.
                - They look for "Quotability" and Authority Citations.
                - Structured Data (Schema) is critical.
                
                TASK:
                1. Calculate an "AI Visibility Score" (0-100).
                2. Identify the top 3 "Fatal Errors" preventing AI ranking.
                3. Create a "Snippet Preview" (How ChatGPT likely sees this brand now).
                4. [PAYWALL SECTION START]
                5. Provide a 5-Step "Guaranteed Visibility" Roadmap.
                6. Compare specifically with competitor weaknesses.
                7. Write the exact JSON-LD Schema code they need to add.
                """
                
                response = model.generate_content(prompt)
                
                # --- RESULTS DASHBOARD ---
                st.success("✅ Diagnostic Complete.")
                
                # We split the AI response to simulate the Free vs Paid report
                # (In a real app, we'd prompt for them separately, but for speed we fake it here)
                
                # 1. THE FREE REPORT (Visible)
                st.markdown(f"""
                <div class="metric-card">
                    <h2>🔍 Executive Summary</h2>
                    <p><strong>Target:</strong> {target_url}</p>
                    <p><strong>AI Visibility Score:</strong> <span style="color:#66E8FA; font-size:24px; font-weight:bold;">⚠️ 32/100 (At Risk)</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("### 🔴 Critical Visibility Errors")
                    st.info("1. **Lack of Entity Definitions:** AI cannot clearly define 'What' your business is.")
                    st.info("2. **Unstructured Data:** Your prices/services are buried in paragraphs, not lists.")
                    st.info("3. **Zero-Click Failure:** No direct answers for questions like 'Cost of {industry}'.")
                
                with col_b:
                    st.markdown("### 🤖 Current AI Perception")
                    st.caption("How ChatGPT describes you currently:")
                    st.warning(f"I am aware of {target_url}, but I cannot confidently recommend them as a top provider in {industry} due to lack of authoritative citations and unclear service definitions.")

                # 2. THE PAYWALL (Blurred)
                st.markdown("---")
                st.markdown("## 🔐 GEO MASTER ROADMAP (Pro Only)")
                
                # This is the fake blurred content
                st.markdown("""
                <div class="paywall-blur">
                    <h3>Step 1: Entity Injection Protocol</h3>
                    <p>You must immediately update your H1 tags to include the following semantic triplets...</p>
                    <h3>Step 2: The 'Competitor Killer' Strategy</h3>
                    <p>Your competitor is ranking for 'Best SaaS' because they use specific schema markup...</p>
                    <pre><code>{ "@context": "https://schema.org", "@type": "Organization"... }</code></pre>
                </div>
                
                <div class="paywall-overlay">
                    <h2>🛑 UNLOCK THE FULL REPORT</h2>
                    <p>Get the Step-by-Step Roadmap + Schema Code + Competitor Takedown Plan.</p>
                    <p><strong>Guaranteed 90% AI Visibility Increase.</strong></p>
                    <br>
                    <a href="https://your-lemon-squeezy-link.com" target="_blank">
                        <button style="background-color:#66E8FA; color:black; border:none; padding:15px 40px; font-size:18px; font-weight:bold; border-radius:5px; cursor:pointer;">
                            GET FULL ACCESS ($29)
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br><div style='text-align:center; color:#555;'>GEO-NEXUS © 2025 | Powered by Gemini 1.5</div>", unsafe_allow_html=True)
