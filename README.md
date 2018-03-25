# audfprint-cut-ads-from-echo-msk
Cut ads from Echo-Msk radio shows using ad fingerprints.

# Requirements
ffmpeg  
pip


# Installation
    pip install virtualenv
    git clone https://github.com/GeorgeFedoseev/audfprint-cut-ads-from-echo-msk
    cd audfprint-cut-ads-from-echo-msk
    pip virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

# Usage
## Cut ads from files in folder
    python cut_ads_echo.py ~/Desktop/echo-test/ ~/Desktop/echo-test/no_ads
## Cut ads in single file
    python cut_ads_echo.py ~/Desktop/echo-test/with_ads.mp3 ~/Desktop/echo-test/without_ads.mp3
