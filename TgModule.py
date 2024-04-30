from telethon import TelegramClient, events
from datetime import datetime
import asyncio
import sqlite3


class TgModule:
    def __init__(self, api_id, api_hash, main_message_link, video_and_photo_group_link, decrypt_bot_link, db_name):
        self.api_id = api_id
        self.api_hash = api_hash
        self.main_message_link = main_message_link
        self.video_and_photo_group_link = video_and_photo_group_link
        self.decrypt_bot_link = decrypt_bot_link
        self.db_name = db_name

    async def start(self):
        session_name = f"id_{self.api_id}"
        client = TelegramClient(session_name, self.api_id, self.api_hash)

        @client.on(events.NewMessage())
        async def global_listening(event):
            await self.get_title(event)
            await self.forward_the_message(event, client)  # Pass the client instance

        await client.start()
        await client.run_until_disconnected()

    async def forward_the_message(self, event, client):
        try:
            if event.sender_id != 6731268134:
                if event.media and event.video:
                    await client.forward_messages(
                        self.video_and_photo_group_link, messages=event.message
                    )
                elif event.media and event.photo:
                    await client.forward_messages(
                        self.video_and_photo_group_link, messages=event.message
                    )
                else:
                    if "v_" in event.raw_text or "p_" in event.raw_text or "d_" in event.raw_text:
                        await client.forward_messages(
                            self.decrypt_bot_link, messages=event.message
                        )
                        await client.forward_messages(
                            self.main_message_link, messages=event.message
                        )


                    else:
                        await client.forward_messages(
                            self.main_message_link, messages=event.message
                        )
            else:
                print("自己的消息不做转发")
        except Exception as e:
            print(f"Error in forwarding message: {e}")

    async def get_title(self, event):
        try:
            group = await event.get_chat()
            session_title = group.title
        except Exception as e:
            session_title = "*私聊*"

        try:
            session_id = str(group.id)
        except Exception as e:
            session_id = '未知群id'

        try:
            sender = await event.get_sender()
            user_name = sender.username if sender.username else sender.first_name
        except Exception as e:
            user_name = "*未知发送者*"

        try:
            user_id = event.sender_id
            if event.media and event.photo:
                user_message = "当前消息是图片"
            elif event.media and event.video:
                user_message = "当前消息是视频"
            else:
                user_message = event.raw_text
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        except Exception as e:
            print("无法获取用户消息对象")

        combination_messages = f"实时消息==============来自群【{session_title}】会话id:【{session_id}】==来自用户【{user_name}】=======用户id【{user_id}】\n{now_time}\n✉️👇\n{user_message}\n"
        print(combination_messages)
        await self.insert_message_to_db(session_title, session_id, user_id, user_name, user_message, now_time)

    def send_message(self, message, event, client):
        # You need to define this method according to your needs
        pass

    # 数据库
    async def insert_message_to_db(self, session_title, session_id, user_id, user_name, user_message, now_time):
        # 连接到 SQLite 数据库
        conn = sqlite3.connect(self.db_name)

        # 创建一个游标对象，用于执行 SQL 语句
        cur = conn.cursor()

        # 检查消息表是否存在，不存在则创建表
        cur.execute(
            "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, user_id INTEGER, username TEXT, session_id TEXT, session_title TEXT, message_content TEXT, message_time TEXT)")

        # 插入数据到消息表
        cur.execute(
            "INSERT INTO messages (user_id, username, session_id, session_title, message_content, message_time) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, user_name, session_id, session_title, user_message,
             now_time))

        # 提交事务
        conn.commit()

        # 关闭游标和连接
        cur.close()
        conn.close()


async def main():
    api_id = "24712420"
    api_hash = '21a296cbfaf9e53a024bf0bc48f14078'
    main_message_link = 'https://t.me/shishixiaoxi'
    video_and_photo_group_link = 'https://t.me/shipinghetupian'
    decrypt_bot_link = "https://t.me/TGFDRobot"
    db_name = "zihao"
    tg_module = TgModule(api_id, api_hash, main_message_link, video_and_photo_group_link, decrypt_bot_link, db_name)
    await tg_module.start()


asyncio.run(main())
