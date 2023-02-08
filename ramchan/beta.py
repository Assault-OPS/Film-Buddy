import requests
from bs4 import BeautifulSoup
import datetime
import re
import json
import ast
import html
import lxml
#requests_session = requests.Session()

class some:
	async def scrape(url, session):
		begin=datetime.datetime.now()

		resp = session.get(url)
		#print(datetime.datetime.now()-begin)
		soup = BeautifulSoup(resp.content,features="lxml")
		tags = soup.find_all("title")
		for tag in tags:
			if tag.text.count('404')>0:
				return None
			else:
				title,grb = (tag.text).split("'s")
		#gettings the stats
		for tag in soup.find_all('div', {'class':"user-statistics mb24"}, id=True):
			t=tag.text.replace('\n', '')
			m = re.search(f"{'Anime History'}(.+?){'Manga Stats'}", t)
			if m:
				m= m.group(1)
			t=t.replace(m, '')
			t,garb=t.split('Manga History')
			t=t.replace('StatisticsAnime Stats','').replace('Anime HistoryManga Stats', '').replace(' ', '').replace(':','').replace(',','')
			#now we have condensed info, time to make it into a dict?
			t="{"+t+"}"
			t=t.replace('Days', '''"ADays":''', 1)
			fields=['MeanScore', 'Watching', 'Completed', 'On-Hold', 'Dropped', 'PlantoWatch', 'TotalEntries', 'Rewatched', 'Episodes']
			for field in fields:
				t=t.replace(field, f''',"A{field}":''', 1)
			anime, manga=t.split(''',"AEpisodes":''')
			epival, manga1 = manga.split('Days')
			anime1=t.replace(manga, f"{epival}"+"}")
			manga1='''{"Days":'''+manga1
			fields=['MeanScore', 'Reading', 'Completed', 'On-Hold', 'Dropped', 'PlantoRead', 'TotalEntries', 'Reread', 'Chapters', 'Volumes']
			for field in fields:
				manga1=manga1.replace(field, f''',"M{field}":''')
			anime1=ast.literal_eval(anime1)
			manga1=ast.literal_eval(manga1)
		#getting favortie anime thingy
		fav_anime=[]
		for tag in soup.find_all('ul', {'class':"favorites-list anime"}):
			x=1
			for tags in tag:
				if str(type(tags))!="<class 'bs4.element.NavigableString'>":
					grb, t=str(tags).replace('</div>', 'splithere', 1).split('splithere')
					grb , t=t.split('<a href=')
					t ,grb=t.split("<br/>")
					t=t.replace('"https:', '{"url":"https:').replace('>', ',"name":"', 1).replace('</a>', '"}')
					#print(t)
					fav_anime.append(ast.literal_eval(t))
		#getting favorite maga thingy
		fav_manga=[]
		for tag in soup.find_all('ul', {'class':"favorites-list manga"}):
			x=1
			for tags in tag:
				if str(type(tags))!="<class 'bs4.element.NavigableString'>":
					grb, t=str(tags).replace('</div>', 'splithere', 1).split('splithere')
					grb , t=t.split('<a href=')
					t ,grb=t.split("<br/>")
					t=t.replace('"https:', '{"url":"https:').replace('>', ',"name":"', 1).replace('</a>', '"}')
					#print(t)
					fav_manga.append(ast.literal_eval(t))
		fav_chars=[]
		for tag in soup.find_all('ul', {'class':"favorites-list characters"}):
			x=1
			for tags in tag:
				if str(type(tags))!="<class 'bs4.element.NavigableString'>":
					grb, t=str(tags).replace('</div>', 'splithere', 1).split('splithere')
					grb , t=t.split('<a href=')
					t ,grb=t.split("<br/>")
					t=t.replace('"https:', '{"url":"https:').replace('>', ',"name":"', 1).replace('</a>', '"}')
					#print(t)
					fav_chars.append(ast.literal_eval(t))
		fav_peps=[]
		for tag in soup.find_all('ul', {'class':"favorites-list people"}):
			x=1
			for tags in tag:
				if str(type(tags))!="<class 'bs4.element.NavigableString'>":
					grb, t=str(tags).replace('</div>', 'splithere', 1).split('splithere')
					grb , t=t.split('<a href=')
					t ,grb=t.split("<br/>")
					t=t.replace('"https:', '{"url":"https:').replace('>', ',"name":"', 1).replace('</a>', '"}')
					#print(t)
					fav_peps.append(ast.literal_eval(t))
		tags=soup.find_all("img", {"class":"lazyload"})
		image_url=None
		for tag in tags:
			image_url,grb=tag['data-src'].split('?')
			break
		if image_url!=None:
			t={"image_url":image_url,"username":title,"Anime":anime1, "Manga":manga1, "favorites":{"Anime":fav_anime, "Manga":fav_manga, "Character":fav_chars, "People":fav_peps}}
		else:
			t={"image_url":None,"username":title,"Anime":anime1, "Manga":manga1, "favorites":{"Anime":fav_anime, "Manga":fav_manga, "Character":fav_chars, "People":fav_peps}}
		#print(t)
		print(datetime.datetime.now()-begin)
		return(t)

	def scrap_anime_list(url, typ):
		begin=datetime.datetime.now()
		resp = requests.get(url)
		soup = BeautifulSoup(resp.content,features="html.parser")
		tags = soup.find_all("table", {"class":"list-table"})
		for tag in tags:
			l=html.unescape(tag['data-items'])
			l=json.loads(l)
		datal=[]
		if typ=='anime':
			for something in l:
				datal.append(f"{something['score']} | {something['anime_title']}")
		if typ=='manga':
			for something in l:
				datal.append(f"{something['score']} | {something['manga_title']}")
		print(datal)
		#return datal
		
#some.scrape('https://myanimelist.net/profile/zerocrystal', requests_session)
#some.scrap_anime_list('https://myanimelist.net/animelist/rem', 'anime')


