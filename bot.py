import config
import logging

from aiogram import Bot, Dispatcher, executor, types

from filters import IsAdminFilter

logging.basicConfig(level=logging.INFO)


#bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

#activate filters
dp.filters_factory.bind(IsAdminFilter)

# ban command
@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Command was respond to a message")
        return

    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply("Banned fucking slave !!!!")


#remove new user joined message
@dp.message_handler(content_types=["new_chat_member"])
async def on_user_joined(message: types.Message):
    await message.delete()

#echo
@dp.message_handler()
async def echo(message: types.Message):
    if "bad word" in message.text:
        await message.delete()

#run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
