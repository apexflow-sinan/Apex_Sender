"""Download notification sounds"""
import os
import urllib.request

def download_sounds():
    """Download free notification sounds"""
    
    sounds_dir = "assets/sounds"
    os.makedirs(sounds_dir, exist_ok=True)
    
    # Free notification sounds from freesound.org (CC0 license)
    sounds = {
        "success.wav": "https://freesound.org/data/previews/320/320655_5260872-lq.mp3",
        "error.wav": "https://freesound.org/data/previews/277/277403_5123851-lq.mp3",
        "notification.wav": "https://freesound.org/data/previews/316/316920_4939433-lq.mp3"
    }
    
    print("Note: Using Windows system sounds instead of downloading.")
    print("The application will use winsound.MessageBeep() for notifications.")
    print("\nIf you want custom sounds, place WAV files in:")
    print(f"  {os.path.abspath(sounds_dir)}")
    print("\nRequired files:")
    print("  - success.wav")
    print("  - error.wav")
    print("  - notification.wav")

if __name__ == "__main__":
    download_sounds()
