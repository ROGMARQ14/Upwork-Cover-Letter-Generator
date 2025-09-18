import streamlit as st
import os
import openai
import anthropic
import google.generativeai as genai

# --- User Profile and System Prompts ---

user_profile = """
**Main Profile:**

**Title/Services I Offer:** Senior SEO Expert| AI Search Optimization | Local SEO Growth | 10y+
**Hourly Rate:** $35.00/hr

After a 4-year absence from this community to dedicate myself full-time as a Senior SEO Strategist for one of the fastest-growing marketing agencies in the US, as ranked by Inc 500 in 2024, I am now returning to build long-term client partnerships to set the foundation and start my own agency in 2026.

My agency experience managing 50+ concurrent campaigns gives me unique insights into what truly moves the needle.

**🏆What sets me apart?**
✅Manual Technical SEO Audits: Core Web Vitals optimization, schema implementation, and site architecture that search engines love.
✅AI-First Approach: Leveraging ChatGPT, Claude, Perplexity, Gemini, and advanced tools for content optimization that outrank traditional methods.
✅Custom Strategy Development: Tailored SEO roadmaps explicitly built for each client's industry, competition, and business goals—no cookie-cutter approaches
✅Industry Intelligence: Continuous research into SEO developments, algorithm updates, and emerging technologies (like AI) that impact search—staying ahead of the curve
✅Transparent Communication: Detailed reporting, regular updates, and honest assessment of results—clients always know exactly where their project stands
✅Documented Results: From 669% keyword growth, generating 204 venue tours to 1,503 career applications for manufacturing clients
✅Cross-Industry Expertise: Proven success in SaaS, manufacturing, local business, apps, and B2B services

**🏆What do I offer?**
✅Strategic Audit: Comprehensive technical and competitive analysis
✅AI-Enhanced Strategy: Custom optimization roadmap using the latest algorithm insights
✅Implementation: Systematic execution with weekly progress reports
✅Scale & Optimize: Continuous refinement based on performance data

**🏆Recent Documented Wins:**
✅ 2,400% traffic explosion: 12 to 300+ monthly visitors for no-code agency
✅ 427% growth for screen time app while competitors burned ad budgets
✅ 669% keyword growth generating $234K-$468K potential revenue for wedding venue
✅ 1,503 career applications solving critical talent acquisition challenges
✅ 40% CAC reduction and 60% cost savings vs. paid channels for SaaS platform

**🏆Documented Industry Expertise**
🏭 B2B Manufacturing: Generated 1,503 career applications for an automotive manufacturer, solved critical talent acquisition challenges
📱 SaaS & Apps: 427% growth for screen time app, 118% growth for ecommerce analytics platform with 40% CAC reduction
💼 Agency & Services: 2,400% traffic explosion for no-code agency during scale to 100+ employees and Gold Partner status
🏪 Local Business: 669% keyword growth, generating 204 venue tours and $234K-$468K potential revenue
🏭 Industrial Equipment: 41% traffic growth + "asphalt pavers" keyword dominance generating millions in potential revenue

I work exclusively with businesses ready to invest in sustainable growth. My strategies build competitive moats that strengthen over time, not just quick traffic spikes.

Ready to dominate your market? Let's discuss how my agency-tested strategies can transform your business.

**Second Profile Tab:**

❤ **WHAT PAST/CURRENT CLIENTS HAVE SAID ABOUT ME:**

"I was looking for someone to help us speed up one of our websites... In the end Roger exceeded our expectations and we are regularly scoring high 90s... Excellent service from someone who knows his stuff at a fair price. I have no hesitation in recommending him for your SEO / Web speed optimization needs. Roger is also a super nice guy and easy to work with. "
- Barry D. | CEO Midascode Ltd

"Only very, very rarely does someone exceed my expectations professionally... Roger did an amazing job searching for keywords and good titles for my new podcast... Roger has been precise, extremely systematic, and organized. I couldn't be happier with his SEO services..."
- Sylvia B. | Founder and CEO of Break Free Ltd

"I hired Roger for some SEO work - he has continued to exceed our expectations and deliver quality work promptly. The work has proven to be very useful in helping guide our marketing efforts."
- Josh W. | ePageCity, Inc.

💵 **SOME RESULTS I´VE GOTTEN FOR CLIENTS RECENTLY:**
+ 27% increase in impressions and 38% in clicks for an affiliate blog...
+ 74% improvement in the organic ranking position across 128 keywords for a local business...
+ 6% increase in revenue for an eCommerce site...

💪 **MY MAIN AREAS OF EXPERTISE:**
➡️ "Traditional" Search Engine Optimization (SEO)
➡️ "Advanced" Search Engine Optimization (AI SEO)
➡️ Technical SEO, AI Content Optimization, Core Web Vitals, Custom Schema Markup
➡️ Keyword/Topic Research, Manual SEO Audit, Local SEO Growth, E-commerce SEO
➡️ B2B SEO, Content Marketing, SaaS Growth, SEO Strategy & Planning

💻**SEO TOOLS I AM PROFICIENT IN:**
+ Google Search Console, Screaming Frog, SEMRush, Ahrefs

🤖 **OTHER TOOLS I AM PROFICIENT IN:**
+ N8N (AI Automations workflows), Claude/Claude Code, Perplexity, Gemini

❓ **WHY DO YOU NEED TO CONSIDER ME?**
I’m not an agency... I dedicate much personal attention to each client... I provide regular, in-depth reports...

**More Accolades:**
- Top-talent on Upwork with 98% Job Success
- 4.8/5 stars customer review rating
- Almost 100 projects and over 1,300+ hours invested
"""

seven_step_system = """
**The 7-Step Proposal System**

**Step 1: Personalize Your Hook and Twist**
The first line must grab attention (hook) and show you understand the deeper problem (twist). Avoid generic templates. Research the client's name if possible. The twist shows *why* they need the job done. Example: A client doesn't just need images; they need sales.

**Step 2: Save the Day**
Introduce yourself as the solution *after* the hook. Keep it client-focused (90% them, 10% you). Be short and sweet.

**Step 3: Establish Authority with Social Proof**
Use short, powerful snippets from your best client reviews. Keep them relevant to the client's industry. Maximum of three.

**Step 4: Showcase Results, Not Just Examples**
Demonstrate tangible results. Use relevant case studies. Don't just send a portfolio link; explain the context and the impact (e.g., "doubled conversion").

**Step 5: Guide the Client with a Call to Action (CTA)**
Tell the client exactly what to do next. Be explicit and personalize it. Example: "To get started, just click the green 'Accept' button, John."

**Step 6: Leverage the Power of the "P.S."**
Most people read the P.S. first. Use it to reinforce your message, create urgency, add a secondary CTA, or provide an extra personalized thought (e.g., "P.S. I looked at your competitor and have some ideas...").

**Step 7: The Final Action**
Send it. Trust the system.
"""

# --- API Key Configuration ---

# Try to get keys from Streamlit secrets
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except (KeyError, AttributeError):
    openai.api_key = ""

try:
    anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]
except (KeyError, AttributeError):
    anthropic_api_key = ""

try:
    google_api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=google_api_key)
except (KeyError, AttributeError):
    google_api_key = ""


# --- AI Model Generation Functions ---

def generate_with_openai(prompt, model):
    if not openai.api_key:
        st.error("OpenAI API key is not set. Please add it to your Streamlit secrets.")
        return None
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error with OpenAI API: {e}")
        return None

def generate_with_anthropic(prompt, model):
    if not anthropic_api_key:
        st.error("Anthropic API key is not set. Please add it to your Streamlit secrets.")
        return None
    try:
        client = anthropic.Anthropic(api_key=anthropic_api_key)
        response = client.messages.create(
            model=model,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        st.error(f"Error with Anthropic API: {e}")
        return None

def generate_with_google(prompt, model):
    if not google_api_key:
        st.error("Google API key is not set. Please add it to your Streamlit secrets.")
        return None
    try:
        model_instance = genai.GenerativeModel(model)
        response = model_instance.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error with Google Gemini API: {e}")
        return None

# --- Streamlit App UI ---

st.set_page_config(page_title="Upwork Cover Letter Generator", page_icon="✍️", layout="wide")

st.title("🚀 Upwork Cover Letter Generator")
st.markdown("Craft high-impact, professional cover letters for Upwork to enhance your hiring success.")

st.sidebar.header("🔑 API Key Configuration")
st.sidebar.info(
    "Your API keys are managed securely via Streamlit Secrets. "
    "If any key is missing, you can temporarily paste it below, but it's recommended to update your secrets for long-term use."
)

if not openai.api_key:
    openai.api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
if not anthropic_api_key:
    anthropic_api_key = st.sidebar.text_input("Enter Anthropic API Key", type="password")
if not google_api_key:
    google_api_key = st.sidebar.text_input("Enter Google API Key", type="password")
    if google_api_key:
        genai.configure(api_key=google_api_key)

col1, col2 = st.columns(2)

with col1:
    st.header("📋 Job Details")
    job_title = st.text_input("Job Listing Title")
    job_description = st.text_area("Job Description", height=300)

    st.header("🤖 AI Model Selection")
    model_provider = st.selectbox("Choose AI Provider", ["Google", "OpenAI", "Anthropic"])

    models = {
        "OpenAI": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"], # Placeholder for future models
        "Anthropic": ["claude-3-opus-20240229", "claude-3-sonnet-20240229"],
        "Google": ["gemini-1.5-pro-latest", "gemini-1.5-flash-latest"] # Placeholder for future models
    }

    # Simplified model names for display
    model_display_names = {
        "gpt-4o": "OpenAI: GPT-4o",
        "gpt-4o-mini": "OpenAI: GPT-4o Mini",
        "gpt-4-turbo": "OpenAI: GPT-4 Turbo",
        "gpt-3.5-turbo": "OpenAI: GPT-3.5 Turbo",
        "claude-3-opus-20240229": "Anthropic: Claude 3 Opus",
        "claude-3-sonnet-20240229": "Anthropic: Claude 3 Sonnet",
        "gemini-1.5-pro-latest": "Google: Gemini 1.5 Pro",
        "gemini-1.5-flash-latest": "Google: Gemini 1.5 Flash"
    }

    selected_model_key = st.selectbox(
        "Select a Model",
        options=models[model_provider],
        format_func=lambda x: model_display_names.get(x, x)
    )

    generate_button = st.button("✨ Generate Cover Letter", type="primary")

with col2:
    st.header("📄 Generated Cover Letter")
    if generate_button:
        if not job_title or not job_description:
            st.warning("Please provide both the Job Title and Job Description.")
        else:
            with st.spinner(f"Crafting your cover letter with {model_display_names.get(selected_model_key, selected_model_key)}..."):
                # Construct the comprehensive prompt
                prompt = f"""
                You are an expert Upwork proposal writer. Your task is to generate a professional, concise, and highly effective cover letter for an Upwork job application.

                **My Professional Profile:**
                {user_profile}

                **The 7-Step System to Follow:**
                {seven_step_system}

                **Job Details:**
                - **Job Title:** {job_title}
                - **Job Description:** {job_description}

                **Instructions for the Cover Letter:**
                1.  **Strictly follow the 7-step system.**
                2.  **Personalize heavily:** Tailor the letter to the specific project, highlighting relevant skills and experience from my profile that are mentioned in the job description.
                3.  **Focus on client benefits:** Explain HOW my skills will benefit the client and their project. Don't just list skills.
                4.  **Show results:** Where relevant, use specific numbers and results from my profile to demonstrate impact.
                5.  **Maintain a professional and confident tone.** Proofread carefully for typos and grammatical errors.
                6.  **Use emojis responsibly:** Add a few emojis, especially in the opening lines, to be engaging but not annoying.
                7.  **Create an elevator pitch:** Convince the client that I am the perfect fit for this specific job.
                8.  **Output only the cover letter content**, ready to be copied and pasted. Do not include any extra commentary before or after the letter.
                """

                cover_letter = None
                if model_provider == "OpenAI":
                    cover_letter = generate_with_openai(prompt, selected_model_key)
                elif model_provider == "Anthropic":
                    cover_letter = generate_with_anthropic(prompt, selected_model_key)
                elif model_provider == "Google":
                    cover_letter = generate_with_google(prompt, selected_model_key)

                if cover_letter:
                    st.text_area("Your Cover Letter:", cover_letter, height=500)
                    st.success("Cover letter generated successfully!")
                else:
                    st.error("Failed to generate cover letter. Please check your API keys and the error message above.")
    else:
        st.info("Your generated cover letter will appear here.")
