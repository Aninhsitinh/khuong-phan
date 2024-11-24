import tkinter as tk
import csv
# Global CSV file name
CSV_FILE = "update_track.csv"
def load_tracks():
    """Load tracks from the CSV file."""
    try:
        with open(CSV_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        return []
def save_tracks(tracks):
    """Save tracks back to the CSV file."""
    try:
        with open(CSV_FILE, mode="w", encoding="utf-8", newline="") as file:
            fieldnames = ["id", "name", "director", "rating"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(tracks)
    except Exception as e:
        print(f"Error saving library to CSV: {e}")
class TrackManager:
    def __init__(self, window):
        window.geometry("800x600")
        window.title("Track Manager")
        window.configure(bg="pink")
        # Widgets for Update/Add Track Section
        tk.Label(window, text="Update/Add Track", bg="pink", font=("Helvetica", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=10
        )
        tk.Label(window, text="Track ID:", bg="pink").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.track_id_txt = tk.Entry(window, width=20)
        self.track_id_txt.grid(row=1, column=1, pady=5)
        tk.Label(window, text="Track Name:", bg="pink").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.track_name_txt = tk.Entry(window, width=20)
        self.track_name_txt.grid(row=2, column=1, pady=5)
        tk.Label(window, text="Director:", bg="pink").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.director_txt = tk.Entry(window, width=20)
        self.director_txt.grid(row=3, column=1, pady=5)
        tk.Label(window, text="Rating (1-5):", bg="pink").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.rating_txt = tk.Entry(window, width=5)
        self.rating_txt.grid(row=4, column=1, pady=5)
        tk.Button(window, text="Update/Add Track", command=self.update_or_add_track).grid(
            row=5, column=0, columnspan=2, pady=10
        )
        # Widgets for Delete Track Section
        tk.Label(window, text="Delete Track", bg="pink", font=("Helvetica", 16, "bold")).grid(
            row=6, column=0, columnspan=2, pady=20
        )
        tk.Label(window, text="Track ID to Delete:", bg="pink").grid(row=7, column=0, sticky="e", padx=10, pady=5)
        self.delete_id_txt = tk.Entry(window, width=20)
        self.delete_id_txt.grid(row=7, column=1, pady=5)
        tk.Button(window, text="Delete Track", command=self.delete_track).grid(row=8, column=0, columnspan=2, pady=10)
        # Status Label
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 12), bg="pink", fg="blue")
        self.status_lbl.grid(row=9, column=0, columnspan=2, pady=10)
    def update_or_add_track(self):
        """Update or add a new track."""
        track_id = self.track_id_txt.get().strip()
        name = self.track_name_txt.get().strip()
        director = self.director_txt.get().strip()
        rating = self.rating_txt.get().strip()
        if not (track_id and name and director and rating):
            self.status_lbl.configure(text="All fields must be filled!", fg="red")
            return
        if not track_id.isdigit() or not rating.isdigit() or not (1 <= int(rating) <= 5):
            self.status_lbl.configure(text="Invalid input: ID and rating must be numbers!", fg="red")
            return
        tracks = load_tracks()
        for track in tracks:
            if track["id"] == track_id:
                track["name"] = name
                track["director"] = director
                track["rating"] = rating
                self.status_lbl.configure(text=f"Track {track_id} updated successfully!", fg="green")
                break
        else:
            tracks.append({"id": track_id, "name": name, "director": director, "rating": rating})
            self.status_lbl.configure(text=f"Track {track_id} added successfully!", fg="green")
        save_tracks(tracks)
    def delete_track(self):
        """Delete a track by ID."""
        track_id = self.delete_id_txt.get().strip()
        if not track_id:
            self.status_lbl.configure(text="Track ID must be provided!", fg="red")
            return
        tracks = load_tracks()
        updated_tracks = [track for track in tracks if track["id"] != track_id]
        if len(updated_tracks) == len(tracks):
            self.status_lbl.configure(text=f"Track {track_id} not found.", fg="red")
            return
        save_tracks(updated_tracks)
        self.status_lbl.configure(text=f"Track {track_id} deleted successfully!", fg="green")


