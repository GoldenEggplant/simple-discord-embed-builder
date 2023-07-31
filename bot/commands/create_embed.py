import disnake
from disnake.ext import commands
import disnake.ui
import urllib.parse


def setup(bot: commands.InteractionBot):
    @bot.slash_command(
        name="create_embed",
        description="Create a custom embed.",
        options=get_create_embed_options(),
    )
    async def create_embed_command(interaction, **kwargs):
        if not kwargs:
            await interaction.response.send_message(
                "Please provide options for the embed.", ephemeral=True
            )
            return

        await create_embed(interaction, **kwargs)


def get_create_embed_options():
    option_data = (
        ("author_icon", "URL", False),
        ("author_name", "TEXT", False),
        ("author_hyperlink", "URL", False),
        ("title", "TEXT", False),
        ("title_hyperlink", "URL", False),
        ("title_description", "TEXT", False),
        ("image_thumbnail", "URL", False),
        ("image_banner", "URL", False),
        ("footer_icon", "URL", False),
        ("footer_text", "TEXT", False),
        ("timestamp", "DEFAULT FALSE", False),
        ("color", "HEX", False),
    )

    return (
        disnake.Option(
            type=disnake.OptionType.boolean
            if name == "timestamp"
            else disnake.OptionType.string,
            name=name,
            description=desc,
            required=req,
        )
        for name, desc, req in option_data
    )


def validate_embed_lengths(author_name, title, description, footer_text):
    if len(author_name or "") > 256 or len(title or "") > 256:
        return "The author name and main title cannot be longer than 256 characters."

    if len(description or "") > 4096:
        return "The description cannot be longer than 4096 characters."

    if len(footer_text or "") > 2048:
        return "The footer text cannot be longer than 2048 characters."

    return ""


class ConfirmationButton(disnake.ui.View):
    def __init__(self, embed, message_content=""):
        super().__init__()
        self.embed = embed
        self.message_content = message_content

    @disnake.ui.button(
        label="Send", style=disnake.ButtonStyle.success, custom_id="send_embed"
    )
    async def send_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        await interaction.send(embed=self.embed)
        self.stop()


async def set_author(embed, author_icon=None, author_name=None, author_hyperlink=None):
    if (author_icon and not urllib.parse.urlparse(author_icon).scheme) or (
        author_hyperlink and not urllib.parse.urlparse(author_hyperlink).scheme
    ):
        raise ValueError("Invalid URL [author_icon/author_hyperlink].")

    if author_icon and author_name and author_hyperlink:
        embed.set_author(name=author_name, url=author_hyperlink, icon_url=author_icon)
    elif author_icon and author_name:
        embed.set_author(name=author_name, icon_url=author_icon)
    elif author_name and author_hyperlink:
        embed.set_author(name=author_name, url=author_hyperlink)
    elif author_name:
        embed.set_author(name=author_name)
    elif author_icon or author_hyperlink:
        raise ValueError(
            "You cannot just leave the URL [author_icon/author_hyperlink]."
        )


async def set_title(embed, title=None, title_hyperlink=None, title_description=None):
    if title_hyperlink and not urllib.parse.urlparse(title_hyperlink).scheme:
        raise ValueError("Invalid URL [title_hyperlink].")

    if title and title_description and title_hyperlink:
        embed.title = title
        embed.description = title_description
        embed.url = title_hyperlink
    elif title and title_description:
        embed.title = title
        embed.description = title_description
    elif title and title_hyperlink:
        embed.title = title
        embed.url = title_hyperlink
    elif (title_description and title_hyperlink) or (title_hyperlink):
        raise ValueError("You cannot just leave the URL [title_hyperlink]")
    elif title:
        embed.title = title
    elif title_description:
        embed.description = title_description


async def set_thumbnail(embed, image_thumbnail=None):
    if image_thumbnail:
        if not urllib.parse.urlparse(image_thumbnail).scheme:
            raise ValueError("Invalid URL [image_thumbnail].")
        embed.set_thumbnail(url=image_thumbnail)


async def set_image(embed, image_banner=None):
    if image_banner:
        if not urllib.parse.urlparse(image_banner).scheme:
            raise ValueError("Invalid URL [image_banner].")
        embed.set_image(url=image_banner)


async def set_footer(embed, footer_text=None, footer_icon=None):
    if footer_text and footer_icon:
        if not urllib.parse.urlparse(footer_icon).scheme:
            raise ValueError("Invalid URL [footer_icon].")
        embed.set_footer(text=footer_text, icon_url=footer_icon)
    elif footer_text:
        embed.set_footer(text=footer_text)
    elif footer_icon:
        raise ValueError("You cannot just leave the URL [footer_icon].")


async def set_timestamp(embed, timestamp=False):
    if timestamp and not any(
        (
            embed.author,
            embed.title,
            embed.description,
            embed.image,
            embed.thumbnail,
            embed.footer,
            embed.url,
            embed.color,
        )
    ):
        raise ValueError("You cannot just use timestamp without any other field.")
    embed.timestamp = disnake.utils.utcnow() if timestamp else None


async def set_color(embed, color=None):
    if color:
        if not color.startswith("#"):
            color = "#" + color
        try:
            color = int(color.replace("#", ""), 16)
        except ValueError:
            raise ValueError("Invalid color [color].")
        if not any(
            (
                embed.author,
                embed.title,
                embed.description,
                embed.image,
                embed.thumbnail,
                embed.footer,
                embed.url,
                embed.timestamp,
            )
        ):
            raise ValueError("You cannot just use color without any other field.")
        embed.color = color


async def create_embed(
    interaction,
    author_icon: str = None,
    author_name: str = None,
    author_hyperlink: str = None,
    title: str = None,
    title_hyperlink: str = None,
    title_description: str = None,
    image_thumbnail: str = None,
    image_banner: str = None,
    footer_icon: str = None,
    footer_text: str = None,
    timestamp: bool = False,
    color: str = None,
):
    embed = disnake.Embed()

    if not interaction.guild:
        await interaction.send(
            "My commands only work in servers.", ephemeral=True, delete_after=5
        )
        return

    try:
        await set_author(embed, author_icon, author_name, author_hyperlink)
        await set_title(embed, title, title_hyperlink, title_description)
        await set_thumbnail(embed, image_thumbnail)
        await set_image(embed, image_banner)
        await set_footer(embed, footer_text, footer_icon)
        await set_timestamp(embed, timestamp)
        await set_color(embed, color)
    except ValueError as error:
        await interaction.response.send_message(
            str(error), ephemeral=True, delete_after=5
        )
        return

    validation_error = validate_embed_lengths(
        author_name, title, title_description, footer_text
    )
    if validation_error:
        await interaction.response.send_message(validation_error, ephemeral=True)
        return

    preview_message = await interaction.response.send_message(
        embed=embed, view=ConfirmationButton(embed), ephemeral=True
    )
