document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.getElementById('markdown_content');
    // 定义转换函数
    function convertMarkdown() {
        const markdownText = textarea.value; // 获取Markdown文本
        // 将转换后的HTML插入到网页中
        document.getElementById('md-content').innerHTML = marked(markdownText);
        // 为生成的HTML中的pre标签添加属性
        document.querySelectorAll('#md-content code').forEach((block) => {
            block.classList.add('layui-code', 'code-demo');
        });
        // 初始化Layui的代码块美化功能
        layui.use('code', function () {
            layui.code({
                elem: '.code-demo'
            });
        });
    }
    // 监听textarea的输入事件
    textarea.addEventListener('input', convertMarkdown);
    // 页面加载时手动触发转换
    if (textarea.value) {
        convertMarkdown();
    }
});