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

OUTPUT_DIR = "@videos"

DEFAULT_RESOLUTION = 1080
MAX_RESOLUTION = 2160


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


def build_opts(kind, resolution=DEFAULT_RESOLUTION):
    """
    Monta as opções do yt-dlp para um tipo de download.

    kind 'video': melhor vídeo com áudio, mesclado em MP4.
    kind 'media': melhor áudio, convertido em MP3.
    resolution: altura máxima do vídeo em pixels.
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
        opts['format'] = f'bv*[height<={resolution}]+ba/b[height<={resolution}]'
        opts['merge_output_format'] = 'mp4'
    else:
        opts['format'] = 'ba/b'
        opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    return opts


def download(url, kinds, browsers=None, resolution=DEFAULT_RESOLUTION):
    """
    Baixa os tipos pedidos ('video' e/ou 'media') do mesmo endereço.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    detected = False
    browser = None
    jar = None

    for kind in kinds:
        with yt_dlp.YoutubeDL(build_opts(kind, resolution)) as ydl:
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


def parse_resolution(value):
    """
    Converte a resolução informada em altura em pixels, limitada a 4K.

    Aceita números (720, 1440, 2160) e sufixos comuns (1080p, 4k).
    """
    text = value.strip().lower()

    if text.endswith('k'):
        text = text[:-1]
        try:
            height = {'2': 1440, '4': 2160}.get(text, int(text) * 1080)
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"resolução inválida: '{value}' (use 720, 1080, 1440, 2160 ou 4k)")
    else:
        if text.endswith('p'):
            text = text[:-1]
        try:
            height = int(text)
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"resolução inválida: '{value}' (use 720, 1080, 1440, 2160 ou 4k)")

    return min(height, MAX_RESOLUTION)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Baixa vídeo e/ou áudio de um vídeo do YouTube.')
    parser.add_argument('url', nargs='?', help='Link do vídeo do YouTube')
    parser.add_argument('-v', '--video', action='store_true',
                        help='Baixa apenas o vídeo (com áudio)')
    parser.add_argument('-m', '--media', '--midia', action='store_true',
                        help='Baixa apenas o áudio (MP3)')
    parser.add_argument('-r', '--resolution', type=parse_resolution, default=DEFAULT_RESOLUTION,
                        metavar='ALTURA',
                        help=f'Resolução máxima do vídeo, até 4K (padrão: {DEFAULT_RESOLUTION}p)')
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
        download(youtube_url, kinds, [args.browser] if args.browser else None, args.resolution)
