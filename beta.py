#imported Modules
from typing import Text
import discord
import sqlite3
from random import choice, choices
from discord import colour
from discord.ext import commands
import asyncio
import datetime
from decouple import config


from discord.ext.commands.core import command

#make connection for database
def connection():
    con=sqlite3.Connection("feeling.db")
    cur=con.cursor()
    return con,cur
#insert to the table function
def insert_sad(con,cur):
    command="INSERT INTO Feeling VALUES('sad',0)"
    cur.execute(command)
    con.commit()

#update Feels
def update_sad(con,cur):
    command="UPDATE Feeling SET Grade=Grade+1 WHERE Feels='sad';"
    cur.execute(command)
    con.commit()
#fetch sad
def get_sad(con,cur):
    cur.execute("SELECT Grade FROM Feeling WHERE Feels = 'sad';")
    rows=cur.fetchone()
    for row in rows:
        return row
#clear function
def clear_data(con,cur):
    command="UPDATE Feeling SET Grade=0 WHERE Feels = 'sad';"
    cur.execute(command)
    con.commit()
#insert notes
def insert_notes(con,cur,texts):
    command="INSERT INTO Notes(Name, Note, Date) VALUES(?,?,?);"
    cur.execute(command,texts)
    con.commit()
#find
def find_notes(con,cur,texts):
    try:
        command="SELECT Note FROM Notes WHERE ID = ? OR Name=?"
        cur.execute(command,[texts,texts])
        rows=cur.fetchone()
        for row in rows:
            return row
        con.commit()
    except TypeError:
        pass
def find_note_by_date(con,cur,texts):
    try:
        command="SELECT Note,Date FROM Notes WHERE ID = ? Or Name = ? "
        cur.execute(command,[texts,texts])
        rows=cur.fetchall()
        for row in rows:
            return row
        con.commit()
    except TypeError:
        pass
#delete notes
def delete_notes(con,cur,texts):
    command="DELETE FROM Notes WHERE ID = ? OR Name = ?"
    cur.execute(command,[texts,texts])
    con.commit()
#insert codes
def insert_codes(con,cur,texts):
    command="INSERT INTO Codes(Name, Code, Date) VALUES(?,?,?);"
    cur.execute(command,texts)
    con.commit()
#find codes
def find_codes(con,cur,texts):
    try:
        command="SELECT Code FROM Codes WHERE ID = ? OR Name=?"
        cur.execute(command,[texts,texts])
        rows=cur.fetchone()
        for row in rows:
            return row
        con.commit()
    except TypeError:
        pass
def find_code_by_date(con,cur,texts):
    try:
        command="SELECT Code,Date FROM Codes WHERE ID = ? Or Name = ? "
        cur.execute(command,[texts,texts])
        rows=cur.fetchall()
        for row in rows:
            return row
        con.commit()
    except TypeError:
        pass
#delete codes
def delete_codes(con,cur,texts):
    command="DELETE FROM Codes WHERE ID = ? OR Name = ?"
    cur.execute(command,[texts,texts])
    con.commit()
con,cur=connection()
#make command prefix and client
client=commands.Bot(command_prefix="alpha ",help_command=None)


#this is on_ready function
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name="alpha help"))
    print("WE ARE READY NOW")

answers=["**OK, Kill Ur Self**","**OK, I Know Life Is Bullshit**","**OK, I Know But It's So Fucking Hard**", "**You Are a Loser, Kill Ur Self**"]

#Help Command
@client.command()
async def help(ctx):
    embed=discord.Embed(
        name="Help Command",
        colour=discord.Colour.dark_blue()
    )
    embed.add_field(name="Add Your Sad Feels To DataBase",value="**`feels *`**",inline=False)
    embed.add_field(name="Show Your Sad Feels",value="**`time`**, **`much`**",inline=False)
    embed.add_field(name="Clear Your Feels From Database",value="**`clear`**",inline=False)
    embed.add_field(name="Inserting Your Notes",value="**`note`**, **`notes`**, **`add-note`**",inline=False)
    embed.add_field(name="Finding Your Notes",value="**`show-note`**, **`see-note`**, **`find-note`**",inline=False)
    embed.add_field(name="Deleting Your Notes",value="**`delete-note`**, **`del-note`**",inline=False)
    embed.add_field(name="Inserting Your Code",value="**`note`**, **`notes`**, **`add-note`**",inline=False)
    embed.add_field(name="Finding Your Code",value="**`show-note`**, **`see-note`**, **`find-note`**",inline=False)
    embed.add_field(name="Deleting Your Code",value="**`delete-note`**, **`del-note`**",inline=False)
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
    embed.set_footer(text="Requested By {}".format(ctx.author),icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

#sad command to make a database
@client.command(pass_context=True)
async def feels(ctx, *, text):
    if ctx.author.id == config("USER_ID"):
        if "sad" in text.lower():
            msg=await ctx.send(f"{choice(answers)}")
            update_sad(con,cur)
            await asyncio.sleep(20)
            await msg.delete()
            await ctx.message.delete()
            await asyncio.sleep(20)
    else:
        msg=await ctx.send("**You Are Not Admin**")
        await asyncio.sleep(6)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(6)

#time to sad command
@client.command(aliases=["time","much"],pass_context=True)
async def _time(ctx):
    if ctx.author.id == config("USER_ID"):
        msg=await ctx.send("You Are Feeling Sad **{}** Times".format(get_sad(con,cur)))
        await asyncio.sleep(15)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(15)
    else:
        msg=await ctx.send("**You Are Not Admin**")
        await asyncio.sleep(6)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(6)

#clear database command
@client.command(pass_context=True)
async def clear(ctx):
    if ctx.author.id == config("USER_ID"):
        msg=await ctx.send("**OK, I'm Clear Your Data**")
        clear_data(con,cur)
        await asyncio.sleep(10)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(10)
    else:
        msg=await ctx.send("**You Are Not Admin**")
        await asyncio.sleep(6)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(6)
#insert note
@client.command(pass_context=True,aliases=["note","notes","add-note"])
async def _note(ctx,name="notname", *, text="nottext"):
    if ctx.author.id == config("USER_ID"):
        msg=await ctx.send(

'''
OK, I Add This Note To Your Data

Name Is **{}** And Your Text Is:
**{}**
'''.format(name.lower(),text)
        )
        insert_notes(con,cur,[name.lower(),text,datetime.datetime.now()])
        await asyncio.sleep(10)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(10)
    else:
        msg=await ctx.send("**You Are Not Admin**")
        await asyncio.sleep(6)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(6)
#find notes
@client.command(pass_context=True,aliases=["show-note","find-note","see-note"])
async def _show(ctx,texts,*,name_or_id):
    if ctx.author.id == config("USER_ID"):
        #if requested by id
        if "=> id" in name_or_id.lower():
            if find_notes(con,cur,texts)==None:
                msg=await ctx.send("**I'm Sorry, I Can't Find This Note, Error 404**")
                await asyncio.sleep(6)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(6)
            else:
                embed=discord.Embed(
                    name="Note",
                    colour=discord.Colour.dark_magenta()
                )
                embed.add_field(name="Note For ID => {}".format(texts),value='''
Your Note Is:
**{}**
                '''.format(find_notes(con,cur,texts)))
                embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Requested By {}".format(ctx.author),icon_url=ctx.author.avatar_url)
                msg=await ctx.send(embed=embed)
        
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
        #if requested by name
        elif "=> name" in name_or_id.lower():
            if find_notes(con,cur,texts)==None:
                msg=await ctx.send("**I'm Sorry, I Can't Find This Note, Error 404**")
                await asyncio.sleep(6)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(6)
            else:
                embed=discord.Embed(
                    name="Note",
                    colour=discord.Colour.dark_magenta()
                )
                embed.add_field(name="Note For Name => {}".format(texts),value='''
Your Note Is:
**{}**
                '''.format(find_notes(con,cur,texts)))
                embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Requested By {}".format(ctx.author),icon_url=ctx.author.avatar_url)
                msg=await ctx.send(embed=embed)
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
    else:
        msg=await ctx.send("**You Are Not Admin**")
        await asyncio.sleep(6)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(6)

@client.command(pass_context=True,aliases=["date-note","when-note"])
async def _date(ctx,texts,*,name_or_id):
    if ctx.author.id == config("USER_ID"):
        #if requested by id
        if "=> id" in name_or_id.lower():
            if find_note_by_date(con,cur,texts)==None:
                msg=await ctx.send("**I'm Sorry, I Can't Find This Note, Error 404**")
                await asyncio.sleep(6)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(6)
            else:
                embed=discord.Embed(
                    name="Note",
                    colour=discord.Colour.dark_magenta()
                )
                embed.add_field(name="Note For ID => {}".format(texts),value='''
Your Note Is:
**{}**
                '''.format(find_note_by_date(con,cur,texts)))
                embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Requested By {}".format(ctx.author),icon_url=ctx.author.avatar_url)
                msg=await ctx.send(embed=embed)
        
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
        #if requested by name
        elif "=> name" in name_or_id.lower():
            if find_note_by_date(con,cur,texts)==None:
                msg=await ctx.send("**I'm Sorry, I Can't Find This Note, Error 404**")
                await asyncio.sleep(6)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(6)
            else:
                embed=discord.Embed(
                    name="Note",
                    colour=discord.Colour.dark_magenta()
                )
                embed.add_field(name="Note For Name => {}".format(texts),value='''
Your Note Is:
**{}**
                '''.format(find_note_by_date(con,cur,texts)))
                embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Requested By {}".format(ctx.author),icon_url=ctx.author.avatar_url)
                msg=await ctx.send(embed=embed)
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
    else:
        msg=await ctx.send("**You Are Not Admin**")
        await asyncio.sleep(6)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(6)

#delete notes
@client.command(pass_context=True,aliases=["delete-note","del-note"])
async def _delete(ctx,texts,*,name_or_id):
    if ctx.author.id == config("USER_ID"):
        if "=> id" in name_or_id.lower():
            if find_notes(con,cur,texts)==None:
                msg=await ctx.send("**I'm Sorry, I Can't Find This Note, Error 404**")
                await asyncio.sleep(6)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(6)
            else:
                embed=discord.Embed(
                    name="Delete",
                    colour=discord.Colour.dark_magenta()
                )
                embed.add_field(name="Note For ID => {}".format(texts),value='''
Your Note Is:
**{}**
                '''.format(find_notes(con,cur,texts)))
                embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Requested By {}".format(ctx.author),icon_url=ctx.author.avatar_url)
                msg=await ctx.send(embed=embed)
                delete_notes(con,cur,texts)
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
        #if requested by name
        elif "=> name" in name_or_id.lower():
            if find_notes(con,cur,texts)==None:
                msg=await ctx.send("**I'm Sorry, I Can't Find This Note, Error 404**")
                await asyncio.sleep(6)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(6)
            else:
                embed=discord.Embed(
                    name="Delete",
                    colour=discord.Colour.dark_magenta()
                )
                embed.add_field(name="Note For Name => {}".format(texts),value='''
Your Note Is:
**{}**
                '''.format(find_notes(con,cur,texts)))
                embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Requested By {}".format(ctx.author),icon_url=ctx.author.avatar_url)
                msg=await ctx.send(embed=embed)
                delete_notes(con,cur,texts)
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
    else:
        msg=await ctx.send("**You Are Not Admin**")
        await asyncio.sleep(6)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(6)

#insert code
@client.command(pass_context=True,aliases=["code","codes","add-code"])
async def _code(ctx,name="notname", *, text="nottext"):
    if ctx.author.id == config("USER_ID"):
        msg=await ctx.send(

'''
OK, I Add This Note To Your Data

Name Is **{}** And Your Text Is:
**{}**
'''.format(name.lower(),text)
        )
        insert_codes(con,cur,[name.lower(),text,datetime.datetime.now()])
        await asyncio.sleep(10)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(10)
    else:
        msg=await ctx.send("**You Are Not Admin**")
        await asyncio.sleep(6)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(6)
#find code
@client.command(pass_context=True,aliases=["show-code","find-code","see-code"])
async def _show_code(ctx,texts,*,name_or_id):
    if ctx.author.id == config("USER_ID"):
        #if requested by id
        if "=> id" in name_or_id.lower():
            if find_codes(con,cur,texts)==None:
                msg=await ctx.send("**I'm Sorry, I Can't Find This Code, Error 404**")
                await asyncio.sleep(6)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(6)
            elif len(find_codes(con,cur,texts)) >= 1020:
                msg=await ctx.send("This Is Your Code For ID {}\n{}".format(texts,find_codes(con,cur,texts)))
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
            else:
                embed=discord.Embed(
                    name="Code",
                    colour=discord.Colour.dark_magenta()
                )
                embed.add_field(name="Code For ID => {}".format(texts),value='''
Your Code Is:
**{}**
                '''.format(find_codes(con,cur,texts)))
                embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Requested By {}".format(ctx.author),icon_url=ctx.author.avatar_url)
                msg=await ctx.send(embed=embed)
        
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
        #if requested by name
        elif "=> name" in name_or_id.lower():
            if find_codes(con,cur,texts)==None:
                msg=await ctx.send("**I'm Sorry, I Can't Find This Note, Error 404**")
                await asyncio.sleep(6)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(6)
            
            elif len(find_codes(con,cur,texts)) >= 1020:
                msg=await ctx.send("This Is Your Code For ID {}\n{}".format(texts,find_codes(con,cur,texts)))
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
            else:
                embed=discord.Embed(
                    name="Code",
                    colour=discord.Colour.dark_magenta()
                )
                embed.add_field(name="Code For Name => {}".format(texts),value='''
Your Code Is:
**{}**
                '''.format(find_codes(con,cur,texts)))
                embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Requested By {}".format(ctx.author),icon_url=ctx.author.avatar_url)
                msg=await ctx.send(embed=embed)
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
    else:
        msg=await ctx.send("**You Are Not Admin**")
        await asyncio.sleep(6)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(6)

@client.command(pass_context=True,aliases=["date-code","when-code"])
async def _date_code(ctx,texts,*,name_or_id):
    if ctx.author.id == config("USER_ID"):
        #if requested by id
        if "=> id" in name_or_id.lower():
            if find_code_by_date(con,cur,texts)==None:
                msg=await ctx.send("**I'm Sorry, I Can't Find This Note, Error 404**")
                await asyncio.sleep(6)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(6)
            elif len(find_code_by_date(con,cur,texts)) >= 1020:
                msg=await ctx.send("This Is Code For ID {}\n{}".format(texts,find_code_by_date(con,cur,texts)))
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
            else:
                embed=discord.Embed(
                    name="Code",
                    colour=discord.Colour.dark_magenta()
                )
                embed.add_field(name="Code For ID => {}".format(texts),value='''
Your Code Is:
**{}**
                '''.format(find_code_by_date(con,cur,texts)))
                embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Requested By {}".format(ctx.author),icon_url=ctx.author.avatar_url)
                msg=await ctx.send(embed=embed)
        
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
        #if requested by name
        elif "=> name" in name_or_id.lower():
            if find_code_by_date(con,cur,texts)==None:
                msg=await ctx.send("**I'm Sorry, I Can't Find This Note, Error 404**")
                await asyncio.sleep(6)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(6)
            elif len(find_code_by_date(con,cur,texts)) >= 1020:
                msg=await ctx.send("This Is Code For ID {}\n{}".format(texts,find_code_by_date(con,cur,texts)))
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
            else:
                embed=discord.Embed(
                    name="Code",
                    colour=discord.Colour.dark_magenta()
                )
                embed.add_field(name="Code For Name => {}".format(texts),value='''
Your Code Is:
**{}**
                '''.format(find_code_by_date(con,cur,texts)))
                embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Requested By {}".format(ctx.author),icon_url=ctx.author.avatar_url)
                msg=await ctx.send(embed=embed)
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
    else:
        msg=await ctx.send("**You Are Not Admin**")
        await asyncio.sleep(6)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(6)

#delete code
@client.command(pass_context=True,aliases=["delete-code","del-code"])
async def _delete_code(ctx,texts,*,name_or_id):
    if ctx.author.id == config("USER_ID"):
        if "=> id" in name_or_id.lower():
            if find_codes(con,cur,texts)==None:
                msg=await ctx.send("**I'm Sorry, I Can't Find This Note, Error 404**")
                await asyncio.sleep(6)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(6)
            else:
                embed=discord.Embed(
                    name="Delete",
                    colour=discord.Colour.dark_magenta()
                )
                embed.add_field(name="Code For ID => {}".format(texts),value='''
Your Code Is:
**{}**
                '''.format(find_codes(con,cur,texts)))
                embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Requested By {}".format(ctx.author),icon_url=ctx.author.avatar_url)
                msg=await ctx.send(embed=embed)
                delete_codes(con,cur,texts)
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
        #if requested by name
        elif "=> name" in name_or_id.lower():
            if find_codes(con,cur,texts)==None:
                msg=await ctx.send("**I'm Sorry, I Can't Find This Note, Error 404**")
                await asyncio.sleep(6)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(6)
            else:
                embed=discord.Embed(
                    name="Delete",
                    colour=discord.Colour.dark_magenta()
                )
                embed.add_field(name="Note Code Name => {}".format(texts),value='''
Your Code Is:
**{}**
                '''.format(find_codes(con,cur,texts)))
                embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Requested By {}".format(ctx.author),icon_url=ctx.author.avatar_url)
                msg=await ctx.send(embed=embed)
                delete_codes(con,cur,texts)
                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                await asyncio.sleep(30)
    else:
        msg=await ctx.send("**You Are Not Admin**")
        await asyncio.sleep(6)
        await msg.delete()
        await ctx.message.delete()
        await asyncio.sleep(6)


client.run("your token here")
if exit():
    con.close()
