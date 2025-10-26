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
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```

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

Após a conclusão do download, o arquivo MP3 será salvo na pasta `@videos` dentro do diretório do projeto.

## Dependências

As principais dependências do projeto estão listadas no arquivo `requirements.txt` e incluem:

- `yt-dlp`: A biblioteca principal para interagir com o YouTube e baixar o conteúdo.
- `FFmpeg`: Necessário para o pós-processamento e conversão para MP3.
