async function submitBlog(is_public) {
    const title = document.getElementById('title').value;
    const markdown_content = document.getElementById('markdown_content').value;
    const tags = document.getElementById('tags').value;

    const formData = new FormData();
    formData.append('title', title);
    formData.append('markdown_content', markdown_content);
    formData.append('tags', tags);
    formData.append('is_public', is_public);

    const response = await fetch(`/user/write_blog`, {
        method: 'POST',
        body: formData,
    });
    // 检查响应状态码
    if (response.status === 422) {
        alert('请求格式错误，请检查输入内容。');
        return;
    }
    // 检查响应的内容类型
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
        const result = await response.json();
        if (result.error) {
            alert(result.error);
        }
    } else {
        // 处理成功的情况，例如重定向到另一个页面
        window.location.href = response.url;
    }
} 