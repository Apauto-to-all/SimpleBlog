layui.use(function () {
    var form = layui.form;
    var layer = layui.layer;
    // 提交事件
    form.on('submit(demo-login)', function (data) {
        var field = data.field; // 获取表单字段值
        // 发送数据到后端
        fetch('/login/api', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            // 发生表单数据
            body: new URLSearchParams(field).toString()
        })
            .then(response => {
                if (response.redirected) {
                    layer.alert('登录成功,点击确定跳转到用户中心', { icon: 6 }, function () {
                        window.location.href = response.url;
                    });
                } else {
                    return response.json();
                }
            })
            .then(result => {
                if (result && result.error) {
                    layer.alert(result.error, { icon: 5 });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                layer.alert('提交失败，请稍后重试', { icon: 5 });
            });
        return false;
    });
});