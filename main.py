# main.py

import asyncio
import TgModule# 假设 TgModule 类定义在 mymodule.py 中


async def main(api_id, api_hash, main_message_link, video_and_photo_group_link, decrypt_bot_link, db_name):
    tg_module = TgModule(api_id, api_hash, main_message_link, video_and_photo_group_link, decrypt_bot_link, db_name)
    await tg_module.start()


if __name__ == "__main__":
    # 假设第一个账号信息
    api_id_1 = "24712420"
    api_hash_1 = "21a296cbfaf9e53a024bf0bc48f14078"
    main_message_link_1 = "https://t.me/shishixiaoxi"
    video_and_photo_group_link_1 = "https://t.me/shipinghetupian"
    decrypt_bot_link_1 = "https://t.me/TGFDRobot"
    db_name_1 = "zihao"

    # 调用 main 函数，传递第一个账号信息作为参数
    asyncio.run(
        main(api_id_1, api_hash_1, main_message_link_1, video_and_photo_group_link_1, decrypt_bot_link_1, db_name_1))

    # # 假设第二个账号信息
    # api_id_2 = "api_id_2"
    # api_hash_2 = "api_hash_2"
    # main_message_link_2 = "main_message_link_2"
    # video_and_photo_group_link_2 = "video_and_photo_group_link_2"
    # decrypt_bot_link_2 = "decrypt_bot_link_2"
    # db_name_2 = "db_name_2"
    #
    # # 调用 main 函数，传递第二个账号信息作为参数
    # asyncio.run(
    #     main(api_id_2, api_hash_2, main_message_link_2, video_and_photo_group_link_2, decrypt_bot_link_2, db_name_2))
