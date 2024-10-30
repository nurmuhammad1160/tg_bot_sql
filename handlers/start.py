from aiogram import Router, F
from aiogram.types import Message, chat_member_updated
from aiogram.types.chat_member import ChatMember
from aiogram.filters import CommandStart
start_router: Router = Router()


from models.sqlite import get_users, create_user,get_user, User

@start_router.message(CommandStart())
async def start_handler(msg: Message):   
    
    user_id = msg.from_user.id
    user_name = msg.from_user.full_name
    user_email = msg.from_user.username if msg.from_user.username else 'email@example.com'

   
    existing_user = await get_user(user_id)

    
    if not existing_user:
        user = User(id=user_id, name=user_name, email=user_email)
        await create_user(user)

    
    users = await get_users()
    welcome_text = "Xush kelibsiz!\n\n"
    if users:
        user_list = "\n".join([f"{user.id}: {user.name} ({user.email})" for user in users])
        await msg.answer(welcome_text + f"Userlar ro'yxati:\n{user_list}")
    else:
        await msg.answer(welcome_text + "Userlar topilmadi.")