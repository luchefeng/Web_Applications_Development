// ==UserScript==
// @name         Video Loop Script
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Make videos on web pages loop continuously.
// @author       Your Name
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    // 当页面加载完成后执行以下代码
    window.addEventListener('load', function() {
        // 获取页面上所有的video和audio元素
        const mediaElements = document.querySelectorAll('video, audio');
        mediaElements.forEach((media) => {
            // 为每个媒体元素添加ended事件监听器
            media.addEventListener('ended', function() {
                // 当媒体播放结束时，将当前播放时间设置回0（回到开头）
                this.currentTime = 0;
                // 再次播放媒体，实现循环播放
                this.play();
            });
        });
    });
})();