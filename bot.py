import random
import re
import threading
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from textblob import TextBlob

# ======= RANDOM RESPONSES ======= #
jokes = [
    "Ek macchar aadmi ko hijda bana deta hai!",
    "Pati: Tum mujhse kitna pyaar karti ho?\nPatni: Shah Jahan jitna!\nPati: Matlab meri bhi kabar banayegi?",
    "Life mein do cheezen kabhi underestimate mat karna: Chhoti pencil aur chhota baccha. Dono chhoti baat nahi maante!"
]

shayari = [
    "Aankhon mein jo neer hai, woh pyaar ki tasveer hai.",
    "Mohabbat bhi ajeeb cheez hai, jis se hoti hai usko pata hi nahi chalta!",
    "Dil to karta hai tere saath jee loon, par fir sochta hoon, kahin tu bhi change na ho jaaye!"
]

weird_facts = [
    "Agar aap chuhe ko gira den to wo super slow motion mein girta hai!",
    "Ek insan apni zindagi ka 6 mahine sirf traffic lights dekhne mein guzar deta hai!",
    "Octopus ke 3 dil hote hain, aur jab wo so raha hota hai to rang badalta hai!"
]

dares = [
    "Apni maa ko call karo aur bina wajah 'I love you' bolo! 😆",
    "1 minute ke liye aankhein band karke sochna, duniya kaisi hoti bina tumhare! 😜",
    "Jo pehle online aaye, usko bina wajah 10 baar 'Hi' bhejo! 😂"
]

roasts = [
    "Tujhse acha toh mera WiFi ka signal hai, kam se kam kabhi kabhi full hota hai!",
    "Teri akal bhi Windows XP jaisi hai, outdated aur slow!",
    "Tujhse zyada toh Google fast reply deta hai!",
    "Teri baatein itni boring hain, ki mera phone bhi vibrate karna bandh kar deta hai!"
]

# Store last activity time for each chat
last_activity = {}

# ======= SMART RESPONSE FUNCTION ======= #
def get_smart_response(message):
    message = message.lower()
    
    if re.search(r'joke|funny|hasi', message):
        return random.choice(jokes)
    elif re.search(r'shayari|poetry|love', message):
        return random.choice(shayari)
    elif re.search(r'fact|weird|interesting', message):
        return random.choice(weird_facts)
    elif re.search(r'dare|challenge', message):
        return random.choice(dares)
    elif re.search(r'roast|insult|taunt', message):
        return random.choice(roasts)
    else:
        analysis = TextBlob(message)
        sentiment = analysis.sentiment.polarity
        if sentiment > 0:
            return "Lagta hai tum mood mein ho! Mazedaar baat suno: " + random.choice(jokes)
        elif sentiment < 0:
            return "Arey dukh mat kar yaar, ek mast joke suno: " + random.choice(jokes)
        else:
            return "Yeh toh ajeeb baat hai! Suno ek weird fact: " + random.choice(weird_facts)

# ======= IDLE CHECK FUNCTION ======= #
def check_idle(updater: Updater):
    while True:
        time.sleep(600)  # 10 minutes
        for chat_id, last_time in list(last_activity.items()):
            if time.time() - last_time >= 600:
                updater.bot.send_message(chat_id, "10 minute ho gaye, sab chup kyun hain? Suno ek mazedaar baat: " + random.choice(jokes))
                last_activity[chat_id] = time.time()

# ======= BOT FUNCTIONS ======= #
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Ajeeb Bot Online hai! Mujhe koi bhi message bhejo aur main kuch ajeeb bataunga! 😜")

def respond(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chat_id = update.message.chat_id
    
    # Update last activity time
    last_activity[chat_id] = time.time()
    
    reply = get_smart_response(user_message)
    update.message.reply_text(reply)

# ======= MAIN BOT CODE ======= #
TOKEN = "7810505308:AAGr-fIzBSy-WXYuCZlH-fvGbCdDhRtuRLI"

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))
    
    # Start idle checker thread
    idle_thread = threading.Thread(target=check_idle, args=(updater,), daemon=True)
    idle_thread.start()
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
