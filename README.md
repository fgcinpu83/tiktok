# Text-to-Video Generator

Generate video TikTok/YouTube dengan script otomatis dari teks.

## Fitur
- ✅ Text-to-Speech (gTTS)
- ✅ Pose/Gesture detection (Mediapipe)
- ✅ Video generation dengan gesture natural
- ✅ Audio sync otomatis

## Requirements
```
pip install -r requirements.txt
```

## Penggunaan

```bash
python generate_video.py --script "Halo antek-antek asing! Saya Om Alex..." --output video.mp4
```

## Output
- `video.mp4` - Video TikTok siap upload
- `audio.wav` - Audio terpisah

## Struktur Folder
```
tiktok/
├── generate_video.py      # Main script
├── requirements.txt       # Dependencies
├── config.py             # Konfigurasi
├── scripts/              # Folder script
│   └── intro.txt
├── output/               # Folder output video
└── README.md
```
