# **MOA Task Controller (OTF)**

- Written by: **Travis M. Moore**
- Latest version: **Version 0.2.1**
- Originally created: **May 25, 2023**
- Last edited: **July 24, 2023**
<br>
<br>

---

## Description
This application provides a set of arrow controls useful for measuring participant perception using the method of adjustment. NOTE: the application <strong>DOES NOT</strong> use an adaptive staircase procedure. The Session dialog provides several customizations to create trains of stimuli using a single, brief, imported .wav file. 

"OTF" in the title stands for "on the fly", in reference to the application's ability to create novel stimuli based on a single instance from a provided .wav file.

If you have a series of .wav files (i.e., you do not want to use the application to create stimuli), please use the regular version of the MOA Task Controller that expects a .wav file for each stimulus.
<br>
<br>

---

## Getting Started

### Dependencies

- Windows 10 or greater (not compatible with Mac OS)

### Installing

- This is a compiled app; the executable file is stored on Starfile at: \\starfile\Public\Temp\MooreT\Custom Software
- Simply copy the executable file and paste to a location on the local machine

### First Use
- Double-click to start the application for the first time.
<br>
<br>

---

## Compiling from Source
```
pyinstaller --noconfirm --onefile --console --add-data "C:/Users/MooTra/Code/Python/moa_task_fly/assets/cal_stim.wav;." --add-data "C:/Users/MooTra/Code/Python/moa_task_fly/assets/README;README/" --add-data "C:/Users/MooTra/Code/Python/moa_task_fly/assets/images;images/"  "C:/Users/MooTra/Code/Python/moa_task_fly/controller.py"
```
<br>
<br>

---

## Contact
Please use the contact information below to submit bug reports, feature requests and any other feedback.

- Travis M. Moore: travis_moore@starkey.com
