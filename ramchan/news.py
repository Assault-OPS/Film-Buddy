import requests
from bs4 import BeautifulSoup
import datetime
import asyncio
import pyrebase

class newscmd:
	def news_links(db):
		today=datetime.date.today()
		news = requests.get("https://www.animenewsnetwork.com/news/")
		soup = BeautifulSoup(news.content,features="html.parser")
		articles=[]
		fil_id_list1=[]
		fil_id_list2=[]
		id_list1=[] #for yesterday
		id_list2=[] #for today
		special=False
		#-----updating json to current date
		data=db.child('ids').child("newsids").get()
		data=data.val()
		firstkey=list(data['ids'])
		if today.day == 1:
			for i in data["ids"]:
				if int(i) == 31 or int(i)==30 or int(i)==29 or int(i)==28:
					data['ids'].pop(i)
					data['ids'].update({"01":["dummy"], "00":["dummy"]})
					break
		else:
			if today.day<10:
				if f"0{today.day-1}" in data['ids']:
					if today.day-1>int(firstkey[0]):
						print(f"cleared! data of {today.day-2}")
						data['ids'].pop(f'0{today.day-2}')
						data['ids'].update({f'0{today.day}':['0']})
				else:
					data['ids']={}
					data['ids'].update({f'0{today.day}':['0'],f'0{today.day-1}':['0']})
			elif today.day==10:
				if "09" in data['ids']:
					if today.day-1>int(firstkey[0]):
						print(f"cleared! data of 08")
						data['ids'].pop(f'08')
						data['ids'].update({today.day:['0']})
				else:
					data['ids']={}
					data['ids'].update({'10':['0'],'09':['0']})
			elif today.day==11:
				if "10" in data['ids']:
					if today.day-1>int(firstkey[0]):
						print(f"cleared! data of 09")
						data['ids'].pop(f'09')
						data['ids'].update({today.day:['0']})
				else:
					data['ids']={}
					data['ids'].update({'11':['0'],'10':['0']})
			elif today.day>10:
				if f"{today.day-1}" in data['ids']:
					if today.day-1>int(firstkey[0]):
						print(f"cleared! data of {today.day-2}")
						data['ids'].pop(str(today.day-2))
						data['ids'].update({today.day:['0']})
				else:
					data['ids']={}
					data['ids'].update({today.day:['0'],today.day-1:['0']})
		db.child('ids').child("newsids").set(data)
		del data
		data=db.child('ids').child("newsids").get()
		data=data.val()
		#-----getting links with "news" in them of current date
		for links in soup.find_all('a',href=True):
			if "/news/" in links['href'] and len(links['href']) > 17:
				if today.day < 10:
					if f'{today.month}-0{str(int(today.day))}' in links['href']:
						if links['href'] not in articles:
							grb, ids2 = links['href'].split('/.')
							id_list2.append(ids2)
							if ids2 in data['ids'][f"0{today.day}"]:
								pass
							else:
								fil_id_list2.append(ids2)
								articles.append(links['href'])
					elif f'{today.month}-0{str(int(today.day)-1)}' in links['href']:
						if links['href'] not in articles:
							grb, ids1 = links['href'].split('/.')
							id_list1.append(ids1)
							if ids1 in data['ids'][f"0{today.day-1}"]:
								pass
							else:
								fil_id_list1.append(ids1)
								articles.append(links['href'])

					#db.child('ids').child("newsids").set(data)
				elif today.day==10:
					special=True
					if f'{today.month}-10' in links['href']:
						if links['href'] not in articles:
							grb, ids2 = links['href'].split('/.')
							id_list2.append(ids2)
							if ids2 in data['ids']["10"]:
								pass
							else:
								fil_id_list2.append(ids2)
								articles.append(links['href'])
					elif f'{today.month}-09' in links['href']:
						if links['href'] not in articles:
							grb, ids1 = links['href'].split('/.')
							id_list1.append(ids1)
							if ids1 in data['ids']["09"]:
								pass
							else:
								fil_id_list1.append(ids1)
								articles.append(links['href'])
				elif today.day==11:
					if f'{today.month}-11' in links['href']:
						if links['href'] not in articles:
							grb, ids2 = links['href'].split('/.')
							id_list2.append(ids2)
							if ids2 in data['ids']["11"]:
								pass
							else:
								fil_id_list2.append(ids2)
								articles.append(links['href'])
					elif f'{today.month}-10' in links['href']:
						if links['href'] not in articles:
							grb, ids1 = links['href'].split('/.')
							id_list1.append(ids1)
							if ids1 in data['ids']["10"]:
								pass
							else:
								fil_id_list1.append(ids1)
								articles.append(links['href'])	
				else:

					if f'{today.month}-{str(int(today.day))}' in links['href']:
						if links['href'] not in articles:
							grb, ids2 = links['href'].split('/.')
							id_list2.append(ids2)
							
							if ids2 in data['ids'][f"{today.day}"]:
								pass
							else:
								fil_id_list2.append(ids2)
								articles.append(links['href'])

					elif f'{today.month}-{str(int(today.day)-1)}' in links['href']:
						if links['href'] not in articles:
							grb, ids1 = links['href'].split('/.')
							id_list1.append(ids1)
							if ids1 in data['ids'][f'{today.day-1}']:
								pass
							else:
								fil_id_list1.append(ids1)
								articles.append(links['href'])
		if today.day <10:
			jsonlist2 = data['ids'][f"0{today.day}"]
			jsonlist2 = jsonlist2+fil_id_list2 
			data['ids'].update({f'0{today.day}':jsonlist2})
			jsonlist1 = data['ids'][f"0{today.day-1}"] 
			jsonlist1 = jsonlist1+fil_id_list1
			data['ids'].update({f'0{today.day-1}':jsonlist1})
			db.child('ids').child("newsids").set(data)
		elif today.day==10:
			jsonlist2 = data['ids']["10"]
			jsonlist2 = jsonlist2+fil_id_list2 
			data['ids'].update({'10':jsonlist2})
			jsonlist1 = data['ids']["09"] 
			jsonlist1 = jsonlist1+fil_id_list1
			data['ids'].update({'09':jsonlist1})
			db.child('ids').child("newsids").set(data)
		elif today.day==11:
			jsonlist2 = data['ids']["11"]
			jsonlist2 = jsonlist2+fil_id_list2 
			data['ids'].update({'11':jsonlist2})
			jsonlist1 = data['ids']["10"] 
			jsonlist1 = jsonlist1+fil_id_list1
			data['ids'].update({'10':jsonlist1})
			db.child('ids').child("newsids").set(data)
		else:
			jsonlist2 = data['ids'][f"{today.day}"]
			jsonlist2 = jsonlist2+fil_id_list2 
			data['ids'].update({today.day:jsonlist2})
			jsonlist1 = data['ids'][f"{today.day-1}"] 
			jsonlist1 = jsonlist1+fil_id_list1
			data['ids'].update({today.day-1:jsonlist1})
			db.child('ids').child("newsids").set(data)
		fil_id_list =fil_id_list1+fil_id_list2
		print("------------news section------------")
		print(fil_id_list2)
		print("------------today's ids^------------")
		print(fil_id_list1)
		print("-----------yesterday's ids^---------")
		print(data['ids'])
		print("--------end of news section---------")
		print("|                                  |\n"*3)
		return fil_id_list

	def news_link_parser(news_links):
		url = 'https://animenewsnetwork.com/.'+news_links
		resp = requests.get(url)
		soup = BeautifulSoup(resp.content,"html.parser")
		tags = soup.find_all("p")
		i=0
		content=[]
		for tag in tags:
			if i<4:
				if tag.text != "":
					content.append(tag.text.replace('\n\n', ' '))
					i+=1
		#---------IMP!!!-------|
		content=''.join(content)
		content = f"{content[0:500]}...."
		
		#---------IMP!!!-------|
		tags= soup.find_all("link")
		for tag in tags:
			if "thumbnail" in tag["href"]:
		#----------IMP!---------|	
				img_link = tag["href"]
		#----------IMP!---------|
		tags = soup.find_all("title")
		for tag in tags:
			title = tag.text
		#----------IMP!---------|
		c=title.count('-')
		d=title.count('Episode')
		if not d >0:
			if c == 2:
				title, g, l = title.split('-')
			elif c==3:
				title, g, l, k = title.split('-')
				title=title+g
			elif c==4:
				title, g, k, l, i = title.split('-')
				title=title+g+k
		else:
			title,g=title.split("- Anime")


		return title, content, img_link, url

		#----------IMP!---------|
	def epiIdGrabber(db):
		today=datetime.date.today()
		review=requests.get("https://www.animenewsnetwork.com/episode-review/")
		soup = BeautifulSoup(review.content,features="html.parser")
		link_list=[]
		fil_link_list=[]
		max_find=10
		for links in soup.find_all('a',href=True):

			if '/review/' in links["href"] and '/episode' in links["href"] and len(links['href']) > 10 and max_find>1:
				if not links.parent.has_attr("class"):
					grb, ids= links["href"].split("/.")
					link_list.append(ids)
					max_find= max_find-1
				if max_find==0:
					break
		data=db.child('ids').child("epiids").get()
		data=data.val()
		for ids in link_list:
			if ids not in fil_link_list:
				if str(ids) not in data:
					fil_link_list.append(ids)

		db.child('ids').update({"epiids":link_list})
		print("------------review section------------")
		print(data)
		print("---------------old data^--------------")
		print(fil_link_list)
		print("------about to post ids^--------------")
		print(list(set(link_list)))
		print("-------data dumped in epiids^--------------")
		print("------------end of review-------------")
		return fil_link_list