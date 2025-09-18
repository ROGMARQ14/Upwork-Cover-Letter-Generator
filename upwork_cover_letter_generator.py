
import streamlit as st

# Minimal imports first - add others only if needed
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    st.error("Requests library not available")

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    st.error("BeautifulSoup not available")

# Configure page
st.set_page_config(
    page_title="Upwork Cover Letter Generator",
    page_icon="✍️",
    layout="wide"
)

# App title
st.title("✍️ Upwork Cover Letter Generator")
st.markdown("Generate compelling, professional cover letters for Upwork job postings using AI")

def test_imports():
    """Test if all required imports work"""
    import_status = {}

    try:
        import openai
        import_status["OpenAI"] = "✅ Available"
    except ImportError as e:
        import_status["OpenAI"] = f"❌ Not available: {e}"

    try:
        import anthropic
        import_status["Anthropic"] = "✅ Available"
    except ImportError as e:
        import_status["Anthropic"] = f"❌ Not available: {e}"

    try:
        import google.generativeai as genai
        import_status["Gemini"] = "✅ Available"
    except ImportError as e:
        import_status["Gemini"] = f"❌ Not available: {e}"

    return import_status

def get_available_providers():
    """Check which AI providers have API keys configured"""
    providers = {}

    # Test OpenAI
    try:
        if st.secrets.get("OPENAI_API_KEY"):
            import openai
            providers["OpenAI"] = {
                "gpt-4o": "GPT-4o",
                "gpt-4o-mini": "GPT-4o Mini",
                "gpt-3.5-turbo": "GPT-3.5 Turbo"
            }
    except Exception as e:
        st.sidebar.error(f"OpenAI setup error: {e}")

    # Test Anthropic
    try:
        if st.secrets.get("ANTHROPIC_API_KEY"):
            import anthropic
            providers["Anthropic"] = {
                "claude-3-5-sonnet-20241022": "Claude 3.5 Sonnet",
                "claude-3-haiku-20240307": "Claude 3 Haiku"
            }
    except Exception as e:
        st.sidebar.error(f"Anthropic setup error: {e}")

    # Test Gemini
    try:
        if st.secrets.get("GEMINI_API_KEY"):
            import google.generativeai as genai
            providers["Gemini"] = {
                "gemini-1.5-pro": "Gemini 1.5 Pro",
                "gemini-1.5-flash": "Gemini 1.5 Flash"
            }
    except Exception as e:
        st.sidebar.error(f"Gemini setup error: {e}")

    return providers

def fetch_job_details(url):
    """Fetch job title, summary, and description from Upwork job URL"""
    if not REQUESTS_AVAILABLE or not BS4_AVAILABLE:
        return {
            'title': "Please enter manually",
            'summary': "Please enter manually", 
            'description': "Please enter manually"
        }

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
            client = openai.OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content

        elif ai_provider == "Anthropic":
            import anthropic
            client = anthropic.Anthropic(api_key=st.secrets.get("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model=model_name,
                max_tokens=500,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

        elif ai_provider == "Gemini":
            import google.generativeai as genai
            genai.configure(api_key=st.secrets.get("GEMINI_API_KEY"))
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text

    except Exception as e:
        return f"Error generating cover letter: {str(e)}"

def main():
    """Main app interface"""

    # Debug section
    with st.expander("🔧 Debug Info", expanded=False):
        st.write("**Import Status:**")
        import_status = test_imports()
        for service, status in import_status.items():
            st.write(f"- {service}: {status}")

        st.write("**Secrets Available:**")
        secrets_info = {
            "OpenAI": "✅ Configured" if st.secrets.get("OPENAI_API_KEY") else "❌ Not configured",
            "Anthropic": "✅ Configured" if st.secrets.get("ANTHROPIC_API_KEY") else "❌ Not configured", 
            "Gemini": "✅ Configured" if st.secrets.get("GEMINI_API_KEY") else "❌ Not configured"
        }
        for service, status in secrets_info.items():
            st.write(f"- {service}: {status}")

    # Check available providers
    available_providers = get_available_providers()

    if not available_providers:
        st.error("⚠️ No AI providers configured!")
        st.info("Please add at least one API key in Streamlit Cloud secrets:")
        st.code("""
OPENAI_API_KEY = "your_openai_key_here"
ANTHROPIC_API_KEY = "your_anthropic_key_here"
GEMINI_API_KEY = "your_gemini_key_here"
        """)
        st.stop()

    # Sidebar for AI model selection
    with st.sidebar:
        st.header("🤖 AI Model Selection")

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

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📋 Job Details")

        job_url = st.text_input(
            "Upwork Job URL:",
            placeholder="https://www.upwork.com/jobs/...",
            help="Paste the full Upwork job posting URL"
        )

        if st.button("🔍 Fetch Job Details", type="primary"):
            if job_url:
                with st.spinner("Fetching job details..."):
                    job_details = fetch_job_details(job_url)

                if job_details:
                    st.session_state.job_details = job_details
                    st.success("✅ Job details fetched successfully!")
            else:
                st.warning("Please enter a job URL first.")

        # Manual entry option
        st.markdown("### Or enter manually:")
        manual_title = st.text_input("Job Title:", key="manual_title")
        manual_summary = st.text_area("Job Summary:", height=100, key="manual_summary")
        manual_description = st.text_area("Job Description:", height=200, key="manual_description")

        if st.button("📝 Use Manual Entry"):
            st.session_state.job_details = {
                'title': manual_title,
                'summary': manual_summary,
                'description': manual_description
            }
            st.success("✅ Manual job details saved!")

        # Display and edit job details if available
        if hasattr(st.session_state, 'job_details'):
            job_data = st.session_state.job_details

            st.subheader("Current Job Information")
            with st.expander("📝 Edit Job Details", expanded=True):
                edited_title = st.text_input("Job Title:", value=job_data.get('title', ''), key="edit_title")
                edited_summary = st.text_area("Summary:", value=job_data.get('summary', ''), height=100, key="edit_summary")
                edited_description = st.text_area("Description:", value=job_data.get('description', ''), height=200, key="edit_desc")

                st.session_state.job_details = {
                    'title': edited_title,
                    'summary': edited_summary,
                    'description': edited_description
                }

    with col2:
        st.header("✍️ Generated Cover Letter")

        if st.button("🚀 Generate Cover Letter", type="primary"):
            if hasattr(st.session_state, 'job_details'):
                with st.spinner(f"Generating cover letter with {available_providers[selected_provider][selected_model]}..."):
                    cover_letter = generate_cover_letter(
                        st.session_state.job_details,
                        selected_provider,
                        selected_model
                    )

                if cover_letter:
                    st.session_state.cover_letter = cover_letter
                    st.success("✅ Cover letter generated successfully!")
            else:
                st.warning("Please enter job details first.")

        # Display generated cover letter
        if hasattr(st.session_state, 'cover_letter'):
            st.subheader("Your Cover Letter")

            cover_letter_text = st.text_area(
                "Generated Cover Letter:",
                value=st.session_state.cover_letter,
                height=400,
                help="Copy this text and paste it into your Upwork proposal"
            )

            # Word count
            word_count = len(cover_letter_text.split())
            if word_count > 250:
                st.warning(f"⚠️ Word count: {word_count} (Recommended: ≤250 words)")
            else:
                st.success(f"✅ Word count: {word_count}/250")

    # Footer
    st.markdown("---")
    st.markdown("Built for professional Upwork freelancers | Follow the 7-step system for maximum impact")

if __name__ == "__main__":
    main()
