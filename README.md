# audfprint-cut-ads-from-echo-msk
Cut ads from Echo-Msk radio shows using ad fingerprints.

# Requirements
ffmpeg

    apt install -y ffmpeg (on Linux) or brew install ffmpeg (on Mac OS)
pip  

    apt install -y pip (on Linux) or brew install pip (on Mac OS)


# Installation
    pip install virtualenv
    git clone https://github.com/GeorgeFedoseev/audfprint-cut-ads-from-echo-msk
    cd audfprint-cut-ads-from-echo-msk
    pip virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

# Usage
## Add ad examples
Just put ad examples to `echo-msk-data/ad_examples` folder  
To update fingerprints db: **remove cache** folder `processing_tmp`
## Cut ads from files in folder
    python cut_ads_echo.py ~/Desktop/echo-test/ ~/Desktop/echo-test/no_ads
## Cut ads in single file
    python cut_ads_echo.py ~/Desktop/echo-test/with_ads.mp3 ~/Desktop/echo-test/without_ads.mp3
