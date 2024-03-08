import logging
import callgpt4  #내가 만든 gpt4호출 모듈
from telegram import __version__ as TG_VER
token = "6314835917:AAEXDiwmq6Ez_WmGe5R0LS47uh1e7v-qz1I"


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
# /start로 대화방을 가동시키는 경우 봇의 첫 메세지
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!, 나는 chatgpt 메신저야",
        reply_markup=ForceReply(selective=True),
    )

#입력된 메세지로,  modgpt4 (gpt4 api를 호출하여 답변을 얻은 모듈) 모듈을 사용
async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """gpt모듈을 호출하는것."""
    print (update.message.text)
    await update.message.reply_text("......") #gpt4 모듈이 응답을 준비하는동한 메세지로 ......을 보냄
    userPrompt = update.message.text
    gptresult = callgpt4.Command(userPrompt)
    await update.message.reply_text(gptresult) #gpt4모듈의 답변을 메세지로 보냄


#위의 함수들을 종합하여 텔레그램에 커맨드와 답변을 처리하는 영역

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram   # /start등 /어쩌고로 지정된 액션을 받아들여, 해당 함수(start)를 호출 동작실행 시키는 커맨드 핸들러
    application.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gpt)) #텔레그램 user messager를 받아 해당 함수(gpt)에 메세지 input을 넣을수 있는 메세지 핸들러

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()