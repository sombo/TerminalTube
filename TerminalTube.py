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

def reverse_title(title) :
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
    return clear_url(br.links())

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

def print_Tilte():
    os.system('clear')
    # print("\n"*100)
    print ( '*'* 10)
    print ( "TerminalTube" )
    print ('*'*10)

def print_song_title():
    print_Tilte()
    print ( "Songs List" )
    print ("-" * 11)

def print_playlists_title():
    print_Tilte()
    print "Playlists List"
    print "-" * 11

def songs_menu():
    print_song_title()
    max_songs = 15;
    for i in range(1,max_songs):
        print "[%d]  %s" % (i,songs_list['song'+str(i)]['name'])
    print "\nPress 0 to return back."

    song_num = input("\nChoose Number:\n")
    if song_num is 0:
        return
    action = input("1: play\t2: Download\n")
    url = 'https://www.youtube.com' + songs_list['song'+str(song_num)]['url']
    if action is 1:
        print "Playing " + songs_list['song'+str(song_num)]['name']
        subprocess.Popen(["mpv","--no-terminal","--autofit=33%","--geometry=99%:1%",url])
    if action is 2:
        print "[*]Downloading " + songs_list['song'+str(song_num)]['name']
        location = "~/Developer/temp_downloads/"+songs_list['song'+str(song_num)]['name']+".%(ext)s"
        call(["youtube-dl",'--output',location,"--extract-audio","--audio-format","mp3",url])
        raw_input("Success, Press Any key to go back...")

def playlists_menu():
    print_playlists_title()
    for i in range(1,len(playlist_dict)-1):
        print "[%d]  %s" % (i,playlist_dict['song'+str(i)]['name'])
    print "\nPress 0 to return back."

    song_num = input("\nChoose Number:\n")
    if song_num is 0:
        return
    action = input("1: play\t2: Download\n")
    url = 'https://www.youtube.com' + playlist_dict['song'+str(song_num)]['url']
    if action is 1:
        print "Playing " + playlist_dict['song'+str(song_num)]['name']
        call(["mpv","--autofit=33%","--geometry=99%:1%",url])
    if action is 2:
        print "[*]Downloading " + playlist_dict['song'+str(song_num)]['name']
        location = "~/Developer/temp_downloads/%(title)s.%(ext)s"
        call(["youtube-dl","--output",location,"--extract-audio","--audio-format","mp3",url])
        raw_input("Success, Press Any key to go back...")


songs_list = {}
playlist_dict = {}
search_query =""

print_Tilte()

try:
    user_in = input("[1]:search\n[0]:exit\n\n?>")

    if user_in is 1:
        print_Tilte()
        songs_list ,playlist_dict = search_song()

    elif user_in is 0:
        print_Tilte()
        print "GoodBye..."
        sys.exit()

    while True:
        try:
            print_Tilte()
            print "Results for '%s'\n" % search_query
            msg = "[1]:Songs (%d)\n[2]:Playlists (%d)\n[3]:New_search\n\n[0]:Exit\n\n?>" % (len(songs_list),len(playlist_dict))
            user_in = input(msg)
            if user_in is 1:
                songs_menu()
                pass
            elif user_in is 2:
                playlists_menu()
                pass
            elif user_in is 3: #new search
                songs_list ,playlist_dict = search_song()
                pass
            elif user_in is 0: #exit
                print "GoodBye..."
                sys.exit()
        except NameError,e:
            print e
            input()
            pass
except KeyboardInterrupt:
    print "You Pressed Ctrl+C"
    sys.exit()
except NameError,e:
    print "Please use ' ' ."










