from telethon import TelegramClient, events
from datetime import datetime
import time
import sqlite3


class TgModule:
    def __init__(self, api_id, api_hash, main_message_link, video_and_photo_group_link, decrypt_bot_link, db_name,
                 oneself_id, fruit_list):
        self.api_id = api_id
        self.api_hash = api_hash
        self.main_message_link = main_message_link
        self.video_and_photo_group_link = video_and_photo_group_link
        self.decrypt_bot_link = decrypt_bot_link
        self.db_name = db_name
        self.oneself_id = oneself_id
        self.fruit_list = fruit_list

    async def start(self):
        session_name = f"id_{self.api_id}"
        client = TelegramClient(session_name, self.api_id, self.api_hash)

        @client.on(events.NewMessage())
        async def global_listening(event):
            try:
                session = await event.get_chat()
                session_title = session.title
                session_id = str(session.id)
            except Exception as e:
                session_title = "*私聊*"
            try:
                session_id = str(session.id)
            except:
                session_id = "私聊无会话id"
            if event.sender_id == self.oneself_id:
                print("自己的消息不做转发")
                return

            for fruit in self.fruit_list:
                if session_id == fruit:
                    print("当前是被屏蔽的" + session_title + session_id)
                    return
            await self.forward_the_message(event, client)
            await self.get_title(event)

        await client.start()
        await client.run_until_disconnected()

    async def forward_the_message(self, event, client):
        try:

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
                    # print("密文消息" + event.raw_text)
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
                    # print("普通消息" + event.raw_text)
        except Exception as e:
            print(f"无法转发此消息: {e}")

    async def get_title(self, event):
        try:
            session = await event.get_chat()
            session_title = session.title
        except Exception as e:
            session_title = "*私聊*"

        try:
            session_id = str(session.id)
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
            elif event.raw_text == "":
                user_message = "当前消息是一个表情"
            else:
                user_message = event.raw_text
            now_time = time.strftime("%Y-%m-%d %H:%M")
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
        conn = sqlite3.connect("message.db")

        # 创建一个游标对象，用于执行 SQL 语句
        cur = conn.cursor()

        # 检查消息表是否存在，不存在则创建表
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {self.db_name} (id INTEGER PRIMARY KEY, user_id INTEGER, username TEXT, session_id TEXT, session_title TEXT, message_content TEXT, message_time TEXT)")

        # 插入数据到消息表
        cur.execute(
            f"INSERT INTO {self.db_name} (user_id, username, session_id, session_title, message_content, message_time) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, user_name, session_id, session_title, user_message,
             now_time))

        # 提交事务
        conn.commit()

        # 关闭游标和连接
        cur.close()
        conn.close()
