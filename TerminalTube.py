#!/usr/bin/python2
# -*- coding: utf-8 -*-

# A Youtube App for Terminal

import mechanize
import re
import sys,os
import subprocess
from subprocess import call


def reverse_word(word):
    end_index = len(word)
    start_index = end_index - 2
    rever_word = ''
    while start_index > 0 :
       rever_word += word[start_index:end_index]
       end_index -= 2
       start_index -= 2
    return rever_word + word[start_index:end_index] + " "

def reverse_title(title):
    words = title.split(' ')
    words = words[0:len(words)-2]
    words = words[::-1]
    #print words
    words_list = list(words)
    reverse = ''
    for word in words_list :
        reverse += reverse_word(word)

    return reverse

def clear_url(urls) :
   songs_dict =[]
   song_id = 1
   # i = 0
   for url in urls:
        split_url = url.url.split('?')
        if 'watch' in split_url[0] and len(split_url[1]) == 13 :
            if "ow" not in url.text :
                reve = reverse_title(url.text)
                if 'o' not in reve or 'a' not in reve :
                    songs_dict += reve,url.url
                    # i+=1

   return songs_dict

def search_song():

    global search_query
    search_query = raw_input("search : ")

    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open('http://www.youtube.com')
    br.select_form(nr=1)
    br.form["search_query"] = search_query
    br.submit()
    return make_songs_list(br.links(),search_query)
    # return clear_url(br.links())

def make_songs_list(songs,search_query):
    songs_dict = {}
    playlist_dict = {}
    i = 1
    j = 1
    for song in songs:
        if "watch?v" in song.url and "IMG" not in song.text:
            index = "song" + str(i)
            songs_dict[index] = {}
            songs_dict[index]["name"] = song.text
            songs_dict[index]["url"] = song.url
            i+=1
        elif "playlist?list" in song.url and "IMG" not in song.text:
            index = "song" + str(j)
            playlist_dict[index] = {}
            playlist_dict[index]["name"] = song.text
            playlist_dict[index]["url"] = song.url
            j+=1

    return songs_dict,playlist_dict

def print_Title():
    os.system('clear')
    print("""
            \t\t\t**********************************
            \t\t\t*                                *
            \t\t\t *         TerminalTube         *
            \t\t\t*                                *
            \t\t\t**********************************
         """)
    # print_Status_Line("www")

def print_Status_Line(msg):
    print """
    playing %s """ % msg

def print_Media_Title(sub_title):
    print_Title()
    print(sub_title+"\n")

def play(url):
    a = subprocess.Popen(["mpv","--no-terminal","--autofit=33%","--geometry=99%:1%",url])
    return a

def download(url,song_num,media_list):
    location = "~/"+media_list['song'+str(song_num)]['name']+".%(ext)s"
    print (songs_list)
    call(["youtube-dl",'--output',location,"--extract-audio","--audio-format","mp3",url])
    raw_input("Success, Press Any key to go back...")

# def menu(media_type):
    # max_items = 0

    # if media_type == 0:
    #     print_Media_Title("Songs List")
    #     media_list = songs_list
    #     max_items = 15
    
    # else: 
    #     print_Media_Title("Playlists List")
    #     media_list = playlist_dict
    #     max_items = len(media_list)


    # for i in range(1,max_items):
    #     print "[%d]  %s" % (i,media_list['song'+str(i)]['name'])
    # print "\nPress 0 to return back."

    # user_select = input("\nChoose Item : \n")
    # if user_select is 0:
    #     return
    
    # url = 'https://www.youtube.com' + media_list['song'+str(user_select)]['url']

    # # Mpv process object
    # proc = play(url)
    
    # # Sub Menu
    # while True:
    #     print_Title()
    #     print "Playing " + songs_list['song'+str(user_select)]['name']

    #     action = raw_input("\n[S]top [D]ownload [B]ack\n\n?>")
        
    #     if action is "d":
    #         print "[*]Downloading " + songs_list['song'+str(user_select)]['name']
    #         download(url,user_select)
    #     elif action is "s":
    #         proc.kill()
    #         return
    #     elif action is "b":
    #         return

    #     else:
    #         pass
def main_menu():
    max_items = 0
    try:
        while True:
            print_Title()
            user_in = raw_input("[1]:search\n[0]:exit\n\n?>")

            if user_in is str(1):
                print_Title()
                songs_list ,playlist_dict = search_song()
                break
            elif user_in is str(0):
                print_Title()
                print "GoodBye..."
                sys.exit()
            else:
                pass

        while True:
            try:
                print_Title()
                print "Results for '%s'\n" % search_query
                msg = "[1]:Songs (%d)\n[2]:Playlists (%d)\n[3]:New_search\n\n[0]:Exit\n\n?>" % (len(songs_list),len(playlist_dict))
                user_in = input(msg)
                if user_in is 1:
                    print_Media_Title("Songs List")
                    media_list = songs_list
                    max_items = 15
                    pass
                elif user_in is 2:
                    print_Media_Title("Playlists List")
                    media_list = playlist_dict
                    max_items = len(media_list)
                    pass
                elif user_in is 3: #new search
                    songs_list ,playlist_dict = search_song()
                    pass
                elif user_in is 0: #exit
                    print "GoodBye..."
                    sys.exit()
        
                for i in range(1,max_items):
                    print "[%d]  %s" % (i,media_list['song'+str(i)]['name'])
                print "\nPress 0 to return back."

                user_select = input("\nChoose Item : \n")
                if user_select is 0:
                    return

                url = 'https://www.youtube.com' + media_list['song'+str(user_select)]['url']

                # Mpv process object
                proc = play(url)
    
                # Sub Menu
                while True:
                    print_Title()
                    print "Playing " + songs_list['song'+str(user_select)]['name']

                    action = raw_input("\n[S]top [D]ownload [B]ack\n\n?>")
        
                    if action is "d":
                        print "[*]Downloading " + songs_list['song'+str(user_select)]['name']
                        download(url,user_select,media_list)
                        pass
                    elif action is "s":
                        proc.kill()
                        break
                    elif action is "b":
                        break

                    else:
                        pass

            except NameError,e:
                print e
                input()
                pass
    except KeyboardInterrupt:
        print "You Pressed Ctrl+C"
        sys.exit()
    except NameError,e:
        print "Please use ' ' ."

songs_list = {}
playlist_dict = {}
search_query =""
max_items = 0

while True:
    main_menu()






