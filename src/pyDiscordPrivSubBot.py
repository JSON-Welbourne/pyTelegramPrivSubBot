# bot.py
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
import discord
import random
import re
import shlex
import config

TOKEN = config['DISCORD_TOKEN']
client = discord.Client()
history = {}
myBot = ChatBot("Noah's Chatbot")
trainer = ListTrainer(myBot)


async def sendMessage(channel, response):
    try:
        await channel.send(response)
    except Exception as e:
        print(f'ERROR Sending Message to {channel}: {response}, {e}')
    else:
        print(f'Sent Message to {channel}: {response}')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await sendMessage(
        member.dm_channel, 
        f'Hi {member.name}, welcome to my Discord server!')

@client.event
async def on_message(message):
    print("Message Received from {}: {}".format(message.author,message.content))
    if message.author == client.user:
        return
    responses = []
    if message.content.lower().startswith('learn'):
        conversation = shlex.split(message.content)[1:] 
        trainer.train(conversation)
        responses.append("Learned:")
        for response in conversation:
            responses.append("    {}".format(response))
    else:
        responses.append(myBot.get_response(message.content))
    for response in responses:    
        await sendMessage(
            message.channel, 
            response)

client.run(TOKEN)
