import aiohttp
import json
import logging
import os

from logger import setup_logger, ContextLogAdapter

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("ACNH_BOT_TOKEN")
VILLAGER_DB_AUTOCOMPLETE_URL = "https://villagerdb.com/autocomplete"
VILLAGER_DB_ITEM_URL = "https://villagerdb.com/item"
VILLAGER_DB_VILLAGER_URL = "https://villagerdb.com/villager"

setup_logger()

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    logger = ContextLogAdapter()
    logger.info("Started up %s", bot.user.name)
    logger.info("Bot running on servers: %s",
                ", ".join([guild.name for guild in bot.guilds]))

@bot.event
async def on_guild_join(guild):
    logger = ContextLogAdapter()
    logger.info("Bot added to new server! Server name: %s", guild.name)


@bot.command(name="item", help="Responds with a link to the item in VillagerDB")
async def item_search(ctx, *item_name):
    logger = ContextLogAdapter(ctx)

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
            error_resp = "No items found with that name"
            await ctx.send(error_resp)
            logger.info(error_resp)
            return

        if len(top_matches) > 1:
            similar_items = [x.lower() for x in top_matches[1:]]
            await ctx.send("Possible alternatives: {}".format(
                ", ".join(similar_items)))

        item_url = "{item_url}/{item_name}".format(
            item_url=VILLAGER_DB_ITEM_URL,
            item_name=top_matches[0].replace(" ", "-").lower())
        await ctx.send(item_url)
        logger.info(f"Found: {item_url}")


@bot.command(name="villager", help="Responds with a link to the villager in VillagerDB")
async def villager_search(ctx, *villager_name):
    logger = ContextLogAdapter(ctx)

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
            error_resp = "No villager found with that name"
            await ctx.send(error_resp)
            logger.info(error_resp)
            return

        await ctx.send(villager_url)
        logger.info(f"Found: {villager_url}")

bot.run(DISCORD_BOT_TOKEN)
