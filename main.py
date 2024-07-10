from pyrogram.types import ChatPrivileges
from pyrogram import Client
from pyrogram.enums.chat_type import ChatType
from pyrogram.enums.message_media_type import MessageMediaType
from pyrogram.raw import functions, types, base
from pyrogram.errors import (
    UsernameInvalid,
    UsernameNotOccupied,
    UserNotMutualContact,
    UserAlreadyParticipant,
    UserChannelsTooMuch,
    UserPrivacyRestricted,
)
import os
import json
import asyncio



media_count = 0

with open("config.json", encoding="utf-8") as file:
    cfg = json.load(file)
    api_id = cfg["api_id"]
    api_hash = cfg["api_hash"]


def downloader(total_chats, exts, output_folder):
    client = Client("current", api_id=api_id, api_hash=api_hash)
    with client:
        dialogs = client.get_dialogs(int(total_chats))
        for dialog in dialogs:
            if dialog.chat.type == ChatType.PRIVATE:
                chat_id = dialog.chat.id
                msgs = client.get_chat_history(chat_id=chat_id)
                for message in msgs:
                    if message.media == MessageMediaType.VIDEO and "video" in exts:
                        client.download_media(
                            message=message, file_name=f"{output_folder}/"
                        )
                    if message.media == MessageMediaType.PHOTO and "photo" in exts:
                        client.download_media(
                            message=message, file_name=f"{output_folder}/"
                        )
    return


def find_session():
    files = os.listdir()
    for file in files:
        if "session" in file:
            try:
                client = Client("current", api_id=api_id, api_hash=api_hash)
                with client:
                    client.get_me()
                print("Последняя сессия валид")
                return True
            except:
                os.remove("current.session")
                print("Последняя сессия невалид")
                return False
    print("Последняя сессия не найдена")
    return False


def main():
    chats_count = input("Введите кол-во чатов: ")
    exts = input("Перечислите тип файлов для выгрузки: ").replace(" ", "").split(",")
    output_folder = input("Укажите папку для выгрузки: ")
    cur_sess = find_session()
    print("\n")
    downloader(chats_count, exts, output_folder)


# client = Client('current.session',api_id=26331650,api_hash='ba7f231c85fd35d37f428550628b0025')
# with client:
#   msgs = client.get_chat_history(chat_id='cash002',limit=5)
#   for message in msgs:
#     client.download_media(message=message,file_name='output/')
#     # if message.media == MessageMediaType.PHOTO:
#     #   client.download_media(message=message.photo.file_id,file_name=f'output/{message.photo.file_id}.jpg')
#     # if message.media == MessageMediaType.VIDEO:
#     #   client.download_media(message=message.photo.file_id,file_name=f'output/{message.photo.file_id}.mp4')
#     media_count += 1

while True:
    main()
