import sys
import os

AIO_PATH = os.path.join(os.path.dirname(__file__), "sd_webui_prompt_all_in_one")
sys.path.append(AIO_PATH)

import gradio as gr
from gradio import Blocks
from typing import Optional, Dict, Any
from server import PromptServer
from aiohttp import web
from .sd_webui_prompt_all_in_one.scripts.on_app_started import on_app_started
from .install import run_install

def app_start():

    # 安装依赖
    run_install()

    static_path = os.path.join(os.path.dirname(__file__), "../prompt_static/")
    dir = os.path.join(os.path.dirname(__file__), "../prompt_js/")
    
    @PromptServer.instance.routes.get("/sd-webui-prompt-all-in-one-js")
    async def _sd_webui_prompt_all_in_one_js(request):
        # 合并JS
        js = ''
        for file in os.listdir(dir):
            if file.endswith('.js'):
                with open(os.path.join(dir, file), 'r', encoding='utf-8') as f:
                    js += f.read() + '\n'
        return web.Response(status=200, text=js, content_type="application/javascript")

    @PromptServer.instance.routes.get("/weilin/web_ui/{file_path:.*}")
    async def _getWebUI(request):
        file_path = request.match_info.get('file_path', '')
        full_path = os.path.join(static_path, file_path)
        # 检查文件路径是否存在
        if os.path.isfile(full_path):
            return web.FileResponse(full_path)
        raise web.HTTPNotFound()

    print("====== WeiLin prompt-all-in-one =====")
    print(f"APP is running  WeiLin prompt-all-in-one!.")
    print(f"WeiLinComfyUIPromptAllInOne 节点已启动成功!.")