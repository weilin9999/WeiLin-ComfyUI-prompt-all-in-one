
import requests
import json
import os
import sys
appendPath = os.path.join(os.path.dirname(__file__), "./")
sys.path.append(appendPath)
import llm.llm as llmc
import Translator


class LLMTranslator(Translator.TranslatorInterface):
     def translate(self,text: str,settings) -> str:  
        # settings['preset']='Translate Chinese into English'
        return llmc.chat(text,**settings)

# 测试专用
class LLMTranslatorTest(Translator.TranslatorInterface):
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
        return llmc.chat(text,**temp)


if __name__ == '__main__':
    appid='xx'
    secretKey='xx'
    text="今天天气非常不错，我们出去玩吧"
    modelName='qwen/qwen1_5-4b-chat-q5_k_m'
    llm_translator = LLMTranslator()
    res =Translator.translate_text(llm_translator,text,modelName)
    # print(res)
            