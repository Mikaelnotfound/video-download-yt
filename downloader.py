import argparse
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import yt_dlp

BROWSERS = (
    'firefox',
    'chrome',
    'chromium',
    'brave',
    'edge',
    'opera',
    'vivaldi',
    'whale',
    'safari',
)

def _default_output_dir():
    """Retorna uma pasta de mídia adequada para o sistema operacional."""
    if sys.platform == 'win32':
        base = Path.home() / 'Videos'
    elif sys.platform == 'darwin':
        base = Path.home() / 'Movies'
    else:
        xdg_videos = os.environ.get('XDG_VIDEOS_DIR')
        base = Path(xdg_videos).expanduser() if xdg_videos else Path.home() / 'Videos'
    return base / 'video-download-yt'


DEFAULT_OUTPUT_DIR = _default_output_dir()

DEFAULT_RESOLUTION = 1080
MIN_RESOLUTION = 144
MAX_RESOLUTION = 2160
VALID_KINDS = {'video', 'media'}
YOUTUBE_HOSTS = {'youtube.com', 'youtu.be', 'youtube-nocookie.com'}


def _is_youtube_cookie(cookie):
    """Retorna True para cookies de domínios do YouTube."""
    domain = (getattr(cookie, 'domain', '') or '').lstrip('.').lower().rstrip('.')
    return any(domain == host or domain.endswith(f'.{host}') for host in YOUTUBE_HOSTS)


def find_browser_cookies(browsers=None):
    """
    Procura o primeiro navegador com cookies do YouTube.

    A extração usa a opção pública ``cookiesfrombrowser`` do yt-dlp. Retorna
    ``(navegador, falhas)``; ``navegador`` é None quando nenhum candidato
    possui cookies do YouTube e ``falhas`` contém os erros de leitura.
    """
    candidates = list(browsers) if browsers else list(BROWSERS)
    failures = []

    for browser in candidates:
        try:
            with yt_dlp.YoutubeDL({
                'quiet': True,
                'no_warnings': True,
                'cookiesfrombrowser': (browser,),
            }) as probe:
                jar = probe.cookiejar
        except Exception as exc:  # noqa: BLE001 - cada navegador pode falhar de forma distinta
            message = str(exc).strip().splitlines()
            failures.append((browser, message[-1] if message else type(exc).__name__))
            continue

        if any(_is_youtube_cookie(cookie) for cookie in (jar or ())):
            return browser, failures

    return None, failures


def _validate_resolution(resolution):
    if not isinstance(resolution, int) or not MIN_RESOLUTION <= resolution <= MAX_RESOLUTION:
        raise ValueError(
            f'resolução deve estar entre {MIN_RESOLUTION} e {MAX_RESOLUTION} pixels')


def build_opts(kind, resolution=DEFAULT_RESOLUTION, output_dir=DEFAULT_OUTPUT_DIR,
               browser=None, quiet=False):
    """
    Monta as opções do yt-dlp para um tipo de download.

    kind 'video': melhor vídeo com áudio, mesclado em MP4.
    kind 'media': melhor áudio, convertido em MP3.
    resolution: altura máxima do vídeo em pixels.
    output_dir: diretório onde os downloads serão salvos.
    browser: navegador de onde os cookies serão carregados, se informado.
    quiet: reduz a saída do yt-dlp.
    """
    if kind not in VALID_KINDS:
        raise ValueError(f"tipo de download inválido: {kind!r}")

    _validate_resolution(resolution)

    output_dir = Path(output_dir).expanduser()
    name_template = '%(title)s [%(id)s]'
    opts = {
        'outtmpl': os.path.join(
            os.fspath(output_dir), name_template, f'{name_template}.%(ext)s'),
        'noplaylist': True,
        'quiet': quiet,
        'no_warnings': quiet,
        'noprogress': quiet,
    }

    if browser:
        opts['cookiesfrombrowser'] = (browser,)

    if kind == 'video':
        # Prioriza H.264/AAC para compatibilidade e usa qualquer codec como fallback.
        opts['format'] = (
            f'bv*[height<={resolution}][vcodec^=avc1]+ba[acodec^=mp4a]/'
            f'bv*[height<={resolution}]+ba/'
            f'b[height<={resolution}]'
        )
        opts['merge_output_format'] = 'mp4'
    else:
        opts['format'] = 'ba/b'
        opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    return opts


def validate_youtube_url(url):
    """Valida e normaliza uma URL do YouTube."""
    if not isinstance(url, str) or not url.strip():
        raise ValueError('informe uma URL do YouTube')

    url = url.strip()
    parsed = urlparse(url)
    if parsed.scheme not in {'http', 'https'}:
        raise ValueError('a URL deve começar com http:// ou https://')

    host = (parsed.hostname or '').lower().rstrip('.')
    if not any(host == allowed or host.endswith(f'.{allowed}') for allowed in YOUTUBE_HOSTS):
        raise ValueError('a URL informada não é do YouTube')

    return url


def download(url, kinds, browser=None, resolution=DEFAULT_RESOLUTION,
             output_dir=DEFAULT_OUTPUT_DIR, quiet=False):
    """
    Baixa os tipos pedidos ('video' e/ou 'media') do mesmo endereço.

    Retorna 0 em caso de sucesso e 1 quando algum download falha.
    """
    url = validate_youtube_url(url)
    kinds = list(kinds)
    if not kinds or any(kind not in VALID_KINDS for kind in kinds):
        raise ValueError('os tipos devem ser uma combinação de "video" e "media"')

    output_dir = Path(output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    detected_browser = browser
    if detected_browser is None:
        detected_browser, failures = find_browser_cookies()
        if detected_browser and not quiet:
            print(f'\nCookies carregados do navegador: {detected_browser}')
        elif not quiet:
            print('\nNenhum navegador com cookies do YouTube foi encontrado. '
                  'Seguindo sem cookies.')
            for failed_browser, message in failures[:3]:
                print(f'  - {failed_browser}: {message}', file=sys.stderr)

    for kind in kinds:
        label = 'Vídeo' if kind == 'video' else 'Áudio'
        if not quiet:
            print(f'\nBaixando {label.lower()}...')

        opts = build_opts(
            kind,
            resolution=resolution,
            output_dir=output_dir,
            browser=detected_browser,
            quiet=quiet,
        )

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                retcode = ydl.download([url])
        except yt_dlp.utils.DownloadError as exc:
            print(f'\nErro ao baixar {label.lower()}: {exc}', file=sys.stderr)
            return 1
        except OSError as exc:
            print(f'\nErro de sistema ao baixar {label.lower()}: {exc}', file=sys.stderr)
            return 1

        if retcode:
            print(f'\nFalha ao baixar {label.lower()}.', file=sys.stderr)
            return retcode

        if not quiet:
            print(f'\n{label} concluído!')

    return 0


def parse_resolution(value):
    """
    Converte a resolução informada em altura em pixels, limitada a 4K.

    Aceita números (720, 1440, 2160) e sufixos comuns (1080p, 4k).
    """
    text = value.strip().lower()

    try:
        if text.endswith('k'):
            number = text[:-1]
            if number == '2':
                height = 1440
            else:
                multiplier = int(number)
                if multiplier <= 0:
                    raise ValueError
                height = multiplier * 1080
        else:
            if text.endswith('p'):
                text = text[:-1]
            height = int(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"resolução inválida: '{value}' "
            f'(use um valor entre {MIN_RESOLUTION} e {MAX_RESOLUTION}, '
            'por exemplo: 720, 1080, 1440 ou 4k)') from exc

    if height < MIN_RESOLUTION:
        raise argparse.ArgumentTypeError(
            f"resolução inválida: '{value}' "
            f'(o valor mínimo é {MIN_RESOLUTION})')

    return min(height, MAX_RESOLUTION)


def _output_dir(value):
    return Path(value).expanduser()


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Baixa vídeo e/ou áudio de um vídeo do YouTube.')
    parser.add_argument('url', nargs='?', help='Link do vídeo do YouTube')
    parser.add_argument('-v', '--video', action='store_true',
                        help='Baixa apenas o vídeo (com áudio)')
    parser.add_argument('-m', '--media', '--midia', action='store_true',
                        help='Baixa apenas o áudio (MP3)')
    parser.add_argument('-r', '--resolution', type=parse_resolution,
                        default=DEFAULT_RESOLUTION, metavar='ALTURA',
                        help=f'Resolução máxima do vídeo, até 4K (padrão: {DEFAULT_RESOLUTION}p)')
    parser.add_argument('-b', '--browser', choices=BROWSERS,
                        help='Navegador de onde extrair os cookies '
                             '(padrão: detectar automaticamente)')
    parser.add_argument('-o', '--output-dir', type=_output_dir,
                        default=DEFAULT_OUTPUT_DIR, metavar='PASTA',
                        help=f'Pasta de saída (padrão: {DEFAULT_OUTPUT_DIR})')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Exibe apenas erros')
    args = parser.parse_args(argv)

    if args.video and args.media:
        kinds = ['video', 'media']
    elif args.video:
        kinds = ['video']
    elif args.media:
        kinds = ['media']
    else:
        kinds = ['video', 'media']

    youtube_url = args.url
    if not youtube_url:
        try:
            youtube_url = input('Por favor, insira o link do vídeo do YouTube: ')
        except EOFError:
            parser.error('informe uma URL do YouTube')

    try:
        youtube_url = validate_youtube_url(youtube_url)
    except ValueError as exc:
        parser.error(str(exc))

    return download(
        youtube_url,
        kinds,
        browser=args.browser,
        resolution=args.resolution,
        output_dir=args.output_dir,
        quiet=args.quiet,
    )


if __name__ == '__main__':
    sys.exit(main())
