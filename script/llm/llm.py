
import time
import os
import folder_paths
import random

# from llama_cpp import Llama
try:
    from llama_cpp import Llama
    extension_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../../models'))
    def chat(question,**kwargs):
        llm = Llama(
            model_path=os.path.join(extension_path,kwargs['llmName'])+'.gguf',
            n_gpu_layers=int(kwargs['n_gpu_layers']),
        )
        res=llm.create_chat_completion(
            messages = [
                {"role": "system", "content":kwargs['preset']},
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=float(kwargs['temperature'])

        )
        return(res['choices'][0]["message"]['content'])
    
        
    def chat_imagine(question,settings):
        return chat(question,**settings)

except Exception as e:
    err_msg='WeiLin-ComfyUI-prompt-all-in-one 找不到llama_cpp模块，以默认不加载本地大模型，可忽略该提示。'
    print(err_msg)
    # 没有模型返回空
    def chat(question,**kwargs):
        return "无法使用llama_cpp模块，请确保你已安装了该模块，如果没有请点击检测模块安装进行安装该模块。"
    def chat_imagine(question,settings):
        return chat(question,**settings)
 

    
      
    
      

 



if __name__ == '__main__':
        start_time = time.time()
        question='一个美女'
        modelName="qwen1_5-4b-chat-q2_k"
        Preset=f'你是一名AI提示词工程师，用提供的关键词构思一副精美的构图画面，只需要提示词，不要你的感受，自定义风格、场景、装饰等，尽量详细，用中文回复'
        res= chat(question,modelName,Preset)
        end_time = time.time()
        run_time = end_time - start_time
        print(run_time)
        print(res)
        pass
 
    
 