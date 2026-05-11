# Nok PDF Translator

<p align="center">
  <img src="./assets/example.png" width=70%>
</p>

<h5 align="center">
  This repository offers a WebUI and API endpoint that translates English PDF files into Japanese and Brazilian Portuguese while preserving the original layout.
</h5>

<p align="center">
  <img src="./assets/example.gif" width=70%>
</p>

## Features

- **Multi-language output**: translate English PDFs into Japanese or Brazilian Portuguese with a single command or through the WebUI.
- To be more readable, the translated PDF file displays the original PDF page in the left side and the translated text in the right side (see the image above).

To speed up the translation process, **translation is performed until "References" section in the PDF file**. After that, the rest of the page is copied as it is.

This repository contains some unsolved issues. Pull requests for improvements are always welcome.

## Installation

1. **Clone this repository**

```bash
   git clone https://github.com/discus0434/pdf-translator.git
   cd pdf-translator/docker
```

2. **Build the docker image via Makefile**

```bash
   make build
```

3. **Run the docker container via Makefile**

```bash
   make run
```

## GUI Usage

Access to GUI via browser.

```bash
http://localhost:8288
```

## CLI Usage

```bash
cd pdf-translator/docker && make translate INPUT="path/to/input_pdf_or_dir" LANG="pt-br"
```

You can translate a single PDF file or a directory containing PDF files.

- Use `LANG="ja"` for Japanese (default) or `LANG="pt-br"` for Brazilian Portuguese.
- The translated PDF files will be saved in the `./outputs` directory.
- Alternatively, call the CLI directly: `python cli.py -i path/to/file.pdf -l pt-br`.

## Requirements

- NVIDIA GPU **(currently only support NVIDIA GPU)**
- Docker

## License

**This repository does not allow commercial use.**

This repository is licensed under CC BY-NC 4.0. See [LICENSE](./LICENSE.md) for more information.

## References

- For PDF layout analysis, using [DiT](https://github.com/microsoft/unilm).

- For PDF to text conversion, using [PaddlePaddle](https://github.com/PaddlePaddle/PaddleOCR) model.

- For text translation, using [FuguMT](https://huggingface.co/staka/fugumt-en-ja) model from [HuggingFace](https://huggingface.co/).

  FuguMT models are distributed under the CC BY-SA 4.0 license. Please also note that the use is clearly stated as "for research purposes only" and that "no responsibility is assumed for operation or output".

- For English to Brazilian Portuguese, using the [Helsinki-NLP/opus-mt-en-pt](https://huggingface.co/Helsinki-NLP/opus-mt-en-pt) model from Hugging Face.

- Font files are from [Source Han Serif](https://github.com/adobe-fonts/source-han-serif).

## TODOs

- [ ] Make possible to highlight the translated text
- [ ] Support M1 Mac or CPU

## Contributors

Thanks to the following people who have contributed to this project:

- [Brendown Ferreira](https://github.com/Br3n0k): First implementation of the project
