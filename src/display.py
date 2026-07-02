import os
import glob
from IPython.display import HTML
from base64 import b64encode

def display_latest_video():
    # Cari file mp4 terbaru di folder media
    list_of_files = glob.glob('media/videos/renderer/480p15/*.mp4')
    if not list_of_files:
        print("[-] Video belum ditemukan.")
        return
    
    latest_file = max(list_of_files, key=os.path.getctime)
    mp4 = open(latest_file, 'rb').read()
    data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
    
    return HTML(f"""
    <video width=600 controls autoplay>
          <source src="{data_url}" type="video/mp4">
    </video>
    """)

if __name__ == "__main__":
    # Fungsi ini akan dipanggil untuk menampilkan video
    display(display_latest_video())
    
