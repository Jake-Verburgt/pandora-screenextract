# pandora-screenextract
Extract Pandora Liked Songs from Screenshots!


## Introduction
If you have liked songs in your Pandora account that you would like to have records of, or would like to transfer to Spotify, you'll find that there aren't a whole lot of working options:

* The Pandora API is no longer accepting new access requests (https://developer.pandora.com/partners/join/)
* All existing solutions that use the API are no longer functional
* The Pandora website doesn't list more that ~260 songs, so you can't extract all songs by parsing from the HTML
    * No javascript seems to be further populating liked songs either

Seemingly, the only place that *all* liked songs are even available are on the Android/IOS app, which doesn't allow any kind of text exporting.

I'm a problem solver, and very determined to get all of my liked songs off of the Pandora platform by any means necessary. Using a series of screensots from your liked songs on the Pandora mobile app, this code allows you to extract the relevant data and import into spotify using a series of computer-vision tools, optical character recognition, and web requests.

This may be a messy solution, but it *is* a solution, and a solution that only needs to work once. I've cleaned up the code quite a bit, but I understand that you'll likely have to tweak the code slightly to make it work properly for your use case, so I've placed the pipeline in an ipython notebook so you can tweak it interactively.

## Dependencies
### Python libraries:
* pandas: ```conda install -c anaconda pandas```
* numpy: ```conda install -c anaconda numpy ```
* requests: ```conda install -c anaconda requests```
* ipykernel: ```conda install ipykernel```
* opencv: ```conda install -c conda-forge opencv```
* thefuzz: ```conda install -c conda-forge thefuzz```

#### With the conda environment manager:
1) Install from file with ```conda env create -f pandora-screenextract.yml```
2) Activate with ```conda activate pandora-screenextract```

### External Programs & Accounts
* tesseract (ubuntu/debian): ```sudo apt install tesseract-ocr```
* Spotify Account

#### Set paths
 * open ```params.json``` and fill in the relevant fields

## How to Run
1) Activate the environment 
2) Go through the ```main.ipynb``` notebook cell by cell. This process is likely to need a fair amount of tweaking and should be done interactively.