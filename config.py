# Konfigurasi Video Generation

# Video Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920  # Portrait untuk TikTok/Shorts
VIDEO_FPS = 30
VIDEO_DURATION = None  # Auto detect dari audio

# Audio Settings
AUDIO_LANGUAGE = "id"  # Bahasa Indonesia
AUDIO_RATE = 44100

# Gesture Settings
GESTURE_INTENSITY = 1.0  # 0.5 - 2.0 (intensity gerakan)
POSE_DETECTION_CONFIDENCE = 0.5
HAND_DETECTION_CONFIDENCE = 0.5

# Color Settings
BACKGROUND_COLOR = (255, 255, 255)  # White
POSE_COLOR = (0, 255, 0)  # Green untuk skeleton

# Output Settings
OUTPUT_QUALITY = "high"  # low, medium, high
OUTPUT_FORMAT = "mp4"
