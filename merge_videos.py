#!/usr/bin/env python3
"""
Script to merge two videos side by side for video comparison.
The output video will have the left video on the left half and the right video on the right half.
"""

import subprocess
import sys
import os

def merge_videos_side_by_side(left_video, right_video, output_video):
    """
    Merge two videos side by side using ffmpeg.
    
    Args:
        left_video: Path to the left video (will appear on the left side)
        right_video: Path to the right video (will appear on the right side)
        output_video: Path for the output merged video
    """
    
    # Check if input files exist
    if not os.path.exists(left_video):
        print(f"Error: Left video not found: {left_video}")
        sys.exit(1)
    if not os.path.exists(right_video):
        print(f"Error: Right video not found: {right_video}")
        sys.exit(1)
    
    # ffmpeg command to stack videos horizontally
    # hstack filter places videos side by side
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output file if exists
        '-i', left_video,
        '-i', right_video,
        '-filter_complex', '[0:v][1:v]hstack=inputs=2[v]',
        '-map', '[v]',
        '-c:v', 'libx264',
        '-crf', '18',  # High quality
        '-preset', 'medium',
        output_video
    ]
    
    print(f"Merging videos...")
    print(f"  Left:   {left_video}")
    print(f"  Right:  {right_video}")
    print(f"  Output: {output_video}")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\nSuccess! Merged video saved to: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"Error running ffmpeg: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg.")
        sys.exit(1)

if __name__ == "__main__":
    # Default paths
    left_video = "resources/videos/PBR_video.mp4"
    right_video = "resources/videos/Ours_video.mp4"
    output_video = "resources/videos/merged_comparison.mp4"
    
    # Allow command line arguments
    if len(sys.argv) == 4:
        left_video = sys.argv[1]
        right_video = sys.argv[2]
        output_video = sys.argv[3]
    elif len(sys.argv) != 1:
        print("Usage: python merge_videos.py [left_video] [right_video] [output_video]")
        print("       python merge_videos.py  # Uses default paths")
        sys.exit(1)
    
    merge_videos_side_by_side(left_video, right_video, output_video)
