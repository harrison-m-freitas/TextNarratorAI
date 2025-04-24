# 📖 TextNarratorAI

Um sistema modular em Python, baseado nos princípios de Clean Code e SOLID, projetado para processar capítulos de novelas (webnovels, manhuas, etc.), traduzindo para o português, classificando personagens e preparando o conteúdo para narração com áudio automatizado.

![CI](https://github.com/harrison-m-freitas/TextNarratorAI/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/harrison-m-freitas/TextNarratorAI/branch/develop/graph/badge.svg)](https://codecov.io/gh/harrison-m-freitas/TextNarratorAI)



## 🎯 Objetivo

- Carregar arquivos `.txt` contendo capítulos.
- Traduzir o conteúdo para o português brasileiro utilizando IA.
- Classificar cada linha como **Narrador**, **Protagonista**, **Personagem Masculino** ou **Personagem Feminino**.
- Gerar uma estrutura de texto organizada para facilitar narração e visualização.
- Criar um resumo dos **cenários principais** presentes no capítulo.
- (Futuro) Gerar narrações em áudio usando diferentes vozes baseadas na classificação dos personagens.

## 🛠 Funcionalidades

- 📄 Carregamento e limpeza de arquivos `.txt`
- 🌍 Tradução automática com IA
- 🧠 Classificação semântica das falas
- 🗣 Geração de estrutura narrativa com categorias
- 🏞 Extração e descrição dos cenários do capítulo
- 🔊 Integração futura com sistemas de narração por voz

## 🧱 Arquitetura

O projeto é estruturado com base nos princípios de Clean Architecture, respeitando separações claras de responsabilidade e facilitando testes e manutenções futuras.

```
text_processor_ai/
├── adapters/              # Integrações com serviços externos (IA, TTS, etc)
├── core/                  # Regras de negócio (modelos, enums, interfaces)
├── use_cases/             # Casos de uso (tradução, classificação, geração)
├── utils/                 # Funções auxiliares
├── data/                  # Arquivos de entrada/saída
├── main.py                # Ponto de entrada do programa
└── di_container.py        # Injeção de dependência
```

## 🚀 Como usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/TextNarratorAI.git
   cd TextNarratorAI
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Coloque seu arquivo `.txt` dentro da pasta `data/input/`.

4. Execute o programa:
   ```bash
   python main.py
   ```

5. O resultado estará disponível em `data/output/`.

## 📦 Dependências sugeridas

- `openai` ou `deep-translator` para tradução
- `pydub` ou `elevenlabs` para geração de áudio (opcional)
- `python-dotenv` para variáveis de ambiente

## 📚 Exemplos de aplicação

- Geração de vídeos com narração para canais de YouTube (recaps, dramatizações)
- Tradução e adaptação de webnovels
- Suporte a criadores de conteúdo com automação de voz e descrição

## 🧠 Roadmap futuro

- [ ] Interface gráfica (Streamlit ou Tkinter)
- [ ] Escolha de vozes por personagem
- [ ] Análise de emoções por frase
- [ ] Exportação para formatos como `.mp3`, `.srt`, `.json`

## 👨‍💻 Autor

Desenvolvido por Harrison M. Freitas — apaixonado por tecnologia, boas práticas de código e storytelling com IA.

---
