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
    if not path.lower().endswith(".heic"):
        return False
    with open(path, 'rb') as f:
        try:
            exifread_data = exifread.process_file(f)
            return str(exifread_data['EXIF LensMake']) == 'Apple' and 'iP' in str(exifread_data['Image HostComputer'])
        except Exception:
            return False

def is_cam_video(path):
    if not path.lower().endswith(".mov"):
        return False
    try:
        info = MediaInfo.parse(path)
        data = info.general_tracks[0].to_data()
        return data['comapplequicktimemake'] == 'Apple' and list_substr_contains(data.keys(), 'livephoto') == None
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

parser = argparse.ArgumentParser(description='')
parser.add_argument('--source', type=str, help='Path to the directory that contains all of the media files from an iOS device.')
parser.add_argument('--photo_dest', help='Path to output photos. Will not overwrite files.')
parser.add_argument('--video_dest', help='Path to output videos. Will not overwrite files.')
parser.add_argument('--screen_recording_dest', help='Path to output screen recordings. Will not overwrite files.')
args = parser.parse_args()

if args.photo_dest and not os.path.isdir(args.photo_dest):
    print('The photo destination path must be a valid directory.')
    sys.exit(1)

if args.video_dest and not os.path.isdir(args.video_dest):
    print('The video destination path must be a valid directory.')
    sys.exit(1)

if args.screen_recording_dest and not os.path.isdir(args.screen_recording_dest):
    print('The screen recording destination path must be a valid directory.')
    sys.exit(1)

cam_photos = []
cam_live_photo_videos = []
cam_videos = []
screen_recordings = []

if args.source:
    for root, dirs, files in os.walk(args.source):
        for name in files:
            path = f'{root}{name}'
            count = 0
            if args.photo_dest and is_cam_photo(path):
                cam_photos.append(path)
                count = count+1
            if args.video_dest and is_cam_video(path):
                cam_videos.append(path)
                count = count+1
            if args.screen_recording_dest and is_screen_recording(path):
                screen_recordings.append(path)
                count = count+1
            if args.photo_dest and is_live_photo_video(path):
                cam_live_photo_videos.append(path)
                count = count+1
            if count > 1:
                print(f'ERROR: Found file "{path}" matches more than one possible type.')

    cam_photos.sort()
    cam_live_photo_videos.sort()
    cam_videos.sort()
    screen_recordings.sort()

    if args.photo_dest:
        for path in cam_photos:
            to_path = args.photo_dest + os.path.sep + os.path.basename(path)
            if os.path.exists(to_path):
                print('Skipping', path)
            else:
                print('Copying', path, 'to', to_path)
                shutil.copyfile(path, to_path)
        for path in cam_live_photo_videos:
            to_path = args.photo_dest + os.path.sep + os.path.basename(path)
            if os.path.exists(to_path):
                print('Skipping', path)
            else:
                print('Copying', path, 'to', to_path)
                shutil.copyfile(path, to_path)
    if args.video_dest:
        for path in cam_videos:
            to_path = args.video_dest + os.path.sep + os.path.basename(path)
            if os.path.exists(to_path):
                print('Skipping', path)
            else:
                print('Copying', path, 'to', to_path)
                shutil.copyfile(path, to_path)
    if args.screen_recording_dest:
        for path in screen_recordings:
            to_path = args.screen_recording_dest + os.path.sep + os.path.basename(path)
            if os.path.exists(to_path):
                print('Skipping', path)
            else:
                print('Copying', path, 'to', to_path)
                shutil.copyfile(path, to_path)
