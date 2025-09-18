# Upwork Cover Letter Generator 📝

A powerful Streamlit app that generates compelling, professional cover letters for Upwork job postings using AI. Built specifically for freelancers who want to follow proven proposal writing strategies.

## Features ✨

- **URL-based Job Extraction**: Simply paste an Upwork job URL to automatically extract job title, summary, and description
- **Multi-AI Provider Support**: Choose from OpenAI, Anthropic, or Google Gemini models
- **7-Step Proven Framework**: Based on the proven Upwork proposal writing system
- **Smart Emoji Integration**: Professional emoji usage that enhances readability
- **Word Count Tracking**: Keeps your proposals within the optimal 250-word limit
- **Editable Job Details**: Manually edit extracted job information if needed
- **Manual Entry Option**: Backup method if URL fetching fails
- **Debug Section**: Shows API status and configuration details

## Supported AI Models 🤖

### OpenAI
- GPT-4o
- GPT-4o Mini
- GPT-3.5 Turbo

### Anthropic
- Claude 3.5 Sonnet
- Claude 3 Haiku

### Google Gemini
- Gemini 1.5 Pro
- Gemini 1.5 Flash

## Installation & Setup 🚀

### 1. Clone or Download
Download the files to your local machine:
- `upwork_cover_letter_generator.py`
- `requirements.txt`
- `.streamlit/config.toml`
- `.streamlit/secrets.toml` (template)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys

#### For Local Development:
Create `.streamlit/secrets.toml` file:
```toml
OPENAI_API_KEY = "your_openai_api_key_here"
ANTHROPIC_API_KEY = "your_anthropic_api_key_here"
GEMINI_API_KEY = "your_gemini_api_key_here"
```

#### For Streamlit Cloud:
Add these in the Streamlit Cloud secrets tab:
```toml
OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxxxxxxxxxx"
ANTHROPIC_API_KEY = "sk-ant-xxxxxxxxxxxxxxxxxxxxx"
GEMINI_API_KEY = "AIzaSyxxxxxxxxxxxxxxxxxxxxx"
```

### 4. Run the Application
```bash
streamlit run upwork_cover_letter_generator.py
```

## How to Use 📋

1. **Enter Job URL**: Paste the Upwork job posting URL
2. **Fetch Details**: Click "Fetch Job Details" to automatically extract job information
3. **Edit if Needed**: Modify the extracted job details or use manual entry
4. **Choose AI Model**: Select your preferred AI provider and model from the sidebar
5. **Generate**: Click "Generate Cover Letter" to create your proposal
6. **Copy & Use**: Copy the generated cover letter and paste it into your Upwork proposal

## The 7-Step System 📈

This app follows a proven 7-step framework for writing effective Upwork proposals:

1. **Hook & Twist** - Grab attention and show understanding of deeper business impact
2. **Save the Day** - Position yourself as the solution they need
3. **Social Proof** - Share one relevant achievement with numbers if possible
4. **Results Preview** - Paint a picture of successful outcomes
5. **Clear CTA** - Tell them exactly what the next step should be
6. **P.S.** - Add unexpected value to create excitement

## Key Features & Rules 🎯

- **250-word maximum** for optimal readability
- **Client-focused approach** (90% client needs, 10% your credentials)
- **Strategic emoji usage** (3-5 professional emojis total)
- **Conversational tone** (friendly but professional)
- **No rate discussions** (unless specifically requested in the job post)

## Deployment to Streamlit Cloud 🌐

### 1. Prepare Your Repository
- Push your code to GitHub
- Ensure all files are in the root directory:
  - `upwork_cover_letter_generator.py`
  - `requirements.txt`
  - `.streamlit/config.toml`

### 2. Deploy on Streamlit Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your repository
4. Set the main file path: `upwork_cover_letter_generator.py`
5. Click "Deploy"

### 3. Configure Secrets
1. Go to your app settings in Streamlit Cloud
2. Navigate to the "Secrets" tab
3. Add your API keys exactly as shown:
```toml
OPENAI_API_KEY = "your_key_here"
ANTHROPIC_API_KEY = "your_key_here"
GEMINI_API_KEY = "your_key_here"
```

## Getting API Keys 🔑

### OpenAI
1. Visit [platform.openai.com](https://platform.openai.com)
2. Sign up/login and go to API keys
3. Create a new secret key (starts with `sk-proj-`)

### Anthropic
1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Sign up/login and navigate to API keys
3. Generate a new API key (starts with `sk-ant-`)

### Google Gemini
1. Visit [aistudio.google.com](https://aistudio.google.com)
2. Sign in with Google account
3. Create an API key (starts with `AIzaSy`)

## Troubleshooting 🔧

### Common Issues:

**"No AI providers configured"**
- Make sure at least one API key is set in your secrets
- Check the debug section to verify API key detection
- Verify the key names match exactly (case-sensitive)

**"Error fetching job details"**
- Ensure the URL is a valid Upwork job posting
- Some job postings may have different HTML structures
- Use the manual entry option as a backup

**API Errors**
- OpenAI: Check your usage limits and billing
- Anthropic: Ensure you have sufficient credits
- Gemini: Verify your quota hasn't been exceeded

**Secrets Not Detected**
- In Streamlit Cloud, make sure API keys are added in the Secrets tab
- Check that there are no extra spaces or quotes
- Use the debug section to verify secret detection

## Tips for Best Results 💡

1. **Use specific job URLs**: Direct job posting URLs work best
2. **Review extracted details**: Always check and refine the extracted job information
3. **Choose the right model**: Different models have different strengths
4. **Stay under 250 words**: Longer proposals perform worse on Upwork
5. **Personalize further**: Use the generated letter as a base, then add personal touches
6. **Check the debug section**: Use it to troubleshoot any configuration issues

## Debug Features 🔍

The app includes a debug section that shows:
- ✅ Which AI libraries are available
- ✅ Which API keys are configured
- ✅ First 10 characters of each API key for verification
- ✅ Import status for all dependencies

## File Structure 📁

```
upwork-cover-letter-generator/
├── upwork_cover_letter_generator.py  # Main application
├── requirements.txt                   # Python dependencies
├── .streamlit/
│   ├── config.toml                   # Streamlit configuration
│   └── secrets.toml                  # API keys (template)
├── .gitignore                        # Git ignore file
└── README.md                         # This file
```

## Support & Feedback 📞

If you encounter issues:
1. Check the debug section in the app
2. Verify your API keys are correctly configured
3. Review the troubleshooting section above
4. Ensure all dependencies are properly installed

## License 📄

This project is designed for professional freelancers using Upwork. Please use responsibly and in accordance with Upwork's terms of service.

---

**Built for professional Upwork freelancers | Follow the 7-step system for maximum impact**
