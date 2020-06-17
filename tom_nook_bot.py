import aiohttp
import json
import logging
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("ACNH_BOT_TOKEN")
VILLAGER_DB_AUTOCOMPLETE_URL = "https://villagerdb.com/autocomplete"
VILLAGER_DB_ITEM_URL = "https://villagerdb.com/item"
VILLAGER_DB_VILLAGER_URL = "https://villagerdb.com/villager"

logging.basicConfig(
    level="INFO",
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%H:%M:%S")
logging.getLogger("discord").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    logger.info("Started up %s", bot.user.name)
    logger.info("Bot running on servers: %s",
                ", ".join([guild.name for guild in bot.guilds]))

@bot.event
async def on_guild_join(guild):
    logger.info("Bot added to new server! Server name: %s", guild.name)


@bot.command(name="item", help="Responds with a link to the item in VillagerDB")
async def item_search(ctx, *item_name):
    item_name = " ".join(item_name)

    logger.info("Item search request: '%s'", item_name)

    if not item_name:
        await ctx.send(
            "Please specify an item name after the command, "
            "ex: `!item giant teddy bear`")
        return

    async with aiohttp.ClientSession() as session:
        r = await session.get(
            VILLAGER_DB_AUTOCOMPLETE_URL,
            params={"q": item_name})
        top_matches = await r.json()

        if not top_matches:
            await ctx.send("No items found with that name")
            return

        if len(top_matches) > 1:
            similar_items = [x.lower() for x in top_matches[1:]]
            await ctx.send("Possible alternatives: {}".format(
                ", ".join(similar_items)))

        await ctx.send("{item_url}/{item_name}".format(
            item_url=VILLAGER_DB_ITEM_URL,
            item_name=top_matches[0].replace(" ", "-").lower()
        ))


@bot.command(name="villager", help="Responds with a link to the villager in VillagerDB")
async def villager_search(ctx, *villager_name):
    villager_name = "-".join(villager_name)

    logger.info("Villager search request: '%s'", villager_name)

    if not villager_name:
        await ctx.send(
            "Please specify an item name after the command, "
            "ex: `!villager raymond`")
        return

    async with aiohttp.ClientSession() as session:
        villager_url = "{villager_url}/{villager_name}".format(
            villager_url=VILLAGER_DB_VILLAGER_URL,
            villager_name=villager_name)

        r = await session.get(villager_url)

        if r.status == 404:
            await ctx.send("No villager found with that name")
            return

        await ctx.send(villager_url)


bot.run(DISCORD_BOT_TOKEN)
