# 🌾 SevaSetu - Multilingual Government Schemes Assistant

> **AI for Bharat Initiative** | Empowering Rural Communities through AI

SevaSetu is a multilingual, voice-enabled AI assistant designed to help rural citizens, especially farmers (kisans), discover and apply for government schemes in their native language. Built with AWS Bedrock and Polly, SevaSetu breaks down language and digital literacy barriers to ensure equitable access to government benefits.

---

## 🎯 Problem Statement

Rural citizens often struggle to:
- Navigate complex government scheme information
- Understand eligibility criteria across multiple schemes
- Access information in their native language
- Complete application processes without assistance

**SevaSetu bridges this gap** by providing an intelligent, conversational assistant that speaks the user's language and guides them through the entire process.

---

## ✨ Key Features

### 🗣️ Multilingual Voice Interface
- **Supported Languages**: Hindi (हिंदी), Tamil (தமிழ்), Telugu (తెలుగు), Bengali (বাংলা), English
- Voice output using AWS Polly
- Browser-based voice input (Chrome/Edge)
- Floating Voice Hub with pulse animations

### 🤖 AI-Powered Scheme Discovery
- Powered by AWS Bedrock Knowledge Base
- Context-aware responses using RAG (Retrieval Augmented Generation)
- Real-time query processing from comprehensive knowledge base
- Answers in user's selected language

### 📋 Application Guidance
- Detailed scheme information
- Eligibility criteria
- Benefits and coverage
- Source attribution with document references

### 🌐 Accessible Design
- Beautiful earthy UI with warm, handmade aesthetic
- Large buttons and high-contrast colors for elderly users
- Visual status indicators (Listening, Processing, Speaking)
- Mobile responsive design
- Works on any modern browser

---

## 🏗️ Architecture

### AWS Services Used

| Service | Purpose | Status |
|---------|---------|--------|
| **AWS Bedrock Knowledge Base** | Vector database for semantic search | ✅ Implemented |
| **AWS Bedrock (Amazon Nova)** | RAG-based response generation | ✅ Implemented |
| **Amazon Polly** | Text-to-speech synthesis | ✅ Implemented |
| **Amazon S3** | Storage for government schemes data | ✅ Implemented |

### System Flow

```
User Input (Text/Voice in any language)
          ↓
    Streamlit Frontend
          ↓
    Language Instruction Added
          ↓
    AWS Bedrock Knowledge Base
          ↓
    Amazon Nova Model (RAG)
          ↓
    Response in Selected Language
          ↓
    AWS Polly (Voice Synthesis)
          ↓
    Audio + Text Output to User
```

---

## 📊 Implementation Status

### ✅ Completed Features
- [x] Beautiful earthy UI with rural India theme
- [x] AWS Bedrock Knowledge Base integration
- [x] Multilingual text input (5 languages)
- [x] Multilingual text output (5 languages)
- [x] AWS Polly voice output
- [x] Floating Voice Hub with animations
- [x] Source attribution with citations
- [x] Language selection dropdown
- [x] Auto-play audio responses
- [x] Mobile responsive design
- [x] High-contrast accessibility features
- [x] Government schemes data (4 major schemes)

### 🎯 Working Features
- ✅ Type questions in any language
- ✅ Get answers in selected language
- ✅ Hear answers with voice output
- ✅ View source documents
- ✅ Clear chat history
- ✅ Visual status indicators

---

## 📁 Project Structure

```
Sevasetu-final/
├── app.py                         # Main Streamlit application ✅
├── bedrock_kb.py                  # AWS Bedrock integration ✅
├── load_config.py                 # Configuration management ✅
├── diagnose.py                    # Diagnostic tool ✅
├── requirements.txt               # Python dependencies ✅
├── .env.template                  # Environment template ✅
├── .env                          # Your AWS credentials (not in git)
├── .gitignore                    # Git ignore rules ✅
├── README.md                     # This file ✅
└── data/                         # Government schemes data ✅
    ├── ayushman_bharat.md        # Ayushman Bharat health scheme
    ├── mgnrega.md                # MGNREGA employment scheme
    ├── mp_kisan.md               # PM-Kisan farmer support
    └── pmay_g.md                 # Pradhan Mantri Awas Yojana
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- AWS Account with:
  - Bedrock access (Knowledge Base enabled)
  - Polly access
  - IAM user with appropriate permissions
- Modern web browser (Chrome/Edge recommended for voice)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Sevasetu-final
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials**
   
   Copy `.env.template` to `.env` and fill in your AWS credentials:
   ```bash
   cp .env.template .env
   ```
   
   Edit `.env`:
   ```
   AWS_REGION=us-east-1
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   KNOWLEDGE_BASE_ID=your_kb_id
   MODEL_ARN=us.amazon.nova-2-lite-v1:0
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```
   
   Or:
   ```bash
   python3 -m streamlit run app.py
   ```

5. **Access the app**
   
   Open your browser to `http://localhost:8501`

---

## 🎮 How to Use

### For Users

1. **Select Language**: Choose your preferred voice output language from the sidebar
2. **Ask Question**: Type your question in ANY language (Hindi, Tamil, Telugu, Bengali, English)
3. **Get Answer**: Receive answer in your selected language
4. **Hear Response**: Audio automatically plays with voice output
5. **View Sources**: Expand "Source Attribution" to see document references

### Voice Input (Optional)

1. Click the floating 🎤 button at the bottom
2. Allow microphone access when prompted
3. Speak your question clearly
4. Watch the pulse animation (red = listening, yellow = processing, green = speaking)

### Example Questions

**English**: "What is PM-Kisan scheme?"

**Hindi**: "पीएम किसान योजना क्या है?"

**Tamil**: "பிரதமர் கிசான் திட்டம் என்றால் என்ன?"

**Telugu**: "పిఎం కిసాన్ పథకం ఏమిటి?"

**Bengali**: "পিএম কিষাণ প্রকল্প কী?"

---

## 📚 Government Schemes Included

| Scheme | Target Beneficiaries | Key Benefits |
|--------|---------------------|--------------|
| **Ayushman Bharat** | Low-income families | Health insurance up to ₹5 lakhs |
| **MGNREGA** | Rural households | 100 days guaranteed employment |
| **PM-Kisan** | Small & marginal farmers | ₹6,000 annual income support |
| **PMAY-G** | Rural homeless | Housing assistance |

---

## 🎨 UI Features

### Beautiful Earthy Design
- Warm terracotta and clay color palette
- Rural India background imagery
- Handcrafted paper texture on messages
- Smooth animations and transitions

### Accessibility
- Large 80px voice button for elderly users
- High-contrast text (black on light backgrounds)
- Clear visual status indicators
- Mobile responsive layout
- Supports high-contrast mode

### Voice Hub
- Floating at bottom center
- Pulse animations:
  - 🔴 Red: Listening
  - 🟡 Yellow: Processing
  - 🟢 Green: Speaking
  - ⚪ White: Ready
- Language badge showing selected language

---

## 🔧 Technical Details

### Technologies Used
- **Frontend**: Streamlit
- **Backend**: Python 3.9+
- **AI/ML**: AWS Bedrock (Amazon Nova model)
- **Voice**: AWS Polly (Aditi voice)
- **Database**: AWS Bedrock Knowledge Base (vector search)
- **Storage**: Amazon S3

### AWS Configuration
- **Region**: us-east-1
- **Model**: Amazon Nova 2 Lite
- **Voice**: Aditi (Indian English)
- **Knowledge Base**: Vector embeddings with S3 data source

---

## 🎯 Future Enhancements

- [ ] Native Hindi/Tamil/Telugu voices (when available in AWS)
- [ ] AWS Transcribe integration for better voice input
- [ ] More government schemes (50+ schemes)
- [ ] User authentication and profiles
- [ ] Application tracking
- [ ] SMS/WhatsApp integration
- [ ] Mobile app (Android/iOS)
- [ ] Offline mode
- [ ] Regional language expansion (Marathi, Gujarati, Punjabi)
- [ ] Integration with government portals

---

## 🐛 Troubleshooting

### Voice not working?
- Use Chrome or Edge browser
- Check microphone permissions
- Ensure volume is up
- Try clicking play button manually on audio player

### AWS errors?
- Run `python3 diagnose.py` to check configuration
- Verify AWS credentials in `.env`
- Check Knowledge Base ID is correct
- Ensure IAM user has Bedrock and Polly permissions

### Text not visible?
- Text is now black for maximum readability
- Check browser zoom level
- Try refreshing the page

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Team

**AI for Bharat - AI for Communities, Access & Public Impact**

Developed for rural communities in India to access government schemes easily.

---

## 🙏 Acknowledgments

- Government of India for open data on schemes
- AWS for Bedrock and Polly services
- AI for Bharat community for guidance
- Rural communities for inspiration

---

## 📞 Contact

For questions, suggestions, or collaboration:
- GitHub Issues
- Project Discussions

---

**Made with ❤️ for Rural India** 🌾

