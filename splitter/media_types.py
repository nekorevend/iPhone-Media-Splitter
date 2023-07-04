import exiftool
from pymediainfo import MediaInfo

def list_substr_contains(l, f):
    for s in l:
        if f in s:
            return s
    return None

def get_exif_data(path):
    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(path)
        if not metadata:
            return None
        return metadata[0]

def is_cam_photo(path):
    if not path.lower().endswith(".heic") and not path.lower().endswith(".jpg"):
        return False
    metadata = get_exif_data(path)
    return metadata is not None \
        and 'Apple' in [metadata.get('EXIF:LensMake', ''),
                       metadata.get('EXIF:Make', '')] \
        and list_substr_contains(
                [metadata.get('EXIF:LensModel', ''),
                metadata.get('EXIF:Model', '')],
                'iP')  # Matches iPhone and iPad

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

def is_screenshot(path):
    if not path.lower().endswith(".png"):
        return False
    metadata = get_exif_data(path)
    return metadata is not None \
        and list_substr_contains(
            [metadata.get('ICC_Profile:DeviceManufacturer', ''),
            metadata.get('ICC_Profile:PrimaryPlatform', '')],
            'APPL') \
        and metadata.get('EXIF:UserComment', '') == 'Screenshot'

def is_screen_recording(path):
    if not path.lower().endswith(".mp4"):
        return False
    try:
        info = MediaInfo.parse(path)
        data = info.general_tracks[0].to_data()
        return data.get('performer') == 'ReplayKitRecording'
    except Exception:
        return False