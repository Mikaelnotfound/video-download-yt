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

Após a conclusão do download, o arquivo MP3 será salvo na pasta `@videos` dentro do diretório do projeto.

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
