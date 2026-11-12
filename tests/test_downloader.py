from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
import yt_dlp

import downloader


YOUTUBE_URL = 'https://www.youtube.com/watch?v=jNQXAC9IVRw'


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('144', 144),
        ('720', 720),
        ('1080p', 1080),
        ('1440', 1440),
        ('2160', 2160),
        ('2161', 2160),
        ('4k', 2160),
        ('2k', 1440),
        ('1k', 1080),
    ],
)
def test_parse_resolution_accepts_valid_values(value, expected):
    assert downloader.parse_resolution(value) == expected


@pytest.mark.parametrize('value', ['abc', '', '0', '-1', '100', '1.5', 'k', 'p'])
def test_parse_resolution_rejects_invalid_values(value):
    with pytest.raises(Exception):
        downloader.parse_resolution(value)


@pytest.mark.parametrize(
    'url',
    [
        'https://www.youtube.com/watch?v=abc',
        'http://youtube.com/watch?v=abc',
        'https://music.youtube.com/watch?v=abc',
        'https://youtu.be/abc',
        'https://www.youtube-nocookie.com/embed/abc',
    ],
)
def test_validate_youtube_url_accepts_youtube_urls(url):
    assert downloader.validate_youtube_url(url) == url


@pytest.mark.parametrize(
    'url',
    [
        '',
        'not-a-url',
        'ftp://youtube.com/watch?v=abc',
        'https://youtube.com.evil.example/watch?v=abc',
        'https://evil.example/?url=youtube.com',
        'https://youtube.com@evil.example/watch?v=abc',
    ],
)
def test_validate_youtube_url_rejects_invalid_urls(url):
    with pytest.raises(ValueError):
        downloader.validate_youtube_url(url)


def test_build_opts_video_uses_safe_template_and_codec_preference(tmp_path):
    opts = downloader.build_opts('video', resolution=720, output_dir=tmp_path)

    assert opts['format'].startswith('bv*[height<=720][vcodec^=avc1]')
    assert opts['merge_output_format'] == 'mp4'
    assert '%(id)s' in opts['outtmpl']
    assert 'remote_components' not in opts
    assert opts['noplaylist'] is True
    assert 'noprogress' in opts


def test_build_opts_media_configures_mp3(tmp_path):
    opts = downloader.build_opts('media', output_dir=tmp_path)

    assert opts['format'] == 'ba/b'
    assert opts['postprocessors'][0]['preferredcodec'] == 'mp3'
    assert opts['postprocessors'][0]['preferredquality'] == '192'


def test_build_opts_rejects_unknown_kind(tmp_path):
    with pytest.raises(ValueError):
        downloader.build_opts('outro', output_dir=tmp_path)


def test_build_opts_rejects_out_of_range_resolution(tmp_path):
    with pytest.raises(ValueError):
        downloader.build_opts('video', resolution=100, output_dir=tmp_path)
    with pytest.raises(ValueError):
        downloader.build_opts('video', resolution=3000, output_dir=tmp_path)


def test_build_opts_adds_cookie_browser(tmp_path):
    opts = downloader.build_opts(
        'video', output_dir=tmp_path, browser='firefox')

    assert opts['cookiesfrombrowser'] == ('firefox',)


def test_is_youtube_cookie_does_not_accept_lookalike_domain():
    assert downloader._is_youtube_cookie(SimpleNamespace(domain='.youtube.com'))
    assert downloader._is_youtube_cookie(SimpleNamespace(domain='youtu.be'))
    assert not downloader._is_youtube_cookie(SimpleNamespace(domain='notyoutube.com'))


@patch('downloader.yt_dlp.YoutubeDL')
def test_find_browser_cookies_returns_browser_with_youtube_cookie(mock_ydl):
    probe = MagicMock()
    probe.cookiejar = [SimpleNamespace(domain='.youtube.com')]
    mock_ydl.return_value.__enter__.return_value = probe

    browser, failures = downloader.find_browser_cookies(['firefox'])

    assert browser == 'firefox'
    assert failures == []


@patch('downloader.yt_dlp.YoutubeDL')
def test_find_browser_cookies_does_not_use_unrelated_cookies(mock_ydl):
    probe = MagicMock()
    probe.cookiejar = [SimpleNamespace(domain='.example.com')]
    mock_ydl.return_value.__enter__.return_value = probe

    browser, failures = downloader.find_browser_cookies(['firefox'])

    assert browser is None
    assert failures == []


@patch('downloader.find_browser_cookies', return_value=(None, []))
@patch('downloader.yt_dlp.YoutubeDL')
def test_download_invokes_ytdlp_and_returns_success(mock_ydl, mock_find, tmp_path):
    ydl = MagicMock()
    ydl.download.return_value = 0
    mock_ydl.return_value.__enter__.return_value = ydl

    assert downloader.download(
        YOUTUBE_URL, ['video'], resolution=720,
        output_dir=tmp_path, quiet=True) == 0

    ydl.download.assert_called_once_with([YOUTUBE_URL])
    opts = mock_ydl.call_args.args[0]
    assert opts['format'].startswith('bv*[height<=720]')


@patch('downloader.find_browser_cookies')
@patch('downloader.yt_dlp.YoutubeDL')
def test_download_uses_explicit_browser_without_detection(mock_ydl, mock_find, tmp_path):
    ydl = MagicMock()
    ydl.download.return_value = 0
    mock_ydl.return_value.__enter__.return_value = ydl

    assert downloader.download(
        YOUTUBE_URL, ['media'], browser='firefox',
        output_dir=tmp_path, quiet=True) == 0

    mock_find.assert_not_called()
    assert mock_ydl.call_args.args[0]['cookiesfrombrowser'] == ('firefox',)


@patch('downloader.find_browser_cookies', return_value=(None, []))
@patch('downloader.yt_dlp.YoutubeDL')
def test_download_reports_ytdlp_error(mock_ydl, mock_find, tmp_path, capsys):
    ydl = MagicMock()
    ydl.download.side_effect = yt_dlp.utils.DownloadError('falha simulada')
    mock_ydl.return_value.__enter__.return_value = ydl

    assert downloader.download(
        YOUTUBE_URL, ['video'], output_dir=tmp_path, quiet=True) == 1

    assert 'Erro ao baixar vídeo' in capsys.readouterr().err


def test_main_rejects_invalid_url_before_downloading(capsys):
    with pytest.raises(SystemExit) as exc_info:
        downloader.main(['not-a-url'])

    assert exc_info.value.code == 2
    error_output = capsys.readouterr().err
    assert 'error:' in error_output
    assert 'URL' in error_output
