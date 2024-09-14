layui.use(['layer'], function () {
    var layer = layui.layer;
    window.submitBlog = async function submitBlog(is_public) {
        const title = document.getElementById('title').value;
        const markdown_content = document.getElementById('markdown_content').value;
        const tags = document.getElementById('tags').value;

        const formData = new FormData();
        formData.append('title', title);
        formData.append('markdown_content', markdown_content);
        formData.append('tags', tags);
        formData.append('is_public', is_public);

        const response = await fetch(`/write_blog`, {
            method: 'POST',
            body: formData,
        });
        // 检查响应状态码
        if (response.status === 422) {
            layer.alert('请求格式错误，请检查输入内容。', { icon: 2, title: '错误提示' });
            return;
        }
        // 检查响应的内容类型
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            const result = await response.json();
            if (result.error) {
                layer.alert(result.error, { icon: 2 });
            }
        } else {
            if (!is_public) {
                layer.msg('保存草稿成功', { icon: 1 });
            } else {
                layer.msg('博客发布成功', { icon: 1 });
            }
            // 休息1秒
            await new Promise(resolve => setTimeout(resolve, 1000));
            // 处理成功的情况，例如重定向到另一个页面
            window.location.href = response.url;
        }
    }
});