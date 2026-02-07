#!/usr/bin/env python3
"""
Script to split a video into two parts and slow down the fps.
"""

import subprocess
import sys
import os

def get_video_info(video_path):
    """Get video fps using ffprobe"""
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=r_frame_rate',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    fps_str = result.stdout.strip()
    # Parse fps (could be like "20/1" or "20")
    if '/' in fps_str:
        num, den = fps_str.split('/')
        return float(num) / float(den)
    return float(fps_str)

def split_and_slow_video(input_video, output1, output2, frames_per_part=120, slowdown_factor=2):
    """
    Split video into two parts and slow down fps.
    
    Args:
        input_video: Path to input video
        output1: Path for first part output
        output2: Path for second part output
        frames_per_part: Number of frames per part (default 120)
        slowdown_factor: How much to slow down (2 = half speed)
    """
    
    if not os.path.exists(input_video):
        print(f"Error: Input video not found: {input_video}")
        sys.exit(1)
    
    # Get original fps
    original_fps = get_video_info(input_video)
    new_fps = original_fps / slowdown_factor
    
    print(f"Original FPS: {original_fps}")
    print(f"New FPS (slowed down {slowdown_factor}x): {new_fps}")
    print(f"Frames per part: {frames_per_part}")
    
    # Calculate time duration for each part at original fps
    duration_per_part = frames_per_part / original_fps
    
    print(f"Duration per part at original fps: {duration_per_part}s")
    
    # First part: frames 0-119 (first 120 frames)
    # Using setpts to slow down and fps filter to set output fps
    cmd1 = [
        'ffmpeg', '-y',
        '-i', input_video,
        '-vf', f'trim=start_frame=0:end_frame={frames_per_part},setpts={slowdown_factor}*PTS',
        '-r', str(new_fps),
        '-c:v', 'libx264',
        '-crf', '18',
        '-preset', 'medium',
        output1
    ]
    
    # Second part: frames 120-239 (second 120 frames)
    cmd2 = [
        'ffmpeg', '-y',
        '-i', input_video,
        '-vf', f'trim=start_frame={frames_per_part}:end_frame={frames_per_part * 2},setpts={slowdown_factor}*(PTS-STARTPTS)',
        '-r', str(new_fps),
        '-c:v', 'libx264',
        '-crf', '18',
        '-preset', 'medium',
        output2
    ]
    
    print(f"\nCreating first part (frames 0-{frames_per_part-1})...")
    print(f"  Output: {output1}")
    try:
        subprocess.run(cmd1, check=True)
        print(f"  Success!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    print(f"\nCreating second part (frames {frames_per_part}-{frames_per_part*2-1})...")
    print(f"  Output: {output2}")
    try:
        subprocess.run(cmd2, check=True)
        print(f"  Success!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    print(f"\nDone! Created two videos with {slowdown_factor}x slower playback.")

if __name__ == "__main__":
    input_video = "resources/videos/merged_comparison.mp4"
    output1 = "resources/videos/comparison_part1.mp4"
    output2 = "resources/videos/comparison_part2.mp4"
    
    split_and_slow_video(input_video, output1, output2, frames_per_part=120, slowdown_factor=2)
