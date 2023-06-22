# iPhone-Media-Splitter
Allows copying photos, videos, and screen recordings into individual folders.

iOS makes it difficult to cleanly/quickly separate different types of files. While it is possible to filter to "only videos", "only live photos", or "only slow-mo", there is no way to filter to "only photos".

When backing up your media from an iOS device, you can bulk copy all of the files into a single folder and then use this tool to separate the different types into separate folders.

Example command:
```
process.py --source "/path/to/all/media/from/iphone" --photo_dest "/path/to/only/photos" --video_dest "/path/to/only/videos" --stray_dest "/path/for/misc/stuff"
```

The video files associated with live photos will be copied to be alongside their photos and are not treated the same as actual videos.
