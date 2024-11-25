from library_item import LibraryItem
import csv
import os
library ={}
def load_library(filename):
    global library
    library = {}   
    with open (filename,'r', newline='', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            id = row[0]
            name = row[1]
            artist = row[2]
            rating = row[3]
            play_count = row[4]
            youtube_link = row[5]
            item1 = LibraryItem(id,name,artist,rating,play_count,youtube_link)
            library[id] = item1
def save_library(filename):
    with open (filename, 'w', newline='') as csvfile:
        fieldnames = ['id','name','artist','rating','play_count','youtube_link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, encoding='utf8')
        writer.writeheader()
        for id, item in library.items():
            writer.writerow({
                'id': id,
                'name': item.name,
                'artist': item.artist,
                'rating': item.rating,
                'play count': item.play_count,
                'youtube_link':item.youtube_link
            })
#Load library data from CSV file
load_library('data_song.csv')
def list_all():
    output = ""
    for key in library:
        item = library[key]
        output += f"{key} {item.info()}\n"
    return output
def get_name(key):
    try:
        item = library[key]
        return item.name
    except KeyError:
        return None
def get_artist(key):
    try:
        item = library[key]
        return item.artist
    except KeyError:
        return None
def get_rating(key):
    try:
        item = library[key]
        return item.rating
    except KeyError:
        return -1
def set_rating(key, rating):
    try:
        item = library[key]
        item.rating = rating
    except KeyError:
        return
def get_play_count(key):
    try:
        item = library[key]
        return item.play_count
    except KeyError:
        return -1
def increment_play_count(key):
    try:
        item = library[key]
        item.play_count += 1
    except KeyError:
        return
def get_youtube_link(key):
    try:
        item = library[key] 
        return item.youtube_link
    except KeyError:
        return None
def get_track_data(key):
    try:
        return library[key]
    except KeyError:
        return None

