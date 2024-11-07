from pyrogram import * 
from pyrogram.types import *
from khayyam import * 
from pyromod import *
import back

app = Client(
    name="friends-bot",
    api_id="26632071",
    api_hash="a3e2d344b037ce0a9ba676509586244f",
    bot_token="6682503012:AAHCNeczjgM2yMHw5VaygoK78qreOW3zMwI"
)


# ========================= START COMMAND =======================


@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    if not back.user_data_view(message.from_user.id):
        back.user_data_insert(message.from_user.id, message.from_user.first_name)
        await message.reply_text(f"hello {message.from_user.first_name}!")
    elif back.user_data_view(message.from_user.id):
        await message.reply_text(f"You've already started the bot, {message.from_user.first_name}. Perhaps you wanted /add ?")

    else:
        await message.reply_text(f"something went wrong, please contact with the admin.")


@app.on_message(filters.command("add") | filters.regex("Add") | filters.regex("add"))
async def add_friend(client: Client, message: Message):
    fullname = await client.ask(chat_id=message.from_user.id, text="So you wanna add one of your friends? Okay! What's the full name of this fella?")
    nickname = await client.ask(chat_id=message.from_user.id, text=f"Okay! So what do you call {fullname.text}?")
    birthday = await client.ask(chat_id=message.from_user.id, text=f"Great! When is their birthday anyway? \n\n It must be in (YYYY-MM-DD) format!")
    phone = await client.ask(chat_id=message.from_user.id, text=f"Now it's time for their phone number.")
    location = await client.ask(chat_id=message.from_user.id, text=f"And where do they live?")
    back.insert(fullname.text, nickname.text, birthday.text, int(phone.text), location.text, message.from_user.id)
    await message.reply_text(f"Awesome! You just added a new friend! it's: \n**{fullname.text}**, they're called **{nickname.text}**, they're born in **{birthday.text}**, their phone number is **{phone.text}** and they live in **{location.text}**.\nTo see a list of all of your friends, you can use the command '/my_friends' or type 'List of Friends' or tap the button below.", parse_mode=enums.ParseMode.MARKDOWN)

@app.on_message(filters.command("my_friends") | filters.regex("List of Friends"))
async def show_list(client: Client, message: Message):
    friends = back.view(message.from_user.id)
    # print(friends[0][1])
    text = ""
    number = 0
    for friend in friends:
        text += f"╭ 👤 Fullname: {friend[1]}\n┊ 💬 Nickname: {friend[2]}\n┊ 🥳 Birthday: {friend[3]}\n┊ 📞 Phone Number: {friend[4]}\n╰ 📍 Location: {friend[5]}\n\n\n"
    await message.reply_text(text)
    print(friends)



print("START")  # to  see  if  the  bot  has  started
app.run()