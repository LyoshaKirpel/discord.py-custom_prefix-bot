import discord
import json
from ruamel.yaml import YAML
from discord.ext import commands

yaml = YAML()

with open("./config.yml", "r", encoding = "utf-8") as file:
    config = yaml.load(file)

token = config['Token']
stdprefix = config['Standard prefix']

def prefix(client, message):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix = prefix)

@bot.event # if bot added to new server
async def on_guild_join(guild):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	prefixes[str(guild.id)] = stdprefix

	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent=4)

@bot.event # if bot removed from the server
async def on_guild_remove(guild):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	prefixes.pop(str(guild.id))

	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent=4)

@bot.command() # the "changeprefix" command
async def changeprefix(ctx, prefix = None):

	if prefix is None:
		await ctx.send(f'Enter a prefix!')
	else:	
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		prefixes[str(ctx.guild.id)] = prefix

		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)

		await ctx.send(f'Prefix changed to: {prefix}')

bot.run(token)