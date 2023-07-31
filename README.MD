This repository contains a Python bot that allows users to create simple custom embeds with various parameters. The bot provides a preview of custom embeds before submitting them to the channel.

#### Prerequisites
- [Python 3.8.10](https://www.python.org/downloads/release/python-3810/)
- [Disnake 2.9.0](https://pypi.org/project/disnake/)

#### Installation
1. Clone the repository
2. Install the required packages
3. Create a bot account on the [Discord Developer Portal](https://discord.com/developers/applications)
4. Copy the bot token and paste it in the `YOUR_DISCORD_BOT_TOKEN` variable in `main.py`

#### Usage
1. Run `main.py`
2. Type `/create_embed` in any channel the bot has access to and set your parameters:
`author_icon`: URL to the author's icon image.
`author_name`: The name of the author.
`author_hyperlink`: URL to the author's profile or website.
`title`: The main title of the embed.
`title_hyperlink`: URL to link the title to.
`title_description`: Description text for the title.
`image_thumbnail`: URL for a thumbnail image.
`image_banner`: URL for a banner image.
`footer_icon`: URL for the footer icon.
`footer_text`: Text for the footer.
`timestamp`: A boolean indicating whether to include a timestamp in the embed.
`color`: A hexadecimal color code for the embed.

#### Screenshots

#### Contributing
Free to contribute to this project.