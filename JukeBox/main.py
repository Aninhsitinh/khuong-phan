import tkinter as tk
import font_manager as fonts
from view_tracks import TrackViewer
from update_tracks import TrackManager
from play_track import PlayTrack
def view_tracks_clicked():
    status_lbl.configure(text="View Tracks button was clicked!")
    TrackViewer(tk.Toplevel(window))
def play_track_clicked():
    status_lbl.configure(text="PlayTrack button was clicked!")
    PlayTrack(tk.Toplevel(window))
def update_tracks_clicked():
    status_lbl.configure(text=" Your New TrackList has been updated!")
    TrackManager(tk.Toplevel(window))  
window = tk.Tk()
window.geometry("1920x1080")
window.title("JukeBox")
window.configure(bg="Pink")
fonts.configure()
header_lbl = tk.Label(window, text="Select an option by clicking the buttons below")
header_lbl.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
# View list
view_tracks_btn = tk.Button(window, text="View Tracks", command=view_tracks_clicked)
view_tracks_btn.grid(row=1, column=0, padx=10, pady=10)
# Update and Delete tracks
update_tracks_btn = tk.Button(window, text="Update Track", command=update_tracks_clicked)
update_tracks_btn.grid(row=1, column=3, padx=10, pady=10)
# Playtrack
play_track_btn=tk.Button(window, text="Playtrack", command=play_track_clicked)
play_track_btn.grid(row=1, column=2, padx=10, pady=10)
status_lbl = tk.Label(window, bg='gray', text="", font=("Helvetica", 10))
status_lbl.grid(row=3, column=2, columnspan=5, padx=10, pady=10)
window.mainloop()
