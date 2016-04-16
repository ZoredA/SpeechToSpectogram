# SpeechToSpectogram
Course Project. Records audio, turns into a spectogram and can perform ASR on it as well.

# Installation

Unfortunately, first time installation is a little bit of a hassle. 

## The Easy Way:

-Install [Miniconda](http://conda.pydata.org/miniconda.html) or Anaconda, but mini is smaller and we can add stuff as we need it.
 
 Be sure to select Python 3.5 64bit installer. During the installation make sure to let it add conda to your path (should be checked by default).
 
Open up a windows command line, and create an environment:

`conda create -n py3k python`

It will ask you if you are okay with installing a few things. Type in y.

Activate the environment:

`activate py3k`

Install numpy

`conda install numpy`

Install matplotlib

`conda install matplotlib`

Install pyaudio

`pip install pyaudio`

Install Speech Recognition library.

`pip install SpeechRecognition`

Now simply navigate to whereever you downloaded SpeechToSpectagram (either the Zip from github or a git clone) and type:
`python main.py`

## The harder way

-Install Python 3.4+ (Can be found here: https://www.python.org/downloads/)

-Install pyaudio, numpy, matplotlib and [speech recognition](https://pypi.python.org/pypi/SpeechRecognition/)

Commands to do so:

 `pip install pyaudio`
 
 `pip install SpeechRecognition`
 
 pip does not work so well for numpy and possibly Matplotlib as well. You can try (this probably works on Linux):
 
 `pip install numpy`
 
 `pip install matplotlib`
 
 but at least for numpy, you'll probably have to work a bit harder. The [website](http://docs.scipy.org/doc/numpy-1.10.1/user/install.html) has a few instructions. [SourceForge](https://sourceforge.net/projects/numpy/files/NumPy/1.10.2/) has an older version with an installer, but I couldn't get the installer to work. You might have better luck if your Python install is properly present in the Windows registry.

Then, download the zip or git clone, extract it. Go into the directory and `python main.py`


# Usage

`python main.py` should open up the main settings window. 

![main window](http://imgur.com/b446vDX.jpg)

This window lets you tune the basic parameters of the spectogram as well as decide on what you wish to show. If you haven't run the program before, you need to create a recording. Press the record button to record some audio. While the button is depressed, your microphone is on and recording. The duration of the recording is determined by the recording length input.

After the button returns to normal, you can press the Generate button to create plots. These plots are made from a wav file called output.wav in the tmp directory. 

Note: Reference for the spectogram colormaps can be found [here](http://matplotlib.org/examples/color/colormaps_reference.html). At this point in time, revese color maps are not supported.

If you check the Use ASR button, the program will pass the audio recording to a speech recognition service (currently only supports Google) and display the result below the spectogram. Note that this is a slightly time consuming network call, so the program will hang for a few seconds while it completes. 

![specto window](http://imgur.com/gCCpIFA.jpg)

Note that more than one possibility is displayed (mostly for educational reasons really) and a confidence threshold, as determined by the speech recognization service is also shown. When the confidence value is low, the number is not displayed because the service doesn't send one. 

If you select Create freq grid, a 3x3 grid of 9 plots showing the frequency spectrum at different time intervals will also be displayed. Note that the y-axis is 10 log of the amplitude, i.e. it is traditional decibels (and not the EE 20log). The maximum frequency of each of the plots in the grid is determined by the Max Freq parameter (this also controls the max Y-axis frequency of the spectogram).

![freq grid](http://imgur.com/JvSiWXz.jpg)

If you select Create time grid, a 3x3 grid of 9 plots showing time vs amplitude (raw signal, not log) will be displayed.

![time grid](http://imgur.com/XCWU5Uh.jpg)

Each plot comes with a fair few Matplotlib controls in the bottom left corner. You can use these to zoom in and adjust the plots a little to your liking.

Pressing the Close button on the original window will close all the plots.
