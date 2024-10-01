
import re
from .sd_webui_prompt_all_in_one_app import launch
import os
import pkg_resources
import comfy.lora
import folder_paths
import comfy.utils
import logging
import re
import locale
import shutil


# 正向提示词 STRING
class WeiLinComfyUIPromptAllInOneGreat:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "positive": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "输入正向提示词",
                })
            },
        }

    RETURN_TYPES = ("STRING",)

    RETURN_NAMES = ("正向 STRING",)

    FUNCTION = "encode"

    #OUTPUT_NODE = False

    CATEGORY = "WeiLin Nodes (WeiLin节点)"

    def encode(self, positive):
        return (positive,)

# 反向提示词 STRING
class WeiLinComfyUIPromptAllInOneNeg:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "negative": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "输入反向提示词",
                })
            },
        }

    RETURN_TYPES = ("STRING",)

    RETURN_NAMES = ("反向 STRING",)

    FUNCTION = "encode"

    #OUTPUT_NODE = False

    CATEGORY = "WeiLin Nodes (WeiLin节点)"

    def encode(self, negative):
        return (negative,)

#提示词编辑器 二合一 转 STRING
class WeiLinPromptToString:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "positive": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "输入正向提示词",
                }),
                "negative": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "输入反向提示词",
                }),
            },
        }

    RETURN_TYPES = ("STRING","STRING")

    RETURN_NAMES = ("正向 STRING","反向 STRING")

    FUNCTION = "encode"

    #OUTPUT_NODE = False

    CATEGORY = "WeiLin Nodes (WeiLin节点)"

    def encode(self, positive,negative):
        return (positive,negative)


# 提示词适配Lora加载器
class WeiLinComfyUIPromptToLoras:

    def __init__(self):
        self.loaded_loraA = None
        self.loaded_loraB = None
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP", ),
                "positive": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "输入正向提示词",
                }),
                "negative": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "输入反向提示词",
                }),
            },
        }

    # RETURN_TYPES = ("STRING",)
    # RETURN_TYPES = ("MODEL", "CLIP")
    RETURN_TYPES = ("MODEL", "CONDITIONING", "CONDITIONING")
    RETURN_NAMES = ("model","正向条件 CONDITIONING","负面条件 CONDITIONING")

    # FUNCTION = "encode"
    FUNCTION = "load_lora_great"

    #OUTPUT_NODE = False

    CATEGORY = "WeiLin Nodes (WeiLin节点)"
    
    # 加载Lora
    def load_lora_great(self, model, clip, positive,negative):
        model_lora_secondA = model
        clip_lora_secondA = clip
        clip_secondB = clip #反向的CLIP

        # 当模型不为空时
        if model != None:
            #处理正向
            arr,rel_str = replaceStrFunc(positive)
            for str_lora_item in arr:
                loar_sim_path,str_n_arr = getStrLoraName(str_lora_item)
                # print(loar_sim_path,str_n_arr)
                print(str_n_arr)
                strength_model = 1
                strength_clip = 1
                if len(str_n_arr) > 0:
                    if len(str_n_arr) == 1:
                        strength_model = float(str_n_arr[0])
                        strength_clip = float(str_n_arr[0])
                    if len(str_n_arr) > 1:
                        strength_model = float(str_n_arr[0])
                        strength_clip = float(str_n_arr[1])
                
                lora_path = folder_paths.get_full_path("loras", loar_sim_path)
                lora = None
                if self.loaded_loraA is not None:
                    if self.loaded_loraA[0] == lora_path:
                        lora = self.loaded_loraA[1]
                    else:
                        temp = self.loaded_loraA
                        self.loaded_loraA = None
                        del temp

                if lora is None:
                    lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
                    self.loaded_loraA = (lora_path, lora)

                model_lora_secondA, clip_lora_secondA = load_lora_for_models(model_lora_secondA, clip_lora_secondA, lora, strength_model, strength_clip)

        # prompt正向返回
        tokensA = clip_lora_secondA.tokenize(rel_str)
        outputA = clip_lora_secondA.encode_from_tokens(tokensA, return_pooled=True, return_dict=True)
        condA = outputA.pop("cond")
        # prompt反向返回 反向不支持Lora
        tokensB = clip_secondB.tokenize(negative)
        outputB = clip_secondB.encode_from_tokens(tokensB, return_pooled=True, return_dict=True)
        condB = outputB.pop("cond")
        return (model_lora_secondA,[[condA, outputA]],[[condB, outputB]])
        # return (model_lora_second, clip_lora_second)

# 仅正向提示词的Lora自动加载器
class WeiLinComfyUIPromptToLorasOnly:

    def __init__(self):
        self.loaded_loraA = None
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP", ),
                "positive": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "输入正向提示词",
                })
            },
        }

    # RETURN_TYPES = ("STRING",)
    # RETURN_TYPES = ("MODEL", "CLIP")
    RETURN_TYPES = ("MODEL", "CONDITIONING",)
    RETURN_NAMES = ("model","正向条件 CONDITIONING",)

    # FUNCTION = "encode"
    FUNCTION = "load_lora_great"

    #OUTPUT_NODE = False

    CATEGORY = "WeiLin Nodes (WeiLin节点)"
    
    # 加载Lora
    def load_lora_great(self, model, clip, positive):
        model_lora_secondA = model
        clip_lora_secondA = clip

        # 当模型不为空时
        if model != None:
            #处理正向
            arr,rel_str = replaceStrFunc(positive)
            for str_lora_item in arr:
                loar_sim_path,str_n_arr = getStrLoraName(str_lora_item)
                # print(loar_sim_path,str_n_arr)
                print(str_n_arr)
                strength_model = 1
                strength_clip = 1
                if len(str_n_arr) > 0:
                    if len(str_n_arr) == 1:
                        strength_model = float(str_n_arr[0])
                        strength_clip = float(str_n_arr[0])
                    if len(str_n_arr) > 1:
                        strength_model = float(str_n_arr[0])
                        strength_clip = float(str_n_arr[1])
                
                lora_path = folder_paths.get_full_path("loras", loar_sim_path)
                lora = None
                if self.loaded_loraA is not None:
                    if self.loaded_loraA[0] == lora_path:
                        lora = self.loaded_loraA[1]
                    else:
                        temp = self.loaded_loraA
                        self.loaded_loraA = None
                        del temp

                if lora is None:
                    lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
                    self.loaded_loraA = (lora_path, lora)

                model_lora_secondA, clip_lora_secondA = load_lora_for_models(model_lora_secondA, clip_lora_secondA, lora, strength_model, strength_clip)

        # prompt正向返回
        tokensA = clip_lora_secondA.tokenize(rel_str)
        outputA = clip_lora_secondA.encode_from_tokens(tokensA, return_pooled=True, return_dict=True)
        condA = outputA.pop("cond")

        return (model_lora_secondA,[[condA, outputA]])
        # return (model_lora_second, clip_lora_second)




def load_lora_for_models(model, clip, lora, strength_model, strength_clip):
    key_map = {}
    if model is not None:
        key_map = comfy.lora.model_lora_keys_unet(model.model, key_map)
    if clip is not None:
        key_map = comfy.lora.model_lora_keys_clip(clip.cond_stage_model, key_map)

    loaded = comfy.lora.load_lora(lora, key_map)
    if model is not None:
        new_modelpatcher = model.clone()
        k = new_modelpatcher.add_patches(loaded, strength_model)
    else:
        k = ()
        new_modelpatcher = None

    if clip is not None:
        new_clip = clip.clone()
        k1 = new_clip.add_patches(loaded, strength_clip)
    else:
        k1 = ()
        new_clip = None
    k = set(k)
    k1 = set(k1)
    for x in loaded:
        if (x not in k) and (x not in k1):
            logging.warning("NOT LOADED {}".format(x))

    return (new_modelpatcher, new_clip)

# 匹配串
def replaceStrFunc(nom_str):
    # 原始字符串
    original_str  = nom_str
    # 使用正则表达式找到所有匹配的lora字符串
    lora_patterns = re.findall(r"<lora:[^<>]*>", original_str)
    # 初始化一个空字符串来存储修改后的结果
    modified_str = ""
    # 遍历原始字符串，移除匹配的lora字符串及其后的逗号
    last_index = 0  # 上一个lora字符串或字符串开头的索引
    for pattern in lora_patterns:
        # 将当前lora字符串之前的内容添加到modified_str中，跳过lora字符串及其后的逗号
        modified_str += original_str[last_index:original_str.find(pattern)]
        # 更新last_index为当前lora字符串之后的位置
        last_index = original_str.find(pattern) + len(pattern)
        # 如果lora字符串后面有逗号，则跳过逗号
        if last_index < len(original_str) and original_str[last_index] == ',':
            last_index += 1
    # 添加原始字符串中最后一个lora字符串之后的所有内容（如果有的话）
    modified_str += original_str[last_index:]
    # 移除尾部可能多余的逗号
    if modified_str.endswith(','):
        modified_str = modified_str[:-1]
    return (lora_patterns,modified_str)

def getStrLoraName(str):
    # 原始字符串  
    str_input = str
    # 使用正则表达式提取<lora:...>中的字符串
    match = re.search(r"<lora:([^>]*)>", str_input)
    if match:
        lora_content = match.group(1)  # 提取出的字符串，不包括<lora:和>
        # 检查是否包含:
        if ':' in lora_content:
            # 分割字符串
            parts = lora_content.split(':')
            # 处理分割后的部分
            main_part = parts[0]  # 第一个部分，即:前的字符串
            # 检查是否有额外的:和对应的数字
            numbers = []
            for part in parts[1:]:
                # 尝试从每个部分中提取数字
                num_match = re.search(r'(-?\d+(\.\d+)?)', part)
                if num_match:
                    numbers.append(num_match.group(0))  # 将找到的数字添加到列表中
            # 输出结果
            # print("Main Part:", main_part)
            # print("Numbers:", numbers)
            return (main_part,numbers)
        else:
            # 如果没有:，则只输出提取的字符串
            # print("Content:", lora_content)
            return (lora_content,None)
    else:
        return (None,None)


base_path = os.path.join(os.path.dirname(__file__), "sd_webui_prompt_all_in_one_app")
req_path = os.path.join(base_path,"requirements.txt")

def dist2package(dist: str):
    return ({
        "gradio": "gradio",
        "ruamel.yaml": "ruamel.yaml",
    }).get(dist, dist)


def install_requirements(requirements_file_path):
    # copy from controlnet, thanks
    with open(requirements_file_path) as file:
        for package in file:
            try:
                package = package.strip()
                if '==' in package:
                    package_name, package_version = package.split('==')
                    installed_version = pkg_resources.get_distribution(package_name).version
                    if installed_version != package_version:
                        launch.run_pip(f"install {package}", f"WeiLinComfyUIPromptAllInOne requirement: changing {package_name} version from {installed_version} to {package_version}")
                elif not launch.is_installed(dist2package(package)):
                    launch.run_pip(f"install {package}", f"WeiLinComfyUIPromptAllInOne requirement: {package}")
            except Exception as e:
                print(e)
                print(f'[错误]: Failed to install {package}, something may not work.')


#安装原APP依赖
print('WeiLinComfyUIPromptAllInOne 请求安装依赖中.......')
loadErr = 0
try:
    install_requirements(req_path)
except:
    loadErr = 1
    print('WeiLinComfyUIPromptAllInOne 请求安装依赖失败 =======')
if loadErr == 0:
    print('WeiLinComfyUIPromptAllInOne 请求安装依赖成功 =======')


# 启动原APP
from .sd_webui_prompt_all_in_one_app.app import app_start
app_start()

# 启动LoraInfo路由
from .script.lorainfo import loraInfoApp
loraInfoApp()
# 启动LLM大模型路由
from .script.llm_server import runLLMServerAPP 
runLLMServerAPP()


def copy_folder(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for item in os.listdir(source_folder):
        source = os.path.join(source_folder, item)
        destination = os.path.join(destination_folder, item)

        if os.path.isdir(source):
            copy_folder(source, destination)
        else:
            shutil.copy2(source, destination)


# 检测Tag组是否存在，不存在则复制模板
dir = os.path.join(os.path.dirname(__file__),'./group_tags/')
filenames=os.listdir(dir)
try:
    filenames.remove(".gitignore")
except:
    None
if len(filenames) <= 0:
    dirDes = os.path.join(os.path.dirname(__file__),'./templete/')
    copy_folder(dirDes, dir)



# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "WeiLinPromptToString": WeiLinPromptToString,
    "WeiLinComfyUIPromptToLoras": WeiLinComfyUIPromptToLoras,
    "WeiLinComfyUIPromptToLorasOnly": WeiLinComfyUIPromptToLorasOnly,
    "WeiLinComfyUIPromptAllInOneGreat": WeiLinComfyUIPromptAllInOneGreat,
    "WeiLinComfyUIPromptAllInOneNeg": WeiLinComfyUIPromptAllInOneNeg,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {}

# 检测系统语言
localLan = locale.getdefaultlocale()[0]
if localLan == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "WeiLinPromptToString": "WeiLin 二合一提示词转String",
        "WeiLinComfyUIPromptToLoras": "WeiLin 二合一提示词Lora自动加载",
        "WeiLinComfyUIPromptToLorasOnly": "WeiLin 正向提示词Lora自动加载",
        "WeiLinComfyUIPromptAllInOneGreat": "WeiLin 正向提示词转String",
        "WeiLinComfyUIPromptAllInOneNeg": "WeiLin 反向提示词转String",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "WeiLinPromptToString": "WeiLin TwoInOne Prompt To String",
        "WeiLinComfyUIPromptToLoras": "WeiLin TwoInOne Prompt To AutoLoras",
        "WeiLinComfyUIPromptToLorasOnly": "WeiLin Positive Prompt To AutoLoras",
        "WeiLinComfyUIPromptAllInOneGreat": "WeiLin Positive Prompt To String",
        "WeiLinComfyUIPromptAllInOneNeg": "WeiLin Negative Prompt To String",
    }

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]