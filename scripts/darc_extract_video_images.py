import os
import subprocess
import logging
from datetime import datetime, timedelta

# Call example
# !python3 ./scripts/darc_extract_video_images.py \
#     --show_name {search_show_name} \
#     --image_zfill_mag {image_zfill_mag} \
#     --fps {fps}

# Get each frames' timestamp and rename file on disk accordingly

def get_timestamp(frame_number, fps=2):
    # Calculate the total time covered by the frame
    time_in_seconds = frame_number / fps
    
    # Convert the time to HH:MM:SS.MMM format
    hours, remainder = divmod(time_in_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    
    timestamp = datetime(1900, 1, 1, int(hours), int(minutes), int(seconds))
    timestamp_str = timestamp.strftime('%H:%M:%S')
    
    return f"{timestamp_str}.{milliseconds:03d}".replace(":", "-")


def rename_files_with_timestamp(directory, image_zfill_mag, fps=2):
    files = sorted([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    # Loop through each file and rename it
    for idx, filename in enumerate(files):
        if not filename.endswith('.jpg'):
            continue

        timestamp = get_timestamp(idx, fps=fps)
        new_filename = f"frame_{str(idx).zfill(image_zfill_mag)}_{timestamp}.jpg"
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))


def darc_extract_video_images(show_name, image_zfill_mag, fps=2):
    logging.info(f"Starting extraction for show: {show_name}")

    videos_dir = f"./data/videos/{show_name}/"
    video_filenames = sorted([f for f in os.listdir(videos_dir) if f.endswith(".mp4")])
    video_filepaths = [os.path.join(videos_dir, vfn) for vfn in video_filenames]
    
    logging.info(f"Videos to analyse: {video_filenames}")

    # Construct image-frame output folder
    images_outputdir = f"./data/images/{show_name}/"
    image_extractfolders = [vfn.replace("-", "").lower().split(".mp4")[0] for vfn in video_filenames]
    image_extractpaths = [os.path.join(images_outputdir, "-".join(folder.split())) for folder in image_extractfolders]

    for vfp, iep, in zip(video_filepaths, image_extractpaths):
        os.makedirs(iep, exist_ok=True) 
        extract_command = ["ffmpeg", "-i", vfp, "-vf", f"fps={fps}", f"{iep}/frame_%0{image_zfill_mag}d.jpg"]
        try:
            subprocess.run(extract_command, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error during ffmpeg execution: {e}")
            continue

        rename_files_with_timestamp(f"{iep}/", image_zfill_mag=image_zfill_mag)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Extract image frames from videos')
    parser.add_argument('--show_name', type=str, required=True, help='Name of the show.')
    parser.add_argument('--image_zfill_mag', type=int, default=5, help='Zero-padding for frame filenames.')
    parser.add_argument('--fps', type=int, default=2, help='Frames per second to extract.')
    
    args = parser.parse_args()
    darc_extract_video_images(args.show_name, args.image_zfill_mag, args.fps)

# Call example from ipynb
# !python3 darc_extract_video_images.py --show_name "life-on-earth" --image_zfill_mag 5 --fps 2