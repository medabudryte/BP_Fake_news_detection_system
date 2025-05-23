# 📰 Fake News Detection System

## Bachelor's Final Project – Streamlit Application

Welcome to the repository for the Fake News Detection System, a key component of a Bachelor's Final Project focused on identifying and analyzing misinformation. The application is designed to explore various machine learning and transformer-based models for evaluating the truthfulness of claims, integrated into an interactive web interface using Streamlit.

# 📁 Project Structure

## Inside the FAKENEWS_APP folder, you'll find modular components for the complete system:

- Pages/ – Individual pages for navigation within the Streamlit app (e.g., dashboard, model results, explanations).
- Models/ – Pretrained or custom-trained ML and transformer-based models for claim classification.
- Reports/ – Locally generated evaluation reports and visualizations.
- Utils/ – Helper functions for data processing, model loading, and prediction logic.
- app.py – application running file

# 🤖 LLM Integration (Optional)

The system allows integration with LLMs for enhanced claim analysis.
To enable this feature:

Sign up at OpenRouter.ai and obtain your API key.
Set your API key as an environment variable or input it directly when prompted in the app.

# 📊 Features

- Multi-model Support: Classic ML models (Logistic Regression, SVM) and advanced LLM.
- Interactive Analysis: Claim-level predictions with metadata, explanations, and visual summaries.
- Justification Analysis: Includes human-written justifications where available.
- User-Friendly UI: Built with Streamlit for smooth navigation and visualization.
- Custom Reports: Evaluation metrics, confusion matrices, and model comparison visuals.

📌 Use Cases

- Educational research on misinformation
- NLP experimentation with claim classification
- Human-centered fact-checking tool prototype

Project is currently running and licensed in Apache 2.0 license.
