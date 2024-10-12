# Pull Request Template Selector

This is chrome extension that will automatically select the required template for a given pull request.

This extension works by filtering the url when creating a pull request (eg. `https://github.com/golfgenius/golfgenius/compare/feature/test_pr_template4?expand=1`) and checks what type of branch this is.
This depends on the name of the branch. If it starts with:
- `hotfix` => `hotfix.md`
- `feature` => `feature.md`
- `release` => `release.md`
- `feature/develop_*` => `streamdevelop.md`

Then it checks if the `template` pare is set and if not it will append to the url the template param with the corresponding template type and reload.



# How to install

1. Download the extension zip from google drive: [Golf Genius Drive](https://drive.google.com/file/d/1BXzQIqbi9KGTjog0rSTrXtEZYT9Av5mU/view?usp=sharing)

2. Unzip the archive

3. Open **Google Chrome** and navigate to `chrome://extensions/`

4. Check `Developer mode` in the top right corner.

5. Click `Load Unpacked` and navigate to the folder you extracted the extension to.

At the end it should look something like this:


# Why custom extension

This type of extensions requires permissions that are outside the comfort zone and can run much more code on the site, so we opted to make our own to avoid any issues.

# Technical Details

This is a Google Chrome extension using the V3 Manifest.

The code that runs the initial setup is in `background.js`. To make this take effect on other sites the url includes check (`url.includes('github.com/golfgenius/golfgenius/compare')`). heeds to have an `||` condition with other repository names.

The code that changes the template param is in `content_scripts/template_selector.js`.