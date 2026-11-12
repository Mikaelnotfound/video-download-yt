# YouTube Video Downloader

Script em Python para baixar vídeos do YouTube em MP4 e/ou o áudio em MP3 usando `yt-dlp`.

## Funcionalidades

- Baixa o vídeo com áudio em MP4.
- Extrai o áudio em MP3 a 192 kbps.
- Organiza cada download em uma pasta própria, usando título e ID do vídeo.
- Limita a resolução máxima do vídeo (padrão: 1080p, máximo: 4K).
- Detecta automaticamente cookies do YouTube em navegadores instalados.
- Permite escolher o navegador, a pasta de saída e o nível de saída do terminal.
- Valida URLs e apresenta mensagens de erro sem despejar tracebacks do `yt-dlp`.

## Pré-requisitos

- Python 3.11 ou superior.
- FFmpeg instalado e disponível no `PATH`. Ele é necessário para mesclar vídeo/áudio e converter MP3.

### Instalação do FFmpeg

- **Debian/Ubuntu:**
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

- **macOS (Homebrew):**
  ```bash
  brew install ffmpeg
  ```

- **Windows:** baixe em [ffmpeg.org/download.html](https://ffmpeg.org/download.html), extraia e adicione a pasta `bin` ao `PATH`.

> O pacote Python `yt-dlp[default,deno]` já inclui as dependências Python e o runtime Deno usados para resolver desafios JavaScript do YouTube. O FFmpeg continua sendo uma dependência de sistema.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/Mikaelnotfound/video-download-yt.git
   cd video-download-yt
   ```

2. Crie e ative um ambiente virtual:

   | Sistema | Shell | Ativar |
   | --- | --- | --- |
   | Linux / macOS | bash/zsh | `source .venv/bin/activate` |
   | Linux / macOS | fish | `source .venv/bin/activate.fish` |
   | Windows | PowerShell | `.venv\Scripts\Activate.ps1` |
   | Windows | CMD | `.venv\Scripts\activate.bat` |

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Como usar

Execute o script:

```bash
python downloader.py
```

O script solicitará a URL do vídeo:

```text
Por favor, insira o link do vídeo do YouTube:
```

Também é possível passar a URL diretamente:

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
| `-o`, `--output-dir` | Pasta de saída (padrão: `@videos` ao lado do script) |
| `-q`, `--quiet` | Exibe apenas erros |

As flags `-v` e `-m` podem ser combinadas (`-vm`), mas nesse caso o resultado é o mesmo de rodar sem nenhuma flag.

Exemplos:

```bash
# Vídeo + áudio separado
python downloader.py "https://www.youtube.com/watch?v=..."

# Apenas o vídeo, com áudio
python downloader.py -v "https://www.youtube.com/watch?v=..."

# Apenas o áudio em MP3
python downloader.py -m "https://www.youtube.com/watch?v=..."

# Vídeo em até 720p
python downloader.py -r 720 "https://www.youtube.com/watch?v=..."

# Vídeo em até 4K, em outra pasta
python downloader.py -r 4k -o "$HOME/Downloads" "https://www.youtube.com/watch?v=..."

# Forçar cookies do Firefox
python downloader.py -b firefox "https://www.youtube.com/watch?v=..."
```

### Resolução

Sem flag, o vídeo é baixado em até **1080p**. Para escolher outra resolução, use `-r` ou `--resolution`:

```bash
python downloader.py -r 1440 "https://www.youtube.com/watch?v=..."
python downloader.py -r 4k "https://www.youtube.com/watch?v=..."
```

Valores acima de `2160` são reduzidos para 2160p. Valores abaixo de `144` são rejeitados. O valor aceita formatos como `720`, `1080p`, `1440`, `2k` e `4k`.

### Organização dos arquivos

Cada vídeo baixado vira uma pasta própria dentro da pasta de saída, contendo o vídeo e/ou o áudio:

```text
@videos/
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
python downloader.py -b firefox "https://www.youtube.com/watch?v=..."
```

> **Nota:** navegadores baseados em Chromium no Linux podem depender do keyring do sistema para descriptografar os cookies. Se o navegador estiver aberto com um perfil protegido por senha, pode ser necessário fechá-lo antes de executar o script.

## Desenvolvimento e testes

Instale as dependências de desenvolvimento:

```bash
pip install -r requirements-dev.txt
```

Execute os testes:

```bash
python -m pytest -q
```

A suíte cobre validação de URL, resolução, montagem das opções do `yt-dlp`, seleção de cookies e tratamento de erros de download. O workflow de CI também audita as dependências com `pip-audit`.

## Dependências

- `yt-dlp[default,deno]`: download, extração e suporte aos desafios JavaScript do YouTube.
- FFmpeg: dependência de sistema para pós-processamento.

## Aviso

Respeite os termos de uso do YouTube e os direitos autorais do conteúdo baixado. Use o projeto apenas para conteúdo que você tem permissão para acessar e armazenar.
