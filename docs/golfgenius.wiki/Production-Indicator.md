# Production indicator

This is chrome extension that will add a banner to the top of [golfgenius](https://www.golfgenius.com/) production environment.

This is meant to give a visual indication that you are in production as to help reduce the possibility of taking certain actions that are not meant to be taken on production.

<img width="1726" alt="Screenshot 2022-11-10 at 16 30 10" src="https://user-images.githubusercontent.com/42933088/201118291-5800697a-f4cb-4631-9177-07f90ca70d70.png">


# How to install

1. Download the extension zip from google drive: [Golf Genius Drive](https://drive.google.com/file/d/1UohK5k7N1fSGIhnNstRcohXgzEqMF46r/view?usp=share_link)

2. Unzip the archive

3. Open **Google Chrome** and navigate to `chrome://extensions/`

4. Check `Developer mode` in the top right corner.

5. Click `Load Unpacked` and navigate to the folder you extracted the extension to.

At the end it should look something like this:
<img width="1708" alt="Screenshot 2022-11-10 at 16 29 17" src="https://user-images.githubusercontent.com/42933088/201118143-18108f00-a7c0-4c72-ac15-cfe04dc8d16d.png">

# Why custom extension

This type of extensions requires permissions that are outside the comfort zone and can run much more code on the site, so we opted to make our own to avoid any issues.

# Technical Details

This is a Google Chrome extension using the V3 Manifest.

The code that runs the initial setup is in `background.js`. To make this take effect on other sites (like other production environments from other products we have) change `let urls = ["www.golfgenius.com"]` to include the desired urls.

The code that adds the banner is in `content_scripts/banner.js`.