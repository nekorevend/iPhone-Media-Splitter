import argparse
import exifread
import os
import shutil
import sys
from pymediainfo import MediaInfo

def list_substr_contains(l, f):
    for s in l:
        if f in s:
            return s
    return None

def is_cam_photo(path):
    if not path.lower().endswith(".heic") and not path.lower().endswith(".jpg"):
        return False
    with open(path, 'rb') as f:
        try:
            exifread_data = exifread.process_file(f)
            return 'Apple' in [str(exifread_data.get('EXIF LensMake')),
                               str(exifread_data.get('Image Make'))] \
                   and list_substr_contains(
                           [str(exifread_data.get('EXIF LensModel')),
                           str(exifread_data.get('Image Model'))],
                           'iP')  # Matches iPhone and iPad
        except Exception:
            return False

def is_cam_video(path):
    if not path.lower().endswith(".mov"):
        return False
    try:
        info = MediaInfo.parse(path)
        data = info.general_tracks[0].to_data()
        return data['comapplequicktimemake'] == 'Apple' \
               and list_substr_contains(data.keys(), 'livephoto') == None
    except Exception:
        return False

def is_live_photo_video(path):
    if not path.lower().endswith(".mov"):
        return False
    try:
        info = MediaInfo.parse(path)
        data = info.general_tracks[0].to_data()
        return list_substr_contains(data.keys(), 'livephoto') != None
    except Exception:
        return False

def is_screen_recording(path):
    if not path.lower().endswith(".mp4"):
        return False
    try:
        info = MediaInfo.parse(path)
        data = info.general_tracks[0].to_data()
        return data['performer'] == 'ReplayKitRecording'
    except Exception:
        return False

def generate_report(args, cam_photos, cam_live_photo_videos, cam_videos, screen_recordings, strays):
    builder = [
        f'Handled:'
    ]
    if args.photo_dest:
        builder.append(f'{os.linesep}{cam_photos} new camera photos.')
        builder.append(f'{os.linesep}{cam_live_photo_videos} new videos from live photos.')
    if args.video_dest:
        builder.append(f'{os.linesep}{cam_videos} new video recordings.')
    if args.screen_recording_dest:
        builder.append(f'{os.linesep}{screen_recordings} new screen recordings.')
    builder.append(f'{os.linesep}{strays} new stray files.')

    return ''.join(builder)

parser = argparse.ArgumentParser(description='')
parser.add_argument('--source', type=str, help='Path to the directory that contains all of the media files from an iOS device.')
parser.add_argument('--photo_dest', help='Path to output photos. Will not overwrite files.')
parser.add_argument('--video_dest', help='Path to output videos. Will not overwrite files.')
parser.add_argument('--screen_recording_dest', help='Path to output screen recordings. Will not overwrite files.')
parser.add_argument('--stray_dest', help='Path to output files that don\'t match any supported category. Will not overwrite files.')
parser.add_argument('--overwrite', dest='overwrite', action='store_true', help='Overwrite files if they exist.')
parser.add_argument('--verbose', '-v', dest='verbose', action='store_true', help='Print verbose output.')
parser.set_defaults(overwrite=False)
parser.set_defaults(verbose=False)
args = parser.parse_args()

if args.photo_dest and not os.path.isdir(args.photo_dest):
    print('The photo destination path must be a valid directory.', file=sys.stderr)
    sys.exit(1)

if args.video_dest and not os.path.isdir(args.video_dest):
    print('The video destination path must be a valid directory.', file=sys.stderr)
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
screen_recordings = []
strays = []

if args.source:
    max_length = 0
    for root, _, files in os.walk(args.source):
        for name in files:
            path = os.path.join(root, name)
            max_length = max(len(path), max_length)
            print(f'Processing {path}...'.ljust(max_length + 14), end='\r')
            count = 0
            if is_cam_photo(path):
                count = count+1
                if args.photo_dest:
                    cam_photos.append(path)
            if is_cam_video(path):
                count = count+1
                if args.video_dest:
                    cam_videos.append(path)
            if is_screen_recording(path):
                count = count+1
                if args.screen_recording_dest:
                    screen_recordings.append(path)
            if is_live_photo_video(path):
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
    screen_recordings.sort()
    new_photo_count = 0
    new_live_photo_video_count = 0
    new_video_count = 0
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
            new_screen_recording_count,
            new_stray_count
        )
    print(f'Done!{os.linesep}{os.linesep}{report}')
