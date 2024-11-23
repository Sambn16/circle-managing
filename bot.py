from pyrogram import * 
from pyrogram.types import *
from pyromod import *
import back

app = Client(
    
    
    name="bot",
    api_id="123123123",
    api_hash="blbl12345",
    bot_token="blahblah1234"
)


# ========================= START COMMAND =========================
#    sending hello message and saving user data to the database

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    if not back.user_data_view(message.from_user.id):
        back.user_data_insert(message.from_user.id, message.from_user.first_name)
        await message.reply_text(f"hello {message.from_user.first_name}!", reply_markup=ReplyKeyboardMarkup([["Add"],["List of Friends"]], resize_keyboard=True))
    elif back.user_data_view(message.from_user.id):
        await message.reply_text(f"You've already started the bot, {message.from_user.first_name}. Perhaps you wanted /add ? Or just tap the buttons below.", reply_markup=ReplyKeyboardMarkup([["Add"],["List of Friends"]], resize_keyboard=True))

    else:
        await message.reply_text(f"something went wrong, please contact the admin.")


# ========================= HELP COMMAND =========================
#     sends a message to guide the user to how to use the bot

@app.on_message(filters.command("help") | filters.regex("help"))
async def help_command(client: Client, message: Message):
    await message.reply_text("Here you are! As you probably know, I'm a bot that helps you manage your circle of connections, wether it's a friend, a co-worker, a classmate or a partner. Here are the command that would help you:\n\n/start - The main command to start the bot.\n/help - You just used it! Sends this message to guide you.\n/add - To add a friend. You can send 'Add' as well, as it's shown in the buttons below.\n/my_friends - To show you a list of all your friends that are added to the bot. You can also send 'List of Friends' by tapping the button below.\n\nHappy managing your circle!")


# ========================= ADD COMMAND =========================
# asking questions about the person they want to add as their friends and saving the friends data

@app.on_message(filters.command("add") | filters.regex("Add") | filters.regex("add"))
async def add_friend(client: Client, message: Message):
    fullname = await client.ask(chat_id=message.from_user.id, text="So you wanna add one of your friends? Okay! What's the full name of this fella?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="cancel", callback_data="cancel")]]))
    nickname = await client.ask(chat_id=message.from_user.id, text=f"Okay! So what do you call {fullname.text}?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="cancel", callback_data="cancel")]]))
    birthday = await client.ask(chat_id=message.from_user.id, text=f"Great! When is their birthday anyway? \n\n It must be in (YYYY-MM-DD) format!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="cancel", callback_data="cancel")]]))
    phone = await client.ask(chat_id=message.from_user.id, text=f"Now it's time for their phone number.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="cancel", callback_data="cancel")]]))
    location = await client.ask(chat_id=message.from_user.id, text=f"And where do they live?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="cancel", callback_data="cancel")]]))
    back.insert(fullname.text, nickname.text, birthday.text, int(phone.text), location.text, message.from_user.id)
    await message.reply_text(f"Awesome! You just added a new friend! it's: \n**{fullname.text}**, they're called **{nickname.text}**, they're born in **{birthday.text}**, their phone number is **{phone.text}** and they live in **{location.text}**.\nTo see a list of all of your friends, you can use the command '/my_friends' or type 'List of Friends' or tap the button below.", parse_mode=enums.ParseMode.MARKDOWN)

# ========================= MY FRIENDS COMMAND =========================
#      show a list of their friends that are stored in the database

@app.on_message(filters.command("my_friends") | filters.regex("List of Friends"))
async def show_list(client: Client, message: Message):
    friends = back.view(message.from_user.id)
    text = ""
    for friend in friends:
        text += f"╭ 👤 Fullname: {friend[1]}\n┊ 💬 Nickname: {friend[2]}\n┊ 🥳 Birthday: {friend[3]}\n┊ 📞 Phone Number: {friend[4]}\n╰ 📍 Location: {friend[5]}\n\n\n"
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Show seperately", callback_data="show")],[InlineKeyboardButton(text="Edit", callback_data="edit"), InlineKeyboardButton(text="Add", callback_data="add")],[InlineKeyboardButton(text="Delete", callback_data="delete")]]))

# ========================= BUTTON ACTIONS =========================
#      how should every button behave, using callback queries

@app.on_callback_query()
async def buttons(client: Client, callback: CallbackQuery):
    friends = back.view(callback.from_user.id)
    list_of_friends = []
    for friend in friends:
        list_of_friends.append([friend[1]])

    if callback.data == "cancel":
        await callback.answer()
        await callback.message.edit_text("Okay! Go back to /start!", reply_markup=None)
        await client.stop_listening(chat_id=callback.from_user.id)

    elif callback.data == "edit":
        await callback.answer()
        friend_to_edit = await client.ask(chat_id=callback.from_user.id,text="So you wanna edit some information about a friend. Which friend is it?", reply_markup=ReplyKeyboardMarkup(list_of_friends, resize_keyboard=True, one_time_keyboard=True))
        
        friend = back.search(friend_to_edit.text)
        # ic(friend[0][1]) SHOWS FULLNAME !!! AND SO ON

        list_of_friends = [friend[0] for friend in list_of_friends]
        if friend_to_edit.text in list_of_friends:
            what_to_edit = await client.ask(chat_id=callback.from_user.id, text=f"And what do you want to change about {friend_to_edit.text}?", reply_markup=ReplyKeyboardMarkup([["Full Name"], ["Nickname", "Birthday"], ["Phone Number", "Location"]], resize_keyboard=True, one_time_keyboard=True))
            
            if what_to_edit.text == "Full Name":
                edited_item = await client.ask(chat_id=callback.from_user.id, text="Alright! What do you want to put as their full name?")
                back.edit(edited_item.text, friend[0][2], friend[0][3], friend[0][4], friend[0][5], friend[0][1])
                await callback.message.reply_text(f"Done! I put their full name as {edited_item.text}!")

            elif what_to_edit.text == "Nickname":
                edited_item = await client.ask(chat_id=callback.from_user.id, text="What do you call them now?")
                back.edit(friend[0][1], edited_item.text, friend[0][3], friend[0][4], friend[0][5], friend[0][1])
                await callback.message.reply_text(f"Done! I put their nickname as {edited_item.text}!")
            
            elif what_to_edit.text == "Birthday":
                edited_item = await client.ask(chat_id=callback.from_user.id, text="Oh! When is their actual birthday then? Remember that you should send it in YYYY-MM-DD format!")
                back.edit(friend[0][1], friend[0][2], edited_item.text, friend[0][4], friend[0][5], friend[0][1])
                await callback.message.reply_text(f"Done! I put their Birthday as {edited_item.text}!")
            
            elif what_to_edit.text == "Phone Number":
                edited_item = await client.ask(chat_id=callback.from_user.id, text="Hmmm... they have a new phone number? What is it?")
                back.edit(friend[0][1], friend[0][2], friend[0][3], edited_item.text, friend[0][5], friend[0][1])
                await callback.message.reply_text(f"Done! I put their phone number as {edited_item.text}!")
            
            elif what_to_edit.text == "Location":
                edited_item = await client.ask(chat_id=callback.from_user.id, text="Okay! Where do they live now?")
                back.edit(friend[0][1], friend[0][2], friend[0][3], friend[0][4], edited_item.text, friend[0][1])
                await callback.message.reply_text(f"Done! I put their location as {edited_item.text}!")

        else:
            await callback.message.reply_text(f"There isn't anyone named {friend_to_edit.text} in your friends!")

    elif callback.data == "delete":
        await callback.answer()
        friend_to_delete = await client.ask(chat_id=callback.from_user.id,text="Oh! You want to delete a friend! I hope there isn't any major problem :(. Which friend you wanna delete?", reply_markup=ReplyKeyboardMarkup(list_of_friends, resize_keyboard=True, one_time_keyboard=True))
        list_of_friends = [friend[0] for friend in list_of_friends]
        if friend_to_delete.text in list_of_friends:
            back.remove(friend_to_delete.text)
            await callback.message.reply_text(f"Okay! I removed {friend_to_delete.text} and everything about them! I still hope everything is okay tho... :(")

        else:
            await callback.message.reply_text(f"There isn't anyone named {friend_to_delete.text} in your friends!")
    elif callback.data == "show":
        await callback.answer()
        for friend in friends:
            await callback.message.reply_text(f"╭ 👤 Fullname: {friend[1]}\n┊ 💬 Nickname: {friend[2]}\n┊ 🥳 Birthday: {friend[3]}\n┊ 📞 Phone Number: {friend[4]}\n╰ 📍 Location: {friend[5]}")

    elif callback.data == "add":
        await callback.answer()
        fullname = await client.ask(chat_id=callback.from_user.id, text="So you wanna add one of your friends? Okay! What's the full name of this fella?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="cancel", callback_data="cancel")]]))
        nickname = await client.ask(chat_id=callback.from_user.id, text=f"Okay! So what do you call {fullname.text}?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="cancel", callback_data="cancel")]]))
        birthday = await client.ask(chat_id=callback.from_user.id, text=f"Great! When is their birthday anyway? \n\n It must be in (YYYY-MM-DD) format!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="cancel", callback_data="cancel")]]))
        phone = await client.ask(chat_id=callback.from_user.id, text=f"Now it's time for their phone number.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="cancel", callback_data="cancel")]]))
        location = await client.ask(chat_id=callback.from_user.id, text=f"And where do they live?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="cancel", callback_data="cancel")]]))
        back.insert(fullname.text, nickname.text, birthday.text, int(phone.text), location.text, callback.from_user.id)
        await callback.message.reply_text(f"Awesome! You just added a new friend! it's: \n**{fullname.text}**, they're called **{nickname.text}**, they're born in **{birthday.text}**, their phone number is **{phone.text}** and they live in **{location.text}**.\nTo see a list of all of your friends, you can use the command '/my_friends' or type 'List of Friends' or tap the button below.", parse_mode=enums.ParseMode.MARKDOWN)



@app.on_callback_query()
async def cancel_conversation(client: Client, callback: CallbackQuery):
    if callback.data == "cancel":
        callback.message.reply_text("Okay!")

# ========================= BIRTHDAY REMINDING =========================
#      all of the functionality of the birthday reminding system






print("START")  # to  see  if  the  bot  has  started
app.run()