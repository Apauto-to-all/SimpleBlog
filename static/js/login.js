async function submitForm(event) {
    event.preventDefault(); // 阻止表单默认提交行为

    const form = event.target; // 获取表单元素
    const formData = new FormData(form); // 创建 FormData 对象
    const data = new URLSearchParams(formData); // 将 FormData 对象转换为 URLSearchParams 对象

    try {
        const response = await fetch(form.action, {
            method: form.method,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: data
        });

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
    } catch (error) {
        console.error('Error:', error);
    }
}
