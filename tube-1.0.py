import mechanicalsoup
import subprocess
from subprocess import call

br = mechanicalsoup.StatefulBrowser()
br.open('https://www.google.com')
q = input("search for song or artist\n")
query = q + " :site:youtube.com"

br.select_form('form[action="/search"]')
br['q'] = query
res = br.submit_selected()

songs = res.soup.find_all('a')
index = 1

songs_dict = {}
for song in songs:
    try:
        title = song.next_element.find('span')
        url = "https://www.youtube.com/watch?v="+song['href'][43:][:11]
        tt =str(title)
        tt = tt[16:-16]
        if len(tt) > 0 :
            if tt[0] != 'y' and tt[1] != 'E':
                songs_dict[index] = {}
                songs_dict[index]['title'] = tt
                songs_dict[index]['url'] = url
                print(str(index) + ">" + str(songs_dict[index]['title']))
                index+=1

    except:
        print ('error')




song_select = input("choose video : ")
action_select = input("[1]: Play [2]: Download\n")

url = songs_dict[int(song_select)]['url']
location = "~/" + songs_dict[int(song_select)]['title']+".%(ext)s"

if action_select == '1':
    a = subprocess.Popen(["mpv","--autofit=33%","-geometry=99%:1%",url])

elif action_select == '2':
    call(["youtube-dl","--output",location,"--extract-audio","--audio-format","mp3",url])

