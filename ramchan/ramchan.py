import discord
from news import newscmd
from discord.ext import commands
import datetime
import json
import pathlib
import asyncio
import pyrebase
from anime import ani
import asyncio
from maw import Maw
from maloauth import oauth
import datetime
from beta import some
import requests

firebaseConfig = {
    "apiKey": "AIzaSyB_WdkwbOyAbq_H4CcZ7eZCRtWznlyzwFQ",
    "authDomain": "fall-of-lion.firebaseapp.com",
    "databaseURL": "https://fall-of-lion-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "fall-of-lion",
    "storageBucket": "fall-of-lion.appspot.com",
    "messagingSenderId": "937498383180",
    "appId": "1:937498383180:web:db9e1439daa93bfb81f5e9",
    "measurementId": "G-YK5EWRS4TR"
  }
firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()
#--------bot--------|
prefix='ram '
async def get_pre(bot, message):
	return ['ram ', 'RAM ', 'rAM ', 'raM ', 'Ram ', 'RAm ', 'RaM ', 'rAm ']
ram = commands.Bot(command_prefix=get_pre, case_insensitive=True)
ram.remove_command('help')
#--------contants & vars--------|
global channels
channels = []
#--------loop--------

async def NewsLoop():
	llist = newscmd.news_links(db)
	if llist:
		data=db.child("servers").order_by_child("NewsChannelId").get()
		data=data.val()
		for i in llist:
			title, content, img_link, news_link= newscmd.news_link_parser(i)

			emb = discord.Embed(title='Anime • Manga News',color=discord.Color.from_rgb(255,182,193))
			emb.add_field(name=f"__**~~{'――'*8}~~**__",value=f"**[{title}:]({news_link})**\n{content}\n__**~~{'――'*8}~~**__")
			emb.set_footer(text='Source Anime News Network')
			emb.set_thumbnail(url=ram.user.avatar_url)
			emb.set_image(url=img_link)
			for sub_guild in data:
				for server in data[sub_guild]:
					d1=data[sub_guild][server]
					if d1["NewsChannelId"]!="None":
						channel = ram.get_channel(int(data[sub_guild][server]["NewsChannelId"]))
						if channel.permissions_for(channel.guild.me).send_messages:
							await channel.send(embed=emb)


async def EpiReviewLoop():
	links = newscmd.epiIdGrabber(db)
	if links:
		data=db.child("servers").order_by_child("NewsChannelId").get()
		data=data.val()
		for link in links:
			title, content, img_link, news_link= newscmd.news_link_parser(link)
			emb = discord.Embed(title='Anime Episode Review',color=discord.Color.from_rgb(255,182,193))
			emb.add_field(name=f"-------------------------------------------------------------",value=f"**[{title}:]({news_link})**\n{content}\n**-------------------------------------------------------------**")
			emb.set_footer(text='Source Anime News Network')
			emb.set_thumbnail(url=ram.user.avatar_url)
			emb.set_image(url=img_link)
			for sub_guild in data:
				for server in data[sub_guild]:
					d1=data[sub_guild][server]
					if d1["EpiRevChannelId"]!="None":
						channel = ram.get_channel(int(data[sub_guild][server]["EpiRevChannelId"]))
						if channel.permissions_for(channel.guild.me).send_messages:
							await channel.send(embed=emb)

async def MainLoop():
	await NewsLoop()
	await EpiReviewLoop()
	print('going to sleep for 6mins')
	await asyncio.sleep(360)
	await MainLoop()

@ram.event
async def on_ready():
	print('Konnichiwa Imoto san!')
	await ram.change_presence(activity=discord.Game('with Rem chan'))
	await MainLoop()

@ram.event
async def on_guild_join(guild):
	dic={'DarkTheme':False,
'NewsChannelId':'None',
'EpiRevChannelId':'None'
	}
	db.child('servers').child(str(guild.id)[:2]).child(guild.id).set(dic)

@ram.event
async def on_guild_remove(guild):
	data=db.child("servers").child(str(guild.id)[:2]).child(guild.id).remove()
	log = ram.get_channel(820280868479303730)
	await log.send(f"Bot was kicked/banned from {guild.name}({guild.id})")


@ram.event
async def on_guild_channel_delete(newschannel):
	guild=newschannel.guild
	data=db.child("servers").child(str(guild.id)[:2]).child(guild.id).get()
	data=data.val()
	for prop in data:
		if data[prop]==str(newschannel.id):
			db.child("servers").child(str(guild.id)[:2]).child(guild.id).update({prop:"None"})
			log = ram.get_channel(820280868479303730)
			await log.send(f"newchannel {newschannel.name} was deleted, updated channel dict")
			break

@ram.command()
async def help(ctx):
	emb = discord.Embed(
		title='Help Section',
		description=f'''
		This message shows usage of this bot's commands''',
		color=discord.Color.from_rgb(255,182,193))
	emb.set_thumbnail(url=ram.user.avatar_url)
	emb.set_footer(text='Rem ♡ Ram')
	emb.add_field(name='Bot prefix', value=f'`{prefix}`', inline=False)
	emb.add_field(name=f'{prefix}ping', inline=False,value=f'''
		_Shows bot's current ping_
		`Ex:{prefix}ping`''')
	emb.add_field(name=f'{prefix}status', inline=False,value=f'''
		_Changes bot's playing status_
		Type the status after the command
		`Ex:{prefix}status with Rem chan`''')
	emb.add_field(name=f'{prefix}set' ,inline=False ,value=f'''
		_Used to set a channel as posting channel_
		_Available channel type is only_ `news and review` _for the time being_
		Type the channel type and channel you want the bot to set as posting channel
		`Ex:{prefix}set newschannel #channel`''')

	await ctx.send(embed=emb)

def RemCheck(ctx):
	if ctx.author.id == 547277685433303040 or ctx.author.id == 656543188969848863:
		return True

@ram.command()
async def todo(ctx, operator, *, stuff=None):
	data=db.child('private').child(ctx.author.id).child('list').get()
	data=data.val()
	operators = ['add','remove','list','format','edit']
	if operator in operators:
		if data==None and operator!='add':
			await ctx.send('your list is empty, use `ram todo add [something]` to add')
		else:
			if operator=='add':
				if stuff==None:
					await ctx.send('what should I add dumbass <:nnav1:810481099045077013>')
				else:
					stuff=stuff.replace('`','')
					if data!=None:
						data.append(stuff)
						db.child('private').child(ctx.author.id).update({'list':data})
						to_send='\n-'.join(data)
						emb=discord.Embed(title='To Do List', description=f'```-{to_send}```', color=discord.Color.from_rgb(255,182,193))
						await ctx.send(embed=emb)
					else:
						db.child('private').child(ctx.author.id).set({'list':[stuff]})
						emb=discord.Embed(title='To Do List', description=f'```-{stuff}```', color=discord.Color.from_rgb(255,182,193))
						await ctx.send(embed=emb)
			elif operator=='list':
				to_send='\n-'.join(data)
				emb=discord.Embed(title='To Do List', description=f'```-{to_send}```', color=discord.Color.from_rgb(255,182,193))
				await ctx.send(embed=emb)

			elif operator=='remove':
				if stuff==None:
					await ctx.send('what should I remove <:nnav1:810481099045077013>')
				else:
					for things in data:
						if things.count(stuff)>0:
							data.remove(things)
					to_send='\n-'.join(data)
					db.child('private').child(ctx.author.id).update({'list':data})
					if to_send == '':
						await ctx.send('list is empty')
					else:
						emb=discord.Embed(title='To Do List', description=f'```-{to_send}```', color=discord.Color.from_rgb(255,182,193))
						await ctx.send(embed=emb)
			elif operator=='format':
				db.child('private').child(ctx.author.id).update({'list':[]})
				await ctx.send('list cleared!')
			elif operator=='edit':
				if stuff==None:
					await ctx.send('what should I edit <:nnav1:810481099045077013>')
				else:
					try:
						stuff , app = stuff.split(',')
					except:
						await ctx.send('Please use a `,` to distinguish between which item you want to edit and what you want to edit it to \n Ex:`ram todo edit Re:Zero, watch Re:Zero season 2`')
						return
					stuff=stuff.replace('`','')
					app=app.replace('`','')
					for things in data:
						if things.count(stuff)>0:
							data.remove(things)
							data.append(app)
					to_send='\n-'.join(data)
					db.child('private').child(ctx.author.id).update({'list':data})
					if to_send == '':
						await ctx.send('list is empty')
					else:
						emb=discord.Embed(title='To Do List', description=f'```-{to_send}```', color=discord.Color.from_rgb(255,182,193))
						await ctx.send(embed=emb)

	else:
		await ctx.send('Error at <0x5F89080> Invalid operation <:nnav1:810481099045077013>')


@ram.command()
async def status(ctx, *, game):
	check = RemCheck(ctx)
	if check:
		if game == 'clear':
			await ctx.message.delete(delay=None)
			await ram.change_presence(status=None)
			msg = await ctx.send(f'Activity removed by <@{ctx.author.id}>')
			await msg.delete(delay=2)
		elif game is None:
			await ctx.send('Mention the status')
		else:
			await ctx.message.delete(delay=None)
			await ram.change_presence(activity=discord.Game(game))
			msg = await ctx.send(f'Activity changed by <@{ctx.author.id}>')
			await msg.delete(delay=2)
	else:
		await ctx.send("You are not Rem chan")
		await ctx.send('''https://tenor.com/blITm.gif''')

@ram.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(ram.latency*1000, 1)} ms')

@ram.command()
async def set(ctx, type, channel=None):
	if channel==None or channel[0]!='<':
			await ctx.send('Provide a valid channel for me to post news')
	else:
		grb, id = channel.split('#')
		id, grb = id.split('>')
		id = int(id)
		channel = ram.get_channel(id)
		if channel.permissions_for(ctx.me).send_messages:
			if type == 'news':
				#--to-do--make it say that the channel is already set as a newschannel if they send the same channel again|
				db.child("servers").child(str(channel.guild.id)[:2]).child(channel.guild.id).update({'NewsChannelId':f'{channel.id}'})
				
				await ctx.send(f'News will now be posted in {channel.mention}')
			elif type == 'review':
				db.child("servers").child(str(channel.guild.id)[:2]).child(channel.guild.id).update({'EpiRevChannelId':f'{channel.id}'})
				await ctx.send(f'Reviews will now be posted in {channel.mention}')

			else:
				await ctx.send('Unknown channel type')
		else:
			await ctx.send("Sorry Moderator-sama, but I can't send messages in that channel please update the channel permissions")


@ram.command()
async def anime(ctx, *,search):
	be=datetime.datetime.now()
	anime = await ani.search(search, 'anime')
	if anime==None:
		await ctx.send("Sorry, couldn't find any anime with that title")
	else:
		if anime['averageScore']==None:
			anime['averageScore']='??'
		if anime['status']==None:
			anime['status']='??'
		else:
			anime['status']=anime['status'].capitalize()
		if anime['format']==None:
			anime['format']='??'
		else:
			anime['format']=anime['format'].capitalize()
		emb = discord.Embed(title=anime['title'],url=anime['siteUrl'],description=f"__**Description:**__\n{anime['description']}", color=discord.Color.from_rgb(255,182,193))
		emb.set_image(url=anime['coverImage']['large'])
		emb.add_field(name='⭐ __**Rating:**__', value=f"{anime['averageScore']}/100")
		emb.add_field(name='⏳ __**Status:**__',value=anime['status'].capitalize())
		emb.add_field(name='🗂️ __**Type:**__',value=anime['format'].capitalize())
		emb.add_field(name='➡️ __**Genre:**__', value=f"{', '.join(anime['genres'])}.",inline=False)
		msg = await ctx.send(embed=emb)
		await msg.add_reaction('⬇️')
		print(datetime.datetime.now()-be)
		def check(r, u):
			return ctx.message.author==u and str(r.emoji)=='⬇️'
		try:
			reaction, usr= await ram.wait_for('reaction_add', timeout=30, check=check)
		except asyncio.TimeoutError:
			await msg.clear_reactions()
			return
		emb = discord.Embed(title=anime['title'],url=anime['siteUrl'],description=f"__**Description:**__\n{anime['description']}", color=discord.Color.from_rgb(255,182,193))
		emb.add_field(name='⭐ __**Rating:**__', value=f"{anime['averageScore']}/100")
		emb.add_field(name='⏳ __**Status:**__',value=anime['status'])
		emb.add_field(name='🗂️ __**Type:**__',value=anime['format'])
		emb.add_field(name='➡️ __**Genre:**__', value=f"{', '.join(anime['genres'])}.",inline=False)
		emb.set_thumbnail(url=anime['coverImage']['large'])
		y,m,d=anime['startDate']['year'],anime['startDate']['month'],anime['startDate']['day']
		if d==None:
			sdate='?'
		else:
			sdate=f'{d}/{m}/{y}'
		y,m,d=anime['endDate']['year'],anime['endDate']['month'],anime['endDate']['day']
		if d==None:
			edate='?'
		else:
			edate=f'{d}/{m}/{y}'
		emb.add_field(name='__🗓️ **Aired:**__', value=f"from **{sdate}** to **{edate}**", inline=False)
		if anime['episodes']==None:
			anime['episodes']='??'
		emb.add_field(name='__💽 **Total Episodes:**__', value=anime['episodes'])
		if anime['duration']==None:
			anime['duration']='??'
		emb.add_field(name='__⏱️ **Duration:**__', value=f"{anime['duration']} mins")
		if anime['rankings'][0]['rank']==None:
			anime['rankings'][0]['rank']='??'
		emb.add_field(name='🏆__ **Rank:**__', value=f"{anime['rankings'][0]['rank']}")
		await msg.edit(embed=emb)
		await msg.clear_reactions()
@anime.error
async def anime_error(ctx, error):
	print(error)
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Specify the anime you are searching please')

@ram.command()
async def manga(ctx, *,search):
	be=datetime.datetime.now()
	anime = await ani.search(search, 'manga')
	if anime==None:
		await ctx.send("Sorry, couldn't find any manga with that title")
	else:
		if anime['averageScore']==None:
			anime['averageScore']='??'
		if anime['status']==None:
			anime['status']='??'
		else:
			anime['status']=anime['status'].capitalize()
		if anime['format']==None:
			anime['format']='??'
		else:
			anime['format']=anime['format'].capitalize()
		emb = discord.Embed(title=anime['title'],url=anime['siteUrl'],description=f"__**Description:**__\n{anime['description']}", color=discord.Color.from_rgb(255,182,193))
		emb.set_image(url=anime['coverImage']['large'])
		emb.add_field(name='⭐ __**Rating:**__', value=f"{anime['averageScore']}/100")
		emb.add_field(name='⏳ __**Status:**__',value=anime['status'].capitalize())
		emb.add_field(name='🗂️ __**Type:**__',value=anime['format'].capitalize())
		emb.add_field(name='➡️ __**Genre:**__', value=f"{', '.join(anime['genres'])}.",inline=False)
		msg = await ctx.send(embed=emb)
		await msg.add_reaction('⬇️')
		print(datetime.datetime.now()-be)
		def check(r, u):
			return ctx.message.author==u and str(r.emoji)=='⬇️'
		try:
			reaction, usr= await ram.wait_for('reaction_add', timeout=30, check=check)
		except asyncio.TimeoutError:
			await msg.clear_reactions()
			return
		emb = discord.Embed(title=anime['title'],url=anime['siteUrl'],description=f"__**Description:**__\n{anime['description']}", color=discord.Color.from_rgb(255,182,193))
		emb.add_field(name='⭐ __**Rating:**__', value=f"{anime['averageScore']}/100")
		emb.add_field(name='⏳ __**Status:**__',value=anime['status'])
		emb.add_field(name='🗂️ __**Type:**__',value=anime['format'])
		emb.add_field(name='➡️ __**Genre:**__', value=f"{', '.join(anime['genres'])}.",inline=False)
		emb.set_thumbnail(url=anime['coverImage']['large'])
		y,m,d=anime['startDate']['year'],anime['startDate']['month'],anime['startDate']['day']
		if d==None:
			sdate='?'
		else:
			sdate=f'{d}/{m}/{y}'
		y,m,d=anime['endDate']['year'],anime['endDate']['month'],anime['endDate']['day']
		if d==None:
			edate='?'
		else:
			edate=f'{d}/{m}/{y}'
		emb.add_field(name='🗓️__ **Published:**__', value=f"from **{sdate}** to **{edate}**", inline=False)
		if anime['chapters']==None:
			anime['chapters']='??'
		emb.add_field(name='📰__ **Chapters:**__', value=anime['chapters'])
		if anime['volumes']==None:
			anime['volumes']='??'
		emb.add_field(name='📚__ **Volumes:**__', value=f"{anime['volumes']}")
		if anime['rankings'][0]['rank']==None:
			anime['rankings'][0]['rank']='??'
		emb.add_field(name='🏆__ **Rank:**__', value=f"{anime['rankings'][0]['rank']}")
		await msg.edit(embed=emb)
		await msg.clear_reactions()
@manga.error
async def manga_error(ctx, error):
	print(error)
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Specify the manga you are searching please')

@ram.command()
async def whois(ctx, char):
	char = await ani.char_search(char)
	if char!=None:
		des=char['description'].replace('~!', '||')
		des=des.replace('!~','||')
		emb = discord.Embed(title=char['name']['full'], url=char['siteUrl'], description=f"__**Description:**__\n{des[:2030]}...",  color=discord.Color.from_rgb(255,182,193))
		emb.set_image(url=char['image']['large'])
		await ctx.send(embed=emb)
	else:
		await ctx.send('Character not found')

@whois.error
async def whois_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Specify the character you are searching please')

@ram.command()
async def muser(ctx, usr):
	emd=discord.Embed(title='Loading...', color=discord.Color.from_rgb(255,182,193))
	msg=await ctx.send(embed=emd)
	url=f'https://myanimelist.net/profile/{usr}'
	user = await some.scrape(url, requests_session)
	if user==None:
		emb=discord.Embed(title='User not found', color=discord.Color.from_rgb(255,182,193))
		await msg.edit(embed=emb)
		return
	astats=[]
	for stat in user['Anime']:
			astats.append(f"{(stat).replace('A', '', 1).capitalize()}: {user['Anime'][str(stat)]}")
	mstats=[]
	for stat in user['Manga']:
			mstats.append(f"{(stat).replace('M', '', 1).capitalize()}: {user['Manga'][str(stat)]}")
	emb=discord.Embed(title=f"{user['username']}'s MyAnimeList Profile" ,url=url, color=discord.Color.from_rgb(255,182,193))
	emb.add_field(name=f"**{'――'*10}**", value="**  **", inline=False)
	t='\n• '.join(astats)
	s='\n• '.join(mstats)
	emb.add_field(name='💽__** Anime Stats:**__', value=f"• {t}")
	emb.add_field(name='📕__** Manga Stats:**__', value=f"• {s}")
	if user['image_url']!=None:
		emb.set_thumbnail(url=user['image_url'])
	await msg.edit(embed=emb)
	next_br=False
	react=False
	for fav in user['favorites']:
		if user['favorites'][fav]:
			l=[]
			for i in user['favorites'][fav]:
				name=i['name']
				url=i['url']
				app=f"[{name}]({url})"
				l.append(app)
			user['favorites'][fav]=l
	for fav in user['favorites']:
		if user['favorites'][fav]:
			next_br=True
	if next_br:
		react=True
		await msg.add_reaction('⬇️')
		emb.add_field(name=f"**{'――'*10}**", value="**  **", inline=False)
	if user['Anime']['ATotalEntries']>0:
		react=True
		await msg.add_reaction('💽')
	if user['Manga']['MTotalEntries']>0:
		react=True
		await msg.add_reaction('📕')
	def check(r, u):
		return ctx.message.author==u  and r.message==msg
	if react:
		global fav_active
		fav_active=False
		try:
			react, usrr= await ram.wait_for('reaction_add', timeout=30, check=check)
		except asyncio.TimeoutError:
			await msg.clear_reactions()
			return
		async def AnimeRLoop(llist):
			await msg.clear_reactions()
			llist=json.loads(llist)
			l=len(llist['data'])
			total_pages=l//30
			if l%30!=0:
				total_pages+=1
			x=0
			somestring=''
			somelist=[]
			for animes in llist['data']:
				if x!=30:
					name=animes['node']['title']
					url=f"https://myanimelist.net/anime/{animes['node']['id']}"
					somestring=somestring+f"[{name}]({url}),"
					x+=1
				else:
					sublist=somestring.split(',')
					somestring=''
					somelist.append(sublist)
					x=0
			if x<30:
				sublist=somestring.split(',')
				somelist.append(sublist)
			current_page=0
			des='\n• '.join(somelist[0])
			emd=discord.Embed(title=f"{user['username']}'s Anime List", description=f"• {des[:-2]}",color=discord.Color.from_rgb(255,182,193))
			await msg.edit(embed=emd)
			if total_pages>1:
				controls=['⏪','🚫','⏩']
				for i in controls:
					await msg.add_reaction(i)
			else:
				await msg.add_reaction('🚫')
			try:
				react, usrr= await ram.wait_for('reaction_add', timeout=30, check=check)
			except asyncio.TimeoutError:
				await msg.clear_reactions()
				return
			if str(react.emoji)=='🚫':
				await msg.edit(embed=emb)
				await msg.clear_reactions()
				await msg.add_reaction('💽')
				await msg.add_reaction('📕')
				await bloopOne(None)

			elif str(react.emoji)=='⏪':
				pass
			elif str(react.emoji)=='⏩':
				pass

			await AnimeRLoop(llist)
		async def MangaRLoop():
			emd=discord.Embed(title='Loading...', color=discord.Color.from_rgb(255,182,193))
			await msg.edit(embed=emd)
			llist=await Maw.manga_list(usr, accessToken)

		async def bloopOne(reaction):
			if reaction!=None:
				if reaction.emoji=='⬇️':
					global fav_active
					if fav_active==False:
						fav_active=True
						x=0
						for fav in user['favorites']:
							if user['favorites'][fav]:
								t='\n• '.join(user['favorites'][fav])
								if x==2 or x==5:
									emb.add_field(name='** **', value='** **', inline=False)
								x+=1
								emb.add_field(name=f"__**Favorite {fav.capitalize()}:**__", value=f"• {t}", inline=True)
						await msg.clear_reaction('⬇️')
						await msg.edit(embed=emb)
					else:
						msg.edit(embed=emb)
				elif reaction.emoji=='💽':
					print('💽')
					emd=discord.Embed(title='Loading...', color=discord.Color.from_rgb(255,182,193))
					await msg.edit(embed=emd)
					llist=await Maw.anime_list(usr, accessToken)
					await AnimeRLoop(llist)
					pass
				elif reaction.emoji=='📕':
					print('📕')
					await MangaRLoop()
					pass
			try:
				react, usrr= await ram.wait_for('reaction_add', timeout=30, check=check)
			except asyncio.TimeoutError:
				await msg.clear_reactions()
				return
			await bloopOne(react)
		await bloopOne(react)
#@muser.error
async def muser_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Please specify the MAL username')


@ram.command()
async def testrun(ctx, url):
	await some.scrape(url)




token="ODA0OTM3NzA3NTY1NzQ0MTQ5.YBTmqA.g7gMeCwYXV31-y1omhSIIYEUZOo"
print('Initialising Ram_chan')
if datetime.datetime.today().day==10 or datetime.datetime.today().day==20:
	print('headed to oauth for MAL')
	data=db.child('secrete').child('inn').get()
	data=data.val()
	AcT, RfT = oauth.use_refresh_token(data['refresh_token'])
	data = {
	'access_token':f'{AcT}',
	'refresh_token':f'{RfT}'
	}
	db.child('secrete').child('inn').update(data)
	print('Oauth complete, headed to newsloop and booting all functions')
	data=db.child('secrete').child('inn').get()
	data=data.val()
	accessToken=data['access_token']
requests_session = requests.Session()
ram.run(token)