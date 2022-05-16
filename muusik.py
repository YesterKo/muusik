import discord
import asyncio
import os
from dotenv import load_dotenv

global recorder

sample_length = 10





load_dotenv()
bot = discord.Bot(debug_guilds=[637793926593642508,884501163502878791])
connections = {}

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    
@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.send("Hey!")
    
@bot.command()
async def record(ctx):
    voice = ctx.author.voice
    
    if not voice:
        await ctx.respond("You aren't in a voice channel!")
        
    vc = await voice.channel.connect()
    connections.update({ctx.guild.id: vc})
    
    vc.start_recording(
        discord.sinks.WaveSink(),
        once_done,
        ctx.channel
    )
    
    await ctx.respond("Started recording!")
    
async def once_done(sink: discord.sinks.Sink, channel: discord.TextChannel, *args):
    recorded_users = [
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]
    await sink.vc.disconnect()
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()] # loe välja failid
    
    print(sink.audio_data)
    for x in sink.audio_data:
        print(x)
    
    with open('heli.wav', 'w+b') as fail:
        fail.write(sink.audio_data[recorder].file.read())
        
    await channel.send(f"finished recording audio for: {', '.join(recorded_users)}.", files=files) # Saada sõnum failidega

@bot.command()
async def stop_recording(ctx):
    if ctx.guild.id in connections:
        vc = connections[ctx.guild.id]
        vc.stop_recording()
        del connections[ctx.guild.id]
        await ctx.delete()
    else:
        await ctx.respond("I am currently not recording here.")

@bot.command()
async def recognize(ctx):
    voice = ctx.author.voice
    
    if not voice:
        await ctx.respond("You aren't in a voice channel!")
        
    vc = await voice.channel.connect()
    connections.update({ctx.guild.id: vc})
    
    vc.start_recording(
        discord.sinks.WaveSink(),
        once_done,
        ctx.channel
    )
    
    await ctx.respond("Started recording!")
    
    await asyncio.sleep(sample_length)
    
    await ctx.respond("waited 5 sec")
    
    await stop_recording(ctx)
    
@bot.command()
async def set_recorder(ctx):
    global recorder
    recorder = ctx.author.id
    await ctx.respond(recorder)
    print(recorder)
    
@bot.command()
async def get_recorder(ctx):
    global recorder
    print(recorder)
    await ctx.respond(recorder)


bot.run(os.getenv('TOKEN'))
