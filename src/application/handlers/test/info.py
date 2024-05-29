from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command('info'))
async def handle_my_id(msg: Message):
    replied = msg.reply_to_message
    if replied:
        if replied.forward_from_chat:
            chat = replied.forward_from_chat
            await msg.reply(f'''
                Сообщение переслано из чата: <b>{chat.title}</b> (<code>{chat.id}</code>)
            ''')
        elif replied.forward_from:
            user = replied.forward_from
            await msg.reply(f'''
                Сообщение переслано от пользователя: <b>{user.full_name}</b> (<code>{user.id}</code>)
            ''')
    else:
        await msg.reply('Вы должны ответить на пересланное сообщение')
