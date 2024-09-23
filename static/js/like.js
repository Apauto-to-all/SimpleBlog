layui.use('layer', function () {
    var layer = layui.layer;

    window.likeBlog = function (button, blogId) {
        var icon = button.querySelector('.layui-icon');
        // 如果已经点赞，发送取消点赞的请求
        if (icon.classList.contains('liked')) {
            // 发送 AJAX 请求到服务器
            fetch(`/blog/api/unlike_blog?blog_id=${blogId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // 使用 Layui 的消息提示功能
                        layer.msg('取消点赞', { icon: 1 });
                        // 改变为灰色的点赞图标，表示未点赞
                        icon.classList.add('layui-icon-praise');
                        icon.classList.remove('liked');
                        // 更新点赞数-1
                        document.getElementById('likes').innerText = '点赞数：' + (parseInt(document.getElementById('likes').innerText.split('：')[1]) - 1);
                    } else {
                        layer.msg('取消点赞失败: ' + data.message, { icon: 2 });
                    }
                })
                .catch(error => {
                    layer.msg('请求失败: ' + error, { icon: 2 });
                });

        }
        else {
            // 发送 AJAX 请求到服务器
            fetch(`/blog/api/like_blog?blog_id=${blogId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // 使用 Layui 的消息提示功能
                        layer.msg('点赞成功', { icon: 1 });
                        // 改变为黄色的点赞图标，表示已经点赞
                        icon.classList.remove('layui-icon-praise');
                        icon.classList.add('liked');
                        // 更新点赞数+1
                        document.getElementById('likes').innerText = '点赞数：' + (parseInt(document.getElementById('likes').innerText.split('：')[1]) + 1);
                    } else {
                        layer.msg('点赞失败: ' + data.message, { icon: 2 });
                    }
                })
                .catch(error => {
                    layer.msg('请求失败: ' + error, { icon: 2 });
                });
        }
    }
});
