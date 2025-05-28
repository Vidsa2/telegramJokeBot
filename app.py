import os
import re # regular expressions for input validation
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes,filters,MessageHandler

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

def setup_llm_chain(topic= "technology"):
    """
    Set up the LLM chain with the given topic.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a joke generating assistant. Generate only ONE joke on the given topic and do NOT continue any conversation include any introductions, explanations, or additional jokes."),
        ("user", "topic: {topic}")
    ])

    llm = ChatGroq(
        model="Gemma2-9b-It",
        api_key=os.getenv("GROQ_API_KEY"),
    )

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    return chain

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    """
    Handle the /start command.
    """
    await update.message.reply_text("Welcome to the Joke Bot! Send me a topic and I'll generate a joke for you.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /help command.
    """
    await update.message.reply_text("Send me a topic and I'll generate a joke for you. For example, @King_of_joke_bot Topic")

async def generate_joke(update: Update, context: ContextTypes.DEFAULT_TYPE,topic: str):
    """
    Handle the /joke command.
    """
    await update.message.reply_text(f"generating a joke about {topic} ")
    joke = setup_llm_chain(topic).invoke({"topic": topic}).strip()

    await update.message.reply_text(joke)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle incoming messages.
    """
    text = update.message.text
    bot_username = context.bot.username
    if f'@{bot_username}' in text:
        match = re.search(f'@{bot_username}\\s+(.*)', text)
        if match and match.group(1).strip():
            await generate_joke(update, context, match.group(1).strip())
        else:
            await update.message.reply_text("Please provide a topic after mentioning me, like this:{bot_username} topic")

def main():
    """
    Start the bot.
    """
    token = os.getenv("TELEGRAM_API_KEY")
    app= Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler( filters.TEXT & ~filters.COMMAND,handle_message))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()