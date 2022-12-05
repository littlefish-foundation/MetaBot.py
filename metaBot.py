# everything starts with meta
import discord
import pymongo
import mytoken

from discord.ext import commands
from pymongo import MongoClient

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

MongoStr = mytoken.MongoStr

client = pymongo.MongoClient(MongoStr)

try:
    db = client.littlefish
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

#db = client["littlefish"]

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')



@bot.command()
async def ikigai(ctx):
    # Ask the user the four questions
    await ctx.send("What do you love doing?")
    response1 = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    await ctx.send("What are you good at?")
    response2 = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    await ctx.send("What does the world need from you?")
    response3 = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    await ctx.send("What can you be paid for?")
    response4 = await bot.wait_for("message", check=lambda message: message.author == ctx.author)

    # Insert the answers into the database
    collection = db["ikigai"]
    document = {
        "user_id": ctx.author.id,
        "love": response1,
        "good_at": response2,
        "world_needs": response3,
        "paid_for": response4
    }
    collection.insert_one(document)

    await ctx.send("Your answers have been saved to the database.")

@bot.command()
async def updateikigai(ctx):
    # Retrieve the user's answers from the database
    collection = db["ikigai"]
    document = collection.find_one({"user_id": ctx.author.id})

    # Update the answers
    await ctx.send("What do you love doing?")
    response1 = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    await ctx.send("What are you good at?")
    response2 = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    await ctx.send("What does the world need from you?")
    response3 = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    await ctx.send("What can you be paid for?")
    response4 = await bot.wait_for("message", check=lambda message: message.author == ctx.author)

    # Update the answers in the database
    document["love"] = response1
    document["good_at"] = response2
    document["world_needs"] = response3
    document["paid_for"] = response4
    collection.replace_one({"user_id": ctx.author.id}, document)

    await ctx.send("Your answers have been updated in the database.")

@bot.command()
async def getikigai(ctx):
    # Retrieve the user's answers from the database
    collection = db["ikigai"]
    document = collection.find_one({"user_id": ctx.author.id})

    # Send the answers to the user
    await ctx.send("What do you love doing?")
    await ctx.send(document["love"])
    await ctx.send("What are you good at?")
    await ctx.send(document["good_at"])
    await ctx.send("What does the world need from you?")
    await ctx.send(document["world_needs"])
    await ctx.send("What can you be paid for?")
    await ctx.send(document["paid_for"])

@bot.command()
async def deleteikigai(ctx):
    # Delete the user's answers from the database
    collection = db["ikigai"]
    collection.delete_one({"user_id": ctx.author.id})

    await ctx.send("Your answers have been deleted from the database.")

DISCORD_TOKEN = mytoken.DISCORD_TOKEN
bot.run(DISCORD_TOKEN)
