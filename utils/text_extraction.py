from utils.pdf_utils import handle_pdf
from utils.image_utils import handle_image
from utils.msg_utils import handle_msg
from utils.eml_utils import handle_eml
from utils.docx_utils import handle_docx
from utils.html_utils import handle_html
from utils.doc_utils import handle_doc
from utils.media_utils import handle_video, handle_audio, handle_gif
from utils.spreadsheet_utils import handle_xlsx
from utils.text_utils import handle_txt, handle_rtf, handle_json
from utils.pptx_utils import handle_pptx

def process_file(file):
    ext = file.suffix.lower()
    if ext == ".pdf":
        return file.name, *handle_pdf(file)
    elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".webp"]:
        return file.name, *handle_image(file)
    elif ext == ".msg":
        return file.name, *handle_msg(file)
    elif ext == ".eml":
        return file.name, *handle_eml(file)
    elif ext == ".docx":
        return file.name, *handle_docx(file)
    elif ext == ".doc":
        return file.name, *handle_doc(file)
    elif ext == ".pptx":
        return file.name, *handle_pptx(file)
    elif ext == ".xlsx":
        return file.name, *handle_xlsx(file)
    elif ext == ".txt":
        return file.name, *handle_txt(file)
    elif ext == ".rtf":
        return file.name, *handle_rtf(file)
    elif ext == ".json":
        return file.name, *handle_json(file)
    elif ext == ".gif":
        return file.name, *handle_gif(file)
    elif ext in [".mp4"]:
        return file.name, *handle_video(file)
    elif ext in [".mp3", ".wav", ".m4a"]:
        return file.name, *handle_audio(file)
    elif ext in [".htm", ".html", ".mht"]:
        return file.name, *handle_html(file)
    else:
        return file.name, None, None  # unsupported
