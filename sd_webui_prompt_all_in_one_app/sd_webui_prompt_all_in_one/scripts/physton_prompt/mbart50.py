import time
import sys
import os

# 修复个别电脑环境会报的错
Path = os.path.dirname(__file__)
sys.path.append(Path)
from get_lang import get_lang

class Translator:
    def __init__(self):
        self.mbart_value_model = None
        self.mbart_value_tokenizer = None
        self.mbart_value_model_name = "facebook/mbart-large-50-many-to-many-mmt"
        self.mbart_value_cache_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + '/../../../../models') 
        self.mbart_value_loading = False


    def initialize(self,reload=False):
        if  self.mbart_value_loading:
            while not  self.mbart_value_loading:
                time.sleep(0.1)
                pass
            if  self.mbart_value_model is None or  self.mbart_value_tokenizer is None:
                raise Exception('error')
            # raise Exception(get_lang('model_is_loading'))
            return
        if not reload and  self.mbart_value_model is not None:
            return

        self.mbart_value_loading = True
        self.mbart_value_model = None
        self.mbart_value_tokenizer = None

        model_path = os.path.join(self.mbart_value_cache_dir, "mbart-large-50-many-to-many-mmt")
        model_file = os.path.join(model_path, "pytorch_model.bin")
        if os.path.exists(model_path) and os.path.exists(model_file):
            self.mbart_value_model_name = model_path
        try:
            from transformers import MBart50TokenizerFast, MBartForConditionalGeneration
            print(f'[sd-webui-prompt-all-in-one] 离线翻译加载中 Loading model {self.mbart_value_model_name} from {self.mbart_value_cache_dir}...')
            self.mbart_value_model = MBartForConditionalGeneration.from_pretrained(self.mbart_value_model_name, cache_dir=self.mbart_value_cache_dir)
            self.mbart_value_tokenizer = MBart50TokenizerFast.from_pretrained(self.mbart_value_model_name, cache_dir=self.mbart_value_cache_dir)
            print(f'[sd-webui-prompt-all-in-one] 离线翻译初始化模型成功  {self.mbart_value_model_name} Model loaded.')
        except Exception as e:
            print(f'[sd-webui-prompt-all-in-one] 离线翻译初始化失败 {e} Model Fail')
            raise e
        finally:
            self.mbart_value_loading = False
            # print(f'[sd-webui-prompt-all-in-one] Initialization complete. model: {mbart_value_model}, tokenizer: {mbart_value_tokenizer}')


    def translate(self,text, src_lang, target_lang):
        # print(self.mbart_value_model,self.mbart_value_tokenizer)
        if not text:
            if isinstance(text, list):
                return []
            else:
                return ''

        if self.mbart_value_model is None:
            raise Exception(get_lang('model_not_initialized'))

        if self.mbart_value_tokenizer is None:
            raise Exception(get_lang('model_not_initialized'))

        if src_lang == target_lang:
            return text

        self.mbart_value_tokenizer.src_lang = src_lang
        encoded_input = self.mbart_value_tokenizer(text, return_tensors="pt", padding=True)
        generated_tokens = self.mbart_value_model.generate(
            **encoded_input, forced_bos_token_id=self.mbart_value_tokenizer.lang_code_to_id[target_lang],
            max_new_tokens=500
        )
        return self.mbart_value_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
