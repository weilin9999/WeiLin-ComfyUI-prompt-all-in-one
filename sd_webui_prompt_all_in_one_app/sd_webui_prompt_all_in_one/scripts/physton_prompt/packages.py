import sys
import os

# 修复个别电脑环境会报的错
Path = os.path.dirname(__file__)
sys.path.append(Path)
from get_lang import get_lang

Path = os.path.join(os.path.dirname(__file__), "../../../")
sys.path.append(Path)
import launch

packages = {
    "chardet": "chardet",
    "fastapi": "fastapi",
    "execjs": "PyExecJS",
    "lxml": "lxml",
    "tqdm": "tqdm",
    "pathos": "pathos",
    "cryptography": "cryptography",

    # The following packages are required for translation service. If you do not need translation service, you can remove them.
    # 以下是翻译所需的包，如果不需要翻译服务，可以删除掉它们。
    "openai": "openai",
    "boto3": "boto3",
    "aliyunsdkcore": "aliyun-python-sdk-core",
    "aliyunsdkalimt": "aliyun-python-sdk-alimt",
}

llmPackages =  {
    "llama-cpp-python": "llama-cpp-python"
}


def get_llm_packages_state():
    states = []
    for package_name in llmPackages:
        package = llmPackages[package_name]
        item = {
            'name': package_name,
            'package': package,
            'state': False
        }
        if launch.is_module_installed("llama_cpp"):
            item['state'] = True

        states.append(item)

    return states



def get_packages_state():
    states = []
    for package_name in packages:
        package = packages[package_name]
        item = {
            'name': package_name,
            'package': package,
            'state': False
        }
        if launch.is_installed(package) or launch.is_installed(package_name):
            item['state'] = True

        states.append(item)

    return states

def install_llm_package(name, package):
    pythonVersion = launch.run_get_python() #获取运行环境的python版本
    version_parts = pythonVersion.split()[1].split('.')[:2]  # 只取前两部分，即主版本和次版本
    major, minor = map(int, version_parts)
    whalPath = ''
    if (major, minor) == (3, 10):
        whalPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../cpp/llama_cpp_python-0.2.63-cp310-cp310-win_amd64.whl"))
    elif (major, minor) == (3, 11):
        whalPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../cpp/llama_cpp_python-0.2.63-cp311-cp311-win_amd64.whl"))
    elif (major, minor) == (3, 12):
        whalPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../cpp/llama_cpp_python-0.2.63-cp312-cp312-win_amd64.whl"))
    elif os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../cpp/llama_cpp_python.whl"))):
        whalPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../cpp/llama_cpp_python.whl"))
    else:
        return {'state': False, 'message': '未找到匹配的内置离线安装包，离线包仅支持Python10、Python11和Python12，低于或高于此版本的请手动安装！详细操作请到本插件的目录里打开cpp文件夹点击txt文件查看详细操作。'}
    result = {'state': False, 'message': ''}
    try:
        launch.run_pip_noex(f"install {whalPath}", f"WeiLin-ComfyUI-prompt-all-in-one: {name}")
        result['state'] = True
        result['message'] = get_lang('install_success', {'0': package})
    except Exception as e:
        print(e)
        print(f'Warning: Failed to install {package}, some preprocessors may not work.')
        result['message'] = get_lang('install_failed', {'0': package}) + '\n' + str(e)
    return result

def install_package(name, package):
    result = {'state': False, 'message': ''}
    try:
        launch.run_pip(f"install {package}", f"WeiLin-ComfyUI-prompt-all-in-one: {name}")
        result['state'] = True
        result['message'] = get_lang('install_success', {'0': package})
    except Exception as e:
        print(e)
        print(f'Warning: Failed to install {package}, some preprocessors may not work.')
        result['message'] = get_lang('install_failed', {'0': package}) + '\n' + str(e)
    return result
