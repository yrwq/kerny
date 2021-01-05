## Introduction

[![forthebadge-made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![PR's welcome](https://img.shields.io/badge/PRs-welcome-purple.svg?style=for-the-badge)](https://makepullrequest.com)

Kerny is just another Discord bot ... Written in python, for your shitty discord server!

## Features

- [x] Set a fetch(like neofetch but with a file hosting)
- [x] Clear your fetch
- [x] Show your or another user's fetch
- [x] Get a random wallpaper from [unsplash](https://unsplash.com)

## Usage

- Setting up
-
    1. If you don't already have one, create a new [Discord Application](https://discord.com/developers/applications)

    2. Clone this repository

    ```bash
    git clone https://github.com/yrwq/kerny
    ```

    3. Set your bot's token as an environment variable (Optional, see 4. if you skip)

    - Bash
    ```bash
    echo 'export DISCORD_TOKEN="yourtoken"' >> ~/.bashrc
    ```

    - Zsh
    ```zsh
    echo 'export DISCORD_TOKEN="yourtoken"' >> ~/.zshrc
    ```

    4. Install python dependencies

    ```bash
    pip install -r requirements.txt
    ```

    5. Edit `bot.py` to match your token

    - Remove the uncommented line that starts with TOKEN_AUTH

    - Uncomment the line that starts with TOKEN_AUTH and paste your token between ""

## Contributing

Any contributions are very welcome, and feel free to make issues, i can't fix things i don't know about!
