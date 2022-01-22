import discord, youtube

bot = discord.Client("A STRING BOT TOKEN")

@bot.thread
def notifier(
    id: str,
    discord_channel_id: int,
    api_key: str,
) -> None:

    video = youtube.LastVideo(id, api_key)
    last_video = video.last_video
    old_last_video = video.old_last_video["new_video"]
    
    if last_video != old_last_video:
        video.update()
        bot.say(
            discord_channel_id,
            content="수상한 보리 밭에서 상추가 자라다?!?!?!",
            components=[
                dict(
                    type=1,
                    components=[
                        dict(
                            type=2,
                            label="이를 클릭!?!??!",
                            style=5,
                            url=last_video
                        )
                    ]
                )
            ]
        )

        last_video = video.last_video
        old_last_video = video.old_last_video

notifier("UChDbYnv1Y_a1AacHM2u2X7w", 929078892118036480, "A STRING YOUTUBE API KEY")
bot.login(bot.token)
