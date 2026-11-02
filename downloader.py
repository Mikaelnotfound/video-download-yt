from typing import Any

import yt_dlp
import os
import argparse
from yt_dlp.cookies import YDLLogger, extract_cookies_from_browser

BROWSERS = [
    'firefox',
    'chrome',
    'chromium',
    'brave',
    'edge',
    'opera',
    'vivaldi',
    'whale',
    'safari',
]


def find_browser_cookies(ydl, browsers=None):
    """
    Procura cookies do YouTube nos navegadores da lista.

    Retorna (navegador, cookiejar) do navegador com cookies do YouTube ou,
    se nenhum tiver, o primeiro que tiver cookies quaisquer. Se nenhum
    navegador funcionar, retorna (None, None).
    """
    candidates = list[Any](browsers) if browsers else BROWSERS
    logger = YDLLogger(ydl)
    fallback = None

    for browser in candidates:
        try:
            jar = extract_cookies_from_browser(browser, None, logger=logger)
        except Exception:
            continue

        if not jar:
            continue

        if any('youtube' in cookie.domain for cookie in jar):
            return browser, jar

        if fallback is None:
            fallback = (browser, jar)

    return fallback if fallback else (None, None)


def download_audio_with_yt_dlp(url, browsers=None):
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
        'extractor_args': {
            'youtube': {
                'player_client': ['default', 'mweb'],
                'remote_components': ['ejs:github']
            }
        },
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            browser, jar = find_browser_cookies(ydl, browsers)

            if jar is not None:
                ydl.cookiejar = jar
                print(f"\nCookies carregados do navegador: {browser}")
            else:
                print("\nNenhum navegador com cookies foi encontrado. Seguindo sem cookies.")

            print(f"\nIniciando download e conversão para MP3...")
            ydl.download([url])
            print(f"\nDownload concluído! O arquivo foi salvo na pasta: {output_dir}")

    except Exception as e:
        print(f"\nOcorreu um erro durante o processo: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Baixa o áudio de um vídeo do YouTube em MP3.')
    parser.add_argument('url', nargs='?', help='Link do vídeo do YouTube')
    parser.add_argument('-b', '--browser', choices=BROWSERS,
                        help='Navegador de onde extrair os cookies (padrão: detectar automaticamente)')
    args = parser.parse_args()

    youtube_url = args.url or input("Por favor, insira o link do vídeo do YouTube: ")
    if youtube_url:
        download_audio_with_yt_dlp(youtube_url, [args.browser] if args.browser else None)
