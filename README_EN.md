<div align="center">
  
### [🇨🇳 简体中文](README.md) | [🇺🇸 English](README_EN.md)

</div>

# Version update introduction

> 2.4.0 Version</br>1. Fixed the BUG of prompt word completion </br>2. The NSFW prompt glossary is added only in Chinese </br>3. Added automatic loading of Lora prompt words. You only need to add Lora in PromptUI, which is the same as that in WebUI </br>4. In the setting of ComfyUI, you can change the "Off" button of PromptUI to the right

> 2.3.0 Version</br>1. Added prompt word completion

> 2.2.0 Version </br>1. Fixed known bug</br>2. Updated with new features: Global Prompt UI, Enlarge Window function

# Lora tips Word writing tips
<lora:xxxx:0.3:0.4> This formulation explains that 0.3 is the model strength and 0.4 is the CLIP strength
If you are <lora:xxxx:0.4> then this interpretation of the model strength and CLIP strength are both 0.4

# Summary

This project is from sd-webui-prompt-all-in-one-app: https://github.com/Physton/sd-webui-prompt-all-in-one-app The project was modified ComfyUI version，However, there are modifications to the original author's project，Please go to the release of this project to download！！！

This project has rewritten the original author's code into the version of ComfyUI, no need to start other scripts, just run ComfyUI to automatically install dependency packages.

# The installation tutorial can be done directly from git this project

> https://github.com/weilin9999/WeiLin-ComfyUI-prompt-all-in-one.git

# Install the plugin in detail, install the version manually

Download the latest release of this project directly, then unzip it, put it in ComfyUI and start ComfyUI directly to use this plugin.
![](https://github.com/weilin9999/WeiLin-ComfyUI-prompt-all-in-one/blob/master/step/1.png)

# How to use the node

Use it as follows
![](https://github.com/weilin9999/WeiLin-ComfyUI-prompt-all-in-one/blob/master/step/2.png)
![](https://github.com/weilin9999/WeiLin-ComfyUI-prompt-all-in-one/blob/master/step/3.png)
![](https://github.com/weilin9999/WeiLin-ComfyUI-prompt-all-in-one/blob/master/step/4.png)

# WeiLin-ComfyUI-Prompt-all-in-one Reference project

WeiLin-ComfyUI-Prompt-all-in-one The ComfyUI version of prompt-all-in-one, a ComfyUI version modified based on the SD-wewe-prompt-all-in-one-app project, Just add the ComfyUI node of the project to ComfyUI to use the visual tag editor. Cue word completion using the https://github.com/pythongosssss/ComfyUI-Custom-Scripts project changes only the function of the completion and make the changes

# A brief description of this item

At the beginning, the project was just convenient for editing the tag, so I wrote my own plugin, and if you have any questions, you can submit an issue, which may not necessarily be dealt with.
