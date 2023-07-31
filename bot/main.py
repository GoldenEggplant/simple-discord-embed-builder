import disnake
from disnake.ext import commands

bot = commands.InteractionBot(intents=disnake.Intents.all())


@bot.event
async def on_ready():
    print(f"\nLogged in as: {bot.user}")
    await bot.change_presence(activity=disnake.Game(name="Simple Embeds"))


def load_extensions(bot, *extensions):
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded extension: {extension}")
        except Exception as error:
            print(f"Failed to load extension {extension}: {error}")


load_extensions(bot, "commands.create_embed")


try:
    bot.run("YOUR_DISCORD_BOT_TOKEN")
except KeyError:
    print("Error: DISCORD_BOT_TOKEN not found.")
