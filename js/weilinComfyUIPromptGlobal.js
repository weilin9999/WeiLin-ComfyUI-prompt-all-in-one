import { app } from '../../scripts/app.js'

// 全局注册

let onlyOne = false
let global_randomID = (Math.random() + new Date().getTime()).toString(32).slice(0,8); // 随机种子ID
localStorage.setItem("weilin_prompt_ui_onfirst", 0);

app.registerExtension({
  name: "weilin.prompt_global",
  
  async init() {

    let getSettingChangUI = localStorage.getItem("weilin_prompt_ui_change_close")
    let getIsWindowMode = localStorage.getItem("weilin_prompt_ui_is_window")
    if(getSettingChangUI == null || getSettingChangUI.length <= 0){
        localStorage.setItem("weilin_prompt_ui_change_close",false)
        getSettingChangUI = false
    }
    if(getIsWindowMode == null || getIsWindowMode.length <= 0){
        localStorage.setItem("weilin_prompt_ui_is_window", 'no')
        getIsWindowMode = 'no'
    }
    // 加载设置
    app.ui.settings.addSetting({
        id: "weilin.prompt_global.changeClose",
        name: "WeiLin PromptUI -- 调整PromptUI的关闭按钮在右边 Change PromptUI close button is on the right",
        type: "boolean",
		defaultValue: getSettingChangUI,
		onChange: function(value) {
            localStorage.setItem("weilin_prompt_ui_change_close",value)
            getSettingChangUI = value
            for (let index = 0; index < window.length; index++) {
                window[index].postMessage({handel: 'changeSettingWeilinPromptUIChangeClose',value:value }, "*");
            }
        }
    });


    // 全局唯一
    const style = document.createElement("style");
    style.innerText = `
        .weilin_draggable_window{
            position: fixed;
            min-width: 40%;
            min-height: 50%;
            width: 80%;
            height: 80%;
            z-index: calc(100 * 100 * 100 * 90);
            display: flex;
            flex-direction: column;
        }
        .weilin_bg_box{
            display: flex;
            justify-content: center;
            align-items: center;
            position: fixed;
            width: 100%;
            height: 100%;
            left: 0;
            top: 0;
            z-index: calc(100 * 100 * 100 * 90);
            background-color: rgba(0, 0, 0, 0.55);
        }
        .weilin_iframe_box{
            border-radius: 10px;
            background-color: #ffffff;
            transition: all 0.4s;
        }
        .weilin_global_floating_window {
            position: absolute;
            bottom: 100px;
            left: 20px;
            width: 45px;
            height: 45px;
            background: #22c1c3;  /* fallback for old browsers */
            background: -webkit-linear-gradient(to bottom, #fdbb2d, #22c1c3);  /* Chrome 10-25, Safari 5.1-6 */
            background: linear-gradient(to bottom, #fdbb2d, #22c1c3); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
            z-index: calc(100 * 100 * 100 * 10);
            border-radius: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
        .weilin-prompt-dragg-resize-handle{
            position: absolute;
            bottom: 0;
            right: 0;
            width: 15px;
            height: 15px;
            background-color: #aaa;
            cursor: se-resize;
            z-index: 100;
            border-bottom-right-radius: 10px;
            border-top-left-radius: 100%;
            user-select: none;
            display: none;
        }
        .weilin-prompt-dragg-bar{
            min-width: 100%;
            min-height: 20px;
            background-color: #f1f1f1;
            cursor: move;
            user-select: none;
            transition: all 0.4s;
            display: none;
            align-items: center;
            justify-content: center;
        }

        .weilin-prompt-dragging-inner-box{
            position: relative;
            min-width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 1;
            flex-direction: column;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        }
        .weilin-prompt-dragging-inner-shan-box{
            position: absolute;
            top: 0;
            left: 0;
            background-color: #02b7fd;
            animation-name: weilin-prompt-dragging-breath;
            animation-duration: 3s;
            animation-timing-function: ease-in-out;
            animation-iteration-count: infinite;
            width: 100%;
            height: 100%;
            z-index: 99;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
            display:none;
        }
        @keyframes weilin-prompt-dragging-breath {
            from {
                opacity: 0.3;
            }
            50% {
                opacity: 0.8;
            }
            to {
                opacity: 0.3;
            }
        }
        
        .weilin_prompt_ui_three_lines {
            width: 100px;
            height: 5px;
            background-color: #9f9f9f;
            border-radius: 20px;
        }

        .weilin-floating-button {
            position: absolute;
            display: none;
            top: 41px;
            left: 315px;
            flex-direction: column;
            align-items: center;
            background-color: rgba(0, 0, 0, 0.6);
            border-radius: 6px;
            padding: 5px;
            z-index: 1000;
        }

        .weilin-option-buttons {
            display: flex;
            gap: 10px;
        }

        .weilin-option-btn{
            background: #91919187;
            padding: 5px;
            font-size: 12px;
            border-radius: 5px;
            color: #fff;
            cursor: pointer;
        }
    `;
    document.head.appendChild(style)

    // 小浮窗
    const floatingWindowBox = document.createElement('div')
    floatingWindowBox.innerHTML = `
    <div style="font-size: small;color: #ffffff;user-select: none;">WeiLin</div>
    <textarea id="weilin_global_great_prompt_input" style="display:none;" ></textarea>
    <textarea id="weilin_global_neg_prompt_input" style="display:none;" ></textarea>
    `
    floatingWindowBox.className = "weilin_global_floating_window"
    floatingWindowBox.id = "weilin_global_floating_window"
    document.body.appendChild(floatingWindowBox);

    // 小浮窗JavaScript
    const script = document.createElement("script");
    script.type = "text/javascript";
    // 直接搬现成的代码 省事
    script.text = `
        const weilin_box = document.getElementById('weilin_global_floating_window')
        weilin_dragElement(weilin_box);
        function weilin_dragElement(elmnt) {
            var weilin_pos1 = 0, weilin_pos2 = 0, weilin_pos3 = 0, weilin_pos4 = 0;

            elmnt.onmousedown = weilin_dragMouseDown;
            elmnt.onmouseup = weilin_dragMouseUp;

            let weilin_isMove = 1

            function weilin_dragMouseUp(e){
                //console.log(weilin_isMove)
                if(weilin_isMove == 0 || weilin_isMove == 1 ){
                    const evt = new CustomEvent("openWeilinGlobalPromptBox", {"detail":{"open":true}});
                    document.dispatchEvent(evt);
                }
            }

            function weilin_dragMouseDown(e) {
                weilin_isMove = 1;
                e = e || window.event;
                e.preventDefault();
                // 在启动时获取鼠标光标位置:
                weilin_pos3 = e.clientX;
                weilin_pos4 = e.clientY;
                document.onmouseup = weilin_closeDragElement;
                // 每当光标移动时调用一个函数:
                document.onmousemove = weilin_elementDrag;
            }

            function weilin_elementDrag(e) {
                weilin_isMove = weilin_isMove - 1;
                weilin_box.style.cursor = "move"
                e = e || window.event;
                e.preventDefault();
                // 计算新的光标位置:
                weilin_pos1 = weilin_pos3 - e.clientX;
                weilin_pos2 = weilin_pos4 - e.clientY;
                weilin_pos3 = e.clientX;
                weilin_pos4 = e.clientY;
                // 设置元素的新位置:
                elmnt.style.top = (elmnt.offsetTop - weilin_pos2) + "px";
                elmnt.style.left = (elmnt.offsetLeft - weilin_pos1) + "px";
            }

            function weilin_closeDragElement() {
                weilin_box.style.cursor = "pointer"
                // 释放鼠标按钮时停止移动:
                document.onmouseup = null;
                document.onmousemove = null;
            }
        }
    `
    document.body.appendChild(script);

    // 全局粘贴浮窗
    const globalPastWindowBox = document.createElement('div')
    globalPastWindowBox.innerHTML = `
        <div style="font-size: 13px;color: #fff;padding-bottom: 5px;">WeiLin全局提示词</div>
        <div class="weilin-option-buttons">
            <div class="weilin-option-btn" id="weilin_positiveButton">替换为正向提示词</div>
            <div class="weilin-option-btn" id="weilin_negativeButton">替换为反向提示词</div>
        </div>
    `
    globalPastWindowBox.className = "weilin-floating-button"
    globalPastWindowBox.id = "weilinFloatingButton"
    document.body.appendChild(globalPastWindowBox);

    // 对应的JavaScript
    const globalPastScript = document.createElement("script");
    globalPastScript.type = "text/javascript";
    globalPastScript.text = `
        const floatingButton = document.getElementById('weilinFloatingButton');
        let activeTextarea = null;
        let isFloatingButtonVisible = false;

        function findTextarea(event) {
            return document.elementFromPoint(event.clientX, event.clientY).closest('textarea');
        }

        function showFloatingButton(event) {
            if (!isFloatingButtonVisible) {
                activeTextarea = findTextarea(event);
                if (activeTextarea) {
                    floatingButton.style.display = 'flex';
                    floatingButton.style.top = event.clientY + 'px';
                    floatingButton.style.left = (event.clientX + 10) + 'px';
                    isFloatingButtonVisible = true;

                    const positiveButton = document.getElementById('weilin_positiveButton');
                    const negativeButton = document.getElementById('weilin_negativeButton');
                    positiveButton.style.display="block"
                    negativeButton.style.display="block"

                    let thisInputGreatElement = document.getElementById("weilin_global_great_prompt_input")
                    let thisInputNegElement = document.getElementById("weilin_global_neg_prompt_input")
                    if(thisInputGreatElement.value.length <= 0){
                        positiveButton.style.display="none"
                    }
                    if(thisInputNegElement.value.length <= 0){
                        negativeButton.style.display="none"
                    }

                    positiveButton.addEventListener('click', function () {
                        let thisInputGreatElement = document.getElementById("weilin_global_great_prompt_input")
                        activeTextarea.value = thisInputGreatElement.value
                    });

                    negativeButton.addEventListener('click', function () {
                        let thisInputNegElement = document.getElementById("weilin_global_neg_prompt_input")
                        activeTextarea.value = thisInputNegElement.value
                    });
                }
            } else {
                // If the user clicks on a different textarea, hide the current floating button and show it for the new textarea.
                if (activeTextarea !== findTextarea(event)) {
                    hideFloatingButton();
                    showFloatingButton(event);
                }
            }
        }

        function hideFloatingButton() {
            floatingButton.style.display = 'none';
            isFloatingButtonVisible = false;
        }

        document.addEventListener('mousedown', function (event) {
            let thisInputGreatElement = document.getElementById("weilin_global_great_prompt_input")
            let thisInputNegElement = document.getElementById("weilin_global_neg_prompt_input")
            if(thisInputGreatElement.value.length > 0 || thisInputNegElement.value.length > 0){
                const getConfig = localStorage.getItem("weilin_prompt_global_past_setting")
                if(getConfig == 1){
                    if (event.target.tagName.toLowerCase() === 'textarea') {
                        showFloatingButton(event);
                    }
                }
            }
        });

        window.addEventListener('click', function (event) {
            let thisInputGreatElement = document.getElementById("weilin_global_great_prompt_input")
            let thisInputNegElement = document.getElementById("weilin_global_neg_prompt_input")
            if(thisInputGreatElement.value.length > 0 || thisInputNegElement.value.length > 0){
                const getConfig = localStorage.getItem("weilin_prompt_global_past_setting")
                if(getConfig == 1){
                    if (!floatingButton.contains(event.target) && !activeTextarea.contains(event.target)) {
                        hideFloatingButton();
                    }
                }
            }
        });
    `
    document.body.appendChild(globalPastScript);


    // 主框架

    const hasIframeBox = document.getElementById('weilin_bg_box_global')
    if(hasIframeBox == null){
        localStorage.setItem("weilin_prompt_global_refid",global_randomID)
        const getBoxStatus = localStorage.getItem("weilin_prompt_box_status");
        let minHeight = '100%';
        let minWidth = '100%';
        if(getIsWindowMode == 'no'){
            if(getBoxStatus == "full"){
                minHeight="100%"
                minWidth="100%"
            }else{
                minHeight="80%"
                minWidth="80%"
            }
        }
        
        // 全局创建一个即可
        const iftramBox = document.createElement("div");
        iftramBox.innerHTML = `
            <div class="weilin-prompt-dragg-bar"  id="weilin_prompr_dragg_bar">
                <div class="weilin_prompt_ui_three_lines"></div>
            </div>
            <div class="weilin-prompt-dragging-inner-box">
                <div class="weilin-prompt-dragging-inner-shan-box" id="weilin_prompt_dragging_inner_shan_box"></div>
                <iframe
                    style="min-width: ${minWidth};min-height: ${minHeight};"
                    class="weilin_iframe_box"
                    id='weilin_prompt_global_box'
                    name='weilin_prompt_global_box'
                    src=''
                    frameborder='0'
                    scrolling='on'
                >
                </iframe>
            </div>
            <div class="weilin-prompt-dragg-resize-handle" id="weilin_prompt_ddragg_resize_handle"></div>
        `;
        iftramBox.id = "weilin_bg_box_global"
        iftramBox.className = "weilin_bg_box" // weilin_bg_box weilin_draggable_window
        iftramBox.style.display = "none"
        document.body.appendChild(iftramBox);


        const draggScript = document.createElement("script");
        script.type = "text/javascript";
        // 拖动事件注册
        draggScript.text = `
            const draggableWindow = document.getElementById('weilin_bg_box_global');
            const titleBar = draggableWindow.querySelector('#weilin_prompr_dragg_bar');
            const resizeHandle = draggableWindow.querySelector('#weilin_prompt_ddragg_resize_handle');
            const iframe = document.getElementById('weilin_prompt_global_box');
            const innerBox = document.getElementById('weilin_prompt_dragging_inner_shan_box');

            let isDragging = false;
            let isResizing = false;
            let offsetX = 0;
            let offsetY = 0;
            let originalWidth = 0;
            let originalHeight = 0;
            let mouseStartX = 0;
            let mouseStartY = 0;

            titleBar.addEventListener('mousedown', function(e) {
                isDragging = true;
                offsetX = e.clientX - draggableWindow.offsetLeft;
                offsetY = e.clientY - draggableWindow.offsetTop;
                iframe.style.display="none";
                innerBox.style.display="block";
            });

            resizeHandle.addEventListener('mousedown', function(e) {
                isResizing = true;
                originalWidth = draggableWindow.offsetWidth;
                originalHeight = draggableWindow.offsetHeight;
                mouseStartX = e.clientX;
                mouseStartY = e.clientY;
                iframe.style.display="none";
                innerBox.style.display="block";
            });

            document.addEventListener('mousemove', function(e) {
                if (isDragging) {
                    draggableWindow.style.left = (e.clientX - offsetX)+'px';
                    draggableWindow.style.top = (e.clientY - offsetY)+'px';
                } else if (isResizing) {
                    const newWidth = Math.max(originalWidth + e.clientX - mouseStartX, 100);
                    const newHeight = Math.max(originalHeight + e.clientY - mouseStartY, 100);
                    draggableWindow.style.width = newWidth+'px';
                    draggableWindow.style.height = newHeight+'px';
                }
            });

            document.addEventListener('mouseup', function() {
                isDragging = false;
                isResizing = false;
                innerBox.style.display="none";
                iframe.style.display="flex";
            });
        `
        document.body.appendChild(draggScript);
    }

  },
  async setup(app) {

  },


  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if(!onlyOne){
        onlyOne = true
        // console.log('onlyOne load',ifreamBox)

        let thisInputGreatElement = document.getElementById("weilin_global_great_prompt_input")
        let thisInputNegElement = document.getElementById("weilin_global_neg_prompt_input")
        let randomID = ''

        document.addEventListener("openWeilinGlobalPromptBox", function (event) {
            randomID = (Math.random() + new Date().getTime()).toString(32).slice(0,8); // 随机种子ID
            localStorage.setItem("weilin_prompt_randomid",randomID);

            for (let index = 0; index < window.length; index++) {
                window[index].postMessage({handel: 'openWeiLinPrompt',
                    g_value: thisInputGreatElement.value,n_value: thisInputNegElement.value,randomid: randomID,type: 'global'}, "*");
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
            if(isFirstOpen == 0){
                localStorage.setItem("weilin_prompt_ui_onfirst",1);
                iframeEle.src = `./weilin/web_ui/index.html?type=prompt&refid=${global_randomID}&__theme=${ui_theme}`
            }

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


        }, false)


        window.addEventListener('message', e => {
            // console.log(e)
            if(e.data.handel == 'changeWeiLinPrompt' && e.data.randomid == randomID){
                thisInputGreatElement.value = e.data.g_value
                thisInputNegElement.value = e.data.n_value
            }else if(e.data.handel  == 'closeWeilinPromptBox' && e.data.randomid == randomID){
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
                    window[index].postMessage({handel: 'responeseWeiLinPrompt',
                        g_value: thisInputGreatElement.value,n_value: thisInputNegElement.value,randomid: randomID,type: 'global'}, "*");
                }
            }else if(e.data.handel == 'refreshWeilinPromptBox'){
                global_randomID = (Math.random() + new Date().getTime()).toString(32).slice(0,8); // 随机种子ID
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
                
                const iframeEle = document.getElementById('weilin_prompt_global_box')
                iframeEle.src = `./weilin/web_ui/index.html?type=prompt&refid=${global_randomID}&__theme=${ui_theme}`
            }else if(e.data.handel == 'fullBoxWeilinPromptBox'){
                localStorage.setItem("weilin_prompt_box_status","full");
                const iframeEle = document.getElementById('weilin_prompt_global_box')
                iframeEle.style.minHeight="100%"
                iframeEle.style.minWidth="100%"
                for (let index = 0; index < window.length; index++) {
                    window[index].postMessage({handel: 'fullBoxWeilinPromptBoxResponse',randomid: randomID,type: 'global'}, "*");
                }
            }else if(e.data.handel == 'nomBoxWeilinPromptBox'){
                localStorage.setItem("weilin_prompt_box_status","nom");
                const iframeEle = document.getElementById('weilin_prompt_global_box')
                iframeEle.style.minHeight="80%"
                iframeEle.style.minWidth="80%"
                for (let index = 0; index < window.length; index++) {
                    window[index].postMessage({handel: 'nomBoxWeilinPromptBoxResponse',randomid: randomID,type: 'global'}, "*");
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
        

    }
  },
});