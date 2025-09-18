Upwork Cover Letter Generator
This Streamlit application generates high-quality, professional cover letter proposals for Upwork job listings. It uses your detailed professional profile and a proven 7-step system to craft personalized and effective cover letters using various state-of-the-art AI models.

How it Works
The app takes a job title and job description as input, combines it with your pre-defined professional background, and uses an AI model of your choice to generate a compelling cover letter. The goal is to increase your chances of getting noticed and hired on Upwork.

Setup and Installation
Clone the repository:

git clone <repository-url>
cd <repository-directory>

Install the dependencies:
Make sure you have Python 3.7+ installed. Then, install the required packages using pip:

pip install -r requirements.txt

Set up Streamlit Secrets:
This app is designed to work with Streamlit Cloud and uses Streamlit Secrets for API key management. You'll need to add your API keys to your Streamlit Cloud workspace.

Create a secrets.toml file in a .streamlit directory in your project's root folder for local development.

Your secrets.toml file should look like this:

# .streamlit/secrets.toml

OPENAI_API_KEY = "your-openai-api-key"
ANTHROPIC_API_KEY = "your-anthropic-api-key"
GOOGLE_API_KEY = "your-google-api-key"

When deploying on Streamlit Cloud, you will copy these key-value pairs into the "Secrets" section of your app's settings.

Run the application:
To run the app locally, use the following command:

streamlit run app.py

Features
Personalized Cover Letters: Generates cover letters tailored to specific job listings.

Multi-model Support: Choose from a variety of powerful AI models from OpenAI, Anthropic, and Google.

Secure API Key Management: Uses Streamlit Secrets to keep your API keys safe.

Based on a Proven System: Incorporates a 7-step proposal system for maximum impact.

Includes Your Professional Profile: Automatically injects your detailed skills, experience, and accolades into the generation process.
