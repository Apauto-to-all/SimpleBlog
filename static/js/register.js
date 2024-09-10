function showTerms() {
    layer.open({
        type: 1,
        area: ['800px', '600px'], // 弹窗大小
        title: '用户协议',
        shade: 0.6, // 遮罩透明度
        shadeClose: true, // 点击遮罩区域，关闭弹层
        maxmin: true, // 允许全屏最小化
        anim: 0, // 0-6 的动画形式，-1 不开启
        content: `
    <div style="padding: 20px;">
        <h2>简易博客用户协议</h2>
        <p>欢迎使用简易博客！在使用本网站前，请您仔细阅读并同意以下用户协议。</p>
        
        <h3>1. 用户注册</h3>
        <p>用户在注册时需提供真实、准确、完整的个人信息。用户应及时更新个人信息，以确保其真实性和有效性。</p>
        
        <h3>2. 用户行为</h3>
        <p>用户在简易博客上发布的内容应遵守相关法律法规，不得发布违法、侵权、虚假、侮辱、诽谤、淫秽、暴力等不良信息。</p>
        <p>用户不得利用简易博客进行任何形式的商业活动，未经简易博客书面许可，不得发布广告或推广信息。</p>
        
        <h3>3. 评论与点赞</h3>
        <p>用户可以对博客文章进行评论和点赞。评论内容应文明、友善，不得包含任何违法、侵权、侮辱、诽谤等不良信息。</p>
        
        <h3>4. 博客创作</h3>
        <p>用户可以在简易博客上创作并发布自己的博客文章。用户应确保其发布的内容不侵犯任何第三方的合法权益。</p>
        <p>简易博客有权对用户发布的内容进行审核，并有权根据相关法律法规和本协议的规定对不符合要求的内容进行删除或屏蔽。</p>
        
        <h3>5. 知识产权</h3>
        <p>用户在简易博客上发布的原创内容的知识产权归用户所有。用户同意授予简易博客在全球范围内免费的、非独占的、可转授权的许可，以展示、传播、推广用户发布的内容。</p>
        
        <h3>6. 免责声明</h3>
        <p>简易博客不对用户发布内容的真实性、准确性、完整性、合法性负责。用户应对其发布的内容承担全部责任。</p>
        <p>简易博客不对因系统维护或升级而导致的服务中断或暂停承担责任。</p>
        
        <h3>7. 协议修改</h3>
        <p>简易博客有权根据需要修改本协议。协议修改后，将通过网站公告或其他适当方式通知用户。用户继续使用简易博客即视为同意修改后的协议。</p>
        
        <h3>8. 其他</h3>
        <p>本协议的解释、效力及纠纷解决，适用于中华人民共和国法律。因本协议产生的任何纠纷，双方应友好协商解决；协商不成的，任何一方均可向简易博客所在地的人民法院提起诉讼。</p>
        
        <p>感谢您使用简易博客！</p>
        <p>本协议最终解释权归简易博客所有。</p>

        <p>就看个乐子，别太认真！</p>
    </div>
`
    });
}
layui.use(function () {
    var $ = layui.$;
    var form = layui.form;
    var layer = layui.layer;
    // 2次密码输入校验
    form.verify({
        // 确认密码
        confirmPassword: function (value, item) {
            var passwordValue = $('#reg-password').val();
            if (value !== passwordValue) {
                return '两次密码输入不一致';
            }
        }
    });
    // 提交事件
    form.on('submit(demo-register)', function (data) {
        var field = data.field; // 获取表单字段值
        // 校验数据
        if (!field.agreement) {
            layer.msg('您必须勾选同意用户协议才能注册');
            return false;
        }
        // 发送数据到后端
        fetch('/user/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            // 发送表单数据
            body: new URLSearchParams(field).toString()
        })
            .then(response => {
                if (response.redirected) {
                    layer.alert('注册成功,点击确定跳转到登入界面进行登入', { icon: 6 }, function () {
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
        return false; // 阻止表单默认提交行为
    });
});