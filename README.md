# Website Checker

The Website Checker is a Python script designed for monitoring the status of websites and sending notifications via Telegram.

## Overview

The Website Checker is a custom Python script developed for private use. It monitors a list of specified websites, checks their availability, performs DNS lookups, and reports the results to a designated Telegram group using a Telegram bot.

## Features

- Monitors the availability of private websites.
- Checks Facebook API for website blocking detection.
- Performs DNS lookups for A and CNAME records.
- Sends status updates to a private Telegram group.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/svanir233/website-checker.git
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Rename `config_example.json` to `config.json`.
2. Open `config.json` and provide the required information:
   - Telegram API Token.
   - Telegram Chat ID.
   - Facebook API Access Token.
   - List of Websites to Monitor.
   - Monitoring Interval.

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```

2. The script will start monitoring the specified websites and send status updates to the designated Telegram group.

## Contributing

As a private project, contributions are not expected. This project is solely for personal use.

## License

This is a private project and not open source. All rights reserved.