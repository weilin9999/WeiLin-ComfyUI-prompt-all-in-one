<div align="center">
  
### [🇨🇳 简体中文](README.md) | [🇺🇸 English](README_EN.md)

</div>


# Please note that this node no longer accepts any feedback or updates!
### This node is no longer updated and will be replaced by a new node. New node: [WeiLin-Comfyui-Tools](https://github.com/weilin9999/WeiLin-Comfyui-Tools) The new node will continue to update and the installation method of the new node is more convenient and better than that of the old node. The new node is not compatible with the old node, but the Tag data of the old node can be migrated to the new node. Please refer to the new node for more information!

# Author Statement

Due to limited personal time, the frequency of updating plug-ins will not be very high, occasionally free may update once, each update as far as possible to meet the proposed needs, generally no big BUG basically update frequency is not high, 2~5 a month, thank you for your use and support of this plug-in. You can submit an Issue or you can submit your Request to help update this plugin.

# Version update introduction

> Last updated: 2024-11-26

> 3.6.9.1 Version Introduction (Due to my work, I have time to update the plug-in, forgive me! Thank you very much for your support of this plugin!)
>
> 1. Fixed an issue in the merge code: [#15](https://github.com/weilin9999/WeiLin-ComfyUI-prompt-all-in-one/pull/15) to the modified Lora loading apis in a timeout situation in (thanks for the code contributor provides the help, Thanks to contributors for supporting this plugin, thanks to everyone who uses this plugin)
> 2. Added a new function to load all Lora covers at the bottom of the input box, and the background can view the loading progress. This code is provided by [#15](https://github.com/weilin9999/WeiLin-ComfyUI-prompt-all-in-one/pull/15) contributor

<details>

<summary>
Click here for more updates from the past
</summary>

> 3.6.9 Version Introduction
>
> 1. Fixed known BUG: Offline translation model translation problem in API Settings, fixed

> 3.6.8 Version Introduction
>
> 1. New - Global shortcut key (Set the default to CTRL+ALT+W in ComfyUI Settings to call the global editor)
> 2. New - Floating ball hiding Settings
> 3. Modification - Settings interface optimization ADAPTS to the new UI of the new version of ComfyUI

> 3.6.5 Version Introduction
>
> 1. Fixed Issue: lora's message note is too long, the ui will be stretched and cannot see the content on the right √
> 2. Fixed Issue: tagcomplete in translation Settings could not be used, red letter popped up in the upper right corner, csv file is fine, √ can be used in webui
> 3. Fixed Issue: AttributeError: module 'ctypes' has no attribute 'windll' (Linux language judgment) √
> 4. Fixed the feature: Update will no longer overwrite added Tag information √
> 5. Added the function of shortcut calling the global window
> 6. Added function: Global Paste board preview

> 3.6.1 Version Introduction
>
> 1. Fixed known bugs
> 2. New - In Global Mode, you can enable the Paste board mode. In this mode, you can click any input box in the node to pop up the paste board in global mode
> 3. Fix the -String return string issue

> Version 3.5.0 Introduction
>
> 0. Because the warehouse uploaded some very large files before, 2024-8-16 warehouse was emptied, so the previous version of the warehouse was deleted in order to reduce the size of the warehouse
> 1. Fixed known bugs
> 2. Modified - Restores the functions of the previous version and supports more node collocation
> 3. New - Added the use of local LLM model to help you continue writing prompts

> Version 3.0.0 Introduction
>
> 1. Fixed known bugs
> 2. New -Tag Add, delete, and modify functions
> 3. New - Open the window mode. You can drag the right corner of the window at will to adjust the window size for use in ComfyUI
> 4. Add -Lora viewer. There is a prompt button in the upper right corner of the Lora card to view Lora information and synchronize C station and set the functions of Lora cover
> 5. The new -Lora prompt words are specially adapted to ComfyUI model strength and CLIP strength regulator

> 2.4.0 Version</br>1. Fixed the BUG of prompt word completion </br>2. The NSFW prompt glossary is added only in Chinese </br>3. Added automatic loading of Lora prompt words. You only need to add Lora in PromptUI, which is the same as that in WebUI </br>4. In the setting of ComfyUI, you can change the "Off" button of PromptUI to the right

> 2.3.0 Version</br>1. Added prompt word completion

> 2.2.0 Version </br>1. Fixed known bug</br>2. Updated with new features: Global Prompt UI, Enlarge Window function

</details>

# Lora tips Word writing tips

<lora:xxxx:0.3:0.4> This formulation explains that 0.3 is the model strength and 0.4 is the CLIP strength
If you are <lora:xxxx:0.4> then this interpretation of the model strength and CLIP strength are both 0.4

# Summary

This project allows you to write Prompt words in ComfyUI like WebUI, modified from the prompt-all-in-one project, but has made most of the changes to adapt to ComfyUI, adding many different functions, as well as the plugin for prompt word completion. The prompt word completion plugin is modified from the ComfyUI-Custom-Scripts project. Thank you for your support of this plugin.

If you are interested in this project, please award a Star!

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

# Plugin Settings preview

![](https://github.com/weilin9999/WeiLin-ComfyUI-prompt-all-in-one/blob/master/step/5.png)

# WeiLin-ComfyUI-Prompt-all-in-one Reference project

WeiLin-ComfyUI-Prompt-all-in-one The ComfyUI version of prompt-all-in-one, a ComfyUI version modified based on the SD-wewe-prompt-all-in-one-app https://github.com/Physton/sd-webui-prompt-all-in-one-app project, Just add the ComfyUI node of the project to ComfyUI to use the visual tag editor. Cue word completion using the https://github.com/pythongosssss/ComfyUI-Custom-Scripts project changes only the function of the completion and make the changes, Projects using local LLM big model borrowed from https://github.com/thisjam/comfyui-sixgod_prompt warehouse code

# A brief description of this item

At the beginning, the project was just convenient for editing the tag, so I wrote my own plugin, and if you have any questions, you can submit an issue, which may not necessarily be dealt with.
