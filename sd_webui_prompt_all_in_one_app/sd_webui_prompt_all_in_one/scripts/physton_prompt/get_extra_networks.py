# -*- coding: UTF-8 -*-
import json
import os
import copy
import sys
import folder_paths
from PIL import Image
import base64
from io import BytesIO
from pathlib import Path

Path = os.path.join(os.path.dirname(__file__), "../../../../")
sys.path.append(Path)
from script.lorainfo import get_model_info

filters = [
    # 'filename',
    # 'description',
    'search_term',
    'local_preview',
    'metadata',
]

def quote_js(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    return f'"{s}"'

async def get_extra_networks():
    loras_path  = folder_paths.get_filename_list("loras")
    result = []
    result_item = {
        'name': "lora",
        'title': "Lora",
        'items': []
    }
    items = []
    for item_path in loras_path:
        lora_path = folder_paths.get_full_path("loras", item_path)
        [model_name, model_extension] = os.path.splitext(item_path)
        file_name = os.path.basename(item_path)
        # 获取个人的设置信息如果有的话
        info_data = await get_model_info(item_path,light = True)
        
        item = {
                "basename": item_path,
                "name": item_path,
                "dirname": os.path.dirname(lora_path),
                "filename": lora_path,
                "description": "",
                "preview":preview_file(lora_path),
                "model_name": model_name,
                "model_type": "loras",
                "model_filename": file_name,
                # "shorthash": lora_on_disk.shorthash,
                # "preview": self.find_preview(path),
                # "description": self.find_description(path),
                # "search_terms": search_terms,
                # "local_preview": f"{path}.{shared.opts.samples_format}",
                # "metadata": lora_on_disk.metadata,
                # "sort_keys": {'default': index, **self.get_sort_keys(lora_on_disk.filename)},
                # "sd_version": lora_on_disk.sd_version.name,
            }
        # item["prompt"] = quote_js(f"<lora:{item_path}:1") + quote_js(">")
        item["prompt"] = f"<lora:{item_path}:"
        item["local_info"] = info_data
        # item["search_terms"] = ["Lora\\"+item_path]
        items.append(item)
    result_item['items'] = items
    result.append(result_item)
    return result

def preview_file(filename: str):
    preview_exts = [".jpg", ".png", ".jpeg", ".gif"]
    preview_exts = [*preview_exts, *[".preview" + x for x in preview_exts]]
    for ext in preview_exts:
        try:
            pathStr = os.path.splitext(filename)[0] + ext
            if os.path.exists(pathStr):
                # because ComfyUI has extra model path feature
                # the path might not be relative to the ComfyUI root
                # so instead of returning the path, we return the image data directly, to avoid security issues
                # print(pathStr)
                bytes = get_thumbnail_for_image_file(pathStr)
                # Get the base64 string
                img_base64 = base64.b64encode(bytes).decode()
                # Return the base64 string
                return f"data:image/jpeg;base64, {img_base64}"
        except Exception as e:
            print(f"读取封面出错: {e}")
            return None


MAX_IMAGE_SIZE = 250

def get_thumbnail_for_image_file(file_path):
    try:
        with Image.open(file_path) as img:
            # If the image is too large, resize it
            if img.width > MAX_IMAGE_SIZE and img.height > MAX_IMAGE_SIZE:
                # Calculate new width to maintain aspect ratio
                width = int(img.width * MAX_IMAGE_SIZE / img.height)
                # Resize the image
                img = img.resize((width, MAX_IMAGE_SIZE))
            img = img.convert("RGB")
            # Save the image to a BytesIO object
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=85)
            return buffer.getvalue()
    except Exception as e:
        print(f"打开封面出错: {e}")
        return None
