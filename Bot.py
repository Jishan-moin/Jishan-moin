import datetime
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Telegram bot token
TOKEN = "<5881618733:AAFf0FseiFxEfqKPj3d0y0SZ_Vo-hyDUu_g>"

# Function to handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! How can I assist you today?")

# Function to handle incoming messages
def receive_message(update, context):
    message = update.message.text.lower()
    
  # Check for specific keywords or commands
    
  if "weather" in message:
        response = get_weather()
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        
   elif "news" in message:
        response = get_news()
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        
  elif "translate" in message:
        query = message.replace("translate ", "")
        response = translate_text(query)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        
  elif "remind me" in message:
        time = message.replace("remind me ", "")
        set_reminder(time, update, context)
        
   # Add more cases for other tasks
    
   else:
      context.bot.send_message(chat_id=update.effective_chat.id, text="I'm sorry, I couldn't understand your request.")

# Function to get current weather conditions
def get_weather():
    # Make a request to a weather API (e.g., OpenWeatherMap) and extract the data
    # Replace <api_key> with your actual API key
    api_key = "<your_api_key>"
    url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}"
    response = requests.get(url).json()
        # Extract relevant information (e.g., temperature, description) from the response
    temperature = response["main"]["temp"]
    description = response["weather"][0]["description"]
    
  # Format and return the weather information
  return f"The current temperature in London is {temperature}°C with {description}."

# Function to get latest news headlines
def get_news():
    # Make a request to a news API (e.g., NewsAPI) and extract the data
    # Replace <api_key> with your actual API key
    api_key = "<your_api_key>"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url).json()
        # Extract relevant information (e.g., headlines) from the response
    headlines = [article["for article in response["articles"][:5]]
        # Format and return the news headlines
    return "n".join(headlines)

# Function to translate text
def translate_text(query):
    # Make a request to a translation API (e.g., Google Translate) and extract the translated text
    # Replace <api_key> with your actual API key
    api_key = "<your_api_key>"
    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}&q={query}&target=en"
    response = requests.get(url).json()
    
  # Extract the translated text from the response    translation = response["data"]["translations"][0]["translatedText"]     
  # Return the translated text
   return f"The translation of "{query}" is "{translation}"."

# Function to set a reminder
def set_reminder(time, update, context):
    # Extract the reminder time from the message
    reminder_time = datetime.datetime.strptime(time, "%H:%M")
    
   # Calculate the time difference between the current time and the reminder time
  current_time = datetime.datetime.now().time()
  time_difference = datetime.datetime.combine(datetime.date.today(), reminder_time) - datetime.datetime.combine(datetime.date.today(), current_time)
    
  # Schedule a job to send a reminder message at the specified time
  context.job_queue.run_once(send_reminder, time_difference.seconds, context=update.effective_chat.id)
    
  context.bot.send_message(chat_id=update.effective_chat.id, text=f"Reminder set for {time}.")
    
# Function to send a reminder message
def send_reminder(context):
    chat_id = context.job.context
    context.bot.send_message(chat_id=chat_id, text="Reminder: Don't forget to do the task!")

# Set up the bot
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Add command handlers
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Add message handler
message_handler = MessageHandler(Filters.text & ~Filters.command, receive_message)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()
