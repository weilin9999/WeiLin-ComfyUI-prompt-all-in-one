
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
     err_msg='找不到llama_cpp模块 无法使用大模型 请安装llama_cpp模块'
     print(err_msg)
 

    
      
    
      

 



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
 
    
 