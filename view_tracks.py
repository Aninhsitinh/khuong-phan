import tkinter as tk
from tkinter import font
import tkinter.scrolledtext as tkst
import csv
import json
import os
# Define the LibraryItem class
class LibraryItem:
    def __init__(self, id, name, artist, rating, play_count, youtube_link):
        self.id = id
        self.name = name
        self.artist = artist
        self.rating = int(rating)
        self.play_count = int(play_count)
        self.youtube_link = youtube_link
    def info(self):
        return f"{self.id}: {self.name} by {self.artist}, rating: {self.rating}, plays: {self.play_count}"
# Global library dictionary
library = {}
def load_library_from_csv(csv_file):
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                library[row["id"]] = LibraryItem(
                    id=row["id"],
                    name=row["name"],
                    artist=row["artist"],
                    rating=row["rating"],
                    play_count=row["play_count"],
                    youtube_link=row["youtube_link"],
                )
    except FileNotFoundError:
        print(f"Error: File {csv_file} not found.")
    except Exception as e:
        print(f"Error loading CSV: {e}")
def save_library_to_csv(csv_file):
    try:
        with open(csv_file, mode='w', encoding='utf-8', newline='') as file:
            fieldnames = ["id","name","artist","rating","play_count","youtube_link"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for track in library.values():
                writer.writerow({
                    "id": track.id,
                    "name": track.name,
                    "artist": track.artist,
                    "rating": track.rating,
                    "play_count": track.play_count,
                    "youtube_link": track.youtube_link,
                })
    except Exception as e:
        print(f"Error saving CSV: {e}")
def list_all():
    output = ""
    for id, track in library.items():
        output += track.info() + "\n"
    return output.strip()
def get_name(key):
    return library[key].name if key in library else None
def get_artist(key):
    return library[key].artist if key in library else None
def get_rating(key):
    return library[key].rating if key in library else None
def get_play_count(key):
    return library[key].play_count if key in library else None
def increment_play_count(key):
    if key in library:
        library[key].play_count += 1
def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)
class TrackViewer:
    def __init__(self, window):
        window.geometry("900x600")
        window.title("Track and Playlist Manager")
        window.configure(bg="lightblue")
        # Section for viewing tracks
        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked)
        list_tracks_btn.grid(row=0, column=0, padx=10, pady=10)
        self.input_lbl = tk.Label(window, text="Enter Track Number:")
        self.input_lbl.grid(row=0, column=1, padx=10, pady=10)
        self.input_txt = tk.Entry(window, width=5)
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)
        view_track_btn = tk.Button(window, text="View Track", command=self.view_track_clicked)
        view_track_btn.grid(row=0, column=3, padx=10, pady=10)
        self.list_txt = tkst.ScrolledText(window, width=50, height=15, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        self.track_txt = tk.Text(window, width=30, height=5, wrap="none")
        self.track_txt.grid(row=1, column=4, sticky="NW", padx=10, pady=10)
        # Section for playlist management
        self.playlist = []
        self.playlist_file = "playlist.json"
        add_to_playlist_btn = tk.Button(window, text="Add to Playlist", command=self.add_to_playlist)
        add_to_playlist_btn.grid(row=2, column=0, padx=10, pady=10)
        play_playlist_btn = tk.Button(window, text="Play Playlist", command=self.play_playlist)
        play_playlist_btn.grid(row=2, column=1, padx=10, pady=10)
        save_playlist_btn = tk.Button(window, text="Save Playlist", command=self.save_playlist)
        save_playlist_btn.grid(row=2, column=2, padx=10, pady=10)
        reset_playlist_btn = tk.Button(window, text="Reset Playlist", command=self.reset_playlist)
        reset_playlist_btn.grid(row=2, column=3, padx=10, pady=10)
        self.playlist_txt = tkst.ScrolledText(window, width=50, height=15, wrap="none")
        self.playlist_txt.grid(row=3, column=0, columnspan=4, padx=10, pady=10)
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=4, column=0, columnspan=5, sticky="W", padx=10, pady=10)
        self.list_tracks_clicked()
        self.load_playlist()
    def list_tracks_clicked(self):
        track_list = list_all()
        set_text(self.list_txt, track_list)
    def view_track_clicked(self):
        key = self.input_txt.get()
        if key in library:
            track = library[key]
            track_details = f"{track.name}\n{track.artist}\nRating: {track.rating}\nPlays: {track.play_count}"
            set_text(self.track_txt, track_details)
            self.status_lbl.configure(text="Track details displayed.")
        else:
            set_text(self.track_txt, "Track not found.")
            self.status_lbl.configure(text="Error: Track not found.")
    def add_to_playlist(self):
        key = self.input_txt.get()
        if key in library:
            self.playlist.append(key)
            self.update_playlist_display()
            self.status_lbl.configure(text=f"Track {key} added to playlist.")
        else:
            self.status_lbl.configure(text=f"Error: Track {key} not found.")
    def play_playlist(self):
        for key in self.playlist:
            increment_play_count(key)
        self.update_playlist_display()
        self.status_lbl.configure(text="Playlist played.")
        save_library_to_csv("data_song.csv")
    def save_playlist(self):
        try:
            with open(self.playlist_file, 'w') as file:
                json.dump(self.playlist, file)
            self.status_lbl.configure(text="Playlist saved.")
        except Exception as e:
            self.status_lbl.configure(text=f"Error saving playlist: {e}")
    def reset_playlist(self):
        self.playlist.clear()
        self.update_playlist_display()
        self.status_lbl.configure(text="Playlist reset.")
    def load_playlist(self):
        try:
            with open(self.playlist_file, 'r') as file:
                self.playlist = json.load(file)
            self.update_playlist_display()
            self.status_lbl.configure(text="Playlist loaded.")
        except FileNotFoundError:
            pass
        except Exception as e:
            self.status_lbl.configure(text=f"Error loading playlist: {e}")
    def update_playlist_display(self):
        set_text(self.playlist_txt, "")
        for key in self.playlist:
            track = library[key]
            self.playlist_txt.insert(tk.END, f"{key}: {track.name} by {track.artist}\n")
# Initialize library
load_library_from_csv("data_song.csv")


