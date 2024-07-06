
# Telegram bot Template

This template has helped me in many of my personal and work projects, so I decided to share it so you can use it with me, maintain it, suggest changes and more. For fast and multiplatform development the bot has been packaged in docker. 


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`BOT_TOKEN` - > @BotFather bot token

`TELEGRAM_ADMIN_ID` - > Write here all admins telelgram ids, use , to add more than one.

`TIMEZONE=Europe/Kyiv` -> TimeZone

`REDIS_HOST=redis` -> Redis host (Ussualy use the name of redis image in docker-compose.yml file)

`REDIS_PORT=6379` -> Redis ports (Change 6379 value to another if you already have set first redis)


