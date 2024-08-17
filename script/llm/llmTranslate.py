
import requests
import json
import os
import sys
dirPath = os.path.join(os.path.dirname(__file__), "../")
sys.path.append(dirPath)
from llm.llm import chat,chat_imagine
from llm.Translator import TranslatorInterface,translate_text


class LLMTranslator(TranslatorInterface):
     def translate(self,text: str,settings) -> str:  
        # settings['preset']='Translate Chinese into English'
        return chat(text,**settings)

# 测试专用
class LLMTranslatorTest(TranslatorInterface):
     def translate(self,text: str,settings) -> str:
        temp = {
            "appid": "",
            "llmName": settings['llmName'],
            "n_gpu_layers": -1,
            "preset": 'Translate Chinese into English',
            "secret": "",
            "server": "llm",
            "temperature": 1.2
        }
        return chat(text,**temp)


if __name__ == '__main__':
    appid='xx'
    secretKey='xx'
    text="今天天气非常不错，我们出去玩吧"
    modelName='qwen/qwen1_5-4b-chat-q5_k_m'
    llm_translator = LLMTranslator()
    res =translate_text(llm_translator,text,modelName)
    # print(res)
            