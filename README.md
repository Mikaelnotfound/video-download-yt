# YouTube Audio Downloader

Este é um simples script em Python para baixar o áudio de vídeos do YouTube e salvá-lo como um arquivo MP3.

## Funcionalidades

- Extrai o áudio de qualquer vídeo do YouTube.
- Salva o áudio no formato MP3 com qualidade de 192kbps.
- Organiza os arquivos baixados em um diretório `@videos`.
- Utiliza a poderosa e atualizada biblioteca `yt-dlp` para o download.

## Pré-requisitos

- Python 3.x
- FFmpeg: `yt-dlp` requer o FFmpeg para converter os arquivos para MP3. Você precisa instalá-lo e garantir que ele esteja acessível no PATH do seu sistema.
  - **Para Debian/Ubuntu:** `sudo apt update && sudo apt install ffmpeg`
  - **Para macOS (usando Homebrew):** `brew install ffmpeg`
  - **Para Windows:** Baixe o executável no [site oficial do FFmpeg](https://ffmpeg.org/download.html) e adicione o diretório `bin` ao PATH do sistema.

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Mikaelnotfound/video-download-yt.git
   cd video-download-yt
   ```

2. **Crie e ative um ambiente virtual (Recomendado):**

   Crie o ambiente virtual:
   ```bash
   python -m venv .venv
   ```

   Depois ative-o de acordo com o seu terminal (o comando muda conforme o sistema operacional e o shell):

   | Sistema | Terminal / Shell | Ativar o ambiente | Desativar |
   | --- | --- | --- | --- |
   | Linux / macOS | `fish` | `source .venv/bin/activate.fish` | `deactivate` |
   | Linux / macOS | `zsh` | `source .venv/bin/activate` | `deactivate` |
   | Linux / macOS | `bash` | `source .venv/bin/activate` | `deactivate` |
   | Windows | PowerShell | `.venv\Scripts\Activate.ps1` | `deactivate` |
   | Windows | Prompt de Comando (CMD) | `.venv\Scripts\activate.bat` | `deactivate` |

   Após ativar, o terminal passa a exibir `(.venv)` no início da linha, indicando que o ambiente virtual está em uso.

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## Como Usar

Execute o script `downloader.py` a partir do seu terminal:

```bash
python downloader.py
```

O script solicitará que você insira o link do vídeo do YouTube que deseja baixar.

```
Por favor, insira o link do vídeo do YouTube: <COLE_O_LINK_AQUI>
```

Você também pode passar o link direto como argumento:

```bash
python downloader.py "https://www.youtube.com/watch?v=..."
```

### Opções

| Flag | O que faz |
| --- | --- |
| *(nenhuma)* | Baixa o vídeo (com áudio) **e** o áudio separado |
| `-v`, `--video` | Baixa apenas o vídeo, já com áudio |
| `-m`, `--media`, `--midia` | Baixa apenas o áudio em MP3 |
| `-r`, `--resolution` | Resolução máxima do vídeo (padrão: `1080`, limite: `2160`) |
| `-b`, `--browser` | Navegador de onde extrair os cookies |

As flags `-v` e `-m` podem ser combinadas (`-vm`), mas nesse caso o resultado é o mesmo de rodar sem nenhuma flag:

```bash
# Vídeo + áudio separado
python downloader.py "https://www.youtube.com/watch?v=..."

# Apenas o vídeo, com áudio
python downloader.py -v "https://www.youtube.com/watch?v=..."

# Apenas o áudio em MP3
python downloader.py -m "https://www.youtube.com/watch?v=..."
```

### Resolução

Sem flag, o vídeo é baixado em até **1080p**. Para escolher outra resolução, use `-r` (ou `--resolution`):

```bash
# Baixa em 720p
python downloader.py -r 720 "https://www.youtube.com/watch?v=..."

# Baixa em 1440p
python downloader.py -r 1440 "https://www.youtube.com/watch?v=..."

# Baixa em 4K (2160p, o máximo suportado)
python downloader.py -r 4k "https://www.youtube.com/watch?v=..."
```

Valores acima de `2160` são reduzidos automaticamente para 2160p. Resoluções acima de 1080p podem usar codecs AV1/VP9, que exigem players atualizados (VLC, FFmpeg, navegadores modernos).

### Organização dos arquivos

Cada vídeo baixado vira uma pasta própria dentro de `@videos`, contendo o vídeo e o áudio separados:

```
@videos/
└── Nome do Vídeo/
    ├── Nome do Vídeo.mp4    # vídeo com áudio
    └── Nome do Vídeo.mp3    # áudio separado
```

O vídeo é salvo em MP4 (H.264/AAC até 1080p, AV1/AAC acima disso) e o áudio é convertido para MP3 com qualidade de 192kbps.

## Cookies do navegador

Para acessar vídeos restritos (ou que exigem login), o script usa os cookies do seu navegador. A lista de navegadores testados, em ordem, é:

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

O script percorre essa lista e usa o primeiro navegador que encontrar com cookies do YouTube. Se nenhum dos navegadores estiver instalado ou não tiver cookies, o download segue sem cookies.

Para forçar um navegador específico, use a opção `-b` (ou `--browser`):

```bash
python downloader.py -b firefox "https://www.youtube.com/watch?v=..."
```

> **Nota:** navegadores baseados em Chromium (Chrome, Edge, Brave, Opera, etc.) no Linux dependem do keyring do sistema para descriptografar os cookies. Se o navegador estiver aberto com um perfil protegido por senha, pode ser necessário fechá-lo antes de rodar o script.

## Dependências

As principais dependências do projeto estão listadas no arquivo `requirements.txt` e incluem:

- `yt-dlp`: A biblioteca principal para interagir com o YouTube e baixar o conteúdo.
- `FFmpeg`: Necessário para o pós-processamento e conversão para MP3.
