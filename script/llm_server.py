import server
from aiohttp import web
import json
import sys
import os

appendPath = os.path.join(os.path.dirname(__file__), "./")
sys.path.append(appendPath)
from .llm import Translator,llmTranslate,llm

def runLLMServerAPP():
    global transObj
    transObj = {}

    settingJsonPath = os.path.join(os.path.dirname(__file__), "../llm_setting.json")

    def readJson():
        # 打开并读取 JSON 文件
        settingJsonPath = os.path.join(os.path.dirname(__file__), "../llm_setting.json")
        with open(settingJsonPath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def translate(text):
        transObj = readJson()
        trans_server=llmTranslate.LLMTranslatorTest()
        return Translator.translate_text(trans_server,text,transObj)

    @server.PromptServer.instance.routes.get("/weilin/api/llm_server/testTransServer")
    async def _testTransServer(request):
      
        trans_text = translate('苹果')
        # print(trans_text)
        if (trans_text.lower()!='apple'):
            trans_text='翻译失败'
            return web.json_response({"info":trans_text},status=201, content_type='application/json')
        else:
            trans_text='接口正常'  
       
        return web.json_response({"info":trans_text}, content_type='application/json')
    
    @server.PromptServer.instance.routes.get("/weilin/api/llm_server/getSetting")
    async def _getSetting(request):
        transObj = readJson()
        return web.json_response({"data":transObj}, content_type='application/json')
    
    @server.PromptServer.instance.routes.post("/weilin/api/llm_server/setTransServer")
    async def _setTransServer(request):
        post = await request.json()
        transObj = readJson()
        transObj["preset"] = post["preset"]
        transObj["llmName"] = post["llmName"]
        transObj["n_gpu_layers"] = int(post["n_gpu_layers"])
        transObj["temperature"] = float(post["temperature"])
        with open(settingJsonPath, 'w', encoding='utf-8') as file:
            json.dump(transObj, file, indent=4)
        transObj = readJson()
        return web.json_response('ok', content_type='application/json')
    
    @server.PromptServer.instance.routes.post("/weilin/api/llm_server/imaginePrompt")
    async def _imaginePrompt(request):
            post = await request.json()
            transObj = readJson()
            try:
                res=llm.chat_imagine(post['content'],transObj)
            except:
                return web.json_response({"info":"无法正常使用大模型，请检查你的配置，或环境有问题"}, content_type='application/json')
            return web.json_response({"info":res}, content_type='application/json')