import os
import pyttsx3
import gradio as gr
from openai import AzureOpenAI

# Initialize environment variables
endpoint = os.getenv("ENDPOINT_URL", "")
deployment = os.getenv("DEPLOYMENT_NAME", "GPT35")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", " ")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)

# Initialize pyttsx3 engine for text-to-speech
engine = pyttsx3.init()

# Function to convert text to speech and play audio automatically
def text_to_speech_auto_play(text):
    engine.save_to_file(text, 'response_audio.wav')
    engine.runAndWait()
    return 'response_audio.wav'

# Maintain a conversation history
conversation_history = [
    {
        "role": "system",
        "content": "You are an AI assistant that helps people find information."
    }
]

# Function to transcribe audio using Whisper
def transcribe_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper",
            file=audio_file,
            response_format="text"
        )
    return transcription

# Main function that handles the entire process
def process_audio(audio_file_path):
    global conversation_history  # Access the global conversation history

    # Transcribe the audio
    transcribed_text = transcribe_audio(audio_file_path)

    # Add user query to conversation history
    conversation_history.append({
        "role": "user",
        "content": transcribed_text
    })

    # Check if user says they don't have any other questions
    if "no other questions" in transcribed_text.lower() or "nothing else" in transcribed_text.lower():
        conversation_history.append({
            "role": "assistant",
            "content": "Thank you for using the service! Have a nice day. Goodbye!"
        })
        audio_response = text_to_speech_auto_play("Thank you for using the service! Have a nice day. Goodbye!")
        conversation_history.clear()  # Clear the conversation history
        return audio_response

    # Generate assistant's response using full conversation history
    completion = client.chat.completions.create(
        model=deployment,
        messages=conversation_history,
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )

    # Extract the assistant's response
    assistant_response = completion.choices[0].message.content

    # Add the assistant's response to conversation history
    conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })

    # Append a follow-up question to the assistant's response
    final_response = assistant_response + " Do you have any other questions?"

    # Convert response to speech and play audio
    audio_response = text_to_speech_auto_play(final_response)

    return audio_response

# Dynamic and colorful interface with Gradio Blocks
with gr.Blocks(css=".gradio-container {background-color: #f0f4f7;}") as app:
    gr.Markdown("""
    <style>
        h1 {
            text-align: center;
            color: #333;
            font-family: Arial, sans-serif;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            color: #777;
        }
    </style>
    <h1>Retail ChatBot</h1>
    """)

    with gr.Row():
        with gr.Column(scale=1, min_width=400):
            # Replace audio input with a record button
            record_button = gr.Audio(type="filepath", label="Click to Record", interactive=True)
        with gr.Column(scale=1, min_width=400):
            gr.Markdown("""
                <div style="font-family: Arial, sans-serif; text-align: center; color: #555;">
                    <h3>AI Assistant Response:</h3>
                    <p>After recording, the AI will respond automatically.</p>
                </div>
            """)
            audio_output = gr.Audio(label="Assistant Response (Auto Play)", autoplay=True)

    # Trigger the process_audio function after recording is finished
    record_button.change(
        fn=process_audio,  # Process the audio after recording
        inputs=record_button,
        outputs=audio_output
    )

    gr.Markdown("""
        <div class="footer">
            <p>Powered by Azure OpenAI & Gradio</p>
        </div>
    """)

# Launch the Gradio app
app.launch()
