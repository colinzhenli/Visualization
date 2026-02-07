#!/usr/bin/env python3
"""
Script to split multiple videos into two parts and slow down the fps.
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
    """
    
    if not os.path.exists(input_video):
        print(f"Error: Input video not found: {input_video}")
        return False
    
    # Get original fps
    original_fps = get_video_info(input_video)
    new_fps = original_fps / slowdown_factor
    
    print(f"  Original FPS: {original_fps}")
    print(f"  New FPS (slowed down {slowdown_factor}x): {new_fps}")
    
    # First part: frames 0-119 (first 120 frames)
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
    
    print(f"  Creating part 1: {output1}")
    try:
        subprocess.run(cmd1, check=True, capture_output=True)
        print(f"    Success!")
    except subprocess.CalledProcessError as e:
        print(f"    Error: {e}")
        return False
    
    print(f"  Creating part 2: {output2}")
    try:
        subprocess.run(cmd2, check=True, capture_output=True)
        print(f"    Success!")
    except subprocess.CalledProcessError as e:
        print(f"    Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    # Videos to process
    videos = ["Ours_video", "PBR_video", "MERL_video", "Light_video"]
    base_path = "resources/videos"
    
    frames_per_part = 120
    slowdown_factor = 2
    
    print(f"Processing {len(videos)} videos...")
    print(f"Frames per part: {frames_per_part}")
    print(f"Slowdown factor: {slowdown_factor}x")
    print("=" * 50)
    
    for video_name in videos:
        input_video = f"{base_path}/{video_name}.mp4"
        output1 = f"{base_path}/{video_name}_1.mp4"
        output2 = f"{base_path}/{video_name}_2.mp4"
        
        print(f"\nProcessing: {video_name}")
        print(f"  Input: {input_video}")
        
        success = split_and_slow_video(input_video, output1, output2, frames_per_part, slowdown_factor)
        
        if success:
            print(f"  Done!")
        else:
            print(f"  Failed!")
    
    print("\n" + "=" * 50)
    print("All videos processed!")
