import argparse
import media_types
import os
import shutil
import sys

def generate_report(args, cam_photos, cam_live_photo_videos, cam_videos, screenshots, screen_recordings, strays):
    builder = [
        f'Handled:'
    ]
    if args.photo_dest:
        builder.append(f'{os.linesep}{cam_photos} new camera photos.')
        builder.append(f'{os.linesep}{cam_live_photo_videos} new videos from live photos.')
    if args.video_dest:
        builder.append(f'{os.linesep}{cam_videos} new camera videos.')
    if args.screenshot_dest:
        builder.append(f'{os.linesep}{screenshots} new screenshots.')
    if args.screen_recording_dest:
        builder.append(f'{os.linesep}{screen_recordings} new screen recordings.')
    builder.append(f'{os.linesep}{strays} new stray files.')

    return ''.join(builder)

parser = argparse.ArgumentParser(description='')
parser.add_argument('--source', required=True, type=str, help='Path to the directory that contains all of the media files from an iOS device.')
parser.add_argument('--photo_dest', help='Path to output photos. Will not overwrite files unless --overwrite is given.')
parser.add_argument('--video_dest', help='Path to output videos. Will not overwrite files unless --overwrite is given.')
parser.add_argument('--screenshot_dest', help='Path to output screenshots. Will not overwrite files unless --overwrite is given.')
parser.add_argument('--screen_recording_dest', help='Path to output screen recordings. Will not overwrite files unless --overwrite is given.')
parser.add_argument('--stray_dest', help='Path to output files that don\'t match any supported category. Will not overwrite files unless --overwrite is given.')
parser.add_argument('--overwrite', dest='overwrite', action='store_true', help='Overwrite files if they exist.')
parser.add_argument('--verbose', '-v', dest='verbose', action='store_true', help='Print verbose output.')
parser.set_defaults(overwrite=False)
parser.set_defaults(verbose=False)
args = parser.parse_args()

try:
    media_types.exiftool.ExifToolHelper()
except FileNotFoundError:
    print('The `exiftool` executable (from exiftool.org) is required. Please add it to your PATH.', file=sys.stderr)

if args.photo_dest and not os.path.isdir(args.photo_dest):
    print('The photo destination path must be a valid directory.', file=sys.stderr)
    sys.exit(1)

if args.video_dest and not os.path.isdir(args.video_dest):
    print('The video destination path must be a valid directory.', file=sys.stderr)
    sys.exit(1)

if args.screenshot_dest and not os.path.isdir(args.screenshot_dest):
    print('The screenshot destination path must be a valid directory.', file=sys.stderr)
    sys.exit(1)

if args.screen_recording_dest and not os.path.isdir(args.screen_recording_dest):
    print('The screen recording destination path must be a valid directory.', file=sys.stderr)
    sys.exit(1)

if args.stray_dest and not os.path.isdir(args.stray_dest):
    print('The stray destination path must be a valid directory.', file=sys.stderr)
    sys.exit(1)

cam_photos = []
cam_live_photo_videos = []
cam_videos = []
screenshots = []
screen_recordings = []
strays = []

max_length = 0
for root, _, files in os.walk(args.source):
    for name in files:
        path = os.path.join(root, name)
        max_length = max(len(path), max_length)
        print(f'Processing {path}...'.ljust(max_length + 14), end='\r')
        count = 0
        if media_types.is_cam_photo(path):
            count = count+1
            if args.photo_dest:
                cam_photos.append(path)
        if media_types.is_cam_video(path):
            count = count+1
            if args.video_dest:
                cam_videos.append(path)
        if media_types.is_screenshot(path):
            count = count+1
            if args.screenshot_dest:
                screenshots.append(path)
        if media_types.is_screen_recording(path):
            count = count+1
            if args.screen_recording_dest:
                screen_recordings.append(path)
        if media_types.is_live_photo_video(path):
            count = count+1
            if args.photo_dest:
                cam_live_photo_videos.append(path)
        if count > 1:
            print(f'{os.linesep}ERROR: Found file "{path}" that matches more than one possible type.', file=sys.stderr)
        elif count < 1:
            if args.verbose:
                print(f'{os.linesep}No match found for: {path}', file=sys.stderr)
            strays.append(path)

print(f'{os.linesep}')

cam_photos.sort()
cam_live_photo_videos.sort()
cam_videos.sort()
screenshots.sort()
screen_recordings.sort()
new_photo_count = 0
new_live_photo_video_count = 0
new_video_count = 0
new_screenshot_count = 0
new_screen_recording_count = 0
new_stray_count = 0

if args.photo_dest:
    for path in cam_photos:
        to_path = os.path.join(args.photo_dest, os.path.basename(path))
        if os.path.exists(to_path) and not args.overwrite:
            if args.verbose:
                print(f'Skipping {path}')
        else:
            print(f'Copying {path} to {to_path}')
            shutil.copy2(path, to_path)
            new_photo_count += 1
    for path in cam_live_photo_videos:
        to_path = os.path.join(args.photo_dest, os.path.basename(path))
        if os.path.exists(to_path) and not args.overwrite:
            if args.verbose:
                print(f'Skipping {path}')
        else:
            print(f'Copying {path} to {to_path}')
            shutil.copy2(path, to_path)
            new_live_photo_video_count += 1
if args.video_dest:
    for path in cam_videos:
        to_path = os.path.join(args.video_dest, os.path.basename(path))
        if os.path.exists(to_path) and not args.overwrite:
            if args.verbose:
                print(f'Skipping {path}')
        else:
            print(f'Copying {path} to {to_path}')
            shutil.copy2(path, to_path)
            new_video_count += 1
if args.screenshot_dest:
    for path in screenshots:
        to_path = os.path.join(args.screenshot_dest, os.path.basename(path))
        if os.path.exists(to_path) and not args.overwrite:
            if args.verbose:
                print(f'Skipping {path}')
        else:
            print(f'Copying {path} to {to_path}')
            shutil.copy2(path, to_path)
            new_screenshot_count += 1
if args.screen_recording_dest:
    for path in screen_recordings:
        to_path = os.path.join(args.screen_recording_dest, os.path.basename(path))
        if os.path.exists(to_path) and not args.overwrite:
            if args.verbose:
                print(f'Skipping {path}')
        else:
            print(f'Copying {path} to {to_path}')
            shutil.copy2(path, to_path)
            new_screen_recording_count += 1
if args.stray_dest:
    for path in strays:
        to_path = os.path.join(args.stray_dest, os.path.basename(path))
        if os.path.exists(to_path) and not args.overwrite:
            if args.verbose:
                print(f'Skipping {path}')
        else:
            print(f'Copying {path} to {to_path}')
            shutil.copy2(path, to_path)
            new_stray_count += 1

report = generate_report(
        args,
        new_photo_count,
        new_live_photo_video_count,
        new_video_count,
        new_screenshot_count,
        new_screen_recording_count,
        new_stray_count
    )
print(f'Done!{os.linesep}{os.linesep}{report}')
