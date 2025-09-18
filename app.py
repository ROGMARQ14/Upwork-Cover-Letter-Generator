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

# This is the old, flawed 7-step system description. We will use a more direct prompt now.
# seven_step_system = "..." # Removed for clarity.

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
                # --- NEW, IMPROVED PROMPT ---
                prompt = f"""
                You are an expert Upwork proposal writer, acting as a consultant. Your goal is to write a cover letter that is **100% client-focused**. It should feel like a direct, thoughtful response to their specific needs, not a generic sales pitch.

                **CRITICAL RULE:** The cover letter must be about the **client's problem** and how I am the unique solution. **DO NOT** just list my skills or accomplishments. Instead, connect my specific experiences directly to the tasks and goals mentioned in the job description.

                **Here is the client's job post:**
                - **Job Title:** {job_title}
                - **Job Description:** {job_description}

                **Here is my professional background (use this as a database of facts to draw from, NOT a template to copy):**
                {user_profile}

                **Follow this specific thought process and structure:**

                **Step 1: The Hook & Twist (First 1-2 lines)**
                - Read the job description carefully. What is the client's *real* goal? What is the underlying business problem they are trying to solve?
                - Start with a hook that immediately addresses that core problem. Show you've thought about their situation. Use an emoji or two here to be personable.
                - Example: If they need SEO for a new SaaS, the real goal isn't just "ranking," it's "acquiring users and reducing CAC." Your hook should reflect that deeper understanding.

                **Step 2: The Bridge (1 paragraph)**
                - Briefly introduce yourself as the solution to the problem you just identified.
                - Connect 1-2 of your MOST RELEVANT experiences or skills from my profile directly to their needs.
                - Example: "Seeing that you need to improve your SaaS platform's organic acquisition, my experience reducing CAC by 40% for a similar platform by optimizing their content strategy comes to mind."

                **Step 3: Provide Evidence (Bulleted list or short paragraph)**
                - Back up your claim from Step 2.
                - Pull 1-2 of the most relevant, quantifiable results (case studies, wins) from my profile that mirror the client's goals.
                - If they are a local business, use my local business case study. If they are SaaS, use my SaaS results. Be highly selective.
                - You can also optionally include a highly relevant snippet from a client testimonial.

                **Step 4: The Call to Action (1 line)**
                - The goal is to start a conversation, not close a sale.
                - Avoid generic or pushy phrases like "click the accept button."
                - Suggest a next step. Examples: "Would you be open to a brief chat next week to discuss your goals?" or "I have a few initial ideas for your strategy. Happy to share them on a quick call."

                **Step 5: The P.S. (Optional but powerful)**
                - Add a final, personalized touch. This shows you've done extra thinking.
                - Example: "P.S. I noticed your main competitor is [Competitor Name]. I have a specific idea on how we could improve your [specific area] to gain an edge." (If you can't find a competitor, make a more general but insightful P.S.).

                **Final Output Instructions:**
                - Keep the tone professional, confident, and consultative.
                - The final letter should be concise and easy to read.
                - **Output ONLY the cover letter content.** No extra text before or after.
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
