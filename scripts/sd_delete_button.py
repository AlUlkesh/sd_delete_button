import gradio as gr
import os
from modules import scripts
from modules import script_callbacks
from pathlib import Path
try:
    from send2trash import send2trash
    send2trash_installed = True
except ImportError:
    print("Delete Button: send2trash is not installed. recycle bin cannot be used.")
    send2trash_installed = False

delete_symbol = '\U0001f5d1'  # 🗑
tab_current = None
image_files = []

def delete(filename):
    if send2trash_installed:
        send2trash(filename)
    else:
        file = Path(filename)
        file.unlink()
    return

def sdelb_delete(delete_info):
    for image_file in reversed(image_files):
        if os.path.exists(image_file):
            name = os.path.basename(image_file)
            if not name.startswith('grid-'):
                delete(image_file)
                delete_info = f"{image_file} deleted"
                break
        delete_info = "Could not delete anything"

    return delete_info

class Script(scripts.Script):
    def title(self):
        return "Add delete button"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def process(self, p):
        global image_files
        image_files = []

def on_after_component(component, **kwargs):
    global tab_current, sdelb_delete_info
    element = kwargs.get("elem_id")
    if element == "extras_tab" and tab_current is not None:
        sdelb_delete_button = gr.Button(value=delete_symbol)
        sdelb_delete_button.click(
            fn=sdelb_delete,
            inputs=[sdelb_delete_info],
            outputs=[sdelb_delete_info],
        )
        tab_current = None
    elif element in ["txt2img_gallery", "img2img_gallery"]:
        tab_current = element.split("_", 1)[0]
        with gr.Column():
            sdelb_delete_info = gr.HTML()
script_callbacks.on_after_component(on_after_component)

def on_image_saved(params : script_callbacks.ImageSaveParams):
    global image_files
    image_files.append(os.path.realpath(params.filename))
script_callbacks.on_image_saved(on_image_saved)
