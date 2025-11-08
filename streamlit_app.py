import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
import os
import queue
import base64
import cv2
import numpy as np
from datetime import datetime
from config import Config
from models.interview_engine import InterviewEngine
from models.speech_processor import SpeechProcessor
from models.gesture_detector import GestureDetector
from utils.helpers import decode_base64_frame, save_audio_chunk
from utils.pdf_generator import generate_interview_report_pdf

# Initialize AI/Model Components
@st.cache_resource
def get_models():
    interview_engine = InterviewEngine(api_key=Config.OPENAI_API_KEY)
    speech_processor = SpeechProcessor()
    gesture_detector = GestureDetector()
    return interview_engine, speech_processor, gesture_detector

interview_engine, speech_processor, gesture_detector = get_models()

def setup_page():
    st.title("🎯 AI Mock Interview System")
    st.markdown("<p class='subtitle'>Practice with an AI-powered interviewer and get real-time feedback</p>", unsafe_allow_html=True)

    with st.form("start_form"):
        name = st.text_input("Your Name *", placeholder="Enter your full name")
        position = st.text_input("Position Applying For *", placeholder="e.g., Software Engineer")
        experience = st.selectbox("Experience Level *", ["", "Entry Level (0-2 years)", "Intermediate (2-5 years)", "Senior (5+ years)"])
        interview_mode = st.selectbox("Interview Mode *", ["Video Interview", "Avatar Interview"])

        submitted = st.form_submit_button("Start Interview")

        if submitted:
            if not name or not position or not experience or not interview_mode:
                st.error("Please fill in all required fields.")
            else:
                st.session_state.user_info = {
                    "name": name,
                    "position": position,
                    "experience_level": experience,
                    "interview_mode": interview_mode
                }
                st.session_state.page = "interview"
                st.rerun()

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

def start_interview(user_info):
    result = interview_engine.start_interview(user_info)
    if result.get("success"):
        st.session_state.questions = interview_engine.interview_data['questions']
        st.session_state.interview_started = True
    else:
        st.error("Failed to start interview.")
        return

def play_question_audio(current_question):
    audio_path = interview_engine.text_to_speech(current_question, f"question_{st.session_state.current_question_index}.mp3")
    if audio_path and os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3")
    else:
        st.error("Failed to generate audio.")

def interview_page():
    st.title("Live Interview Session")

    interview_mode = st.session_state.user_info.get("interview_mode", "Video Interview")

    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
        st.session_state.current_question_index = 0
        st.session_state.questions = []
        st.session_state.responses = []
        st.session_state.audio_buffer = queue.Queue()
        st.session_state.gesture_data = []

    if not st.session_state.interview_started:
        start_interview(st.session_state.user_info)

    if st.session_state.interview_started and st.session_state.questions:
        current_question = st.session_state.questions[st.session_state.current_question_index]

        if interview_mode == "Avatar Interview":
            # Display simple avatar (image-based)
            col1, col2 = st.columns([1, 2])
            with col1:
                avatar_path = "static/assets/avatar/avatar.jpg"
                if os.path.exists(avatar_path):
                    st.image(avatar_path, caption="AI Interviewer", width=200)
                else:
                    st.markdown("🤖 **AI Interviewer**")

            with col2:
                st.header("Question:")
                st.write(current_question)

                # Play TTS for the question
                if st.button("Play Question Audio"):
                    play_question_audio(current_question)

        elif interview_mode == "Video Interview":
            st.header("Question:")
            st.write(current_question)

        # WebRTC setup for both modes
        if interview_mode == "Video Interview":
            webrtc_ctx = webrtc_streamer(
                key="interview_video",
                mode=WebRtcMode.SENDRECV,
                rtc_configuration=RTC_CONFIGURATION,
                media_stream_constraints={"video": True, "audio": True},
                video_frame_callback=video_frame_callback,
                audio_frame_callback=audio_frame_callback,
                async_processing=True)
        elif interview_mode == "Avatar Interview":
            webrtc_ctx = webrtc_streamer(
                key="interview_audio",
                mode=WebRtcMode.SENDRECV,
                rtc_configuration=RTC_CONFIGURATION,
                media_stream_constraints={"video": False, "audio": True},
                audio_frame_callback=audio_frame_callback,
                async_processing=True)

        if st.session_state.responses:
            st.header("Feedback on Previous Answer")
            last_response = st.session_state.responses[-1]
            st.write(f"**Transcription:** {last_response['transcription']}")

            # Display individual question evaluation
            eval_data = last_response['evaluation']
            st.subheader("Question Evaluation")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Content", f"{eval_data.get('content_score', 0):.2f}")
            col2.metric("Speech", f"{eval_data.get('speech_score', 0):.2f}")
            col3.metric("Body Language", f"{eval_data.get('gesture_score', 0):.2f}")
            col4.metric("Overall", f"{eval_data.get('overall_score', 0):.2f}")

            # Show specific feedback for this question
            question_feedback = eval_data.get('feedback', {})
            if question_feedback.get('improvements'):
                st.subheader("Areas for Improvement (This Question)")
                for improvement in question_feedback['improvements']:
                    st.write(f"• {improvement}")

        if not webrtc_ctx.state.playing:
            if interview_mode == "Video Interview":
                st.warning("Please allow camera and microphone access and start the stream.")
            elif interview_mode == "Avatar Interview":
                st.warning("Please allow microphone access and start the audio stream.")

        if webrtc_ctx.state.playing:
            if st.button("Next Question"):
                handle_next_question()

        if st.button("Finish Interview"):
            st.session_state.page = "results"
            st.rerun()
    else:
        st.error("Failed to start interview or no questions available.")

def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    img = frame.to_ndarray(format="bgr24")

    processed_data = gesture_detector.process_frame(img)
    # processed_data["processed_frame"] is base64, but we need numpy array for av.VideoFrame
    # Decode base64 back to numpy array
    processed_image_b64 = processed_data["processed_frame"]
    header, encoded = processed_image_b64.split(',', 1)
    decoded_data = base64.b64decode(encoded)
    processed_image = cv2.imdecode(np.frombuffer(decoded_data, np.uint8), cv2.IMREAD_COLOR)

    st.session_state.gesture_data.append(processed_data['gesture_data'])

    return av.VideoFrame.from_ndarray(processed_image, format="bgr24")

def audio_frame_callback(frame: av.AudioFrame):
    st.session_state.audio_buffer.put(frame)

def handle_next_question():
    from pydub import AudioSegment
    import wave
    import os

    audio_frames = []
    while not st.session_state.audio_buffer.empty():
        audio_frames.append(st.session_state.audio_buffer.get())

    if audio_frames:
        # Save audio to a temporary WAV file
        temp_wav_path = f"temp_audio_{st.session_state.current_question_index}.wav"
        with wave.open(temp_wav_path, 'wb') as wf:
            wf.setnchannels(audio_frames[0].layout.nb_channels)
            wf.setsampwidth(audio_frames[0].format.bytes)
            wf.setframerate(audio_frames[0].sample_rate)
            for frame in audio_frames:
                wf.writeframes(frame.to_ndarray().tobytes())

        # Convert WAV to MP3 for processing
        sound = AudioSegment.from_wav(temp_wav_path)
        audio_path = f"temp_audio_{st.session_state.current_question_index}.mp3"
        sound.export(audio_path, format="mp3")

        transcription = speech_processor.transcribe_audio(audio_path)
        speech_analysis = speech_processor.analyze_speech(audio_path)

        # Clean up temporary files
        try:
            os.remove(temp_wav_path)
            os.remove(audio_path)
        except OSError:
            pass  # Ignore if files don't exist or can't be deleted
    else:
        transcription = ""
        speech_analysis = {}

    # Aggregate gesture data
    gesture_aggregate = gesture_detector.get_aggregate_data()
    gesture_detector.reset_buffer()

    response_data = {
        'question': st.session_state.questions[st.session_state.current_question_index],
        'transcription': transcription,
        'speech_analysis': speech_analysis,
        'gesture_data': gesture_aggregate
    }

    evaluation = interview_engine.evaluate_response(response_data)
    response_data['evaluation'] = evaluation

    st.session_state.responses.append(response_data)

    if st.session_state.current_question_index < len(st.session_state.questions) - 1:
        st.session_state.current_question_index += 1
    else:
        st.session_state.page = "results"

    st.rerun()


def results_page():
    st.title("Interview Performance Report")

    if hasattr(st.session_state, 'responses') and st.session_state.responses:
        try:
            final_report = interview_engine.generate_final_report()

            candidate_name = st.session_state.user_info["name"]
            position_applied = st.session_state.user_info["position"]
            st.header(f"Candidate: {candidate_name}")
            st.subheader(f"Position: {position_applied}")
            st.metric("Overall Grade", final_report.get("grade", "N/A"))

            overall_score = final_report.get("scores", {}).get("overall", 0)
            st.progress(overall_score)

            col1, col2, col3 = st.columns(3)
            col1.metric("Content Quality", f"{final_report.get('scores', {}).get('content', 0)*100:.0f}%")
            col2.metric("Speech Clarity & Pace", f"{final_report.get('scores', {}).get('speech', 0)*100:.0f}%")
            col3.metric("Body Language", f"{final_report.get('scores', {}).get('body_language', 0)*100:.0f}%")

            st.header("Detailed Feedback")
            st.subheader("👍 Strengths")
            strengths = final_report.get("feedback", {}).get("strengths", [])
            if strengths:
                for strength in strengths:
                    st.write(f"• {strength}")
            else:
                st.write("No specific strengths identified.")

            st.subheader("📝 Areas for Improvement")
            improvements = final_report.get("feedback", {}).get("improvements", [])
            if improvements:
                for improvement in improvements:
                    st.write(f"• {improvement}")
            else:
                st.write("No specific areas for improvement identified.")

            # Add specific improvement tips section
            st.header("💡 Interview Improvement Tips")
            st.markdown("""
            **General Tips:**
            • **Preparation:** Research the company and role thoroughly before the interview
            • **Practice:** Rehearse common interview questions with a friend or in front of a mirror
            • **Follow-up:** Send a thank-you email within 24 hours after the interview

            **Content Tips:**
            • Use the STAR method for behavioral questions (Situation, Task, Action, Result)
            • Prepare 2-3 specific examples from your experience for each major skill
            • Quantify your achievements with numbers when possible

            **Communication Tips:**
            • Speak slowly and clearly - it's better to be understood than to speak fast
            • Pause briefly after important points to let them sink in
            • Show enthusiasm and energy in your responses

            **Body Language Tips:**
            • Sit up straight with good posture
            • Maintain eye contact (look at the camera in video interviews)
            • Use natural hand gestures to emphasize points
            • Smile and show confidence through your expressions
            """)
        except Exception as e:
            st.error(f"Error generating final report: {str(e)}")
            st.write("Unable to generate detailed report. Please try again.")
    else:
        st.warning("No interview data found. Please complete an interview first.")

    # PDF Download Section
    if hasattr(st.session_state, 'responses') and st.session_state.responses:
        st.header("📄 Download Report")
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("Generate PDF Report", type="primary"):
                with st.spinner("Generating PDF report..."):
                    try:
                        final_report = interview_engine.generate_final_report()
                        pdf_path = generate_interview_report_pdf(final_report)

                        if pdf_path and os.path.exists(pdf_path):
                            with open(pdf_path, "rb") as pdf_file:
                                pdf_bytes = pdf_file.read()

                            st.success("PDF report generated successfully!")

                            # Download button
                            st.download_button(
                                label="📥 Download Interview Report PDF",
                                data=pdf_bytes,
                                file_name=f"interview_report_{st.session_state.user_info['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf",
                                key="download_pdf"
                            )
                        else:
                            st.error("Failed to generate PDF report. Please try again.")
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")

        with col2:
            st.markdown("""
            **Report Includes:**
            • Candidate information
            • Performance scores and grade
            • Detailed feedback analysis
            • Personalized improvement tips
            • Professional formatting
            """)

    if st.button("Start New Interview"):
        st.session_state.page = "setup"
        st.rerun()

def main():
    if "page" not in st.session_state:
        st.session_state.page = "setup"

    if st.session_state.page == "setup":
        setup_page()
    elif st.session_state.page == "interview":
        interview_page()
    elif st.session_state.page == "results":
        results_page()

if __name__ == "__main__":
    main()
