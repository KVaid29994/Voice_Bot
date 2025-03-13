# Azure OpenAI Voice Output Project

## Introduction
This project leverages **Azure OpenAI** to generate voice outputs from text using **GPT-3.5**, **pyttsx3**, and **Gradio**. It integrates speech synthesis and interactive UI components to create a seamless text-to-speech experience.

## Technologies Used
- **Azure OpenAI (GPT-3.5)** – For generating natural language responses.
- **pyttsx3** – A Python-based text-to-speech engine for local voice synthesis.
- **Gradio** – A simple UI framework to create interactive web interfaces.
- **OpenAI API** – For accessing language models and generating responses.

## Features
- Converts text responses from **GPT-3.5** into speech.
- Provides an interactive web-based UI using **Gradio**.
- Supports **multiple voice settings** and playback options.
- Enables real-time text-to-speech processing with **low latency**.

## Installation
Ensure you have the required dependencies installed:
```bash
pip install openai pyttsx3 gradio
```

## Usage
1. Set up your **Azure OpenAI API key**:
   ```python
   import openai
   openai.api_key = "your_azure_openai_key"
   ```
2. Run the Gradio interface:
   ```python
   python app.py
   ```
3. Enter text in the Gradio UI and listen to the generated voice output.

## Future Enhancements
- Integrate **Azure Speech Services** for improved voice synthesis.
- Add **multilingual support** for broader accessibility.
- Enhance **UI customization** with additional voice settings.

## Conclusion
This project demonstrates how **Azure OpenAI** can be used to build **interactive and accessible voice AI applications**. By combining **GPT-3.5**, **pyttsx3**, and **Gradio**, we create a powerful text-to-speech pipeline with a user-friendly interface.
