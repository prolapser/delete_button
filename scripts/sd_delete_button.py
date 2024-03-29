import gradio as gr
import os
from modules import scripts
from modules import script_callbacks
from pathlib import Path


delete_symbol = '\U0001F5D1'  # 🗑️
tab_current = None
image_files = []

def delete(filename):
    try:
        os.remove(filename)
    except:
        file = Path(filename)
        file.unlink()
    return

def sdelb_delete(delete_info):
    for image_file in reversed(image_files):
        if os.path.exists(image_file):
            name = os.path.basename(image_file)
            if not name.startswith('grid-'):
                delete(image_file)
                delete_info = f"{image_file} удалено"

                txt_file = os.path.splitext(image_file)[0] + ".txt"
                if os.path.exists(txt_file):
                    delete(txt_file)
                    delete_info = f"{image_file} и .txt удалено"
                
                break
        delete_info = "удалять нечего"
    delete_info = f"<b>{delete_info}</b>"

    return delete_info

class Script(scripts.Script):
    def title(self):
        return "добавление кнопки удаления"

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
            _js=tab_current + "_sdelb_addEventListener",
        )
        tab_current = None
    elif element in ["txt2img_gallery", "img2img_gallery"]:
        tab_current = element.split("_", 1)[0]
        with gr.Column():
            sdelb_delete_info = gr.HTML(elem_id=tab_current + "_sdelb_delete_info")
script_callbacks.on_after_component(on_after_component)

def on_image_saved(params : script_callbacks.ImageSaveParams):
    global image_files
    image_files.append(os.path.realpath(params.filename))
script_callbacks.on_image_saved(on_image_saved)
