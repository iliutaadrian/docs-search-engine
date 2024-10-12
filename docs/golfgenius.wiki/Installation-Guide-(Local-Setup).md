This guide will help you install the Golf Genius Tournament Management app. It is part of the [Onboarding Checklist](https://github.com/golfgenius/golfgenius/wiki/Onboarding-Checklist) for new TM developers.

## 1. For Macs with M1 processors
### 1.1 Install Rosetta
```
/usr/sbin/softwareupdate --install-rosetta --agree-to-license
```
### 1.2 Run the terminal with Rosetta
I. Close all running instances of the terminal

II. Go to **Finder > Applications > Utilities**
<details>
  <summary>Click for screenshot</summary>
<img width="1728" alt="Screenshot 2022-06-28 at 10 21 48" src="https://user-images.githubusercontent.com/42933088/176120239-50c08f57-051b-4de6-888f-7b62b6b22cd6.png">
</details>

III. Right-click Terminal > Get Info
<details>
  <summary>Click for screenshot</summary>
<img width="982" alt="Screenshot 2022-06-28 at 10 26 15" src="https://user-images.githubusercontent.com/42933088/176120290-4f597c51-3d9c-4995-9ca1-7e54f1554057.png">
</details>

IV. Check _Open using Rosetta_
<details>
  <summary>Click for screenshot</summary>
<img width="274" alt="Screenshot 2022-06-28 at 10 26 31" src="https://user-images.githubusercontent.com/42933088/176120310-333eb703-ca72-4d98-a979-371838d7196d.png">
</details>

## 2. Install Apple Developer Tools
This installs **git** among other necessary tools:
```
xcode-select --install
```

## 3. Add an ssh key
### 3.1 Generate an ssh key
```
ssh-keygen
```

### 3.2 Copy the key
```
cat ~/.ssh/id_ed25519.pub | pbcopy
```

### 3.3 Add ssh key to GitHub

I. Go to **Settings** on GitHub

II. Click **SSH and GPG keys**

III. Click **New SSH key**

IV. Paste the key and give it a title, then click **Add SSH key**

**Warning:**
While GitHub usually immediately recognizes the new key, in some rare cases, it can take up to 2 hours. So if you get an error while trying to clone the repository, give it a few minutes and try again.

## 4. Install
### 4.1 Prerequisites
I. Clone the repository
```
git clone git@github.com:golfgenius/golfgenius.git
```

II. Request AWS keys from your manager

III. Once you have the AWS keys run the script from the project folder `./golf_genius_setup` and follow the instructions below.

**Warning:**
Replace the keys below with your respective AWS KEYS

### 4.2 (Re)Install and config all required programs:
```
./golf_genius_setup -p AWS_KEY_ID="XXXXXXXXXXXXXXXXXXXX" AWS_SECRET_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

**Warning:**
In some cases, not all packages are detected after this step. To be sure, close the terminal, open a new one, and go to the project's root folder to ensure there are no issues with the following steps.

**Warning:**
Sometimes, after running the script, it might stop after installing `oh-my-zsh`. Just rerun this step.

### 4.3 (Re)Create required config files
```
./golf_genius_setup -c AWS_KEY_ID="XXXXXXXXXXXXXXXXXXXX" AWS_SECRET_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

### 4.4 (Re)Install all ruby gems and js packages
```
./golf_genius_setup -d
```

### 4.5 (Re)Create the DB structure and restore the backups needed locally
```
./golf_genius_setup -D
```
