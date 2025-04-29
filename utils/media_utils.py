import cv2
from PIL import Image
import speech_recognition as sr
from pydub import AudioSegment
from config import OUTPUT_DIR
from reportlab.pdfgen import canvas
import os

def handle_video(file):
    try:
        # Open video file
        cap = cv2.VideoCapture(str(file))
        
        # Extract frames
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()
        
        if not frames:
            raise ValueError("No frames could be extracted from the video")
            
        # Save first frame as PDF
        first_frame = cv2.cvtColor(frames[0], cv2.COLOR_BGR2RGB)
        img = Image.fromarray(first_frame)
        pdf_path = OUTPUT_DIR / file.with_suffix(".pdf").name
        img.save(str(pdf_path), "PDF")
        
        # Create simple text description
        text = f"Video File: {file.name}\nTotal Frames: {len(frames)}"
        
        return pdf_path, text
        
    except Exception as e:
        print(f"Error processing video file {file}: {str(e)}")
        return None, f"Error: {str(e)}"

def handle_audio(file):
    try:
        # Convert audio to wav format if needed
        if file.suffix.lower() in ['.mp3', '.m4a']:
            audio = AudioSegment.from_file(str(file))
            temp_wav = str(OUTPUT_DIR / "temp_audio.wav")
            audio.export(temp_wav, format="wav")
            audio_path = temp_wav
        else:
            audio_path = str(file)
        
        # Extract text using speech recognition
        text = transcribe_audio(audio_path)
        
        # Create PDF with audio info and transcription
        pdf_path = OUTPUT_DIR / file.with_suffix(".pdf").name
        create_media_pdf(pdf_path, file.name, text, media_type="Audio")
        
        # Cleanup
        if audio_path != str(file) and os.path.exists(audio_path):
            os.remove(audio_path)
            
        return pdf_path, text
        
    except Exception as e:
        print(f"Error processing audio file {file}: {str(e)}")
        return None, f"Error: {str(e)}"

def handle_gif(file):
    try:
        # Open GIF
        gif = Image.open(file)
        
        # Create PDF
        pdf_path = OUTPUT_DIR / file.with_suffix(".pdf").name
        
        # Save first frame as PDF
        if gif.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', gif.size, (255, 255, 255))
            background.paste(gif, mask=gif.split()[-1])
            background.save(pdf_path, 'PDF', resolution=100.0)
        else:
            gif.convert('RGB').save(pdf_path, 'PDF', resolution=100.0)
        
        # Create simple text description
        text = f"GIF Image: {file.name}\nFrames: {getattr(gif, 'n_frames', 1)}\nSize: {gif.size}"
        
        return pdf_path, text
        
    except Exception as e:
        print(f"Error processing GIF file {file}: {str(e)}")
        return None, f"Error: {str(e)}"

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            return f"Could not request results from Speech Recognition service; {str(e)}"

def create_media_pdf(pdf_path, filename, text, duration=None, media_type="Media"):
    c = canvas.Canvas(str(pdf_path))
    y = 800
    
    # Write header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"{media_type} Transcription: {filename}")
    y -= 30
    
    # Write duration if available
    if duration:
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Duration: {int(duration)} seconds")
        y -= 30
    
    # Write transcription
    c.setFont("Helvetica", 12)
    words = text.split()
    line = ""
    for word in words:
        if len(line + " " + word) < 80:
            line += " " + word
        else:
            c.drawString(50, y, line.strip())
            y -= 15
            line = word
            if y < 50:
                c.showPage()
                y = 800
    if line:
        c.drawString(50, y, line.strip())
    
    c.save() 