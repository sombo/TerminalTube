#coding:utf-8
import mechanicalsoup
import re
import time
import os
import sys
import subprocess
from subprocess import call
from tqdm import tqdm

def statusBar():
	with tqdm(total=100) as pp:
		for i in range(10):
			time.sleep(0.1)
			pp.update(10)

# query = input("חפש :")
# query = "\\" + query

def connect():

	browser = mechanicalsoup.StatefulBrowser()
	print("connecting YouTube...")
	browser.open('https://youtube.com')
	return browser



def search(browser):
	global query
	query = input('search? ')

	print('Searching ' + query + ' ...')

	browser.select_form('form[action="/results"]')

	browser['search_query'] = query

	res = browser.submit_selected()
	statusBar()

	songs = res.soup.find_all('a')

	return create_list(songs,query)

def create_list(songs,query):
	songs_dict = {}
	list_dict = {}
	non_titles_found = 0
	i = 1
	j=1

	for song in songs:
		try:
			title = song['title']
			url = song['href']

			if "watch?v" in url  and "video-time" not in song['class']:
				if 'list' in url:
					index = "song" + str(j)
					list_dict[index] = {}
					list_dict[index]['title'] = title
					list_dict[index]['url'] = song['href']
					j += 1
				else:
					index = "song" + str(i)
					songs_dict[index] = {}
					songs_dict[index]['title'] = title
					songs_dict[index]['url'] = song['href']
					i += 1


		except:
			non_titles_found += 1

	return songs_dict,list_dict

def print_title():
    os.system('clear')
    print("""
            \t\t\t**********************************
            \t\t\t*                                *
            \t\t\t *         TerminalTube         *
            \t\t\t*                                *
            \t\t\t**********************************
         """)

def print_media_title(sub_title):
    print_title()
    print(sub_title+'\n' + '-'*len(sub_title))
def quit_program():
	print_title()
	print("GoodBye ;) ")
	sys.exit()

def play(url):
    a = subprocess.Popen(["mpv","--no-terminal","--autofit=33%","--geometry=99%:1%",url])
    return a

def create_url(website,link):
	url = website + link
	return url


def main_menu():
	max_items = 0

  ### Connection Loop
	try:
		while True:
			print_title()
			user_selection = input("[1] : Search Youtube\n[q] : Exit\n\n?>")
			if user_selection == '1':
				print_title()
				browser = connect()

				songs_list, playlist_list = search(browser)
				break
			elif user_selection == 'q':
				quit_program()
			else:
				pass
    ### Results Loop
		while True:
			try:
				i = 0
				print_title()
				title_len = 12 + len(query)
				print("Results for {}\n".format(query) + '-'*title_len)
				msg = "[1]: {} songs has found\n[2]: {} playlist has found\n[3]: Search something else\n\n[q]: Exit\n\n?> ".format(len(songs_list),len(playlist_list))

				user_selection = input(msg)

				if user_selection == '1':
					print_media_title("Songs")
					media_list = songs_list
					max_items = len(songs_list)
					results_menu(max_items,media_list)
					pass
				elif user_selection == '2':
					print_media_title("Playlists")
					media_list = playlist_list
					max_items = len(playlist_list)
					results_menu(max_items,media_list)
					pass
				elif user_selection == '3':
					# songs_list, playlist_list = search(browser)
					break
					# pass

				elif user_selection == 'q':
					quit_program()

				

			except NameError as e:
				print(e)
				input()
				pass

	except KeyboardInterrupt as e:
		os.system('clear')
		res = input("\nYou presses Ctrl+c, Are you sure you want to quit? : (y/n) ")
		if res == 'y' or res == 'Y':
			sys.exit()
		else:
			main_menu()
	except NameError as e:
		print ("Please use ' ' .")


def results_menu(max_items,media_list):
	for i in range(1,max_items):
		print ("({}) {}".format(i,media_list['song'+str(i)]['title']))

	print('\nPress [b] to return back, Or [q] to exit.\n')
				# while True:
	user_selection = input('Choose Song\n')

	if user_selection.isalpha():
		if user_selection == 'q':
			quit_program()
		elif user_selection == 'b':
			return


	url = create_url("https://www.youtube.com",media_list['song' + str(user_selection)]['url'])
	proc = play(url)
	action_menu(proc,media_list,user_selection,url)

def action_menu(proc,media_list,user_selection,url):

	print_title()
	
	print ("Playing " + media_list['song'+str(user_selection)]['title'])

	action = input("\n[S]top [D]ownload [B]ack\n\n?>")
	if action is "d":
		print ("[*]Downloading " + media_list['song'+str(user_selection)]['title'])
		download(url,user_selection,media_list)
	elif action is "s":
		proc.kill()

def download(url,song_num,media_list):
    location = "~/"+media_list['song'+str(song_num)]['title']+".%(ext)s"
    
    call(["youtube-dl",'--output',location,"--extract-audio","--audio-format","mp3",url])
    input("Success, Press Any key to go back...")	

songs_list = {}
playlist_list = {}

while True:
	main_menu()


