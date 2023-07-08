# iPhone Media Splitter
Allows copying photos, videos, and screen recordings into individual folders.

iOS makes it difficult to cleanly/quickly separate different types of files. While it is possible to filter to "only videos", "only live photos", or "only slow-mo", there is no way to filter to "only photos". I've written an article about this tool [here](https://victorchang.codes/separating-iphone-media-types) talking about how it works.

When backing up your media from an iOS device, you can bulk copy all of the files into a single folder and then use this tool to separate the different types into separate folders.

Example command:
```
process.py --source "/path/to/all/media/from/iphone" --photo_dest "/path/to/only/photos" --video_dest "/path/to/only/videos" --stray_dest "/path/for/misc/stuff"
```

The video files associated with live photos will be copied to be alongside their photos and are not treated the same as actual videos.

### "Works On My Machine" disclaimer!
I developed this tool based on parsing files from iOS 15 and 16. It is possible other versions of iOS do not include the metadata that this tool depends on to work.

## How to Install
Every platform is different so these instructions are only in general terms.

1. Download the *.py files in the [splitter](https://github.com/nekorevend/iPhone-Media-Splitter/tree/main/splitter) directory.
    - Or install [git](https://git-scm.com/) and `git clone` this repository.
1. Install [ExifTool](https://exiftool.org/).
    - Make sure it's in your PATH environment variable so your command-line is able to run it.
1. Use a [Python virtual environment](https://docs.python.org/3/library/venv.html) with [pip](https://packaging.python.org/en/latest/key_projects/#pip) to set up the dependencies for this tool.

## Known Problems
- Modified files (ex: cropped or marked up images) might not be detected because they can have metadata stripped away.
- Can be slow depending on amount of files. I did not multi-thread this tool yet.
  - FWIW: The initial run will be slow but you can clear out the `--source` directory of the files you have already processed and it won't take very long for incremental runs.

## Future Work
- Support differentiating between your own files and files that were sent to you.