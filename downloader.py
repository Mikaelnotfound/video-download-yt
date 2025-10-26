import yt_dlp
import os

def download_audio_with_yt_dlp(url):
    """
    Downloads the audio from a YouTube video as an MP3 file using yt-dlp.
    """
    output_dir = "@videos"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\nIniciando download e conversão para MP3...")
            ydl.download([url])
            print(f"\nDownload concluído! O arquivo foi salvo na pasta: {output_dir}")

    except Exception as e:
        print(f"\nOcorreu um erro durante o processo: {e}")

if __name__ == "__main__":
    youtube_url = input("Por favor, insira o link do vídeo do YouTube: ")
    if youtube_url:
        download_audio_with_yt_dlp(youtube_url)
