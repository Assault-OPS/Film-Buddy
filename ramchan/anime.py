import json
import requests
from difflib import SequenceMatcher
import datetime
from jikanpy import Jikan

class ani:
	async def search(search, typ):
		search=search.lower()
		symbols=['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '|', '}', '{', '\\', ']', '[', '"', "'", '?', '?', '.', ',', '>', '<', '`']
		for i in symbols:
			search=search.replace(i, ' ')
		l=len(search)
		query = '''
query ($id: Int, $page: Int, $perPage: Int, $search: String) {
	Page (page: $page, perPage: $perPage) {
		pageInfo {
			total
			currentPage
			lastPage
			hasNextPage
			perPage
		}
		media (id: $id, search: $search, type: REPLAC3, isAdult:false) {
			id
			title {
				english
				romaji
			
			}
			description
			coverImage{
				large
			}
			status(version: 2)
			format
			genres
			averageScore
			REP1
			REP2
			rankings{
				rank
			}
			startDate{
			year
			month
			day
			}
			endDate{
			year
			month
			day
			}
			siteUrl
			rankings{
				rank
			}
		}
	}
}
'''
		variables={
		'search':search,
		'page': 1,
		'perPage': 5
		}
		if typ=='anime':
			query=query.replace('REPLAC3', 'ANIME')
			query=query.replace('REP1', 'episodes')
			query=query.replace('REP2', 'duration')
		elif typ=='manga':
			query=query.replace('REPLAC3', 'MANGA')
			query=query.replace('REP1', 'chapters')
			query=query.replace('REP2', 'volumes')
		hr=0.0
		hra=None
		rhr=0.0
		rhra=None
		url = 'https://graphql.anilist.co'
		response = requests.post(url, json={'query': query, 'variables': variables})
		data=json.loads(response.text)
		#print(data)
		if data['data']['Page']['pageInfo']['total']==0:
			return None
		else:
			for anime in data['data']['Page']['media']:
				if anime['title']['english']!=None:
					ratio=round(SequenceMatcher(None, search, anime['title']['english'].lower()[:l]).ratio(), 3)
					if ratio>hr:
						hr=ratio
						hra=anime
				if anime['title']['romaji']!=None:
					ratio=round(SequenceMatcher(None, search, anime['title']['romaji'].lower()[:l]).ratio(), 3)
					if ratio>rhr:
						rhr=ratio
						rhra=anime

			if hr>rhr:
				hra['title']=hra['title']['english']
				ranime=hra
			else:
				rhra['title']=rhra['title']['romaji']
				ranime=rhra

			description=ranime['description'].replace('<br>','')
			description=description.replace('</br>','')
			description=description.replace('<i>','')
			description=description.replace('</i>','')
			description=description.replace('<b>','**')
			ranime['description']=description.replace('</b>','**')
			print(ranime)
			return ranime

	async def char_search(search):
		search=search.lower()
		symbols=['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '|', '}', '{', '\\', ']', '[', '"', "'", '?', '?', '.', ',', '>', '<', '`']
		for i in symbols:
			search=search.replace(i, ' ')
		l=len(search)
		query='''
query ($search: String) {
	Character(search: $search) {
		name{
			full
			}
		image{
				large
			}
		description
		siteUrl
	}
}
'''
		variables={
		'search':search,
		}
		url = 'https://graphql.anilist.co'
		response = requests.post(url, json={'query': query, 'variables': variables})
		data=json.loads(response.text)
		data = data['data']['Character']
		return data
	async def user_lookup(usr, jikan, req):
		if req=='p':
			user = jikan.user(username=usr, request='profile')
			#print(user)
			astats=[]
			mstats=[]
			for stat in user['anime_stats']:
				astats.append(f"{((stat).replace('_', ' ')).capitalize()}: {user['anime_stats'][str(stat)]}")
			for stat in user['manga_stats']:
				mstats.append(f"{((stat).replace('_', ' ')).capitalize()}: {user['manga_stats'][str(stat)]}")
			user['astats']=astats
			user['mstats']=mstats

			for fav in user['favorites']:
				if user['favorites'][fav]:
					l=[]
					for i in user['favorites'][fav]:
						name=i['name']
						url=i['url']
						app=f"[{name}]({url})"
						l.append(app)
					user['favorites'][fav]=l
			return user








#single file test sections------------
#
#
#be=datetime.datetime.now()
#anime_list=['AoT','Death Note','Steins Gate',' Demon Slayer','Hyouka','Violet Evergarden','Kokoro Connect','The promised neverland','Karakai Jouzu No takagi San','Asobi Asobase']

#for i in anime_list:
#	ani.anime_search(i)
#ani.manga_search('demon slayer')
#
#
#
#print(datetime.datetime.now()-be)
#ani.char_search('Rem')
#single file test sections------------