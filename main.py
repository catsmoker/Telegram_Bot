import json
import telebot
from telebot import types, util
from decouple import config
from translate import Translator as TranslateTranslator  # Assuming you want to use this library
from googletrans import Translator as GoogleTranslator  # Renaming to avoid conflicts
from weather import getCurrentWeather

BOT_TOKEN = config("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

weather_keywords = ["weather", "temp", "temperature"]
greetings = ["hello", "hi", "hey"]
whoAreYou = ["who", "what"]
botName = "my bot name"

bot_data = {
    "name": ["my bot name"]
}

text_messages = {
    "welcome": "Welcome to xxxx Telegram group",
    "welcomeNewMember": "Hey, {name}, welcome to our private group",
    "sayingGoodbye": "The member {name} left the group",
    "leave": "I have been added to a group other than the group I was designed for, bye🧐",
    "call": "How can I help? 😀",
    "warn": "❌ {name}, you have used one of the forbidden words ❌\n"
            "🔴 You have {safeCounter} chances left. If exceeded, you will be expelled 🔴",
    "kicked": "👮‍♂️⚠ The member {name}, ID owner {username}, has been kicked out for violating one of the group rules 👮‍♂️⚠"
}

commands = {
    "translate": ["translate"]
}

def handleNewUserData(message):
    id = str(message.new_chat_member.user.id)
    name = message.new_chat_member.user.first_name
    username = message.new_chat_member.user.username

    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)

    users = data.get("users", {})
    if id not in users:
        print("New user detected!")
        users[id] = {"safeCounter": 5, "username": username, "name": name}
        print("New user data saved!")

    data["users"] = users
    with open("data.json", "w") as editedFile:
        json.dump(data, editedFile, indent=3)

def handleOffensiveMessage(message):
    id = str(message.from_user.id)
    name = message.from_user.first_name
    username = message.from_user.username

    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)

    users = data.get("users", {})
    if id not in users:
        print("New user detected!")
        users[id] = {"safeCounter": 5, "username": username, "name": name}
        print("New user data saved!")

    users[id]["safeCounter"] -= 1
    safeCounterFromJson = users[id]["safeCounter"]
    if safeCounterFromJson == 0:
        bot.kick_chat_member(message.chat.id, id)
        users.pop(id)
        bot.send_message(message.chat.id, text_messages["kicked"].format(name=name, username=username))
    else:
        bot.send_message(message.chat.id, text_messages["warn"].format(name=name, safeCounter=safeCounterFromJson))

    data["users"] = users
    with open("data.json", "w") as editedFile:
        json.dump(data, editedFile, indent=3)

    return bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(commands=["start"])
def startBot(message):
    bot.send_message(message.chat.id, text_messages["welcome"])

def is_msg(message):
    return True

@bot.message_handler(func=is_msg)
def reply(message):
    words = message.text.split()
    first_word = words[0].lower()
    
    if first_word in weather_keywords:
        report = getCurrentWeather()
        bot.send_message(message.chat.id, report or "Failed to get weather!!")
    elif first_word in whoAreYou:
        bot.reply_to(message, f"I am {botName}")
    elif first_word in greetings:
        bot.reply_to(message, "Hey, how's it going!")
    elif first_word in bot_data["name"]:
        bot.reply_to(message, text_messages["call"])
    elif first_word in commands["translate"]:
        translator = GoogleTranslator()
        translation = translator.translate(" ".join(words[1:]), dest="ar")
        bot.reply_to(message, translation.text)
    else:
        bot.reply_to(message, "That's not a command of mine!")

@bot.chat_member_handler()
def handleUserUpdates(message: types.ChatMemberUpdated):
    newResponse = message.new_chat_member
    if newResponse.status == "member":
        handleNewUserData(message)
        bot.send_message(message.chat.id, text_messages["welcomeNewMember"].format(name=newResponse.user.first_name))
    elif newResponse.status == "left":
        bot.send_message(message.chat.id, text_messages["sayingGoodbye"].format(name=newResponse.user.first_name))

@bot.my_chat_member_handler()
def leave(message: types.ChatMemberUpdated):
    update = message.new_chat_member
    if update.status == "member":
        bot.send_message(message.chat.id, text_messages["leave"])
        bot.leave_chat(message.chat.id)

bot.infinity_polling(allowed_updates=util.update_types)
