import gradio as gr
import os
from modules import scripts
from modules import script_callbacks
from modules.ui_components import ToolButton
from pathlib import Path
try:
    from send2trash import send2trash
    send2trash_installed = True
except ImportError:
    print("Delete Button: send2trash is not installed. recycle bin cannot be used.")
    send2trash_installed = False

delete_symbol = '\U0000274c'  # ❌
tab_current = ""
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

                txt_file = os.path.splitext(image_file)[0] + ".txt"
                if os.path.exists(txt_file):
                    delete(txt_file)
                    delete_info = f"{image_file} and .txt deleted"
                
                break
        delete_info = "Could not delete anything"
    delete_info = f"<b>{delete_info}</b>"

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
    send_extras_name_old = "extras_tab"
    send_extras_name_new = tab_current + "_send_to_extras"
    element = kwargs.get("elem_id")
    if element in (send_extras_name_old, send_extras_name_new) and tab_current != "":
        if element == send_extras_name_old:
            sdelb_delete_button = gr.Button(value=delete_symbol)
        else:
            sdelb_delete_button = ToolButton(delete_symbol, elem_id=tab_current + "_sdelb_delete_button", tooltip="Delete")
        sdelb_delete_button.click(
            fn=sdelb_delete,
            inputs=[sdelb_delete_info],
            outputs=[sdelb_delete_info],
            _js=tab_current + "_sdelb_addEventListener",
        )
        tab_current = ""
    elif element in ["txt2img_gallery", "img2img_gallery"]:
        tab_current = element.split("_", 1)[0]
        with gr.Column():
            sdelb_delete_info = gr.HTML(elem_id=tab_current + "_sdelb_delete_info")
script_callbacks.on_after_component(on_after_component)

def on_image_saved(params : script_callbacks.ImageSaveParams):
    global image_files
    image_files.append(os.path.realpath(params.filename))
script_callbacks.on_image_saved(on_image_saved)
