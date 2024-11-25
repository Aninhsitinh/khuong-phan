import tkinter as tk
from tkinter import messagebox, ttk
import csv
import webbrowser
import tkinter.scrolledtext as tkst

# Define a simple LibraryItem class to manage tracks
class LibraryItem:
    def __init__(self, id, name, artist, rating, youtube_link):
        self.id = id
        self.name = name
        self.artist = artist
        self.rating = int(rating)
        self.youtube_link = youtube_link

    def info(self):
        return f"{self.id}: {self.name} by {self.artist}, rating: {self.rating}"


# Global library dictionary to hold all tracks
library = {}
playlists = {}  # New dictionary to hold playlists


# Helper function to load tracks from CSV
def load_library_from_csv(csv_file):
    try:
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                library[row["id"]] = LibraryItem(
                    id=row["id"],
                    name=row["name"],
                    artist=row["artist"],
                    rating=row["rating"],
                    youtube_link=row["youtube_link"],
                )
    except FileNotFoundError:
        print(f"Error: File {csv_file} not found.")
    except Exception as e:
        print(f"Error loading CSV: {e}")


# Helper function to save tracks to CSV
def save_library_to_csv(csv_file):
    try:
        with open(csv_file, mode="w", encoding="utf-8", newline="") as file:
            fieldnames = ["id", "name", "artist", "rating", "youtube_link"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for track in library.values():
                writer.writerow({
                    "id": track.id,
                    "name": track.name,
                    "artist": track.artist,
                    "rating": track.rating,
                    "youtube_link": track.youtube_link,
                })
    except Exception as e:
        print(f"Error saving CSV: {e}")


# Save playlists to CSV
def save_playlists_to_csv():
    try:
        with open("playlists.csv", mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["playlist_name", "track_ids"])
            for playlist_name, track_ids in playlists.items():
                writer.writerow([playlist_name, ",".join(track_ids)])
    except Exception as e:
        print(f"Error saving playlists: {e}")


# Load playlists from CSV
def load_playlists_from_csv():
    try:
        with open("playlists.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                playlists[row["playlist_name"]] = row["track_ids"].split(",")
    except FileNotFoundError:
        print("Playlists file not found. Starting with an empty playlist.")
    except Exception as e:
        print(f"Error loading playlists: {e}")


# Play track function
def play_track(key):
    if key in library:
        youtube_link = library[key].youtube_link
        if youtube_link:
            webbrowser.open(youtube_link)
        else:
            messagebox.showerror("Error", "No YouTube link for this track.")
    else:
        messagebox.showerror("Error", "Track not found!")


# Create the main window 
class JukeBoxApp:
    def __init__(self, window):
        window.geometry("900x600")
        window.title("JukeBox Application")
        window.configure(bg="pink")

        # Tabs
        self.notebook = ttk.Notebook(window)
        self.notebook.pack(expand=True, fill="both")

        # View Tracks Section
        self.view_frame = tk.Frame(self.notebook, bg="pink")
        self.notebook.add(self.view_frame, text="View Tracks")
        self.view_track_listbox = tk.Listbox(self.view_frame, width=100, height=20)
        self.view_track_listbox.pack(pady=10)
        self.view_button = tk.Button(self.view_frame, text="Load Tracks", command=self.load_tracks)
        self.view_button.pack(pady=10)

        # Playlist Management Section
        self.playlist_frame = tk.Frame(self.notebook, bg="pink")
        self.notebook.add(self.playlist_frame, text="Playlist Management")

        # Create playlist UI
        self.playlist_name_entry = tk.Entry(self.playlist_frame, width=30)
        self.playlist_name_entry.pack(pady=5)
        self.create_playlist_button = tk.Button(self.playlist_frame, text="Create Playlist", command=self.create_playlist)
        self.create_playlist_button.pack(pady=5)

        # Listbox for songs to add to playlist
        self.song_listbox = tk.Listbox(self.playlist_frame, width=100, height=10, selectmode=tk.MULTIPLE)
        self.song_listbox.pack(pady=5)
        self.add_to_playlist_button = tk.Button(self.playlist_frame, text="Add to Playlist", command=self.add_to_playlist)
        self.add_to_playlist_button.pack(pady=5)

        # Playlist listbox
        self.playlist_listbox = tk.Listbox(self.playlist_frame, width=100, height=5)
        self.playlist_listbox.pack(pady=5)
        self.playlist_listbox.bind("<<ListboxSelect>>", self.show_playlist_details)

        # Playlist details listbox
        self.playlist_details_listbox = tk.Listbox(self.playlist_frame, width=100, height=10)
        self.playlist_details_listbox.pack(pady=5)

        # Play playlist button
        self.play_playlist_button = tk.Button(self.playlist_frame, text="Play Playlist", command=self.play_playlist)
        self.play_playlist_button.pack(pady=5)


        # Load library and playlists
        load_library_from_csv("data_song.csv")
        load_playlists_from_csv()
        self.load_tracks()
        self.update_playlist_listbox()

    def load_tracks(self):
        self.view_track_listbox.delete(0, tk.END)
        self.song_listbox.delete(0, tk.END)
        for key, track in library.items():
            display_text = f"{track.id} - {track.name} by {track.artist}"
            self.view_track_listbox.insert(tk.END, display_text)
            self.song_listbox.insert(tk.END, display_text)

    def create_playlist(self):
        playlist_name = self.playlist_name_entry.get().strip()
        if playlist_name and playlist_name not in playlists:
            playlists[playlist_name] = []
            self.update_playlist_listbox()
            save_playlists_to_csv()
            messagebox.showinfo("Success", f"Playlist '{playlist_name}' created successfully.")
        else:
            messagebox.showerror("Error", "Invalid or duplicate playlist name.")

    def add_to_playlist(self):
        selected_indices = self.song_listbox.curselection()
        playlist_name = self.playlist_name_entry.get().strip()
        if selected_indices and playlist_name in playlists:
            for index in selected_indices:
                song_id = self.song_listbox.get(index).split(" - ")[0]
                if song_id not in playlists[playlist_name]:
                    playlists[playlist_name].append(song_id)
            save_playlists_to_csv()
            self.show_playlist_details()
            messagebox.showinfo("Success", f"Songs added to playlist '{playlist_name}'.")
        else:
            messagebox.showerror("Error", "Select songs and a valid playlist.")

    def update_playlist_listbox(self):
        self.playlist_listbox.delete(0, tk.END)
        for playlist_name in playlists.keys():
            self.playlist_listbox.insert(tk.END, playlist_name)

    def show_playlist_details(self, event=None):
        """Display the details of the selected playlist."""
        self.playlist_details_listbox.delete(0, tk.END)
        selected_index = self.playlist_listbox.curselection()
        if selected_index:
            playlist_name = self.playlist_listbox.get(selected_index)
            track_ids = playlists[playlist_name]
            for track_id in track_ids:
                if track_id in library:
                    track = library[track_id]
                    self.playlist_details_listbox.insert(tk.END, f"{track.id} - {track.name} by {track.artist}")

    def play_playlist(self):
        selected_index = self.playlist_listbox.curselection()
        if selected_index:
            playlist_name = self.playlist_listbox.get(selected_index)
            for track_id in playlists[playlist_name]:
                play_track(track_id)
    

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = JukeBoxApp(root)
    root.mainloop()
