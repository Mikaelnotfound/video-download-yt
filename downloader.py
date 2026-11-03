import yt_dlp
import os
import argparse
from yt_dlp.cookies import YDLLogger, extract_cookies_from_browser

# Navegadores suportados pelo yt-dlp, na ordem em que são testados.
# O primeiro que tiver cookies do YouTube é o usado.
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

OUTPUT_DIR = "@videos"


def find_browser_cookies(ydl, browsers=None):
    """
    Procura cookies do YouTube nos navegadores da lista.

    Retorna (navegador, cookiejar) do navegador com cookies do YouTube ou,
    se nenhum tiver, o primeiro que tiver cookies quaisquer. Se nenhum
    navegador funcionar, retorna (None, None).
    """
    candidates = list(browsers) if browsers else BROWSERS
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


def build_opts(kind):
    """
    Monta as opções do yt-dlp para um tipo de download.

    kind 'video': melhor vídeo com áudio, mesclado em MP4.
    kind 'media': melhor áudio, convertido em MP3.
    """
    opts = {
        'outtmpl': os.path.join(OUTPUT_DIR, '%(title)s', '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
        'extractor_args': {
            'youtube': {
                'player_client': ['default', 'mweb'],
                'remote_components': ['ejs:github']
            }
        },
    }

    if kind == 'video':
        # Prefere H.264 + AAC (MP4) por compatibilidade; cai para o melhor
        # disponível caso o vídeo não tenha esses codecs.
        opts['format'] = 'bv*[vcodec^=avc1]+ba[ext=m4a]/bv*+ba/b'
        opts['merge_output_format'] = 'mp4'
    else:
        opts['format'] = 'ba/b'
        opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    return opts


def download(url, kinds, browsers=None):
    """
    Baixa os tipos pedidos ('video' e/ou 'media') do mesmo endereço.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    detected = False
    browser = None
    jar = None

    for kind in kinds:
        with yt_dlp.YoutubeDL(build_opts(kind)) as ydl:
            if not detected:
                detected = True
                browser, jar = find_browser_cookies(ydl, browsers)

                if jar is not None:
                    print(f"\nCookies carregados do navegador: {browser}")
                else:
                    print("\nNenhum navegador com cookies foi encontrado. Seguindo sem cookies.")

            if jar is not None:
                ydl.cookiejar = jar

            label = 'Vídeo' if kind == 'video' else 'Áudio'
            print(f"\nBaixando {label.lower()}...")
            ydl.download([url])
            print(f"\n{label} concluído!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Baixa vídeo e/ou áudio de um vídeo do YouTube.')
    parser.add_argument('url', nargs='?', help='Link do vídeo do YouTube')
    parser.add_argument('-v', '--video', action='store_true',
                        help='Baixa apenas o vídeo (com áudio)')
    parser.add_argument('-m', '--media', '--midia', action='store_true',
                        help='Baixa apenas o áudio (MP3)')
    parser.add_argument('-b', '--browser', choices=BROWSERS,
                        help='Navegador de onde extrair os cookies (padrão: detectar automaticamente)')
    args = parser.parse_args()

    if args.video and args.media:
        kinds = ['video', 'media']
    elif args.video:
        kinds = ['video']
    elif args.media:
        kinds = ['media']
    else:
        kinds = ['video', 'media']

    youtube_url = args.url or input("Por favor, insira o link do vídeo do YouTube: ")
    if youtube_url:
        download(youtube_url, kinds, [args.browser] if args.browser else None)
