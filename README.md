# Telegram Bot

This is a Telegram bot that provides weather updates and other functionalities like greeting new members, translating text, and managing group members. The bot is built using Python and leverages the OpenWeatherMap API for weather updates.

## Features

- **Weather Updates**: Get current weather information for a predefined city.
- **Greetings**: Welcomes new members and says goodbye to members who leave the group.
- **Offensive Message Handling**: Tracks users who send offensive messages and kicks them out after a predefined number of warnings.
- **Translation**: Translates text to Arabic using the Google Translate API.

## Setup and Installation

### Prerequisites

- Python 3.x
- A Telegram bot token from [BotFather](https://core.telegram.org/bots#botfather)
- OpenWeatherMap API key from [OpenWeatherMap](https://home.openweathermap.org/users/sign_up)

### Environment Variables

Create a `.env` file in the root directory of your project and add your Telegram bot token and OpenWeatherMap API key:


### Installation

in env:

BOT_TOKEN=your-telegram-bot-token

WEATHER=your-openweathermap-api-key

1. Clone the repository:
    ```sh
    git clone https://github.com/catsmoker/Telegram_Bot.git
    cd Telegram_Bot
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Bot

Run the bot using:
```sh
python bot.py
