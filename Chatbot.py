import openai
import gradio as gr
import os
from typing import List, Dict, Tuple

# Load your key from your environment variables
openai.api_key = "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"

personalities = {
    "Donald Trump": "You are Donald Trump. Be confident, bold, and use simple, direct language. Make statements with certainty and use a lot of superlatives.",
    "Tony Robbins": "You are Tony Robbins. Be inspirational, motivational, and positive. Speak in a charismatic and enthusiastic manner, and be very supportive.",
    "Funniest man in the world": "You are the funniest man in the world. Use humor and witticisms in your responses. Your goal is to make people laugh."
}

def append_system_message(messages: List[Dict[str, str]], system_content: str) -> List[Dict[str, str]]:
    messages.append({"role": "system", "content": system_content})
    return messages

def append_user_message(messages: List[Dict[str, str]], user_content: str) -> List[Dict[str, str]]:
    messages.append({"role": "user", "content": user_content})
    return messages

def append_assistant_message(messages: List[Dict[str, str]], assistant_content: str) -> List[Dict[str, str]]:
    messages.append({"role": "assistant", "content": assistant_content})
    return messages

def handle_conversation(messages: List[Dict[str, str]], user_input: str) -> Tuple[List[Dict[str, str]], str]:
    messages = append_user_message(messages, user_input)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    response_content = response['choices'][0]['message']['content']
    messages = append_assistant_message(messages, response_content)
    return messages, response_content

def CustomChatGPT(user_input: str, personality: str, reset: bool) -> str:
    global messages
    
    if reset or not 'messages' in globals():
        messages = append_system_message([], personalities[personality])

    try:
        messages, reply = handle_conversation(messages, user_input)
    except Exception as e:
        print(e)
        reply = "Sorry, I couldn't process that. Let's try again."

    return reply

iface = gr.Interface(
    fn=CustomChatGPT, 
    inputs=[
        gr.inputs.Textbox(lines=2, label="Your Message"),
        gr.inputs.Dropdown(choices=list(personalities.keys()), label="Personality"),
        gr.inputs.Checkbox(label="Reset Conversation")
    ],
    outputs=gr.outputs.Textbox(label="Assistant's Reply"),
    title="AI Chat",
    description="Welcome to the AI Chat. Choose the personality you want the assistant to adopt.",
    theme="huggingface", # Use the 'huggingface' theme
    allow_flagging=False,
)

iface.launch(share=True)

