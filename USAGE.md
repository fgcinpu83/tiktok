# Cara Menggunakan Text-to-Video Generator

## 1. Setup Environment

### Install Python 3.8+
```bash
python --version  # Pastikan versi 3.8 atau lebih tinggi
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

Jika ada error pada `moviepy`, install ffmpeg terlebih dahulu:
- **Windows**: https://ffmpeg.org/download.html
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

## 2. Cara Menggunakan Script

### Option A: Gunakan Script Default (Recommended)
```bash
python generate_video.py
```

Output: `output/video.mp4`

### Option B: Gunakan Custom Script
```bash
python generate_video.py --script "Teks Anda di sini" --output "custom_output.mp4"
```

### Option C: Gunakan Script dari File
```bash
# Buat file script
echo "Teks video Anda" > scripts/my_script.txt

# Baca dari file
python generate_video.py --script "$(cat scripts/my_script.txt)" --output output/video_custom.mp4
```

## 3. Konfigurasi (Optional)

Edit `config.py` untuk mengatur:

```python
VIDEO_WIDTH = 1080          # Lebar video
VIDEO_HEIGHT = 1920         # Tinggi video (portrait untuk TikTok)
VIDEO_FPS = 30              # Frame per detik
AUDIO_LANGUAGE = "id"       # Bahasa Indonesia
GESTURE_INTENSITY = 1.0     # Intensitas gerakan (0.5-2.0)
```

## 4. Output

Hasil video akan tersimpan di:
- `output/video.mp4` (default)
- Atau path yang Anda tentukan

Format: MP4, Codec: H.264 (kompatibel TikTok/YouTube)

## 5. Troubleshooting

### Error: "No module named 'cv2'"
```bash
pip install opencv-python
```

### Error: "ffmpeg not found"
Install ffmpeg di sistem Anda (lihat Setup Environment)

### Video Processing Lambat
- Gunakan GPU jika tersedia
- Kurangi resolusi atau FPS di `config.py`

### Audio Tidak Sync
Pastikan ffmpeg terinstall dengan benar

## 6. Tips Optimasi

- **Durasi Video**: Lebih panjang = waktu proses lebih lama
- **Resolusi**: 1080x1920 (TikTok standard)
- **FPS**: 30 FPS optimal untuk TikTok
- **Bahasa**: Support semua bahasa gTTS

## 7. Next Steps

- Edit gesture animation di `generate_video.py` (method `generate_pose_keypoints`)
- Tambahkan background custom
- Implementasi face detection untuk talking head realistis
- Gunakan AI model untuk gesture lebih natural

---

**Contoh Full Command:**
```bash
python generate_video.py --script "Halo semua!" --output output/intro.mp4
```
