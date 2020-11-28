import discord
from discord import Member
from discord.ext import commands
from discord.utils import get
import pandas as pd
import numpy as np

from discord.ext import commands
from zipfile import BadZipFile


#Nickname   K   A   D   Diff    k/d Maps    Maps Won    Games   Games Won   Rounds  Rounds won  Coef    DRP     
#SVR    KPR Impact  RPG Rating  sand_rounds     sand_rounds_won     rust_rounds     rust_rounds_won     zone9_rounds    zone9_rounds_won    province_rounds province_rounds_won     




bot = commands.Bot(command_prefix='-')
p = pd.read_excel('f1.xlsx')
nicks = [] 
for i in range(len(p)):    
    nicks.append(p['Nick'][i])

c = list(p.columns)

c = c[:-1]
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

maps = ["Sandstone", "Rust", "Zone9", "Province"]






@bot.command()
async def stats(ctx, member: Member):
    p = pd.read_excel('f1.xlsx')
    nicks = [] 
    for i in range(len(p)):
        nicks.append(p['Nick'][i])
    c = list(p.columns)

    c = c[:-1]  
    output = ''
    nick = member.name
    if nick in nicks:
        npy = p.loc[p['Nick'] == nick].to_numpy()
        npy = npy[:, :-1]
        for i in range(len(c)):
            if c[i] in ["Nick", "K", "D", "SVR", "k/d", "Rating", "Maps", "Maps win rate", "Win rate on Sandstone", "Win rate on Rust", "Win rate on Zone 9", "Win rate on Province"]:
                output =  output + str(c[i]) + ": " + str(npy[0][i]) + '\n'
            embed = discord.Embed(title = 'Ваша персональная статистика', description = '**' +output+ '**', color = discord.Color.blue())
        await ctx.send(embed = embed)
    elif nick not in nicks:
        await ctx.send('Такого нет в дата базе')
    a = str(ctx.author.roles)
    a = a.split(',')
    idr = []
    for i in range(len(a)):
        k = a[i].split(' ') 
        if k[0]!='[<Role':
            del k[0]
                
        k1 = k[1].split('=')
        idr.append(k1[1])
        

    role = str()
    if "@everyone" in ctx.author.roles:
        print("oda")
@bot.command()
async def mystats(ctx): 
    p = pd.read_excel('f1.xlsx')
    nicks = [] 
    for i in range(len(p)):
        nicks.append(p['Nick'][i])
    c = list(p.columns)

    c = c[:-1]  
    output = ''
    nick = ctx.author.name
    if nick in nicks:   
        npy = p.loc[p['Nick'] == nick].to_numpy()
        npy = npy[:, :-1]
        for i in range(len(c)):
            if c[i] in ["Nick", "K", "D", "SVR", "k/d", "Rating", "Maps", "Maps win rate", "Win rate on Sandstone", "Win rate on Rust", "Win rate on Zone 9", "Win rate on Province"]:
                output =  output + str(c[i]) + ": " + str(npy[0][i]) + '\n'
            embed = discord.Embed(title = 'Ваша персональная статистика', description = '**' +output+ '**', color = discord.Color.blue())
        await ctx.send(embed = embed)    
    elif nick not in nicks:
        await ctx.send('Такого нет в дата базе')

@bot.command()
async def add(ctx, member: Member, arg):
    maps = ["Sandstone", "Rust", "Zone9", "Province"]
    p = pd.read_excel('f1.xlsx')
    nicks = [] 
    for i in range(len(p)):    
        nicks.append(p['Nick'][i])

    c = list(p.columns)

    c = c[:-1]
    j = -1
    adds = arg.split('-') 
    for i in range(len(adds)):          
        if i!=3:
            adds[i] = int(adds[i])
    nick = member.name
    if nick in nicks:
        for i in range(len(c)):
            if c[i] in ["K", "A", "D"]:
                j= j +1
                p.loc[p['Nick'] == nick, c[i]] = p.loc[p['Nick'] == nick, c[i]] + int(adds[j])
                
        p.loc[p['Nick'] == nick, 'Maps'] = p.loc[p['Nick'] == nick, 'Maps'] +1
        tr = adds[4] + adds[5]
        p.loc[p['Nick'] == nick, 'Rounds'] = p.loc[p['Nick'] == nick, 'Rounds']  +int(tr)
        p.loc[p['Nick'] == nick, 'Rounds won'] = p.loc[p['Nick'] == nick, 'Rounds won'] +adds[4]
    else:
        j = -1
        zr = pd.DataFrame(np.zeros((1, len(c))), columns = c)

        p = p.append(zr)
        p.iloc[len(p)-1, 0] = nick
        for i in range(len(c)):
            if c[i] in ["K", "A", "D"]:
                j= j +1
                p.loc[p['Nick'] == nick, c[i]] = p.loc[p['Nick'] == nick, c[i]] + int(adds[j])
                
        p.loc[p['Nick'] == nick, 'Maps'] = p.loc[p['Nick'] == nick, 'Maps'] +1
        tr = adds[4] + adds[5]
        p.loc[p['Nick'] == nick, 'Rounds'] = p.loc[p['Nick'] == nick, 'Rounds']  +int(tr)
        p.loc[p['Nick'] == nick, 'Rounds won'] = p.loc[p['Nick'] == nick, 'Rounds won'] +adds[4]

    if adds[4] > adds[5]:
        p.loc[p['Nick'] == nick, 'Maps won'] = p.loc[p['Nick'] == nick, 'Maps won'] +1


    
    if adds[3] == maps[0]:
        p.loc[p['Nick'] == nick, 'sr'] = p.loc[p['Nick'] == nick, 'sr'] + int(tr)
        p.loc[p['Nick'] == nick, 'srw'] = p.loc[p['Nick'] == nick, 'srw'] +int(adds[4])
        p.loc[p['Nick'] == nick, 'sm'] = p.loc[p['Nick'] == nick, 'sm'] +1
        if adds[4] > adds[5]:
            p.loc[p['Nick'] == nick, 'smw']= p.loc[p['Nick'] == nick, 'smw'] +1
        p.loc[p['Nick'] == nick, 'Win rate on Sandstone'] = round(p.loc[p['Nick'] == nick, 'smw']*100/p.loc[p['Nick'] == nick, 'sm'], 2)
    elif adds[3] == maps[1]:
        p.loc[p['Nick'] == nick, 'rr'] = p.loc[p['Nick'] == nick, 'rr'] +int(tr)
        p.loc[p['Nick'] == nick, 'rrw'] = p.loc[p['Nick'] == nick, 'rrw'] + int(adds[4])
        p.loc[p['Nick'] == nick, 'rm'] = p.loc[p['Nick'] == nick, 'rm'] +int(1)
        if adds[4] > adds[5]:
            p.loc[p['Nick'] == nick, 'rmw'] = p.loc[p['Nick'] == nick, 'rmw'] + 1
        p.loc[p['Nick'] == nick, 'Win rate on Rust'] = round(p.loc[p['Nick'] == nick, 'rmw']*100/p.loc[p['Nick'] == nick, 'rm'], 2)
    elif adds[3] == maps[2]:
        p.loc[p['Nick'] == nick, 'zr'] = p.loc[p['Nick'] == nick, 'zr'] +int(tr)
        p.loc[p['Nick'] == nick, 'zrw'] = p.loc[p['Nick'] == nick, 'zrw'] +int(adds[4])
        p.loc[p['Nick'] == nick, 'zm'] = p.loc[p['Nick'] == nick, 'zm'] +1  
        if adds[4] > adds[5]:   
            p.loc[p['Nick'] == nick, 'zmw']= p.loc[p['Nick'] == nick, 'zmw'] +1
        p.loc[p['Nick'] == nick, 'Win rate on Zone9'] = round(p.loc[p['Nick'] == nick, 'zmw']*100/p.loc[p['Nick'] == nick, 'zm'], 2)
    elif adds[3] == maps[3]:
        p.loc[p['Nick'] == nick, 'pr'] = p.loc[p['Nick'] == nick, 'pr'] +int(tr)
        p.loc[p['Nick'] == nick, 'prw'] = p.loc[p['Nick'] == nick, 'prw'] +int(adds[4])
        p.loc[p['Nick'] == nick, 'pm'] = p.loc[p['Nick'] == nick, 'pm'] +1
        if adds[4] > adds[5]:
            p.loc[p['Nick'] == nick, 'pmw']= p.loc[p['Nick'] == nick, 'pmw'] +1
        p.loc[p['Nick'] == nick, 'Win rate on Province'] = round(p.loc[p['Nick'] == nick, 'pmw']*100/p.loc[p['Nick'] == nick, 'pm'], 2)


    p.loc[p['Nick'] == nick, 'Maps win rate'] = round(100*p.loc[p['Nick'] == nick, 'Maps won']/p.loc[p['Nick'] == nick, 'Maps'], 2)
    p.loc[p['Nick'] == nick, 'Rounds win rate'] = round(100*p.loc[p['Nick'] == nick, 'Rounds won']/p.loc[p['Nick'] == nick, 'Rounds'], 2)

    p.loc[p['Nick'] == nick, 'Diff'] = 1
    p.loc[p['Nick'] == nick, 'k/d'] = 1
    p.loc[p['Nick'] == nick, 'DRP'] = 1
    p.loc[p['Nick'] == nick, 'SVR'] = 1
    p.loc[p['Nick'] == nick, 'KPR'] = 1
    p.loc[p['Nick'] == nick, 'Impact'] = 1
    drp = p.loc[p['Nick'] == nick, 'DRP'].astype(float)
    Impact = p.loc[p['Nick'] == nick, 'Impact'].astype(float)
    kpr = p.loc[p['Nick'] == nick, 'KPR'].astype(float)
    rw = p.loc[p['Nick'] == nick, 'Rounds win rate'].astype(float)
    p.loc[p['Nick'] == nick, 'RPG'] = 1
    rpg = 1

    maxround = p['Rounds'].max()
    
    p.loc[p['Nick'] == nick, 'Coef'] = 1
    coef = 1
    
    
    
    
    p.loc[p['Nick'] == nick, 'Rating'] = 1

    


    a = "Статистика " + str(nick) +" была обновленна!"
    with pd.ExcelWriter('f1.xlsx') as writer:
        p.to_excel(writer, index = False)
    embed = discord.Embed(title = a, color = discord.Color.blue())
    await ctx.send(embed = embed) 

bot.run('NzM1NzExNDE0OTE1ODI1Njc1.XxkOpg.R0KkSl7DaJnN8XlytrQRUKTPbKk')        
"""@commands.has_any_role(781542383904620574)"""