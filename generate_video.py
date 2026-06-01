#!/usr/bin/env python3
"""
Text-to-Video Generator
Generate TikTok video dengan gesture natural dari script teks.
"""

import cv2
import numpy as np
import argparse
import os
from gtts import gTTS
from pathlib import Path
import mediapipe as mp
from moviepy.editor import ImageSequenceClip, AudioFileClip
import config
import time

class TextToVideoGenerator:
    def __init__(self, script, output_path="output/video.mp4"):
        self.script = script
        self.output_path = output_path
        self.audio_path = "output/temp_audio.wav"
        
        # Create output dir
        os.makedirs("output", exist_ok=True)
        
        # Mediapipe setup
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=config.POSE_DETECTION_CONFIDENCE
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
    def generate_audio(self):
        """Convert teks ke audio menggunakan gTTS"""
        print("[*] Generating audio from text...")
        tts = gTTS(text=self.script, lang=config.AUDIO_LANGUAGE, slow=False)
        tts.save(self.audio_path)
        print(f"[✓] Audio saved: {self.audio_path}")
        
        # Get audio duration
        audio = AudioFileClip(self.audio_path)
        duration = audio.duration
        audio.close()
        return duration
    
    def create_gesture_frame(self, frame_index, total_frames):
        """Create frame dengan gesture natural"""
        frame = np.ones(
            (config.VIDEO_HEIGHT, config.VIDEO_WIDTH, 3),
            dtype=np.uint8
        ) * 255
        
        # Calculate animation progress (0 to 1)
        progress = frame_index / total_frames
        
        # Generate pose keypoints berdasarkan progress
        pose_keypoints = self.generate_pose_keypoints(progress)
        
        # Draw skeleton
        frame = self.draw_skeleton(frame, pose_keypoints)
        
        # Draw text
        frame = self.draw_text(frame, self.script)
        
        return frame
    
    def generate_pose_keypoints(self, progress):
        """Generate pose keypoints yang berubah sesuai progress video"""
        # Base pose (neutral standing)
        keypoints = {
            'nose': [540, 400],
            'left_shoulder': [400, 600],
            'right_shoulder': [680, 600],
            'left_elbow': [350, 900],
            'right_elbow': [730, 900],
            'left_wrist': [300, 1200],
            'right_wrist': [780, 1200],
            'left_hip': [420, 1200],
            'right_hip': [660, 1200],
            'left_knee': [420, 1500],
            'right_knee': [660, 1500],
            'left_ankle': [420, 1800],
            'right_ankle': [660, 1800],
        }
        
        # Animation cycle: 0-1 progress
        cycle = (progress * 4) % 1  # 4 cycles per video
        
        # Head gesture (mengangguk/nod)
        if cycle < 0.25:
            keypoints['nose'][1] -= int(30 * (cycle / 0.25))
        elif cycle < 0.5:
            keypoints['nose'][1] += int(30 * ((cycle - 0.25) / 0.25))
        
        # Right hand gesture (pointing/explaining)
        hand_angle = cycle * 2 * np.pi
        keypoints['right_wrist'][0] = int(730 + 150 * np.cos(hand_angle))
        keypoints['right_wrist'][1] = int(1200 + 100 * np.sin(hand_angle))
        keypoints['right_elbow'][0] = int(730 + 75 * np.cos(hand_angle))
        keypoints['right_elbow'][1] = int(900 + 50 * np.sin(hand_angle))
        
        # Left hand gesture (supporting)
        hand_angle_left = (cycle + 0.3) * 2 * np.pi
        keypoints['left_wrist'][0] = int(300 + 100 * np.cos(hand_angle_left))
        keypoints['left_wrist'][1] = int(1200 + 80 * np.sin(hand_angle_left))
        
        # Body sway (side to side)
        sway = int(30 * np.sin(cycle * 2 * np.pi))
        for key in keypoints:
            keypoints[key][0] += sway
        
        return keypoints
    
    def draw_skeleton(self, frame, keypoints):
        """Draw skeleton/pose di frame"""
        # Connections (pose structure)
        connections = [
            ('nose', 'left_shoulder'),
            ('nose', 'right_shoulder'),
            ('left_shoulder', 'left_elbow'),
            ('left_elbow', 'left_wrist'),
            ('right_shoulder', 'right_elbow'),
            ('right_elbow', 'right_wrist'),
            ('left_shoulder', 'left_hip'),
            ('right_shoulder', 'right_hip'),
            ('left_hip', 'left_knee'),
            ('left_knee', 'left_ankle'),
            ('right_hip', 'right_knee'),
            ('right_knee', 'right_ankle'),
        ]
        
        # Draw connections (garis)
        for start, end in connections:
            p1 = tuple(keypoints[start])
            p2 = tuple(keypoints[end])
            cv2.line(frame, p1, p2, (0, 150, 0), 3)
        
        # Draw keypoints (lingkaran)
        for key, point in keypoints.items():
            cv2.circle(frame, tuple(point), 8, (0, 255, 0), -1)
            cv2.circle(frame, tuple(point), 8, (0, 0, 0), 2)
        
        return frame
    
    def draw_text(self, frame, text):
        """Draw text di frame"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.2
        color = (0, 0, 0)
        thickness = 2
        
        # Split text into lines
        max_width = 60
        lines = []
        words = text.split()
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) < max_width:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word + " "
        if current_line:
            lines.append(current_line)
        
        # Draw text at bottom
        y_offset = config.VIDEO_HEIGHT - 200
        for i, line in enumerate(lines):
            y = y_offset + (i * 50)
            cv2.putText(frame, line, (50, y), font, font_scale, color, thickness)
        
        return frame
    
    def generate_video(self):
        """Generate video dari frames + audio"""
        print("[*] Generating audio...")
        audio_duration = self.generate_audio()
        
        total_frames = int(audio_duration * config.VIDEO_FPS)
        print(f"[*] Generating {total_frames} frames ({audio_duration:.1f}s)...")
        
        frames = []
        for i in range(total_frames):
            frame = self.create_gesture_frame(i, total_frames)
            frames.append(frame)
            
            if (i + 1) % 30 == 0:
                print(f"    Progress: {i + 1}/{total_frames} frames")
        
        print("[*] Combining frames with audio...")
        
        # Convert frames to RGB for moviepy
        frames_rgb = [cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in frames]
        
        # Create video clip
        video_clip = ImageSequenceClip(frames_rgb, fps=config.VIDEO_FPS)
        
        # Add audio
        audio_clip = AudioFileClip(self.audio_path)
        video_clip = video_clip.set_audio(audio_clip)
        
        # Write to file
        print(f"[*] Writing to {self.output_path}...")
        video_clip.write_videofile(
            self.output_path,
            verbose=False,
            logger=None,
            codec='libx264',
            audio_codec='aac'
        )
        
        # Cleanup
        video_clip.close()
        audio_clip.close()
        os.remove(self.audio_path)
        
        print(f"[✓] Video generated: {self.output_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate video dari teks')
    parser.add_argument('--script', type=str, required=False, 
                        default="Halo antek-antek asing! Saya Om Alex. Ini adalah video pertama saya di channel ini. Ke depannya, saya akan membagikan berbagai konten menarik, mulai dari pesan moral yang mendalam, filosofi kehidupan, sampai review produk yang jujur tanpa gimik. Penasaran? Pastikan kalian nantikan konten saya selanjutnya, ya!",
                        help='Script teks untuk video')
    parser.add_argument('--output', type=str, default='output/video.mp4',
                        help='Output video path')
    
    args = parser.parse_args()
    
    print("\n" + "="*50)
    print("TEXT-TO-VIDEO GENERATOR")
    print("="*50)
    print(f"\nScript: {args.script[:80]}...")
    print(f"Output: {args.output}")
    print("="*50 + "\n")
    
    generator = TextToVideoGenerator(args.script, args.output)
    generator.generate_video()
    
    print("\n[✓] DONE!")

if __name__ == "__main__":
    main()
