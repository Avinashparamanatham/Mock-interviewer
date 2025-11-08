# 🎯 AI Mock Interview System

An advanced AI-powered mock interview platform that provides real-time feedback on interview performance through video analysis, speech processing, and gesture detection. Perfect for job seekers to practice and improve their interview skills.

## ✨ Features

### Core Interview Capabilities
- **Video Interview Mode**: Real-time video streaming with WebRTC
- **Avatar Interview Mode**: 3D avatar-based interviews with pythreejs
- **Multi-Modal Analysis**: Comprehensive evaluation across content, speech, and body language
- **Real-Time Feedback**: Immediate scoring and suggestions after each response

### AI-Powered Analysis
- **Speech Processing**: Whisper AI transcription and speech quality analysis
- **Gesture Detection**: OpenCV and MediaPipe-powered body language analysis
- **Content Evaluation**: OpenAI GPT-powered response quality assessment
- **Personalized Feedback**: Tailored improvement suggestions based on performance

### Professional Reporting
- **PDF Report Generation**: Downloadable comprehensive performance reports
- **Detailed Analytics**: Scores across multiple categories with improvement tips
- **Progress Tracking**: Session-based performance monitoring
- **Grade Calculation**: Overall performance grading system

### Question Bank
- **Categorized Questions**: Behavioral, technical, project-based, and logical thinking questions
- **Dynamic Selection**: Personalized question selection based on candidate profile
- **Extensible Framework**: Easy to add new question categories and types

## 🚀 Installation

### Prerequisites
- Python 3.8+
- OpenAI API Key
- Webcam access (for video interviews)

### Step-by-Step Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd mock-interview-system
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Install fpdf2 for PDF generation**:
   ```bash
   pip install --upgrade fpdf2
   ```

6. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SECRET_KEY=your_secret_key_here
   SECRET_KEY_SOCKET=your_socket_secret_key_here
   ```

## 📋 Requirements

### Core Dependencies
- `streamlit==1.33.0` - Web application framework
- `streamlit-webrtc==0.47.6` - Real-time video streaming
- `openai==1.6.1` - AI-powered evaluation
- `opencv-python==4.8.1.78` - Computer vision for gesture detection
- `mediapipe==0.10.8` - Pose and gesture recognition
- `whisper` - Speech-to-text transcription
- `fpdf2` - PDF report generation

### Additional Libraries
- `numpy`, `scipy` - Numerical computing
- `Pillow` - Image processing
- `pydub` - Audio processing
- `gtts` - Text-to-speech for avatars
- `pythreejs` - 3D avatar rendering

## 🎮 Usage

### Starting the Application

1. **Navigate to the project directory**:
   ```bash
   cd mock-interview-system
   ```

2. **Activate virtual environment**:
   ```bash
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Run the Streamlit application**:
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open your browser** and navigate to the provided local URL (typically `http://localhost:8501`)

### Interview Process

1. **Setup Phase**:
   - Enter your name, target position, and experience level
   - Choose interview mode (Video or Avatar)
   - Click "Start Interview"

2. **Interview Phase**:
   - Answer questions presented by the AI interviewer
   - Receive real-time feedback after each response
   - Continue through all questions

3. **Results Phase**:
   - View comprehensive performance report
   - Download PDF report for future reference
   - Start new interview or exit

## 🏗️ Project Structure

```
mock-interview-system/
├── streamlit_app.py          # Main Streamlit application
├── config.py                 # Configuration and environment variables
├── requirements.txt          # Python dependencies
├── questions.json           # Interview question database
├── generate_questions.py    # Question generation utilities
├── pythreejs_component.py   # 3D avatar component
├── models/
│   ├── __init__.py
│   ├── interview_engine.py  # Core interview logic and AI evaluation
│   ├── speech_processor.py  # Speech analysis and transcription
│   └── gesture_detector.py  # Body language and gesture detection
├── utils/
│   ├── __init__.py
│   ├── helpers.py           # Utility functions for media processing
│   └── pdf_generator.py     # PDF report generation
├── static/
│   ├── assets/
│   │   └── avatar/
│   │       └── avatar.jpg   # Avatar image assets
│   └── temp_uploads/        # Temporary file storage
├── pose/                    # OpenPose model files
├── venv/                    # Virtual environment (created during setup)
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for AI evaluation
- `SECRET_KEY`: Flask application secret key
- `SECRET_KEY_SOCKET`: Socket.IO secret key

### Model Configurations
- **Whisper Model**: Uses "base.en" for efficient speech transcription
- **OpenPose**: MPI model for pose estimation
- **OpenCV**: Haar cascades for face detection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors with fpdf**:
   ```bash
   pip uninstall pypdf fpdf
   pip install --upgrade fpdf2
   ```

2. **WebRTC Camera Issues**:
   - Ensure camera permissions are granted
   - Try different browsers (Chrome recommended)
   - Check camera is not in use by other applications

3. **OpenAI API Errors**:
   - Verify your API key is correct and has sufficient credits
   - Check your internet connection
   - Ensure the API key is properly set in `.env`

4. **Model Loading Errors**:
   - Ensure sufficient disk space for AI models
   - Check internet connection for model downloads
   - Verify all dependencies are installed

### Performance Optimization

- Use GPU acceleration for better performance with MediaPipe
- Reduce video resolution for slower systems
- Close other applications to free up system resources

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section above
- Ensure all dependencies are correctly installed

## 🎯 Future Enhancements

- [ ] Mobile application support
- [ ] Additional interview question categories
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Integration with job platforms
- [ ] Voice cloning for more natural AI interviewer

---

**Happy Interviewing! 🚀**

Practice makes perfect. Use this AI Mock Interview System to build confidence and improve your interview performance.
