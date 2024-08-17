import { app } from '../../scripts/app.js'

// 提示词 Node

let global_randomID = (Math.random() + new Date().getTime()).toString(32).slice(0,8); // 随机种子ID

app.registerExtension({
  name: "weilin.prompt_node_to_string",
  
  async init() {},
  async setup() {},


  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    // console.log(app)
    if (
      nodeData.name === "WeiLinPromptToString" || nodeData.name === "WeiLinComfyUIPromptToLoras"
      || nodeData.name === "WeiLinComfyUIPromptToLorasOnly" || nodeData.name === "WeiLinComfyUIPromptAllInOneGreat"
      || nodeData.name === "WeiLinComfyUIPromptAllInOneNeg"
    ) {
      // console.log(nodeData)
      // Create node
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = async function () {
        const r = onNodeCreated ? onNodeCreated.apply(this, arguments): undefined;

        const thisNodeName = nodeData.name // 存储当前的节点名称

        for (let index = 0; index < this.widgets.length; index++) {
          const element = this.widgets[index];
          let thisInputElement = element.element
          if(element.type == "customtext"){
            if(thisInputElement.placeholder == "输入正向提示词"){
              thisInputElement.style.backgroundColor="#335533"
            }else if(thisInputElement.placeholder == "输入反向提示词"){
              thisInputElement.style.backgroundColor="#553332"
            }
          } 
        }

        let thisInputElements = {g:null,n:null}
        let randomID = ''

        this.addWidget("button", "打开可视化PromptUI", '', ($e) => {
          randomID = (Math.random() + new Date().getTime()).toString(32).slice(0,8); // 随机种子ID
          localStorage.setItem("weilin_prompt_randomid",randomID);

          for (let index = 0; index < this.widgets.length; index++) {
            const element = this.widgets[index];
            if(element.type == "customtext"){
              // console.log(element,randomID)
              let thisInputElement = element.element
              thisInputElement.readOnly = true
              if(thisInputElement.placeholder == "输入正向提示词"){
                thisInputElements.g = thisInputElement
              }else if(thisInputElement.placeholder == "输入反向提示词"){
                thisInputElements.n = thisInputElement
              }
            } 
          }

          // element.element.value
          for (let index = 0; index < window.length; index++) {
            const gValue = thisInputElements.g == null ? "":thisInputElements.g.value;
            const nValue = thisInputElements.n == null ? "":thisInputElements.n.value;
            window[index].postMessage({handel: 'openWeiLinPrompt',
              g_value: gValue,n_value: nValue,randomid: randomID,type: 'prompt',nodeName: thisNodeName}, "*");
          }

          const ui_theme = localStorage.getItem("weilin_prompt_theme");
          const iframeEle = document.getElementById('weilin_prompt_global_box')

          const params = new URL(iframeEle.src)
          const searchParams = params.searchParams
          const theme_type =  searchParams.get("__theme")
          // console.log(ui_theme.toString() , theme_type.toString() )
          if(String(ui_theme)  != String(theme_type) ){
            iframeEle.src = `./weilin/web_ui/index.html?type=prompt&refid=${global_randomID}&__theme=${ui_theme}`
          }

          const isFirstOpen = localStorage.getItem("weilin_prompt_ui_onfirst");

          if(!isFirstOpen){
            localStorage.setItem("weilin_prompt_ui_onfirst",1);
            iframeEle.src = `./weilin/web_ui/index.html?type=prompt&refid=${global_randomID}&__theme=${ui_theme}`
          }

          localStorage.setItem("weilin_prompt_open_mode",thisNodeName);

          let getIsWindowMode = localStorage.getItem("weilin_prompt_ui_is_window")
          const getBoxStatus = localStorage.getItem("weilin_prompt_box_status");
          const ifreamBox = document.getElementById('weilin_bg_box_global')
          const titleBar = ifreamBox.querySelector('#weilin_prompr_dragg_bar');
          const resizeHandle = ifreamBox.querySelector('#weilin_prompt_ddragg_resize_handle');
          const innerBox = document.getElementById('weilin_prompt_dragging_inner_shan_box');

          if(getIsWindowMode == 'no'){
              if(getIsWindowMode == 'no'){
                  if(getBoxStatus == "full"){
                      iframeEle.style.minHeight="100%"
                      iframeEle.style.minWidth="100%"
                  }else{
                      iframeEle.style.minHeight="80%"
                      iframeEle.style.minWidth="80%"
                  }
              }
              // 取消dragg模式
              ifreamBox.className = "weilin_bg_box";
              titleBar.style.display = "none";
              resizeHandle.style.display = "none";
              innerBox.style.display = "none";
              iframeEle.style.flex = "0"
              iframeEle.style.borderTopRightRadius = "10px"
              iframeEle.style.borderTopLeftRadius = "10px"
              ifreamBox.style.left = 0;
              ifreamBox.style.top = 0;
              ifreamBox.style.width = "100%";
              ifreamBox.style.height = "100%";
              ifreamBox.style.display = "flex"
          }else{
              // 启用dragg模式
              if(ui_theme == 'dark'){
                titleBar.style.backgroundColor = "#5d5d5d";
                innerBox.style.backgroundColor = "#082d4d";
              }else{
                titleBar.style.backgroundColor = "#f1f1f1";
                innerBox.style.backgroundColor = "#02b7fd";
              }
              ifreamBox.className = "weilin_draggable_window";
              iframeEle.style.minHeight = "100%"
              iframeEle.style.minWidth = "100%"
              iframeEle.style.flex = "1"
              iframeEle.style.borderTopRightRadius = "0px"
              iframeEle.style.borderTopLeftRadius = "0px"
              titleBar.style.display = "flex";
              resizeHandle.style.display = "block";
              ifreamBox.style.width = "80%";
              ifreamBox.style.height = "80%";
              ifreamBox.style.display = "flex"
              var divWidth = ifreamBox.offsetWidth;
              var divHeight = ifreamBox.offsetHeight;
              // 重新计算div的left和top值
              ifreamBox.style.left = (window.innerWidth - divWidth) / 2 + 'px';
              ifreamBox.style.top = (window.innerHeight - divHeight) / 2 + 'px';
          }
        });


        window.addEventListener('message', e => {
          // console.log(e.data,randomID)
          if(e.data.handel == 'changeWeiLinPrompt' && e.data.randomid == randomID)
          {
            if(thisInputElements.g != null){
              thisInputElements.g.value = e.data.g_value
            }
            if(thisInputElements.n != null){
              thisInputElements.n.value = e.data.n_value
            }
          }else if(e.data.handel  == 'closeWeilinPromptBox' && e.data.randomid == randomID){
            if(thisInputElements.g != null){
              thisInputElements.g.readOnly = false
            }
            if(thisInputElements.n != null){
              thisInputElements.n.readOnly = false
            }
            const ifreamBox = document.getElementById('weilin_bg_box_global')
            ifreamBox.style.display = "none"
          }else if(e.data.handel == 'getWeilinPromptBox' && e.data.randomid == randomID){
            const ui_theme = localStorage.getItem("weilin_prompt_theme");
            const ifreamBox = document.getElementById('weilin_bg_box_global')
            const titleBar = ifreamBox.querySelector('#weilin_prompr_dragg_bar');
            if(ui_theme == 'dark'){
                titleBar.style.backgroundColor = "#5d5d5d";
                innerBox.style.backgroundColor = "#082d4d";
            }else{
                titleBar.style.backgroundColor = "#f1f1f1";
                innerBox.style.backgroundColor = "#02b7fd";
            }
            for (let index = 0; index < window.length; index++) {
              const gValue = thisInputElements.g == null ? "":thisInputElements.g.value;
              const nValue = thisInputElements.n == null ? "":thisInputElements.n.value;
              window[index].postMessage({handel: 'responeseWeiLinPrompt',
                g_value: gValue,n_value: nValue,randomid: randomID,type: 'prompt',nodeName: thisNodeName}, "*");
            }
          }else if(e.data.handel == 'refreshWeilinPromptBox'){
            const ui_theme = localStorage.getItem("weilin_prompt_theme");
            const ifreamBox = document.getElementById('weilin_bg_box_global')
            const titleBar = ifreamBox.querySelector('#weilin_prompr_dragg_bar');
            if(ui_theme == 'dark'){
                titleBar.style.backgroundColor = "#5d5d5d";
                innerBox.style.backgroundColor = "#082d4d";
            }else{
                titleBar.style.backgroundColor = "#f1f1f1";
                innerBox.style.backgroundColor = "#02b7fd";
            }

            global_randomID = (Math.random() + new Date().getTime()).toString(32).slice(0,8); // 随机种子ID
            const iframeEle = document.getElementById('weilin_prompt_global_box')
            iframeEle.src = `./weilin/web_ui/index.html?type=prompt&refid=${global_randomID}&__theme=${ui_theme}`
          }else if(e.data.handel == 'fullBoxWeilinPromptBox'){
            localStorage.setItem("weilin_prompt_box_status","full");
            const iframeEle = document.getElementById('weilin_prompt_global_box')
            iframeEle.style.minHeight="100%"
            iframeEle.style.minWidth="100%"
            for (let index = 0; index < window.length; index++) {
              window[index].postMessage({handel: 'fullBoxWeilinPromptBoxResponse',randomid: randomID,nodeName: thisNodeName}, "*");
            }
          }else if(e.data.handel == 'nomBoxWeilinPromptBox'){
            localStorage.setItem("weilin_prompt_box_status","nom");
            const iframeEle = document.getElementById('weilin_prompt_global_box')
            iframeEle.style.minHeight="80%"
            iframeEle.style.minWidth="80%"
            for (let index = 0; index < window.length; index++) {
              window[index].postMessage({handel: 'nomBoxWeilinPromptBoxResponse',randomid: randomID,nodeName: thisNodeName}, "*");
            }
          }else if(e.data.handel == 'changeWeilinPromptWindowMode'){
            const iframeEle = document.getElementById('weilin_prompt_global_box')
            const getIsWindowMode = localStorage.getItem("weilin_prompt_ui_is_window")
            const getBoxStatus = localStorage.getItem("weilin_prompt_box_status");
            const ifreamBox = document.getElementById('weilin_bg_box_global')
            const titleBar = ifreamBox.querySelector('#weilin_prompr_dragg_bar');
            const resizeHandle = ifreamBox.querySelector('#weilin_prompt_ddragg_resize_handle');
            const innerBox = document.getElementById('weilin_prompt_dragging_inner_shan_box');
            
            if(getIsWindowMode == 'no'){
                if(getIsWindowMode == 'no'){
                    if(getBoxStatus == "full"){
                        iframeEle.style.minHeight="100%"
                        iframeEle.style.minWidth="100%"
                    }else{
                        iframeEle.style.minHeight="80%"
                        iframeEle.style.minWidth="80%"
                    }
                }
                // 取消dragg模式
                ifreamBox.className = "weilin_bg_box";
                titleBar.style.display = "none";
                resizeHandle.style.display = "none";
                innerBox.style.display = "none";
                iframeEle.style.flex = "0"
                iframeEle.style.borderTopRightRadius = "10px"
                iframeEle.style.borderTopLeftRadius = "10px"
                ifreamBox.style.left = 0;
                ifreamBox.style.top = 0;
                ifreamBox.style.width = "100%";
                ifreamBox.style.height = "100%";
                ifreamBox.style.display = "flex"
            }else{
                // 启用dragg模式
                const ui_theme = localStorage.getItem("weilin_prompt_theme");
                if(ui_theme == 'dark'){
                  titleBar.style.backgroundColor = "#5d5d5d";
                  innerBox.style.backgroundColor = "#082d4d";
                }else{
                  titleBar.style.backgroundColor = "#f1f1f1";
                  innerBox.style.backgroundColor = "#02b7fd";
                }
                ifreamBox.className = "weilin_draggable_window";
                iframeEle.style.minHeight = "100%"
                iframeEle.style.minWidth = "100%"
                iframeEle.style.flex = "1"
                iframeEle.style.borderTopRightRadius = "0px"
                iframeEle.style.borderTopLeftRadius = "0px"
                titleBar.style.display = "flex";
                resizeHandle.style.display = "block";
                ifreamBox.style.width = "80%";
                ifreamBox.style.height = "80%";
                ifreamBox.style.display = "flex"
                var divWidth = ifreamBox.offsetWidth;
                var divHeight = ifreamBox.offsetHeight;
                // 重新计算div的left和top值
                ifreamBox.style.left = (window.innerWidth - divWidth) / 2 + 'px';
                ifreamBox.style.top = (window.innerHeight - divHeight) / 2 + 'px';
            }
          }
        }, false);

        return r;
      };
    }
  },
});