import streamlit as st

# Minimal imports first - add others only if needed
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# Configure page
st.set_page_config(
    page_title="Upwork Cover Letter Generator",
    page_icon="✍️",
    layout="wide"
)

# App title
st.title("✍️ Upwork Cover Letter Generator")
st.markdown("Generate compelling, professional cover letters for Upwork job postings using AI")

def check_secret_exists(key):
    """Check if a secret exists in Streamlit Cloud"""
    try:
        if hasattr(st.secrets, key):
            value = getattr(st.secrets, key)
            return value is not None and value != ""
        elif key in st.secrets:
            value = st.secrets[key]
            return value is not None and value != ""
        else:
            return False
    except Exception:
        return False

def get_secret_value(key):
    """Get secret value from Streamlit Cloud"""
    try:
        if hasattr(st.secrets, key):
            return getattr(st.secrets, key)
        elif key in st.secrets:
            return st.secrets[key]
        else:
            return None
    except Exception:
        return None

def get_available_providers():
    """Check which AI providers have API keys configured"""
    providers = {}
    
    # Test OpenAI
    try:
        if check_secret_exists("OPENAI_API_KEY"):
            import openai
            providers["OpenAI"] = {
                "gpt-4o": "GPT-4o",
                "gpt-4o-mini": "GPT-4o Mini",
                "gpt-3.5-turbo": "GPT-3.5 Turbo"
            }
    except Exception:
        pass  # Silently fail
    
    # Test Anthropic
    try:
        if check_secret_exists("ANTHROPIC_API_KEY"):
            import anthropic
            providers["Anthropic"] = {
                "claude-3-5-sonnet-20241022": "Claude 3.5 Sonnet",
                "claude-3-haiku-20240307": "Claude 3 Haiku"
            }
    except Exception:
        pass  # Silently fail
    
    # Test Gemini
    try:
        if check_secret_exists("GEMINI_API_KEY"):
            import google.generativeai as genai
            providers["Gemini"] = {
                "gemini-1.5-pro": "Gemini 1.5 Pro",
                "gemini-1.5-flash": "Gemini 1.5 Flash"
            }
    except Exception:
        pass  # Silently fail
    
    return providers

def fetch_job_details(url):
    """Fetch job title, summary, and description from Upwork job URL"""
    if not REQUESTS_AVAILABLE or not BS4_AVAILABLE:
        st.warning("⚠️ URL fetching not available. Please use manual entry below.")
        return None
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try multiple selectors for job title
        job_title = "Job title not found"
        title_selectors = [
            'h2.text-base.flex-1',
            'h1.job-title',
            'h1[data-test="job-title"]',
            '.job-title',
            'h1'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                job_title = element.get_text(strip=True)
                break
        
        # Try multiple selectors for summary
        summary = "Summary not found"
        summary_selectors = [
            '.text-base-sm',
            '.job-summary',
            '[data-test="job-summary"]'
        ]
        
        for selector in summary_selectors:
            element = soup.select_one(selector)
            if element:
                summary = element.get_text(strip=True)
                break
        
        # Try multiple selectors for description
        description = "Description not found"
        desc_selectors = [
            '.text-body-sm',
            '.job-description',
            '[data-test="job-description"]',
            '.description'
        ]
        
        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                description = element.get_text(strip=True)
                break
        
        return {
            'title': job_title,
            'summary': summary,
            'description': description
        }
        
    except Exception as e:
        st.error(f"Error fetching job details: {str(e)}")
        return None

def generate_cover_letter(job_details, ai_provider, model_name):
    """Generate cover letter using the specified AI provider and model"""
    
    base_prompt = """You are an expert Upwork proposal writer. Create a compelling cover letter that follows this EXACT 7-step structure, incorporating strategic emoji usage.

**CRITICAL RULES:**
- Maximum 250 words total
- Write conversationally, not formally
- Focus on the client's needs (90%), not your credentials (10%)
- Be specific to their project
- Never mention rates unless they asked
- Client can see your Upwork profile, so don't repeat bio info

**EMOJI USAGE RULES:**
- Use 3-5 emojis TOTAL throughout the entire letter
- MUST use 1-2 emojis in the first 2 lines to catch attention
- Use professional emojis that enhance meaning, not decorative ones
- Good emojis: 🎯 (goals), 💡 (ideas), ✅ (solutions), 📈 (growth), 🚀 (launch/speed), ⚡ (fast), 🔥 (urgent/hot), 💪 (strength), 🏆 (success), 👉 (pointing)
- Place emojis at the END of sentences, not in the middle
- Never use multiple emojis in a row
- Don't use childish or unprofessional emojis

**THE 7-STEP STRUCTURE:**

1. **Hook & Twist (2-3 sentences)**
   - Start with "Hey [Name]," only if you have their name
   - Hook: Reference their specific need (ADD EMOJI HERE)
   - Twist: Show you understand the deeper business impact

2. **Save the Day (2-3 sentences)**
   - Position yourself as the solution
   - Focus on what you'll achieve for them
   - No credential listing

3. **Social Proof (1-2 sentences)**
   - One specific relevant achievement
   - Include numbers if possible (can add emoji if impressive)

4. **Results Preview (2-3 sentences)**
   - Paint the picture of success
   - Be specific about outcomes

5. **Clear CTA (1-2 sentences)**
   - Tell them the next step (can add action emoji)
   - Make it easy to say yes

6. **P.S. (1-2 sentences)**
   - Add unexpected value
   - Create excitement (optional emoji)

**TONE:** Confident, friendly, enthusiastic but professional.
**REMEMBER:** Emojis should feel natural and enhance the message, not distract from it.

**JOB DETAILS:**
Title: {job_title}
Summary: {job_summary}
Description: {job_description}

Please generate a cover letter following the above structure and rules."""
    
    prompt = base_prompt.format(
        job_title=job_details.get('title', ''),
        job_summary=job_details.get('summary', ''),
        job_description=job_details.get('description', '')
    )
    
    try:
        if ai_provider == "OpenAI":
            import openai
            api_key = get_secret_value("OPENAI_API_KEY")
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
            
        elif ai_provider == "Anthropic":
            import anthropic
            api_key = get_secret_value("ANTHROPIC_API_KEY")
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model=model_name,
                max_tokens=500,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
            
        elif ai_provider == "Gemini":
            import google.generativeai as genai
            api_key = get_secret_value("GEMINI_API_KEY")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
            
    except Exception as e:
        return f"Error generating cover letter: {str(e)}. Please check your API configuration."

def main():
    """Main app interface"""
    
    # Check available providers
    available_providers = get_available_providers()
    
    # Always show the interface, even if no API keys are configured
    # Sidebar for AI model selection
    with st.sidebar:
        st.header("🤖 AI Model Selection")
        
        if not available_providers:
            st.error("⚠️ No AI providers configured!")
            st.markdown("**Configure API keys in Streamlit Cloud:**")
            st.markdown("1. Go to your app settings")
            st.markdown("2. Click 'Secrets' tab")
            st.markdown("3. Add your API keys:")
            st.code("""
OPENAI_API_KEY = "sk-proj-your_key"
ANTHROPIC_API_KEY = "sk-ant-your_key"
GEMINI_API_KEY = "AIzaSy-your_key"
            """, language="toml")
            
            st.markdown("**Get API keys:**")
            st.markdown("- [OpenAI API](https://platform.openai.com/api-keys)")
            st.markdown("- [Anthropic API](https://console.anthropic.com/)")
            st.markdown("- [Gemini API](https://aistudio.google.com/)")
            
            # Show disabled selections
            st.selectbox("Choose AI Provider:", ["Please configure API keys first"], disabled=True)
            st.selectbox("Choose Model:", ["Please configure API keys first"], disabled=True)
            
        else:
            provider_options = list(available_providers.keys())
            selected_provider = st.selectbox("Choose AI Provider:", provider_options)
            
            model_options = available_providers[selected_provider]
            selected_model = st.selectbox(
                "Choose Model:",
                options=list(model_options.keys()),
                format_func=lambda x: model_options[x]
            )
        
        st.markdown("---")
        st.markdown("### 📝 7-Step System")
        st.markdown("""
        1. **Hook & Twist** - Grab attention + show understanding
        2. **Save the Day** - Position as solution
        3. **Social Proof** - Relevant achievement
        4. **Results Preview** - Paint success picture
        5. **Clear CTA** - Tell them next step
        6. **P.S.** - Add unexpected value
        """)
        
        # Add usage tips
        with st.expander("💡 Usage Tips"):
            st.markdown("""
            - Keep proposals under 250 words
            - Focus 90% on client needs, 10% on you
            - Use 3-5 professional emojis total
            - Never mention rates unless asked
            - Be conversational, not formal
            """)
    
    # Main content area - ALWAYS SHOW THIS
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 Job Details")
        
        # URL input section - ALWAYS VISIBLE
        st.subheader("🔗 Paste Upwork Job URL")
        job_url = st.text_input(
            "Upwork Job URL:",
            placeholder="https://www.upwork.com/jobs/...",
            help="Paste the full Upwork job posting URL to auto-extract details",
            key="job_url_input"
        )
        
        if st.button("🔍 Fetch Job Details", type="primary", use_container_width=True):
            if job_url:
                with st.spinner("Fetching job details..."):
                    job_details = fetch_job_details(job_url)
                    
                if job_details:
                    st.session_state.job_details = job_details
                    st.success("✅ Job details fetched successfully!")
                else:
                    st.warning("Could not fetch details. Please use manual entry below.")
            else:
                st.warning("Please enter a job URL first.")
        
        st.markdown("---")
        
        # Manual entry section - ALWAYS VISIBLE
        st.subheader("✍️ Manual Entry")
        manual_title = st.text_input("Job Title:", key="manual_title")
        manual_summary = st.text_area("Job Summary:", height=100, key="manual_summary", 
                                     help="Brief description or requirements from the job post")
        manual_description = st.text_area("Job Description:", height=200, key="manual_description",
                                         help="Full job description with requirements and details")
        
        if st.button("📝 Use Manual Entry", type="secondary", use_container_width=True):
            if manual_title or manual_description:
                st.session_state.job_details = {
                    'title': manual_title,
                    'summary': manual_summary,
                    'description': manual_description
                }
                st.success("✅ Manual job details saved!")
            else:
                st.warning("Please enter at least a job title and description.")
        
        # Display current job details if available
        if hasattr(st.session_state, 'job_details'):
            job_data = st.session_state.job_details
            
            st.markdown("---")
            st.subheader("📄 Current Job Information")
            with st.expander("📝 Review & Edit Details", expanded=False):
                edited_title = st.text_input("Job Title:", value=job_data.get('title', ''), key="edit_title")
                edited_summary = st.text_area("Summary:", value=job_data.get('summary', ''), height=100, key="edit_summary")
                edited_description = st.text_area("Description:", value=job_data.get('description', ''), height=200, key="edit_desc")
                
                if st.button("💾 Update Details"):
                    st.session_state.job_details = {
                        'title': edited_title,
                        'summary': edited_summary,
                        'description': edited_description
                    }
                    st.success("✅ Details updated!")
                    st.experimental_rerun()
    
    with col2:
        st.header("✍️ Generated Cover Letter")
        
        # Generate button - show but disable if no API configured
        if not available_providers:
            st.button("🚀 Generate Cover Letter", type="primary", use_container_width=True, disabled=True,
                     help="Please configure API keys in the sidebar first")
            st.info("👈 Configure your API keys in the sidebar to enable cover letter generation")
            
        else:
            if st.button("🚀 Generate Cover Letter", type="primary", use_container_width=True):
                if hasattr(st.session_state, 'job_details'):
                    job_data = st.session_state.job_details
                    
                    # Validate that we have meaningful job details
                    if not job_data.get('title') and not job_data.get('description'):
                        st.error("Please provide at least a job title and description before generating.")
                    else:
                        with st.spinner(f"Generating cover letter with {available_providers[selected_provider][selected_model]}..."):
                            cover_letter = generate_cover_letter(
                                st.session_state.job_details,
                                selected_provider,
                                selected_model
                            )
                            
                        if cover_letter and not cover_letter.startswith("Error"):
                            st.session_state.cover_letter = cover_letter
                            st.success("✅ Cover letter generated successfully!")
                        else:
                            st.error(f"Failed to generate cover letter: {cover_letter}")
                else:
                    st.warning("Please enter job details first using one of the options on the left.")
        
        # Display generated cover letter - ALWAYS SHOW THIS SECTION
        if hasattr(st.session_state, 'cover_letter'):
            st.subheader("📝 Your Cover Letter")
            
            cover_letter_text = st.text_area(
                "Generated Cover Letter:",
                value=st.session_state.cover_letter,
                height=400,
                help="Copy this text and paste it into your Upwork proposal",
                key="final_cover_letter"
            )
            
            # Word count and analysis
            col_a, col_b = st.columns(2)
            with col_a:
                word_count = len(cover_letter_text.split())
                if word_count > 250:
                    st.warning(f"⚠️ Word count: {word_count} (Recommended: ≤250)")
                else:
                    st.success(f"✅ Word count: {word_count}/250")
            
            with col_b:
                # Count emojis (simple detection)
                emoji_count = sum(1 for char in cover_letter_text if ord(char) > 127)
                if emoji_count >= 3 and emoji_count <= 5:
                    st.success(f"✅ Emojis: {emoji_count}/3-5")
                else:
                    st.info(f"📊 Emojis: {emoji_count} (Recommended: 3-5)")
            
            # Copy button hint
            st.info("💡 **Tip**: Select all text above (Ctrl+A) and copy (Ctrl+C) to use in your Upwork proposal")
        
        else:
            # Show placeholder when no cover letter generated yet
            st.subheader("📝 Your Cover Letter")
            st.info("👈 Enter job details on the left and click 'Generate Cover Letter' to create your proposal")
            
            # Show sample cover letter structure
            with st.expander("📋 Preview: 7-Step Structure"):
                st.markdown("""
                **Sample Cover Letter Structure:**
                
                1. **Hook & Twist**: "Hi [Name], I see you need help with [specific need] 🎯..."
                
                2. **Save the Day**: "I can solve this by [your solution]..."
                
                3. **Social Proof**: "I recently helped a similar client achieve [result with numbers]..."
                
                4. **Results Preview**: "For your project, you can expect [specific outcomes]..."
                
                5. **Clear CTA**: "Ready to get started? Let's discuss your timeline 👉"
                
                6. **P.S.**: "P.S. I noticed [additional value/insight] 💡"
                """)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 14px;'>
            <p>Built for professional Upwork freelancers | Follow the 7-step system for maximum impact</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
