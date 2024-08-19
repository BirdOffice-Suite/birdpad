# birdpad
A minimalist but good-looking text editor for Windows and macOS.

I created this project while on the search for a text editor that felt native to my machine.

WordPad and Notepad served very well for a while, but with Windows 11, WordPad was deprecated and Notepad started looking like a generic web app, so I had to continue looking.

Then, I remembered BirdPad, an old hobby project I'd made privately a few months prior.

I improved the UI and added functionality, and BirdPad as we know it today was born.

Now, I've added support for macOS, and I've improved window resizing greatly.

# Requirements
- Either an x86_64 Windows PC or a Mac with macOS and Apple Silicon
- ~10 megabytes of unused space

# Installation
Open the Releases tab, and download the latest build for your device.

BirdPad is portable, but on macOS you can always drag it to your Applications folder.

# Building from source
To build BirdPad from source, first install the latest version of Python 3. BirdPad is built on Python 3.12, so we recommend using 3.12 for the best experience.

Then, download a buildkit from the Releases tab. The buildkit will work on either Windows or macOS as long as Python is in your PATH (`python` for Windows, `python3` for macOS).

To build from source, extract the buildkit and run your operating system's respective build script (`build-birdpad.bat` for Windows, `sudo bash ./build-birdpad.sh` for macOS).

The build script will install/update all required modules (`pyinstaller`, `tkmacosx`, and `pillow`) and produce an executable file in the `dist` folder.
