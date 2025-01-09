import os
import requests
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

# Load API keys from .env file
load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

# Function to download a file
def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")
        return filename
    else:
        print(f"Failed to download {filename}")
        return None

# Function to fetch video from Pexels based on category
def fetch_video_from_pexels(category):
    url = f"https://api.pexels.com/videos/search?query={category}&per_page=5"
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        videos = response.json().get("videos", [])
        if videos:
            video = videos[0]  # Use the first video
            video_url = video["video_files"][0]["link"]
            return download_file(video_url, "short_video.mp4")
    print(f"No video found for category '{category}' on Pexels.")
    return None

# Function to fetch audio from Pixabay based on category
def fetch_audio_from_pixabay(category):
    url = f"https://pixabay.com/api/audio/?key={PIXABAY_API_KEY}&q={category}&per_page=5"
    response = requests.get(url)
    if response.status_code == 200:
        audios = response.json().get("hits", [])
        if audios:
            audio = audios[0]  # Use the first audio
            audio_url = audio["audio"]
            return download_file(audio_url, "background_music.mp3")
    print(f"No audio found for category '{category}' on Pixabay.")
    return None

# Function to create the video short
def create_short_video(category, text_content):
    print(f"Creating a short video for category: {category}")

    # Fetch video and audio
    video_file = fetch_video_from_pexels(category)
    audio_file = fetch_audio_from_pixabay(category)

    if not video_file or not audio_file:
        print("Failed to fetch resources. Aborting.")
        return

    # Load video and audio
    video_clip = VideoFileClip(video_file).subclip(0, 10)  # Limit video to 10 seconds
    audio_clip = AudioFileClip(audio_file).set_duration(10)

    # Add text overlay
    text_clip = TextClip(text_content, fontsize=50, color="white", bg_color="black", size=video_clip.size).set_duration(10).set_position("center")

    # Combine video, text, and audio
    final_video = CompositeVideoClip([video_clip, text_clip]).set_audio(audio_clip)

    # Output final video
    output_filename = f"{category}_short.mp4"
    final_video.write_videofile(output_filename, fps=24, codec="libx264", audio_codec="aac")
    print(f"Video created: {output_filename}")

    # Clean up temporary files
    os.remove(video_file)
    os.remove(audio_file)

# Main function
if __name__ == "__main__":
    print("Enter the category for the video (e.g., nature, travel, motivation): ")
    category = input().strip()
    print("Enter the text content to overlay on the video: ")
    text_content = input().strip()

    create_short_video(category, text_content)
