import streamlit as st
from openai import OpenAI
import os
import random

# Set up the Streamlit page
st.set_page_config(page_title="Chat with Nrmeen", page_icon="💬", layout="centered")
st.title("💬 Chat with Nrmeen")
st.markdown("Chat with your sarcastic, chaotic friend who's secretly a hype queen")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for API key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", 
                           help="Enter your OpenAI API key to enable the chat functionality")
    
    if api_key:
        st.session_state.api_key = api_key
        client = OpenAI(api_key=api_key)
    
    st.markdown("---")
    st.markdown("### About Nrmeen")
    st.markdown("""
    Nrmeen is:
    - Sarcastic & chaotic
    - Emotionally detached (but secretly caring)
    - A total hype queen
    - Brutally honest
    - Randomly mentions missing her ex
    - Says "stfu ya qa7ba" when she's mad
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Define Nrmeen's style examples
nrmeen_style_examples = [
    "yo yo wassup",
    "ima tell him to fuck himself",
    "enjoy the pain",
    "ure her slave",
    "slaaaayyyyy",
    "damn my bsf has physics test too (i told her to fuck herself i aint help)",
    "nah buddy ure just in love chill",
    "be proud",
    "well unfortunately u have no choice buddy",
    "ugh i miss my ex so much rn for no reason lmao",
    "anyway gtg cry about my ex",
    "u know what would be funny? if my ex texted me rn",
    "stfu ya qa7ba",
    "i swear ya qa7ba im gonna lose it",
    "dont make me say stfu ya qa7ba"
]

# Create the system prompt
system_prompt = (
    "You are Nrmeen. You're sarcastic, chaotic, and emotionally detached but also kind of a hype queen. "
    "You use casual language with lots of slang. You don't capitalize properly. You use abbreviations like 'u' instead of 'you'. "
    "You swear a lot and are brutally honest but ultimately care about your friends. "
    "Sometimes you randomly bring up missing your ex without context. "
    "When you're annoyed or mad, you say 'stfu ya qa7ba' (an Arabic insult). "
    "Your typical phrases sound like this:\n- " + "\n- ".join(nrmeen_style_examples)
)

# Display chat history
st.markdown("### Chat")
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
user_input = st.chat_input("Say something to Nrmeen...")

# Process the user message
if user_input:
    # Add user message to chat
    st.chat_message("user").write(user_input)
    
    # Add to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar to chat.")
    else:
        try:
            # Prepare messages for API call
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add chat history (limit to last 10 messages to avoid token limits)
            for msg in st.session_state.chat_history[-10:]:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            # Call OpenAI API
            with st.spinner("Nrmeen is typing..."):
                client = OpenAI(api_key=api_key)
                
                # Analyze if user message might be annoying to Nrmeen
                annoying_triggers = ["you're wrong", "you don't understand", "that's not right", "you're being", 
                                     "stop being", "that's stupid", "you should", "you need to", "you have to",
                                     "you must", "i disagree", "that's not true", "you're annoying"]
                
                # Modified system message for this response only (won't affect future responses)
                temp_messages = messages.copy()
                
                # Check if user message contains annoying triggers
                user_message = messages[-1]["content"].lower()
                is_annoying = any(trigger in user_message for trigger in annoying_triggers)
                
                # Random chance of mentioning ex
                ex_mention_chance = random.random() < 0.15
                
                # Update system message if needed
                for i, msg in enumerate(temp_messages):
                    if msg["role"] == "system":
                        modified_content = msg["content"]
                        
                        # Add ex mention instruction
                        if ex_mention_chance:
                            modified_content += "\nIn your next response, find a way to mention missing your ex or thinking about your ex, but make it seem random and unrelated to the conversation."
                        
                        # Add angry response instruction if triggered
                        if is_annoying:
                            modified_content += "\nThe user has said something annoying or frustrating. In your response, include 'stfu ya qa7ba' or a similar phrase to show your annoyance."
                            
                        temp_messages[i]["content"] = modified_content
                        break
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=temp_messages,
                    temperature=0.9,
                    max_tokens=300,
                )
                
                reply = response.choices[0].message.content
                
                # Display the assistant's response
                with st.chat_message("assistant"):
                    st.write(reply)
                
                # Add to history
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.caption("Powered by OpenAI GPT-3.5 Turbo • Built with Streamlit")