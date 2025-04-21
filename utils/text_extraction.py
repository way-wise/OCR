from utils.pdf_utils import handle_pdf
from utils.image_utils import handle_image
from utils.msg_utils import handle_msg

def process_file(file):
    ext = file.suffix.lower()
    if ext == ".pdf":
        return file.name, *handle_pdf(file)
    elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".tif"]:
        return file.name, *handle_image(file)
    elif ext == ".msg":
        return file.name, *handle_msg(file)
    else:
        return file.name, None, None  # unsupported
