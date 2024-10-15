
<p align="center">
  <a href="https://github.com/TechShreyash/AniDL">
    <img src="https://socialify.git.ci/TechShreyash/AniDL/image?description=1&font=Source%20Code%20Pro&forks=1&issues=1&pattern=Charlie%20Brown&pulls=1&stargazers=1&theme=Dark" alt="AniDL" width="640" height="320" />
  </a>
</p>

<h1 align="center">AniDL</h1>
<h3 align="center">A Lightweight Anime Downloader Built with Python and Powered by TechZApi</h3>

AniDL is a simple yet powerful anime downloader built in Python. It offers fast downloads with support for batch and parallel downloading, making it an ideal tool for anime enthusiasts who want to download multiple episodes efficiently.

## Features

- **Batch Downloader Support**: Download multiple episodes in one go.
- **Fast Download Speed**: Optimized for faster downloads.
- **Parallel Downloading**: Download multiple episodes simultaneously for quicker completion.

## Installation

### 1. Install Requirements

To get started, first install the required dependencies:

```bash
pip install -U -r requirements.txt
```

### 2. Install [ffmpeg](https://ffmpeg.org/)

`ffmpeg` is required for video processing. 

- **For Windows users**: Make sure to add `ffmpeg` to your system PATH. 
  You can download it from [this link](https://drive.google.com/file/d/1jaE4SFombXVXvLsaRtU0siQFTF7F3hL0/view?usp=sharing).

### 3. Deploy Your Own Instance of AnimeDexApi

AniDL uses the [AnimeDexApi](https://github.com/TechShreyash/AnimeDexApi) for fetching anime details and episodes. You will need to deploy your own instance of this API using **Cloudflare Workers** (it's free!).

- After deploying, retrieve the API URL of your instance.
- Then, update the API URL in the following file:

  [`Utils/TechZApi.py`](https://github.com/TechShreyash/AniDL/blob/4b95f19efb99c0199e8540bad6a1a149ea5ea396/Utils/TechZApi.py#L6)

## Usage

Once everything is set up, you can start downloading anime episodes using AniDL.

### 1. Start AniDL

```bash
python AniDL.py
```

### 2. Enter Anime Details

- **Anime Name**: Enter the name of the anime.
- **Episodes to Download**:
  - To download a single episode, enter the episode number (e.g., `3`).
  - To download a range of episodes, enter the range (e.g., `2-7`).
  - To download all available episodes, enter `*`.

### 3. Wait for the Download

All downloaded episodes will be saved in the `Downloads` folder.

## Powered by TechZApi

AniDL is powered by **TechZApi**, ensuring smooth and fast access to anime episodes.

## Support and Updates

For the latest updates and support, join our community on Telegram:

<p align="center">
  <a href="https://telegram.me/TechZBots">
    <img src="https://img.shields.io/static/v1?label=Join&message=Telegram%20Channel&color=blueviolet&style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Channel" />
  </a>
  <a href="https://telegram.me/TechZBots_Support">
    <img src="https://img.shields.io/static/v1?label=Join&message=Telegram%20Group&color=blueviolet&style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Group" />
  </a>
</p>
