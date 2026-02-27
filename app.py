"""
SevaSetu - Government Schemes Assistant
Beautiful Earthy UI + Multilingual Voice Output
"""

import os
from dotenv import load_dotenv
import streamlit as st
from bedrock_kb import query_knowledge_base
import boto3
import time

load_dotenv()

# AWS Polly client
polly_client = boto3.client('polly', region_name=os.getenv('AWS_REGION', 'us-east-1'))

# Page configuration
st.set_page_config(
    page_title="SevaSetu - Government Schemes Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language configuration for voice output
# Note: AWS Polly has limited Indian language support in us-east-1
# Using Aditi (Indian English) which can pronounce Hindi/Tamil text reasonably well
LANGUAGES = {
    "English": {"code": "en-IN", "voice": "Aditi", "display": "English"},
    "Hindi (हिंदी)": {"code": "hi-IN", "voice": "Aditi", "display": "हिंदी"},
    "Tamil (தமிழ்)": {"code": "ta-IN", "voice": "Aditi", "display": "தமிழ்"},
    "Telugu (తెలుగు)": {"code": "te-IN", "voice": "Aditi", "display": "తెలుగు"},
    "Bengali (বাংলা)": {"code": "bn-IN", "voice": "Aditi", "display": "বাংলা"}
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "sources" not in st.session_state:
    st.session_state.sources = []
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"
if "voice_status" not in st.session_state:
    st.session_state.voice_status = "idle"  # idle, listening, processing, speaking

def generate_speech(text, language="English"):
    """Generate speech using AWS Polly"""
    try:
        lang_config = LANGUAGES.get(language, LANGUAGES["English"])
        
        # Log for debugging
        print(f"Generating speech for language: {language}")
        print(f"Using voice: {lang_config['voice']}, code: {lang_config['code']}")
        print(f"Text length: {len(text)} characters")
        
        response = polly_client.synthesize_speech(
            Text=text[:3000],
            OutputFormat='mp3',
            VoiceId=lang_config['voice'],
            LanguageCode=lang_config['code'],
            Engine='standard'
        )
        
        if 'AudioStream' in response:
            audio_data = response['AudioStream'].read()
            print(f"✅ Audio generated successfully: {len(audio_data)} bytes")
            return audio_data
        else:
            print("❌ No AudioStream in response")
            return None
    except Exception as e:
        print(f"❌ Voice generation error: {e}")
        import traceback
        traceback.print_exc()
        return None

# Beautiful Earthy CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Nunito', sans-serif;
    }
    
    /* Main background with warm earthy tones and image */
    .stApp {
        background-image: 
            linear-gradient(135deg, 
                rgba(245, 230, 211, 0.85) 0%,
                rgba(232, 213, 196, 0.85) 25%,
                rgba(212, 181, 160, 0.88) 50%,
                rgba(201, 168, 138, 0.90) 75%,
                rgba(184, 153, 104, 0.92) 100%),
            url('https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-blend-mode: overlay;
    }
    
    /* Sidebar with terracotta and clay tones */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            rgba(139, 90, 60, 0.95) 0%,
            rgba(160, 102, 68, 0.95) 50%,
            rgba(139, 90, 60, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-right: 3px solid rgba(210, 180, 140, 0.3);
    }
    
    /* Chat messages with handcrafted paper texture */
    .stChatMessage {
        background: linear-gradient(145deg, #faf8f3, #f5f1e8);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 
            5px 5px 15px rgba(139, 90, 60, 0.2),
            -2px -2px 10px rgba(255, 255, 255, 0.7);
        border: 2px solid rgba(210, 180, 140, 0.3);
        transition: transform 0.2s ease;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 
            7px 7px 20px rgba(139, 90, 60, 0.25),
            -3px -3px 12px rgba(255, 255, 255, 0.8);
    }
    
    /* Chat message text - make it black and readable */
    .stChatMessage p,
    .stChatMessage div,
    .stChatMessage span,
    [data-testid="stChatMessageContent"] {
        color: #000000 !important;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* User message styling */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(145deg, #e8f5e9, #c8e6c9);
    }
    
    /* Assistant message styling */
    [data-testid="stChatMessage"]:not([data-testid*="user"]) {
        background: linear-gradient(145deg, #fff9f0, #f5e6d3);
    }
    
    /* Input box with clay pot inspiration */
    .stChatInputContainer {
        background: linear-gradient(145deg, #fff9f0, #f5e6d3);
        border-radius: 30px;
        padding: 12px;
        box-shadow: 
            inset 3px 3px 8px rgba(139, 90, 60, 0.2),
            inset -2px -2px 8px rgba(255, 255, 255, 0.8),
            0 4px 12px rgba(139, 90, 60, 0.15);
        border: 2px solid rgba(160, 102, 68, 0.3);
    }
    
    /* Buttons with handmade pottery feel */
    .stButton button {
        background: linear-gradient(135deg, #c17854 0%, #a0664a 100%);
        color: #fff9f0;
        border: none;
        border-radius: 30px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 
            4px 4px 12px rgba(139, 90, 60, 0.4),
            -2px -2px 8px rgba(255, 255, 255, 0.2);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 
            6px 6px 16px rgba(139, 90, 60, 0.5),
            -2px -2px 10px rgba(255, 255, 255, 0.3);
        background: linear-gradient(135deg, #d4845f 0%, #b87555 100%);
    }
    
    /* Expander with natural paper feel */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f4e4c1 0%, #e8d5b7 100%);
        border-radius: 12px;
        font-weight: 600;
        color: #000000 !important;
        border: 2px solid rgba(160, 102, 68, 0.2);
        box-shadow: 2px 2px 8px rgba(139, 90, 60, 0.15);
    }
    
    /* Expander content text */
    .streamlit-expanderContent {
        color: #000000 !important;
    }
    
    .streamlit-expanderContent p,
    .streamlit-expanderContent div {
        color: #000000 !important;
    }
    
    /* Title styling */
    h1 {
        color: #5d4037;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.5);
        font-weight: 700;
    }
    
    /* Sidebar text with cream color */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] label {
        color: #fff9f0 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    /* Main content area */
    .block-container {
        background-color: rgba(255, 249, 240, 0.4);
        border-radius: 25px;
        padding: 2rem;
        backdrop-filter: blur(15px);
        box-shadow: 
            0 8px 32px rgba(139, 90, 60, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(245, 230, 211, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #c17854, #a0664a);
        border-radius: 10px;
        border: 2px solid rgba(245, 230, 211, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #d4845f, #b87555);
    }
    
    /* Voice Hub - Floating Bottom Section */
    .voice-hub {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, rgba(193, 120, 84, 0.95), rgba(160, 102, 74, 0.95));
        padding: 25px 40px;
        border-radius: 50px;
        box-shadow: 0 10px 40px rgba(139, 90, 60, 0.5),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border: 3px solid rgba(210, 180, 140, 0.5);
        z-index: 9999;
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    /* Voice Button with Pulse Animation */
    .voice-button {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #fff9f0, #f5e6d3);
        border: 4px solid #c17854;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .voice-button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Pulse Animation for Active State */
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(193, 120, 84, 0.7);
        }
        50% {
            box-shadow: 0 0 0 20px rgba(193, 120, 84, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(193, 120, 84, 0);
        }
    }
    
    .voice-button.listening {
        animation: pulse 1.5s infinite;
        background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
        border-color: #ff6b6b;
    }
    
    .voice-button.processing {
        animation: pulse 1s infinite;
        background: linear-gradient(135deg, #ffd93d, #ffb700);
        border-color: #ffd93d;
    }
    
    .voice-button.speaking {
        animation: pulse 2s infinite;
        background: linear-gradient(135deg, #6bcf7f, #4caf50);
        border-color: #6bcf7f;
    }
    
    /* Status Text */
    .voice-status {
        color: #fff9f0;
        font-size: 1.3rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        min-width: 150px;
        text-align: center;
    }
    
    /* Language Badge */
    .language-badge {
        background: rgba(255, 249, 240, 0.2);
        padding: 10px 20px;
        border-radius: 25px;
        color: #fff9f0;
        font-size: 1rem;
        font-weight: 600;
        border: 2px solid rgba(255, 249, 240, 0.3);
    }
    
    /* Accessibility - High Contrast Mode */
    @media (prefers-contrast: high) {
        .voice-hub {
            border: 4px solid #000;
            background: rgba(193, 120, 84, 1);
        }
        .voice-button {
            border: 5px solid #000;
        }
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .voice-hub {
            bottom: 10px;
            padding: 20px 25px;
            flex-direction: column;
            gap: 15px;
        }
        .voice-button {
            width: 70px;
            height: 70px;
            font-size: 2rem;
        }
        .voice-status {
            font-size: 1.1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("# 🌾 SevaSetu")
    st.markdown("### Multilingual Voice Assistant")
    st.markdown("---")
    
    st.markdown("### 🗣️ Select Voice Output Language")
    st.markdown("*Choose which language you want to hear the response in*")
    selected_lang = st.selectbox(
        "Voice Language",
        options=list(LANGUAGES.keys()),
        index=0,
        label_visibility="collapsed"
    )
    st.session_state.selected_language = selected_lang
    
    st.markdown("---")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #d4a574 0%, #b8936d 100%); 
                padding: 20px; border-radius: 18px; margin: 10px 0;
                box-shadow: 4px 4px 12px rgba(139, 90, 60, 0.3),
                            -2px -2px 8px rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(210, 180, 140, 0.3);'>
        <h3 style='color: #fff9f0; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>💬 How to Use</h3>
        <ol style='color: #fff9f0; margin-top: 10px; line-height: 1.8;'>
            <li><strong>Select</strong> your preferred voice language above</li>
            <li><strong>Type or speak</strong> in ANY language (Hindi, Tamil, etc.)</li>
            <li><strong>Get answer</strong> in the same language you asked</li>
            <li><strong>Hear voice</strong> in your selected language</li>
        </ol>
        <p style='color: #fff9f0; margin-top: 10px; font-size: 0.9rem;'>
            💡 AWS Bedrock understands multiple languages!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #c9a88a 0%, #a68968 100%); 
                padding: 18px; border-radius: 18px; margin: 10px 0;
                box-shadow: 4px 4px 12px rgba(139, 90, 60, 0.3),
                            -2px -2px 8px rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(210, 180, 140, 0.3);'>
        <h4 style='color: #fff9f0; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>🌐 Language Support</h4>
        <ul style='color: #fff9f0; margin-top: 10px; line-height: 1.8;'>
            <li><strong>Text:</strong> Ask in Hindi, Tamil, Telugu, Bengali, English</li>
            <li><strong>Voice:</strong> Hear answers in selected language</li>
            <li><strong>Note:</strong> Voice uses Indian English accent (Aditi)</li>
            <li><strong>Quality:</strong> Can pronounce Indian language text</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.sources = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; padding: 15px;'>
        <p style='color: #fff9f0; font-size: 0.9rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>
            <strong>AI for Bharat Initiative</strong><br>
            <em>Empowering Rural Communities</em>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main Header
st.markdown("""
<div style='text-align: center; background: linear-gradient(135deg, rgba(193, 120, 84, 0.9) 0%, rgba(160, 102, 74, 0.9) 100%);
            padding: 40px 30px;
            border-radius: 25px;
            box-shadow: 0 10px 40px rgba(139, 90, 60, 0.3),
                        inset 0 1px 0 rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(210, 180, 140, 0.4);
            margin-bottom: 30px;'>
    <h1 style='color: #fff9f0; 
               margin: 0 0 15px 0; 
               font-size: 3rem;
               text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
               letter-spacing: 2px;'>
        🌾 SevaSetu 🌾
    </h1>
    <p style='color: #fff9f0; 
              font-size: 1.3rem; 
              margin: 0;
              text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
              line-height: 1.6;'>
        Your AI Companion for Government Schemes
    </p>
    <div style='margin-top: 25px; display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;'>
        <div style='background: rgba(255, 249, 240, 0.2); 
                    padding: 15px 25px; 
                    border-radius: 15px;
                    backdrop-filter: blur(10px);'>
            <span style='font-size: 2rem;'>💬</span>
            <p style='color: #fff9f0; margin: 5px 0 0 0; font-size: 0.9rem;'>Type in English</p>
        </div>
        <div style='background: rgba(255, 249, 240, 0.2); 
                    padding: 15px 25px; 
                    border-radius: 15px;
                    backdrop-filter: blur(10px);'>
            <span style='font-size: 2rem;'>🗣️</span>
            <p style='color: #fff9f0; margin: 5px 0 0 0; font-size: 0.9rem;'>Hear in 5 Languages</p>
        </div>
        <div style='background: rgba(255, 249, 240, 0.2); 
                    padding: 15px 25px; 
                    border-radius: 15px;
                    backdrop-filter: blur(10px);'>
            <span style='font-size: 2rem;'>🤖</span>
            <p style='color: #fff9f0; margin: 5px 0 0 0; font-size: 0.9rem;'>AI Powered</p>
        </div>
        <div style='background: rgba(255, 249, 240, 0.2); 
                    padding: 15px 25px; 
                    border-radius: 15px;
                    backdrop-filter: blur(10px);'>
            <span style='font-size: 2rem;'>☁️</span>
            <p style='color: #fff9f0; margin: 5px 0 0 0; font-size: 0.9rem;'>AWS Bedrock</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"<h2 style='text-align: center; color: #5d4037; text-shadow: 1px 1px 2px rgba(255,255,255,0.5); margin-bottom: 10px;'>Voice Output Language: {selected_lang}</h2>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align: center; color: #8b5a3c; font-size: 1.1rem; text-shadow: 1px 1px 2px rgba(255,255,255,0.5); margin-bottom: 30px;'>
    💬 Type or speak your question in ANY language<br>
    🗣️ Voice output will be in your selected language above
</p>
""", unsafe_allow_html=True)

# Voice Hub - Floating Voice Assistant UI
voice_status_text = {
    "idle": "🎤 Ready to Listen",
    "listening": "🎤 Listening...",
    "processing": "⚙️ Processing...",
    "speaking": "🔊 Speaking..."
}

voice_button_class = {
    "idle": "",
    "listening": "listening",
    "processing": "processing",
    "speaking": "speaking"
}

current_status = st.session_state.voice_status
status_text = voice_status_text.get(current_status, "🎤 Ready")
button_class = voice_button_class.get(current_status, "")

st.markdown(f"""
<div class='voice-hub'>
    <div class='voice-button {button_class}' id='voiceButton' onclick='toggleVoice()'>
        🎤
    </div>
    <div class='voice-status' id='voiceStatus'>
        {status_text}
    </div>
    <div class='language-badge'>
        🌐 {selected_lang}
    </div>
</div>

<script>
let isListening = false;
let recognition = null;

if ('webkitSpeechRecognition' in window) {{
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-IN';
}}

function toggleVoice() {{
    if (!recognition) {{
        alert('Voice recognition not supported. Please use Chrome or Edge browser.');
        return;
    }}
    
    if (isListening) {{
        recognition.stop();
        isListening = false;
        return;
    }}
    
    isListening = true;
    const button = document.getElementById('voiceButton');
    const status = document.getElementById('voiceStatus');
    
    // Update UI to listening state
    button.classList.add('listening');
    status.innerHTML = '🎤 Listening...';
    
    recognition.onresult = function(event) {{
        const transcript = event.results[0][0].transcript;
        
        // Update UI to processing state
        button.classList.remove('listening');
        button.classList.add('processing');
        status.innerHTML = '⚙️ Processing...';
        
        // Insert into chat input
        const chatInput = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
        if (chatInput) {{
            chatInput.value = transcript;
            chatInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            
            // Auto-submit
            setTimeout(() => {{
                const submitBtn = window.parent.document.querySelector('button[data-testid="stChatInputSubmitButton"]');
                if (submitBtn) {{
                    submitBtn.click();
                }}
                
                // Reset to idle after submission
                setTimeout(() => {{
                    button.classList.remove('processing');
                    status.innerHTML = '🎤 Ready to Listen';
                    isListening = false;
                }}, 1000);
            }}, 500);
        }}
    }};
    
    recognition.onerror = function(event) {{
        button.classList.remove('listening', 'processing');
        status.innerHTML = '❌ Error: ' + event.error;
        isListening = false;
        
        setTimeout(() => {{
            status.innerHTML = '🎤 Ready to Listen';
        }}, 3000);
    }};
    
    recognition.onend = function() {{
        if (isListening) {{
            button.classList.remove('listening');
            status.innerHTML = '🎤 Ready to Listen';
            isListening = false;
        }}
    }};
    
    recognition.start();
}}

// Update speaking status when audio plays
window.addEventListener('message', function(event) {{
    if (event.data.type === 'audio-playing') {{
        const button = document.getElementById('voiceButton');
        const status = document.getElementById('voiceStatus');
        button.classList.add('speaking');
        status.innerHTML = '🔊 Speaking...';
        
        setTimeout(() => {{
            button.classList.remove('speaking');
            status.innerHTML = '🎤 Ready to Listen';
        }}, event.data.duration || 5000);
    }}
}});
</script>
""", unsafe_allow_html=True)

# Display chat messages
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Audio player for assistant messages
        if message["role"] == "assistant" and "audio" in message:
            st.audio(message["audio"], format='audio/mp3')
        
        # Show sources
        if message["role"] == "assistant" and i < len(st.session_state.sources):
            sources = st.session_state.sources[i]
            if sources:
                with st.expander("📚 Source Attribution"):
                    for idx, source in enumerate(sources, 1):
                        st.markdown(f"**Source {idx}:**")
                        st.markdown(f"- **Document:** `{source['document']}`")
                        if source.get('excerpt'):
                            st.markdown(f"- **Excerpt:** {source['excerpt']}")
                        st.markdown("---")

# Chat input
if prompt := st.chat_input("Type in ANY language... (हिंदी, தமிழ், తెలుగు, বাংলা, English)"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Query knowledge base with language instruction
            with st.spinner("🔍 Searching AWS Bedrock Knowledge Base..."):
                # Add language instruction to the prompt
                lang_instruction = {
                    "English": "",
                    "Hindi (हिंदी)": "Please respond in Hindi language (हिंदी में जवाब दें). ",
                    "Tamil (தமிழ்)": "Please respond in Tamil language (தமிழில் பதிலளிக்கவும்). ",
                    "Telugu (తెలుగు)": "Please respond in Telugu language (తెలుగులో సమాధానం ఇవ్వండి). ",
                    "Bengali (বাংলা)": "Please respond in Bengali language (বাংলায় উত্তর দিন). "
                }
                
                instruction = lang_instruction.get(selected_lang, "")
                modified_prompt = instruction + prompt
                
                response = query_knowledge_base(modified_prompt)
                full_response = response.get('text', 'Sorry, I could not find an answer.')
                citations = response.get('citations', [])
            
            # Display response with typing effect
            displayed_text = ""
            for char in full_response:
                displayed_text += char
                message_placeholder.markdown(displayed_text + "▌")
                time.sleep(0.01)
            
            message_placeholder.markdown(full_response)
            
            # Generate voice in selected language
            st.info(f"🗣️ Generating voice in {selected_lang}...")
            audio_data = generate_speech(full_response, selected_lang)
            
            if audio_data:
                st.success(f"✅ Voice ready! Playing in {selected_lang}...")
                st.audio(audio_data, format='audio/mp3', autoplay=True)
            else:
                st.warning("⚠️ Voice generation failed. Text answer is available above.")
            
            # Process sources
            sources = []
            if citations:
                for citation in citations:
                    for ref in citation.get('retrievedReferences', []):
                        location = ref.get('location', {})
                        s3_location = location.get('s3Location', {})
                        uri = s3_location.get('uri', 'Unknown')
                        doc_name = uri.split('/')[-1] if '/' in uri else uri
                        content = ref.get('content', {})
                        excerpt = content.get('text', '')[:300]
                        if len(content.get('text', '')) > 300:
                            excerpt += "..."
                        sources.append({
                            'document': doc_name,
                            'uri': uri,
                            'excerpt': excerpt
                        })
            
            # Show sources
            if sources:
                with st.expander("📚 Source Attribution"):
                    for idx, source in enumerate(sources, 1):
                        st.markdown(f"**Source {idx}:**")
                        st.markdown(f"- **Document:** `{source['document']}`")
                        if source.get('excerpt'):
                            st.markdown(f"- **Excerpt:** {source['excerpt']}")
                        st.markdown("---")
            
            # Save to session state
            message_data = {
                "role": "assistant",
                "content": full_response
            }
            if audio_data:
                message_data["audio"] = audio_data
            
            st.session_state.messages.append(message_data)
            st.session_state.sources.append(sources)
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}\n\nPlease check your AWS credentials and ensure the Bedrock Knowledge Base is accessible."
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.session_state.sources.append([])

# Footer with examples
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 25px; background: rgba(255,255,255,0.7); border-radius: 20px;
            box-shadow: 0 4px 12px rgba(139, 90, 60, 0.2);'>
    <h3 style='color: #5d4037; margin-bottom: 15px;'>💡 Try asking in any language:</h3>
    <p style='color: #5d4037; line-height: 2; font-size: 1.05rem;'>
        <strong>English:</strong> "What is PM-Kisan scheme?" <br>
        <strong>Hindi:</strong> "पीएम किसान योजना क्या है?" <br>
        <strong>Tamil:</strong> "பிரதமர் கிசான் திட்டம் என்றால் என்ன?" <br>
        <strong>Telugu:</strong> "పిఎం కిసాన్ పథకం ఏమిటి?" <br>
        <strong>Bengali:</strong> "পিএম কিষাণ প্রকল্প কী?"
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #8b5a3c; margin-top: 20px; text-shadow: 1px 1px 2px rgba(255,255,255,0.5);'>🌾 SevaSetu - AI for Bharat Initiative | Made with ❤️ for Rural India</p>", unsafe_allow_html=True)
