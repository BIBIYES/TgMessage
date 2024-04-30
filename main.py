import asyncio
import configparser

from TgModule import TgModule

config = configparser.ConfigParser()
config.read("config.ini")
shield_config = config.get("Telegram", "shield_config")

fruit_list = shield_config.split(',')
print(f"已加载屏蔽群组{fruit_list}")


async def main():
    api_id = "24712420"
    api_hash = '21a296cbfaf9e53a024bf0bc48f14078'
    main_message_link = 'https://t.me/shishixiaoxi'
    video_and_photo_group_link = 'https://t.me/shipinghetupian'
    decrypt_bot_link = "https://t.me/filespanbot"
    db_name = "zihao.db"
    oneself_id = 6731268134  # 替换成你的 Telegram ID

    tg_module = TgModule(api_id, api_hash, main_message_link, video_and_photo_group_link, decrypt_bot_link, db_name,
                         oneself_id, fruit_list)

    api_id_2 = "21383434"
    api_hash_2 = '14245aed1a3cd1aac9d5af8973027161'
    main_message_link_2 = 'https://t.me/jiantingXP001'
    video_and_photo_group_link_2 = 'https://t.me/tuheshiXP001'
    decrypt_bot_link_2 = "https://t.me/filespanbot"
    db_name_2 = "muzi.db"
    oneself_id_2 = 6524572433  # 替换成你的 Telegram ID

    tg_module_2 = TgModule(api_id_2, api_hash_2, main_message_link_2, video_and_photo_group_link_2, decrypt_bot_link_2,
                           db_name_2,
                           oneself_id_2, fruit_list)
    task1 = asyncio.create_task(tg_module.start())
    task2 = asyncio.create_task(tg_module_2.start())


    await asyncio.gather(task1, task2)


if __name__ == "__main__":
    print("自动转发脚本成功运行中")
    asyncio.run(main())
