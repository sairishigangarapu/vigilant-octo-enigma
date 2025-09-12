import os
import cv2
import whisper
import yt_dlp
from typing import Dict, List, Any

def deconstruct_video(video_url: str, output_dir: str = "output") -> Dict[str, Any]:
    """
    Download a video, extract frames, transcribe audio, and clean up.
    
    Args:
        video_url (str): URL of the video to process
        output_dir (str): Directory to store output files (default: "output")
        
    Returns:
        Dict containing paths to extracted frames and transcript
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up yt-dlp options
    video_path = os.path.join(output_dir, "video.mp4")
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': video_path,
        'quiet': True
    }
    
    # Download video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    
    # Extract frames
    frames = []
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Extract one frame every 5 seconds
        if frame_count % int(fps * 5) == 0:
            frame_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            frames.append(frame_path)
            
        frame_count += 1
    
    cap.release()
    
    # Transcribe audio
    model = whisper.load_model("base")
    transcript = model.transcribe(video_path)
    
    transcript_path = os.path.join(output_dir, "transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        text = transcript["text"]
        if isinstance(text, list):
            text = "\n".join(str(t) for t in text)
        f.write(text)
    
    # Clean up video file
    os.remove(video_path)
    
    return {
        "frames": frames,
        "transcript_path": transcript_path
    }