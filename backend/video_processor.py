# video_processor.py
import cv2
import yt_dlp
import os

def download_video_and_get_metadata(url: str) -> dict:
    """Downloads a video from a URL and extracts its metadata."""
    # TODO: Implement yt-dlp logic to download video to a temp path
    # and extract title, uploader, description.
    print(f"Downloading video from {url}...")
    # Placeholder implementation
    return {
        "video_path": "temp_video.mp4",
        "title": "Example Video Title",
        "uploader": "Example Uploader"
    }

def extract_keyframes(video_path: str, num_frames: int = 5) -> list[str]:
    """Extracts a set number of keyframes from a video file."""
    # TODO: Implement OpenCV logic to capture frames from the video
    # and save them as temporary image files.
    print(f"Extracting {num_frames} keyframes from {video_path}...")
    # Placeholder implementation
    frame_paths = [f"frame_{i}.jpg" for i in range(num_frames)]
    return frame_paths

def cleanup_files(files: list[str]):
    """Deletes a list of temporary files."""
    for file_path in files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Cleaned up {file_path}")
