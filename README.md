# YouTube Video Downloader

CLI em Python para baixar vídeos do YouTube em MP4 e/ou o áudio em MP3 usando `yt-dlp`.

Após instalado, o comando `video-download` pode ser executado de qualquer pasta.

## Funcionalidades

- Baixa o vídeo com áudio em MP4.
- Extrai o áudio em MP3 a 192 kbps.
- Organiza cada download em uma pasta própria, usando título e ID do vídeo.
- Limita a resolução máxima do vídeo (padrão: 1080p, máximo: 4K).
- Detecta automaticamente cookies do YouTube em navegadores instalados.
- Permite escolher o navegador, a pasta de saída e o nível de saída do terminal.
- Valida URLs e apresenta mensagens de erro sem despejar tracebacks do `yt-dlp`.
- Pode ser instalado como comando global com `pipx` ou `uv`.

## Pré-requisitos

- Python 3.11 ou superior.
- FFmpeg instalado e disponível no `PATH`. Ele é necessário para mesclar vídeo/áudio e converter MP3.

### Instalação do FFmpeg

O FFmpeg precisa estar instalado e disponível no `PATH`. Depois de instalar, confirme com:

```bash
ffmpeg -version
```

#### Debian, Ubuntu, Linux Mint e Pop!_OS

```bash
sudo apt update
sudo apt install ffmpeg
```

#### Arch Linux, Manjaro, EndeavourOS e derivados

```bash
sudo pacman -Syu ffmpeg
```

#### Fedora

```bash
sudo dnf install ffmpeg
```

Caso o pacote não seja encontrado, habilite o RPM Fusion e tente novamente:

```bash
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install ffmpeg
```

#### RHEL, CentOS Stream, Rocky Linux e AlmaLinux

```bash
sudo dnf install epel-release
sudo dnf install https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-$(rpm -E %rhel).noarch.rpm
sudo dnf install ffmpeg
```

#### openSUSE

```bash
sudo zypper refresh
sudo zypper install ffmpeg
```

Para suporte a todos os codecs, pode ser necessário habilitar o repositório Packman. Consulte a [documentação do openSUSE](https://en.opensuse.org/Additional_package_repositories#Packman) caso o pacote não esteja disponível.

#### Alpine Linux

```bash
sudo apk add ffmpeg
```

#### Void Linux

```bash
sudo xbps-install -S ffmpeg
```

#### Gentoo

```bash
sudo emerge --ask media-video/ffmpeg
```

#### NixOS

Adicione o pacote à configuração do sistema:

```nix
environment.systemPackages = with pkgs; [
  ffmpeg
];
```

Depois aplique a configuração:

```bash
sudo nixos-rebuild switch
```

Para uma sessão temporária, também é possível usar:

```bash
nix-shell -p ffmpeg
```

#### macOS

Com Homebrew:

```bash
brew install ffmpeg
```

Com MacPorts:

```bash
sudo port install ffmpeg
```

#### Windows

Com `winget`:

```powershell
winget install --id Gyan.FFmpeg -e
```

Com Chocolatey:

```powershell
choco install ffmpeg
```

Com Scoop:

```powershell
scoop install ffmpeg
```

Também é possível baixar manualmente em [ffmpeg.org/download.html](https://ffmpeg.org/download.html), extrair o arquivo e adicionar a pasta `bin` ao `PATH`.

Após a instalação no Windows, feche e abra o terminal novamente e confirme com `ffmpeg -version`.

> O pacote Python `yt-dlp[default,deno]` já inclui as dependências Python e o runtime Deno usados para resolver desafios JavaScript do YouTube. O FFmpeg continua sendo uma dependência de sistema.

## Instalação como comando global

Esta é a forma recomendada para usar o projeto no dia a dia.

### Com `pipx`

```bash
pipx install .
```

Ou diretamente do GitHub:

```bash
pipx install git+https://github.com/Mikaelnotfound/video-download-yt.git
```

### Com `uv`

```bash
uv tool install .
```

Ou diretamente do GitHub:

```bash
uv tool install git+https://github.com/Mikaelnotfound/video-download-yt.git
```

Depois da instalação, confirme que o comando está disponível:

```bash
video-download --help
```

O comando funciona de qualquer diretório:

```bash
cd ~/Downloads
video-download "https://www.youtube.com/watch?v=..."
```

## Uso

Baixar vídeo e áudio separado:

```bash
video-download "https://www.youtube.com/watch?v=..."
```

Baixar apenas o vídeo, já com áudio:

```bash
video-download -v "https://www.youtube.com/watch?v=..."
```

Baixar apenas o áudio em MP3:

```bash
video-download -m "https://www.youtube.com/watch?v=..."
```

Também é possível executar sem informar a URL; o programa solicitará o link:

```bash
video-download
```

### Opções

| Flag | O que faz |
| --- | --- |
| *(nenhuma)* | Baixa o vídeo (com áudio) **e** o áudio separado |
| `-v`, `--video` | Baixa apenas o vídeo, já com áudio |
| `-m`, `--media`, `--midia` | Baixa apenas o áudio em MP3 |
| `-r`, `--resolution` | Resolução máxima do vídeo (padrão: `1080`, limite: `2160`) |
| `-b`, `--browser` | Navegador de onde extrair os cookies |
| `-o`, `--output-dir` | Pasta de saída |
| `-q`, `--quiet` | Exibe apenas erros |

As flags `-v` e `-m` podem ser combinadas (`-vm`), mas nesse caso o resultado é o mesmo de rodar sem nenhuma flag.

### Exemplos

```bash
# Vídeo em até 720p
video-download -r 720 "https://www.youtube.com/watch?v=..."

# Vídeo em até 4K, em outra pasta
video-download -r 4k -o "$HOME/Downloads" "https://www.youtube.com/watch?v=..."

# Forçar cookies do Firefox
video-download -b firefox "https://www.youtube.com/watch?v=..."

# Apenas áudio, sem mensagens de progresso
video-download -q -m "https://www.youtube.com/watch?v=..."
```

### Resolução

Sem flag, o vídeo é baixado em até **1080p**. Para escolher outra resolução, use `-r` ou `--resolution`:

```bash
video-download -r 1440 "https://www.youtube.com/watch?v=..."
video-download -r 4k "https://www.youtube.com/watch?v=..."
```

Valores acima de `2160` são reduzidos para 2160p. Valores abaixo de `144` são rejeitados. O valor aceita formatos como `720`, `1080p`, `1440`, `2k` e `4k`.

### Organização dos arquivos

Por padrão, os downloads são salvos em:

- **Linux/Windows:** `~/Videos/video-download-yt`
- **macOS:** `~/Movies/video-download-yt`

Use `-o` / `--output-dir` para escolher outra pasta.

Cada vídeo baixado vira uma pasta própria:

```text
video-download-yt/
└── Nome do Vídeo [ID_DO_VIDEO]/
    ├── Nome do Vídeo [ID_DO_VIDEO].mp4
    └── Nome do Vídeo [ID_DO_VIDEO].mp3
```

O vídeo é salvo em um contêiner MP4. O script prioriza H.264/AAC para compatibilidade, mas pode usar outros codecs, como VP9/Opus ou AV1, quando não houver uma combinação compatível disponível na resolução solicitada. O áudio separado é convertido para MP3 com qualidade de 192 kbps.

## Cookies do navegador

Para acessar vídeos restritos ou que exigem login, o script pode usar os cookies do navegador. A lista de navegadores testados, em ordem, é:

| Navegador | Identificador |
| --- | --- |
| Firefox | `firefox` |
| Google Chrome | `chrome` |
| Chromium | `chromium` |
| Brave | `brave` |
| Microsoft Edge | `edge` |
| Opera | `opera` |
| Vivaldi | `vivaldi` |
| Naver Whale | `whale` |
| Safari | `safari` |

Sem `-b`, o script procura o primeiro navegador que tenha cookies do YouTube. Se nenhum navegador possuir esses cookies ou se a leitura falhar, o download segue sem cookies.

Para forçar um navegador específico:

```bash
video-download -b firefox "https://www.youtube.com/watch?v=..."
```

> **Nota:** navegadores baseados em Chromium no Linux podem depender do keyring do sistema para descriptografar os cookies. Se o navegador estiver aberto com um perfil protegido por senha, pode ser necessário fechá-lo antes de executar o script.

## Desenvolvimento

Clone o repositório:

```bash
git clone https://github.com/Mikaelnotfound/video-download-yt.git
cd video-download-yt
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows PowerShell, use:

```powershell
.venv\Scripts\Activate.ps1
```

Instale o projeto em modo editável com as dependências de desenvolvimento:

```bash
pip install -r requirements-dev.txt
```

Executar sem instalar o comando global:

```bash
python downloader.py --help
```

Executar os testes:

```bash
python -m pytest -q
```

Construir o pacote:

```bash
python -m build
```

O pacote gera `video-download` no Linux/macOS e `video-download.exe` no Windows.

## Dependências

- `yt-dlp[default,deno]`: download, extração e suporte aos desafios JavaScript do YouTube.
- FFmpeg: dependência de sistema para pós-processamento.

## Aviso

Respeite os termos de uso do YouTube e os direitos autorais do conteúdo baixado. Use o projeto apenas para conteúdo que você tem permissão para acessar e armazenar.
