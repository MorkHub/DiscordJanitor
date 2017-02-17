import asyncio
import discord
import datetime
import os
import atexit

last_clear = datetime.datetime.min
client = discord.Client()
VERSION = '0.1.0'

"""Respond to events"""
@client.event
async def on_ready():
    print('Version ' + VERSION)
    print('Logged in as:')
    print(' ->    Name: '+ client.user.name)
    print(' ->    User ID: '+ client.user.id)
    info = await client.application_info()
    invite_link = discord.utils.oauth_url(info.id,permissions=discord.Permissions(permissions=76800))
    print(' ->    Invite Link: '+ invite_link)

    await update_status()

@client.event
async def on_message(message):
    global last_clear
    if message.author.id != client.user.id and message.content.startswith('!purge'):
        if message.channel.name == 'daily_clear':
            if datetime.datetime.now() >= next_clear():
                await client.send_message(message.channel,'**Last clear**```{}```\n**Earliest**```{}```\nI h**Now**```{}```'.format(str(last_clear),last_clear - datetime.timedelta(hours=-last_clear.hour,minutes=last_clear.minute,seconds=last_clear.second,microseconds=last_clear.microsecond),str(datetime.datetime.now())))
                last_clear = datetime.datetime.now()
                await asyncio.sleep(5)
                succeed = await client.purge_from(message.channel)
                if succeed:
                    msg = await client.send_message(message.channel,'I killed everything. Next clear available from {}'.format(next_clear().strftime('%D %m %I:%M%p')))
                    await asyncio.sleep(10)
                    await client.delete_message(msg)
            else:
                msg = await client.send_message(message.channel, 'Too early to clear. Next clear available from {}'.format(next_clear().strftime('%D %m %I:%M%p')))
                await asyncio.sleep(10)
                await client.delete_message(msg)

def next_clear():
    """returns the next earliest time the channel can be cleared"""
    global last_clear;
    return last_clear - datetime.timedelta(hours=last_clear.hour-24,minutes=last_clear.minute,seconds=last_clear.second,microseconds=last_clear.microsecond)

"""Update bot status: "Playing Janitor" """
async def update_status():
    try:
        await client.change_presence(game=discord.Game(name='Janitor'),afk=False,status=None)
    except:
        pass

@atexit.register
def save_last_clear():
    """save last cleared time to file"""
    global last_clear
    with open('last_clear','w') as file:
        file.write(last_clear.timestamp())

"""Locate OAuth token"""
with open('tokens.txt') as file:
    token = file.read().splitlines()[0]

"""Run program"""
if __name__ == '__main__':
    last_clear = datetime.datetime.min
    if os.path.isfile('last_clear'):
        last_clear = datetime.datetime.fromtimestamp(float(open('last_clear','r').read().splitlines()[0].strip()))
    client.run(token, bot=True)
