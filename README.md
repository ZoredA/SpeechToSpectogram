# SpeechToSpectogram
Course Project. Records audio, turns into a spectogram and can perform ASR on it as well.

Installation instructions:

Unfortunately, first time installation is a little bit of a hassle. 

## The Easy Way:

-Install [Miniconda](http://conda.pydata.org/miniconda.html) or Anaconda, but mini is smaller and we can add stuff as we need it.
 
 Be sure to select Python 3.5 64bit installer. During the installation make sure to let it add conda to your path (should be checked by default).
 
-Create an environment:
`conda create -n py3k python`

It will ask you if you are okay with installing a few things. Type in y.

-Activate the environment:
`activate py3k`

-Install numpy
`conda install numpy`

-Install matplotlib
`conda install matplotlib`

-Install pyaudio
`pip install pyaudio`

-Install Speech Recognition library.
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
