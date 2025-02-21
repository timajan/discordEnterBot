import asyncio
import discord
from dotenv import load_dotenv
import os


# Load environment variables from the .env file
load_dotenv()

# Access environment variables
token = os.getenv("TOKEN")
path_var = os.getenv('PATH')

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.message_content = True

client = discord.Client(intents=intents)
threadStarted = False
isPlaying = True


ffmpeg_path = ''

# Find which part of PATH contains FFmpeg (assuming ffmpeg executable is named ffmpeg or ffmpeg.exe)
for path in path_var.split(';'):
    if 'ffmpeg' in path.lower():
        ffmpeg_path = path


@client.event
async def on_ready():
    print(f'Logged on as {client.user}')


@client.event
async def on_message(message):
    global threadStarted, vClient, isPlaying
    if message.content.startswith('!stop') and not threadStarted:
        isPlaying = False
    elif message.content.startswith('!start') and not threadStarted:
        isPlaying = True


@client.event
async def on_voice_state_update(member, before, after):
    if isPlaying and after.channel is not None:
        print(f"{member.name} has joined {after.channel.name}")
        try:
            if after.channel:  # Ensure the channel exists
                vClient = await after.channel.connect()
                source = discord.FFmpegOpusAudio('sound.mp3', executable=f"{ffmpeg_path}\\ffmpeg.exe")
                vClient.play(source)
                while vClient.is_playing():
                    await asyncio.sleep(1)
                await vClient.disconnect()
        except Exception as e:
            print(f"Failed to handle voice state update: {e}")

client.run(token)
