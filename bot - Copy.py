import discord
from discord.ext import commands
import random
import string
import time
import asyncio

TOKEN = "UR TOKEN HERE"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

licenses = {}
active_tickets = {}
user_levels = {}
user_xp = {}
user_warnings = {}

DURATION_DAYS = {
    "day": 1, "days": 1, "1day": 1,
    "week": 7, "weeks": 7, "1week": 7,
    "month": 30, "months": 30, "1month": 30,
    "year": 365, "years": 365, "1year": 365,
    "lifetime": 36500, "lt": 36500, "forever": 36500
}

PRICES = {
    "tweaker": {"day": 1, "week": 5, "month": 8, "year": 12, "lifetime": 15},
    "spoofer": {"day": 2, "week": 7, "month": 10, "year": 15, "lifetime": 20},
    "both": {"day": 3, "week": 10, "month": 15, "year": 25, "lifetime": 30}
}

SHOP_URL = "https://solidzshopp.netlify.app/"
TWEAKER_DOWNLOAD_URL = "https://github.com/solidz0239/SolidZ-Tweaker-Installer"
SPOOFER_DOWNLOAD_URL = "https://github.com/solidz0239/SolidZ-Spoofer"

def get_days(duration):
    return DURATION_DAYS.get(duration.lower(), 1)

def generate_license(license_type, duration):
    days = get_days(duration)
    key = "SOLIDZ-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    licenses[key] = {
        "type": license_type,
        "duration": duration,
        "days": days,
        "expiry": time.time() + days * 86400,
        "used": False,
        "used_by": None
    }
    return key

def is_owner(ctx):
    return ctx.author.id == 1500096157878059138

def is_staff(ctx):
    if not ctx.guild:
        return False
    staff_roles = ["👑 Sakura Owner", "⚙️ Blossom Admin", "🛡️ Head Petal", "🔧 Petal Mod", "🎫 Blossom Support"]
    for role_name in staff_roles:
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role and role in ctx.author.roles:
            return True
    return is_owner(ctx)

def get_level_role_name(level):
    emojis = {
        1: "🌱", 2: "🍃", 3: "🌿", 4: "🌸", 5: "🌼", 6: "🌻", 7: "🌺", 8: "🌷", 9: "🌹", 10: "🌳",
        11: "🍀", 12: "🍂", 13: "🍁", 14: "🌾", 15: "💮", 16: "🎋", 17: "🎍", 18: "🍃", 19: "🌱", 20: "🍎",
        21: "🍊", 22: "🍋", 23: "🍒", 24: "🍑", 25: "🥝", 26: "🥥", 27: "🥑", 28: "🍆", 29: "🥔", 30: "🥕",
        31: "🌽", 32: "🥦", 33: "🥒", 34: "🌶️", 35: "🧅", 36: "🧄", 37: "🥐", 38: "🥨", 39: "🥯", 40: "🍞",
        41: "🧀", 42: "🍖", 43: "🍗", 44: "🥩", 45: "🥓", 46: "🍔", 47: "🍟", 48: "🍕", 49: "🌭", 50: "🥪",
        51: "🌮", 52: "🌯", 53: "🥙", 54: "🧆", 55: "🥚", 56: "🍳", 57: "🥘", 58: "🍲", 59: "🥣", 60: "🥗",
        61: "🍿", 62: "🧈", 63: "🧂", 64: "🥫", 65: "🍱", 66: "🍘", 67: "🍙", 68: "🍚", 69: "🍛", 70: "🍜",
        71: "🍝", 72: "🍠", 73: "🍢", 74: "🍣", 75: "🍤", 76: "🍥", 77: "🥮", 78: "🍡", 79: "🥟", 80: "🥠",
        81: "🥡", 82: "🍦", 83: "🍧", 84: "🍨", 85: "🍩", 86: "🍪", 87: "🎂", 88: "🍰", 89: "🧁", 90: "🥧",
        91: "🍫", 92: "🍬", 93: "🍭", 94: "🍮", 95: "🍯", 96: "🍼", 97: "🥛", 98: "☕", 99: "🍵", 100: "🏆"
    }
    return f"{emojis.get(level, '⭐')} Lvl {level}"

@bot.event
async def on_ready():
    print(f"🌸 Sakura Bot Online: {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="🌸 !cmds"))

@bot.event
async def on_member_join(member):
    unverified_role = discord.utils.get(member.guild.roles, name="🚫 Unverified")
    if unverified_role:
        await member.add_roles(unverified_role)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if not isinstance(message.channel, discord.DMChannel) and message.guild:
        user_id = str(message.author.id)
        if user_id not in user_xp:
            user_xp[user_id] = 0
            user_levels[user_id] = 0
        
        user_xp[user_id] += random.randint(5, 15)
        xp_needed = (user_levels[user_id] + 1) * 100
        
        if user_xp[user_id] >= xp_needed:
            user_levels[user_id] += 1
            user_xp[user_id] = 0
            level = user_levels[user_id]
            
            role_name = get_level_role_name(level)
            role = discord.utils.get(message.guild.roles, name=role_name)
            if role and role not in message.author.roles:
                await message.author.add_roles(role)
    
    if isinstance(message.channel, discord.DMChannel):
        if message.content.startswith("!activate"):
            parts = message.content.split()
            if len(parts) != 2:
                await message.channel.send("🌸 Usage: !activate YOUR-KEY")
                return
            
            key = parts[1].upper()
            if key not in licenses:
                await message.channel.send("❌ Invalid key!")
                return
            
            data = licenses[key]
            if data["used"]:
                await message.channel.send("❌ Already used!")
                return
            if time.time() > data["expiry"]:
                await message.channel.send("❌ Expired!")
                return
            
            data["used"] = True
            data["used_by"] = message.author.id
            
            for guild in bot.guilds:
                member = guild.get_member(message.author.id)
                if member:
                    uv = discord.utils.get(guild.roles, name="🚫 Unverified")
                    if uv and uv in member.roles:
                        await member.remove_roles(uv)
                    
                    v = discord.utils.get(guild.roles, name="✅ Verified")
                    if v:
                        await member.add_roles(v)
                    
                    m = discord.utils.get(guild.roles, name="🌸 Member")
                    if m:
                        await member.add_roles(m)
                    
                    t = data["type"].lower()
                    if t == "tweaker":
                        b = discord.utils.get(guild.roles, name="🌸 Tweaker")
                        a = discord.utils.get(guild.roles, name="🎮 Tweaker Access")
                        if b:
                            await member.add_roles(b)
                        if a:
                            await member.add_roles(a)
                    elif t == "spoofer":
                        b = discord.utils.get(guild.roles, name="⚔️ Spoofer")
                        a = discord.utils.get(guild.roles, name="🛡️ Spoofer Access")
                        if b:
                            await member.add_roles(b)
                        if a:
                            await member.add_roles(a)
                    break
            
            days_left = int((data["expiry"] - time.time()) / 86400)
            embed = discord.Embed(title="✅ ACTIVATED! 🌸", color=0x00ff00)
            embed.add_field(name="Product", value=data["type"].upper())
            embed.add_field(name="Duration", value=data["duration"].upper())
            embed.add_field(name="Days Left", value=str(days_left))
            await message.channel.send(embed=embed)
            return
        
        await message.channel.send("🌸 **SolidZ Sakura Bot** 🌸\nActivate: `!activate KEY`\nBuy: `!buy`")
        return
    
    await bot.process_commands(message)

# ========== COMMANDS ==========

@bot.command(name="cmds")
async def cmds(ctx):
    e = discord.Embed(title="🌸 Sakura Commands 🌸", color=0xff69b4)
    e.add_field(name="🔑 License", value="`!activate` `!status` `!gen` `!prices`", inline=False)
    e.add_field(name="🎮 Products", value="`!tweaker` `!spoofer` `!buy`", inline=False)
    e.add_field(name="📊 Levels", value="`!rank` `!leaderboard`", inline=False)
    e.add_field(name="🎫 Support", value="`!ticket` `!close` `!verify`", inline=False)
    e.add_field(name="👑 Staff", value="`!kick` `!ban` `!clear`", inline=False)
    e.add_field(name="👑 Owner", value="`!reset` `!wiperoles` `!fullsetup` `!shutdown` `!shoplink`", inline=False)
    await ctx.send(embed=e)

@bot.command(name="shoplink")
async def shoplink(ctx):
    embed = discord.Embed(title="💚 SOLIDZ SHOP 💚", color=0x00ff00)
    embed.add_field(name="🛒 Purchase Licenses", value=f"[Click here to open the shop]({SHOP_URL})", inline=False)
    embed.add_field(name="🔧 Tweaker", value="Day: $3 | Week: $10 | Month: $20 | Year: $60 | Lifetime: $100", inline=False)
    embed.add_field(name="🛡️ Spoofer", value="Day: $7 | Week: $15 | Month: $25 | Year: $65 | Lifetime: $85", inline=False)
    embed.add_field(name="💎 Both", value="Day: €7 | Week: €15 | Month: €25 | Year: €110 | Lifetime: €150", inline=False)
    embed.set_footer(text="🌸 SolidZ - Your trusted gaming enhancement provider")
    await ctx.send(embed=embed)

@bot.command(name="ticket")
async def ticket_command(ctx, *, reason="Support"):
    if ctx.author.id in active_tickets:
        ch = bot.get_channel(active_tickets[ctx.author.id])
        if ch:
            return await ctx.send(f"🌸 You already have a ticket: {ch.mention}")
    
    cat = discord.utils.get(ctx.guild.categories, name="🎫 TICKETS")
    if not cat:
        cat = await ctx.guild.create_category("🎫 TICKETS")
    
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, view_channel=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True)
    }
    
    staff_roles = ["👑 Sakura Owner", "⚙️ Blossom Admin", "🛡️ Head Petal", "🔧 Petal Mod", "🎫 Blossom Support"]
    for role_name in staff_roles:
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True)
    
    channel_name = f"🌸ticket-{ctx.author.name}".lower()
    ticket_channel = await ctx.guild.create_text_channel(channel_name, category=cat, overwrites=overwrites)
    active_tickets[ctx.author.id] = ticket_channel.id
    
    embed = discord.Embed(title=f"🌸 {reason} Ticket Created 🌸", color=0xff69b4)
    embed.add_field(name="Customer", value=ctx.author.mention)
    embed.add_field(name="Reason", value=reason)
    embed.add_field(name="Instructions", value="Staff will assist you shortly.\nType `!close` to close this ticket.")
    await ticket_channel.send(embed=embed)
    await ctx.send(f"🌸 Ticket created: {ticket_channel.mention}")

@bot.command(name="gen")
async def gen(ctx, typ=None, duration=None):
    if not is_owner(ctx):
        return await ctx.send("👑 Owner only!")
    
    if not typ or not duration:
        e = discord.Embed(title="🌸 License Generator 🌸", color=0xff69b4)
        e.add_field(name="Usage", value="`!gen <product> <duration>`", inline=False)
        e.add_field(name="Products", value="`tweaker` `spoofer` `both`", inline=False)
        e.add_field(name="Durations", value="`day` `week` `month` `year` `lifetime`", inline=False)
        await ctx.send(embed=e)
        return
    
    typ = typ.lower()
    duration = duration.lower()
    
    if typ not in ["tweaker", "spoofer", "both"]:
        return await ctx.send("❌ Invalid product!")
    
    if duration not in DURATION_DAYS:
        return await ctx.send("❌ Invalid duration!")
    
    key = generate_license(typ, duration)
    days = get_days(duration)
    
    embed = discord.Embed(title="🌸 License Generated 🌸", color=0x00ff00)
    embed.add_field(name="🔑 Key", value=f"```{key}```", inline=False)
    embed.add_field(name="📦 Product", value=typ.upper(), inline=True)
    embed.add_field(name="⏰ Duration", value=duration.upper(), inline=True)
    embed.add_field(name="📅 Days", value=str(days), inline=True)
    await ctx.send(embed=embed)

@bot.command(name="status")
async def status(ctx):
    for k, d in licenses.items():
        if d.get("used_by") == ctx.author.id:
            days_left = int((d["expiry"] - time.time()) / 86400)
            if days_left > 0:
                embed = discord.Embed(title="🌸 License Status 🌸", color=0x00ff00)
                embed.add_field(name="Product", value=d["type"].upper(), inline=True)
                embed.add_field(name="Duration", value=d["duration"].upper(), inline=True)
                embed.add_field(name="Days Left", value=str(days_left), inline=True)
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Your license has expired! 🌸")
            return
    await ctx.send("❌ No active license! Buy with `!buy` 🌸")

@bot.command(name="prices")
async def prices(ctx):
    embed = discord.Embed(title="🌸 Sakura Prices 🌸", color=0xff69b4)
    tweaker = "\n".join([f"• {k.upper()}: ${v}" for k, v in PRICES["tweaker"].items()])
    spoofer = "\n".join([f"• {k.upper()}: ${v}" for k, v in PRICES["spoofer"].items()])
    both = "\n".join([f"• {k.upper()}: ${v}" for k, v in PRICES["both"].items()])
    embed.add_field(name="🌸 Tweaker", value=tweaker, inline=True)
    embed.add_field(name="⚔️ Spoofer", value=spoofer, inline=True)
    embed.add_field(name="💎 Both", value=both, inline=True)
    embed.add_field(name="🛒 Shop", value=f"[Click here to buy]({SHOP_URL})", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="buy")
async def buy(ctx, product=None, duration=None):
    if not product or not duration:
        embed = discord.Embed(title="🌸 How to Buy 🌸", color=0xff69b4)
        embed.add_field(name="🛒 Website", value=f"[Click here to buy securely]({SHOP_URL})", inline=False)
        embed.add_field(name="Usage", value="`!buy <product> <duration>`", inline=False)
        embed.add_field(name="Products", value="`tweaker` `spoofer` `both`", inline=False)
        embed.add_field(name="Durations", value="`day` `week` `month` `year` `lifetime`", inline=False)
        embed.add_field(name="Alternative", value="Type `!ticket I want to buy` to purchase via staff", inline=False)
        await ctx.send(embed=embed)
        return
    
    product = product.lower()
    duration = duration.lower()
    
    if product not in PRICES:
        return await ctx.send("❌ Invalid product!")
    
    if duration not in PRICES[product]:
        return await ctx.send("❌ Invalid duration!")
    
    price = PRICES[product][duration]
    
    embed = discord.Embed(title="🌸 Purchase Request 🌸", color=0xff69b4)
    embed.add_field(name="Product", value=product.upper(), inline=True)
    embed.add_field(name="Duration", value=duration.upper(), inline=True)
    embed.add_field(name="Price", value=f"${price}", inline=True)
    embed.add_field(name="🛒 Complete Purchase", value=f"[Buy now on our website]({SHOP_URL})", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="spoofer")
async def spoofer(ctx):
    e = discord.Embed(title="⚔️ SolidZ Spoofer ⚔️", color=0x6c5ce7)
    e.add_field(name="📥 Download", value=f"[Click Here]({SPOOFER_DOWNLOAD_URL})", inline=False)
    e.add_field(name="🔧 Features", value="• HWID Spoofing\n• Serial Spoofing\n• MAC Spoofing", inline=False)
    e.add_field(name="🛒 Buy", value=f"[Purchase License]({SHOP_URL})", inline=False)
    await ctx.send(embed=e)

@bot.command(name="tweaker")
async def tweaker(ctx):
    e = discord.Embed(title="🌸 SolidZ Tweaker 🌸", color=0xff69b4)
    e.add_field(name="📥 Download", value=f"[Click Here]({TWEAKER_DOWNLOAD_URL})", inline=False)
    e.add_field(name="🚀 Features", value="• FPS Boost (+30-50)\n• Ping Reduction\n• Game Optimization", inline=False)
    e.add_field(name="🛒 Buy", value=f"[Purchase License]({SHOP_URL})", inline=False)
    await ctx.send(embed=e)

@bot.command(name="rank")
async def rank(ctx, member=None):
    target = member or ctx.author
    if isinstance(target, str):
        try:
            target = await commands.MemberConverter().convert(ctx, target)
        except:
            target = ctx.author
    
    uid = str(target.id)
    lvl = user_levels.get(uid, 0)
    xp = user_xp.get(uid, 0)
    needed = 100
    
    e = discord.Embed(title=f"🌸 {target.name}'s Rank 🌸", color=0xff69b4)
    e.add_field(name="📈 Level", value=str(lvl), inline=True)
    e.add_field(name="✨ XP", value=f"{xp}/{needed}", inline=True)
    bar = "🌸" * min(20, int(xp/5)) + "🌿" * (20 - min(20, int(xp/5)))
    e.add_field(name="📊 Progress", value=bar, inline=False)
    await ctx.send(embed=e)

@bot.command(name="leaderboard")
async def leaderboard(ctx):
    top = sorted(user_levels.items(), key=lambda x: x[1], reverse=True)[:10]
    e = discord.Embed(title="🏆 Sakura Leaderboard 🏆", color=0xffd700)
    for i, (uid, lvl) in enumerate(top, 1):
        try:
            u = await bot.fetch_user(int(uid))
            name = u.name[:15]
        except:
            name = "Unknown"
        medal = ["👑", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
        e.add_field(name=f"{medal} {name}", value=f"Level {lvl}", inline=False)
    await ctx.send(embed=e)

@bot.command(name="close")
async def close(ctx):
    if not ctx.channel.name.startswith("🌸ticket-"):
        return await ctx.send("🌸 This command only works in ticket channels!")
    
    for uid, cid in list(active_tickets.items()):
        if cid == ctx.channel.id:
            del active_tickets[uid]
            break
    
    await ctx.channel.delete()

@bot.command(name="verify")
async def verify(ctx):
    if ctx.channel.name != "verify":
        return await ctx.send("🌸 Please use the #verify channel!")
    
    uv = discord.utils.get(ctx.guild.roles, name="🚫 Unverified")
    v = discord.utils.get(ctx.guild.roles, name="✅ Verified")
    m = discord.utils.get(ctx.guild.roles, name="🌸 Member")
    
    if v and v in ctx.author.roles:
        return await ctx.send("🌸 You are already verified!")
    
    if uv and uv in ctx.author.roles:
        await ctx.author.remove_roles(uv)
    if v:
        await ctx.author.add_roles(v)
    if m:
        await ctx.author.add_roles(m)
    
    await ctx.send("✅ Verified! Welcome to Sakura Garden! 🌸")

@bot.command(name="kick")
async def kick(ctx, member: discord.Member, *, reason=None):
    if not is_staff(ctx):
        return await ctx.send("❌ Only staff can use this command!")
    await member.kick(reason=reason)
    await ctx.send(f"✅ Kicked {member.mention}")

@bot.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason=None):
    if not is_staff(ctx):
        return await ctx.send("❌ Only staff can use this command!")
    await member.ban(reason=reason)
    await ctx.send(f"✅ Banned {member.mention}")

@bot.command(name="clear")
async def clear(ctx, amount: int):
    if not is_staff(ctx):
        return await ctx.send("❌ Only staff can use this command!")
    amount = min(amount, 100)
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"✅ Cleared {amount} messages", delete_after=3)

@bot.command(name="shutdown")
async def shutdown(ctx):
    if not is_owner(ctx):
        return await ctx.send("👑 Owner only!")
    await ctx.send("🌸 Shutting down bot...")
    await bot.close()

# ========== WIPE ROLES COMMAND ==========
@bot.command(name="wiperoles")
async def wipe_roles(ctx):
    if not is_owner(ctx):
        return await ctx.send("👑 **Owner only!**")
    
    await ctx.send("⚠️ **WARNING: This will delete ALL roles in the server (except @everyone)!** ⚠️")
    await ctx.send("Type `CONFIRM WIPE` within 30 seconds to proceed.")
    
    def check(m):
        return m.author == ctx.author and m.content == "CONFIRM WIPE"
    
    try:
        await bot.wait_for('message', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        return await ctx.send("❌ Role wipe cancelled - timeout.")
    
    await ctx.send("🗑️ **Wiping all roles...**")
    g = ctx.guild
    
    roles_deleted = 0
    for role in g.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                roles_deleted += 1
                await asyncio.sleep(0.2)
            except:
                pass
    
    await ctx.send(f"✅ **Deleted {roles_deleted} roles!**")
    await ctx.send("🎉 All roles have been wiped! Use `!fullsetup` to create new ones.")

# ========== RESET COMMAND (PRESERVES PAYMENT) ==========
@bot.command(name="reset")
async def reset_server(ctx):
    if not is_owner(ctx):
        return await ctx.send("👑 **Owner only!**")
    
    await ctx.send("⚠️ **WARNING: This will delete ALL channels, categories, and roles EXCEPT the 💵 PAYMENT category and payment channel!** ⚠️")
    await ctx.send("Type `CONFIRM RESET` within 30 seconds to proceed.")
    
    def check(m):
        return m.author == ctx.author and m.content == "CONFIRM RESET"
    
    try:
        await bot.wait_for('message', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        return await ctx.send("❌ Reset cancelled.")
    
    await ctx.send("🗑️ **Cleaning server (preserving 💵 PAYMENT)...**")
    g = ctx.guild
    
    protected_category_names = ["💵 PAYMENT", "💰 STORE"]
    protected_channel_names = ["payment", "💵 payment", "💰 pricing", "📖 how-to-buy"]
    
    for channel in g.channels:
        if channel.name not in protected_channel_names:
            try:
                await channel.delete()
                await asyncio.sleep(0.1)
            except:
                pass
    
    for category in g.categories:
        if category.name not in protected_category_names:
            try:
                await category.delete()
                await asyncio.sleep(0.1)
            except:
                pass
    
    for role in g.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                await asyncio.sleep(0.1)
            except:
                pass
    
    await ctx.send("🎉 **Server cleaned! 💵 PAYMENT category and payment channel were preserved!**")
    await ctx.send("Use `!fullsetup` to create everything else!")

# ========== FULL SETUP ==========
@bot.command(name="fullsetup")
async def full_setup(ctx):
    if not is_owner(ctx):
        return await ctx.send("👑 Owner only!")
    
    await ctx.send("🌸 **Starting FULL server creation with EMOJI LEVEL ROLES!** 🌸")
    await ctx.send("⏰ **This will take 10-15 minutes. Please wait...**")
    
    g = ctx.guild
    
    # Create basic roles
    unverified = await g.create_role(name="🚫 Unverified", color=discord.Color.dark_gray())
    await ctx.send("✅ Created 🚫 Unverified")
    await asyncio.sleep(0.5)
    
    verified = await g.create_role(name="✅ Verified", color=discord.Color.green())
    await ctx.send("✅ Created ✅ Verified")
    await asyncio.sleep(0.5)
    
    member = await g.create_role(name="🌸 Member", color=discord.Color.from_rgb(255, 182, 193))
    await ctx.send("✅ Created 🌸 Member")
    await asyncio.sleep(0.5)
    
    owner = await g.create_role(name="👑 Sakura Owner", color=discord.Color.gold())
    await ctx.send("✅ Created 👑 Sakura Owner")
    await asyncio.sleep(0.5)
    
    admin = await g.create_role(name="⚙️ Blossom Admin", color=discord.Color.red())
    await ctx.send("✅ Created ⚙️ Blossom Admin")
    await asyncio.sleep(0.5)
    
    mod = await g.create_role(name="🛡️ Head Petal", color=discord.Color.orange())
    await ctx.send("✅ Created 🛡️ Head Petal")
    await asyncio.sleep(0.5)
    
    support = await g.create_role(name="🎫 Blossom Support", color=discord.Color.blue())
    await ctx.send("✅ Created 🎫 Blossom Support")
    await asyncio.sleep(0.5)
    
    tweak_access = await g.create_role(name="🎮 Tweaker Access", color=discord.Color.green())
    await ctx.send("✅ Created 🎮 Tweaker Access")
    await asyncio.sleep(0.5)
    
    spoof_access = await g.create_role(name="🛡️ Spoofer Access", color=discord.Color.dark_green())
    await ctx.send("✅ Created 🛡️ Spoofer Access")
    await asyncio.sleep(0.5)
    
    vet70 = await g.create_role(name="🏆 Veteran 70+", color=discord.Color.gold())
    await ctx.send("✅ Created 🏆 Veteran 70+")
    await asyncio.sleep(0.5)
    
    elite80 = await g.create_role(name="👑 Elite 80+", color=discord.Color.dark_gold())
    await ctx.send("✅ Created 👑 Elite 80+")
    await asyncio.sleep(0.5)
    
    tweaker_role = await g.create_role(name="🌸 Tweaker", color=discord.Color.from_rgb(255, 105, 180))
    await ctx.send("✅ Created 🌸 Tweaker")
    await asyncio.sleep(0.5)
    
    spoofer_role = await g.create_role(name="⚔️ Spoofer", color=discord.Color.from_rgb(108, 92, 231))
    await ctx.send("✅ Created ⚔️ Spoofer")
    await asyncio.sleep(0.5)
    
    # Create level roles with EMOJIS
    await ctx.send("📝 Creating level roles with EMOJIS (Lvl 100 to Lvl 1)...")
    
    level_emojis = {
        1: "🌱", 2: "🍃", 3: "🌿", 4: "🌸", 5: "🌼", 6: "🌻", 7: "🌺", 8: "🌷", 9: "🌹", 10: "🌳",
        11: "🍀", 12: "🍂", 13: "🍁", 14: "🌾", 15: "💮", 16: "🎋", 17: "🎍", 18: "🍃", 19: "🌱", 20: "🍎",
        21: "🍊", 22: "🍋", 23: "🍒", 24: "🍑", 25: "🥝", 26: "🥥", 27: "🥑", 28: "🍆", 29: "🥔", 30: "🥕",
        31: "🌽", 32: "🥦", 33: "🥒", 34: "🌶️", 35: "🧅", 36: "🧄", 37: "🥐", 38: "🥨", 39: "🥯", 40: "🍞",
        41: "🧀", 42: "🍖", 43: "🍗", 44: "🥩", 45: "🥓", 46: "🍔", 47: "🍟", 48: "🍕", 49: "🌭", 50: "🥪",
        51: "🌮", 52: "🌯", 53: "🥙", 54: "🧆", 55: "🥚", 56: "🍳", 57: "🥘", 58: "🍲", 59: "🥣", 60: "🥗",
        61: "🍿", 62: "🧈", 63: "🧂", 64: "🥫", 65: "🍱", 66: "🍘", 67: "🍙", 68: "🍚", 69: "🍛", 70: "🍜",
        71: "🍝", 72: "🍠", 73: "🍢", 74: "🍣", 75: "🍤", 76: "🍥", 77: "🥮", 78: "🍡", 79: "🥟", 80: "🥠",
        81: "🥡", 82: "🍦", 83: "🍧", 84: "🍨", 85: "🍩", 86: "🍪", 87: "🎂", 88: "🍰", 89: "🧁", 90: "🥧",
        91: "🍫", 92: "🍬", 93: "🍭", 94: "🍮", 95: "🍯", 96: "🍼", 97: "🥛", 98: "☕", 99: "🍵", 100: "🏆"
    }
    
    for i in range(100, 0, -1):
        try:
            emoji = level_emojis.get(i, "⭐")
            role_name = f"{emoji} Lvl {i}"
            
            if i >= 90:
                color = discord.Color.from_rgb(255, 215, 0)
            elif i >= 70:
                color = discord.Color.purple()
            elif i >= 50:
                color = discord.Color.blue()
            elif i >= 30:
                color = discord.Color.teal()
            elif i >= 10:
                color = discord.Color.green()
            else:
                color = discord.Color.light_gray()
            
            await g.create_role(name=role_name, color=color)
            if i % 20 == 0:
                await ctx.send(f"✅ Created levels down to {emoji} Lvl {i}")
            await asyncio.sleep(0.15)
        except:
            pass
    
    await ctx.send("✅ **ALL EMOJI LEVEL ROLES CREATED!**")
    await asyncio.sleep(2)
    
    # Create verify channel
    verify