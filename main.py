import discord
from discord.ext import commands
import inspect,ast,re
import requests
import datetime
from datetime import datetime , timedelta
now = datetime.now()
TOKEN = ""
#your bot token here
intents = discord.Intents.all()
color = 00000
client = commands.Bot(command_prefix = ".",intents = intents,help_command = None)

@client.event
async def on_ready():
    print(f"Connected to {client.user}")
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name=f'Listening to Transcations'))

#mobile status
def source(o):
    a = inspect.getsource(o).split("\n")
    indent = len(a[0]) - len(a[0].lstrip())
    return "\n".join(i[indent:] for i in a)


source_ = source(discord.gateway.DiscordWebSocket.identify)
patched = re.sub(r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])',
                 r"\1Discord Android\2", source_)
loc = {}
exec(compile(ast.parse(patched), "<string>", "exec"), discord.gateway.__dict__,
     loc)
discord.gateway.DiscordWebSocket.identify = loc["identify"]

#error handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Failed to execute this command\n`Missing requirements`\n`Try {ctx.command} <input>`')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'Failed to execute this command\n`Missing permissions`')
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'Failed to execute this command\n`This command is on a %.2fs cooldown`' %
                       error.retry_after)

#price for the coins
@client.command()
async def price(ctx, *, currency="bitcoin"):
    request = requests.get(
        f"https://api.coingecko.com/api/v3/coins/{currency}")
    if request.status_code == 200:
        request = request.json()
    
        embed = discord.Embed(title=f"{request['name']} Data",
                                  color=00000)
        embed.add_field(name="Scores",
                            value=f"""```
Coingecko score: {request['coingecko_score']}
Liquidity score: {request['liquidity_score']}
Developer score: {request['developer_score']}
Commuinity score: {request['community_score']}
```""",
                            inline=False)
        embed.add_field(name="Current Prices",
                            value=f"""```
USD: {'{:,}'.format(request['market_data']['current_price']['usd'])}
CAD: {'{:,}'.format(request['market_data']['current_price']['cad'])}
AUD: {'{:,}'.format(request['market_data']['current_price']['aud'])}
GBP: {'{:,}'.format(request['market_data']['current_price']['gbp'])}
EUR: {'{:,}'.format(request['market_data']['current_price']['eur'])}
```""",
                            inline=False)
        embed.add_field(name="Last 24h Price Change",
                            value=f"""```
USD: {'{:,}'.format(request['market_data']['price_change_24h_in_currency']['usd'])}
CAD: {'{:,}'.format(request['market_data']['price_change_24h_in_currency']['cad'])}
AUD: {'{:,}'.format(request['market_data']['price_change_24h_in_currency']['aud'])}
GBP: {'{:,}'.format(request['market_data']['price_change_24h_in_currency']['gbp'])}
EUR: {'{:,}'.format(request['market_data']['price_change_24h_in_currency']['eur'])}
```""",
                            inline=False)
        embed.set_thumbnail(url=request["image"]["large"])

        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed = discord.Embed(title = "Error occured",description = f"Couldnt Find a currency: `{currency}`\nPlease make sure u have spelled it right!",color = 00000))
#litecoin transcation finder
@client.command(aliases = ['ltc'])
async def litecoin(ctx,*,id):
    r = requests.get(f"https://api.blockcypher.com/v1/ltc/main/txs/{id}")

    if r.status_code == 200:
        request = r.json()
        height = request['block_height']
        addresses = request['addresses']
        total =  request['total']
        fees = request['fees']
        size = request['size']
        vsize = request['vsize']
        pref = request['preference']
        confirmations = request['confirmations']
        embed = discord.Embed(title = "Transaction Found",description = f"*Total* : `{total}`\n*height* : `{height}`\n*addresses* : `{addresses}`\n*fees* : `{fees}`\n*size* : `{size}`\n*vsize* : `{vsize}`\n*preferance* : `{pref}`\n*confirmations* : `{confirmations}`\n")
        await ctx.send(embed=embed)
    else:
        await ctx.send('id not found or wrong input')
#biecoin transcation finder
@client.command(aliases = ['btc'])
async def bitcoin(ctx,*,id):
    r = requests.get(f"https://api.blockcypher.com/v1/btc/main/txs/{id}")

    if r.status_code == 200:
        request = r.json()
        height = request['block_height']
        addresses = request['addresses']
        total =  request['total']
        fees = request['fees']
        size = request['size']
        vsize = request['vsize']
        pref = request['preference']
        confirmations = request['confirmations']
        embed = discord.Embed(title = "Transaction Found",description = f"*Total* : `{total}`\n*height* : `{height}`\n*addresses* : `{addresses}`\n*fees* : `{fees}`\n*size* : `{size}`\n*vsize* : `{vsize}`\n*preferance* : `{pref}`\n*confirmations* : `{confirmations}`\n")
        await ctx.send(embed=embed)
    else:
        await ctx.send('id not found or wrong input')
#eth transcation finder
@client.command(aliases = ['eth'])
async def ethereum(ctx,*,id):
    r = requests.get(f"https://api.blockcypher.com/v1/eth/main/txs/{id}")

    if r.status_code == 200:
        request = r.json()
        height = request['block_height']
        addresses = request['addresses']
        total =  request['total']
        fees = request['fees']
        size = request['size']
        vsize = request['vsize']
        pref = request['preference']
        confirmations = request['confirmations']
        embed = discord.Embed(title = "Transcation Found",description = f"*Total* : `{total}`\n*height* : `{height}`\n*addresses* : `{addresses}`\n*fees* : `{fees}`\n*size* : `{size}`\n*vsize* : `{vsize}`\n*preferance* : `{pref}`\n*confirmations* : `{confirmations}`\n")
        await ctx.send(embed=embed)
    else:
        await ctx.send('id not found or wrong input')   
#help select menu
class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Crypto",
                                 emoji="<:tick:939956831130898442>",  #edit this id
                                 description="Shows crypto Cmds"),
            discord.SelectOption(label="Info",
                                 emoji="<:tick:939956831130898442>", #edit this id
                                 description="Shows Info  Cmds")

        ]
        super().__init__(placeholder="Select an option",
                         max_values=1,
                         min_values=1,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        em1 = discord.Embed(
            title="Crypto",
            color=00000,
            description=
            "**• `price <cryptoname>`, `eth <transcation id>`, `btc <transcation id>`, `eth <transcation id>`**"
        )
        em2 = discord.Embed(
            color=color,
            title="Info commands",
            description=
            "**• `help`, `botinfo`,`ping`**"
        )

        if self.values[0] == "Crypto":
            await interaction.response.edit_message(embed=em1)
        elif self.values[0] == "Info":
            await interaction.response.edit_message(embed=em2)



class SelectView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(Select())


dot = ":skull:"  #edit these
reply = ":moyai:"  #edit these 
 
#help menu
@client.command()
@commands.cooldown(1, 5, commands.BucketType.guild)
async def help(ctx):
    embed = discord.Embed(
        color=color,
        title="Crypto Bot | Help",
        description=
        f" **Crypto** : `Shows Crypto commands`\n**Info** : `Shows other commands`\n\n"
    )
    embed.set_thumbnail(
        url=
        "https://images-ext-2.discordapp.net/external/jo-RdNad3jpMjtlVyP0L1Ub8Bba85opxbV79e7e_l_A/%3Fsize%3D512/https/cdn.discordapp.com/banners/765153748916895754/b02c275e7290db4ff85696aa17960dee.png"
    )
    embed.set_footer(text="Phantom#7777", icon_url="https://images-ext-2.discordapp.net/external/maSKb9KO2bdtykbCSdyk7KK8BxFZkR7y5CtxcSb0r08/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/765153748916895754/3f85eb216e723e388b75d2a9a4a06be1.png?width=663&height=663")

    embed.timestamp = datetime.now()
    await ctx.send(embed=embed, view=SelectView())
    
#botinfo menu
@client.command(aliases=['bi'])
@commands.cooldown(1, 5, commands.BucketType.guild)
async def botinfo(ctx):
    embed = discord.Embed(
        color=color,
        title="Crypto Bot | Info",
        description=
        f"**{dot} | Bot Name and Discrim\n | {client.user}\n\n  | Versions\n | Python - `3.8.12` |  Discord -  `2.0.1`\n\n  | Total Guilds\n  | `{len(client.guilds)}`\n\n {dot} | Total Users\n  | `{len(set(client.get_all_members()))}`\n\n  | Developer\n  | Phantom#6666**")

    await ctx.send(embed=embed)

#invite link
@client.command()
async def invite(ctx):
    embed = discord.Embed(title = "Invite Link",description= f"[Invite Link](https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot)")
    await ctx.send(embed=embed)
    
    
client.run(TOKEN)
