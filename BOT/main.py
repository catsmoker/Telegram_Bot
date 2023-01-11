import json
import telebot
from telebot import types,util
from decouple import config
from googletrans import Translator
import telebot
from decouple import config
from weather import getCurrentWeather

BOT_TOKEN = config("BOT_TOKEN")
bot= telebot.TeleBot(BOT_TOKEN)

#main commands and bot creation

weather = ["weather","temp","temprature"]
greetings = ["hello","hi","hey"]
whoAreYou = ["who","what"]
botName = "WAGNIMN"

bot_data={
    "name" : ["WAGNIMN","Wagnimn","wagnimn"]
}

text_messages = {
    "welcome": "welcome to WAGNIMN Bot",
    "welcome_new_member" : "Welcome {name} to our group",
    "saying_goodbye": "User {name} has left the group",
    "leave":"You've been added to a different group, Goodbye",
    "call" : "How can I help you?",
    "warn": u"{name} has used a forbidden word ****"
            u"You have {safeCounter} more chance(s) left before you get kicked",
    "kicked": u"User {name} (username: {username}) has been kicked for breaking group rules"
}

text_list={
    "offensive":["cat","puppy"]
}

commands = {
    "translate":["translate"]
}
def handleNewUserData(message):
    id = str(message.new_chat_member.user.id)
    name = message.new_chat_member.user.first_name
    username =  message.new_chat_member.user.username

    with open("data.json","r") as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    
    users = data["users"]
    if id not in users:
        print("new user detected !")
        users[id] = {"safeCounter":5}
        users[id]["username"] = username
        users[id]["name"] = name
        print("new user data saved !")

    data["users"] = users
    with open("data.json","w") as editedFile:
        json.dump(data,editedFile,indent=3)
    editedFile.close()
def handleOffensiveMessage(message):
    id = str(message.from_user.id)
    name = message.from_user.first_name
    username =  message.from_user.username
    
    with open("data.json","r") as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    
    users = data["users"]
    if id not in users:
        print("new user detected !")
        users[id] = {"safeCounter":5}
        users[id]["username"] = username
        users[id]["name"] = name
        print("new user data saved !")

    for index in users:
        if index == id :
            print("guilty user founded !")
            users[id]["safeCounter"] -= 1

    safeCounterFromJson = users[id]["safeCounter"]
    if safeCounterFromJson == 0:
        bot.kick_chat_member(message.chat.id,id)
        users.pop(id)
        bot.send_message(message.chat.id,text_messages["kicked"].format(name=name , username = username))
    else:
        bot.send_message(message.chat.id,text_messages["warn"].format(name=name , safeCounter = safeCounterFromJson))

    data["users"] = users
    with open("data.json","w") as editedFile:
        json.dump(data,editedFile,indent=3)
    editedFile.close()

    return bot.delete_message(message.chat.id,message.message_id)
    
@bot.message_handler(commands=["start"])
def startBot(message):
    bot.send_message(message.chat.id,text_messages["welcome"])

@bot.message_handler(commands=["commands"])
def answer(message):
    bot.send_message(message.chat.id,["/start /help and you can say weather,temp,temprature to get the weather of agadir city also you can say hello,hi,hey,who,what,wagnimn to talk whit the bot and for now im trying to add translation by typing translate,trans,ترجم,ترجملي and more features in the future"])

@bot.message_handler(commands=["help"])
def answer(message):
    bot.send_message(message.chat.id,["talk to the admin"])

#answering every message not just commands 
def isMSg(message):
    return True

@bot.message_handler(func=isMSg)
def reply(message):
    words = message.text.split()
    if words[0].lower() in weather :
        report = getCurrentWeather()
        return bot.send_message(message.chat.id,report or "failed to get weather !!")
    if words[0].lower() in whoAreYou :
        return bot.reply_to(message,f"i am wagnimn bot")
    if words[0].lower() in greetings :
        return bot.reply_to(message,"hey how is going!")

#* adding googletrans api
#* translating word to arabic
#* translating sentence to arabic
    if words[0] in commands["translate"]:
        translator = Translator()
        translation = translator.translate(" ".join(words[1:]),dest="ar")
        bot.reply_to(message,translation.text)
    
    for word in words:
        if word in text_list["offensive"]:
            handleOffensiveMessage(message=message)

#* saying Welcome to joined members
#* saying goodbye to left members
@bot.chat_member_handler()
def handleUserUpdates(message:types.ChatMemberUpdated):
    newResponse = message.new_chat_member
    if newResponse.status == "member":
        handleNewUserData(message=message)
        bot.send_message(message.chat.id,text_messages["welcomeNewMember"].format(name=newResponse.user.first_name))
    if newResponse.status == "left":
        bot.send_message(message.chat.id,text_messages["saying goodbye"].format(name=newResponse.user.first_name))

#* leave anychat thats not mine
@bot.my_chat_member_handler()
def leave(message:types.ChatMemberUpdated):
    update = message.new_chat_member
    if update.status == "member":
        bot.send_message(message.chat.id,text_messages["leave"])
        bot.leave_chat(message.chat.id)

#* listening to group messages
#* respond to bot name
@bot.message_handler(func=lambda m:True)
def reply(message):
    words = message.text.split()
    if words[0] in bot_data["name"]:
        bot.reply_to(message,text_messages["call"])

#* : checking if any word in message is offensive print("offensive")
#* : creating a data json file reading/writing 
#* : saving users info from message (id,name,username)
#* : adding safeCounter data to each user safeCounter = TRIES
#* : kick chat member that break the rules

bot.infinity_polling(allowed_updates=util.update_types)
