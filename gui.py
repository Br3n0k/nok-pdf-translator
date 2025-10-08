from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import gradio as gr
import requests
from pdf2image import convert_from_path
from PIL import Image

from utils.languages import DEFAULT_LANGUAGE_CODE, LANGUAGE_CONFIGS

TRANSLATE_URL = "http://localhost:8765/translate_pdf/"
CLEAR_TEMP_URL = "http://localhost:8765/clear_temp_dir/"

LANGUAGE_OPTIONS = {
    f"{config.label} ({config.code})": config.code
    for config in sorted(LANGUAGE_CONFIGS.values(), key=lambda cfg: cfg.label)
}
DEFAULT_LANGUAGE_LABEL = next(
    label for label, code in LANGUAGE_OPTIONS.items() if code == DEFAULT_LANGUAGE_CODE
)


def translate_request(file: Any, language_label: str) -> tuple[Path, list[Image.Image]]:
    """Sends a POST request to the translator server to translate a PDF.

    Parameters
    ----------
    file : Any
        the PDF to be translated.
    language_label : str
        Human-readable label of the selected target language.

    Returns
    -------
    tuple[Path, list[Image.Image]]
        Path to the translated PDF and a list of images of the
        translated PDF.
    """
    if file is None:
        raise ValueError("No PDF uploaded.")

    if language_label not in LANGUAGE_OPTIONS:
        raise ValueError("Unsupported language selection.")

    with open(file.name, "rb") as input_pdf:
        response = requests.post(
            TRANSLATE_URL,
            files={"input_pdf": input_pdf},
            data={"target_language": LANGUAGE_OPTIONS[language_label]},
        )

    if response.status_code == 200:
        with open(Path(temp_dir) / "translated.pdf", "wb") as f:
            f.write(response.content)

        images = convert_from_path(Path(temp_dir) / "translated.pdf")

        requests.get(CLEAR_TEMP_URL)
        return str(Path(temp_dir) / "translated.pdf"), images
    else:
        print(f"An error occurred: {response.status_code}")


if __name__ == "__main__":
    global temp_dir
    with TemporaryDirectory() as temp_dir:
        with gr.Blocks(theme="Soft") as demo:
            with gr.Column():
                title = gr.Markdown("## PDF Translator")
                file = gr.File(label="Upload PDF")
                language = gr.Dropdown(
                    choices=list(LANGUAGE_OPTIONS.keys()),
                    value=DEFAULT_LANGUAGE_LABEL,
                    label="Target language",
                )
                btn = gr.Button(value="Translate")
                translated_file = gr.File(label="Translated PDF", file_types=[".pdf"])
                pdf_images = gr.Gallery(label="Translated PDF preview")

                btn.click(
                    translate_request,
                    inputs=[file, language],
                    outputs=[translated_file, pdf_images],
                )

        demo.queue().launch(server_name="0.0.0.0", server_port=8288)
