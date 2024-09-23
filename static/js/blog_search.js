document.addEventListener('DOMContentLoaded', function () {
    layui.use(['layer', 'flow'], function () {
        var layer = layui.layer;
        var flow = layui.flow;

        // 当前keyword内容
        const keyword = document.getElementById('hidden-div').querySelector('#keyword').value;
        const count = 10; // 每页显示的博客数量
        // 初始化流加载
        flow.load({
            elem: '#show_blogs', // 流加载容器
            done: function (page, next) { // 执行下一页的回调
                // page会自动从1开始，每次递增1
                fetchBlogList(keyword, (page - 1) * count, count, next);
            }
        });
        // 获取博客列表
        async function fetchBlogList(keyword, start = 0, count = 10, next) {
            try {
                // 发送请求获取博客列表
                const response = await fetch(`/blog/api/search?keyword=${keyword}&start=${start}&count=${count}`);
                // 判断响应是否成功
                if (!response.ok) {
                    layer.msg('获取博客列表失败', { icon: 2 });
                    return;
                }
                // 获取博客列表,json()格式化响应数据
                const blogList = await response.json();
                // 使用map()方法遍历blogList数组，生成的HTML内容
                const lis = blogList.map(blog => createBlogCard(blog)).join('');
                // 调用next()方法加载下一页，如果加载页数不满count，判断为最后一页
                next(lis, blogList.length === count);
            } catch (error) {
                // 提示错误信息
                layer.msg('获取博客列表失败', { icon: 2 });
            }
        }
        // 创建博客卡片
        function createBlogCard(blog) {
            return `
                <div class="layui-card blog-card" onclick="window.location.href='/blog/${blog.blog_id}'">
                    <div class="layui-card-header">
                        <h2 class="blog-title">${blog.title}</h2>
                    </div>
                    <div class="layui-card-body">
                        <div class="blog-meta">
                            <span><i class="layui-icon layui-icon-read"></i> ${blog.views} 阅读量</span>
                            <span><i class="layui-icon layui-icon-praise"></i> ${blog.likes} 点赞量</span>
                            <span><i class="layui-icon layui-icon-username"></i> ${blog.nickname}</span>
                        </div>
                        <div class="blog-content">
                            ${blog.content}
                        </div>
                    </div>
                </div>
                `;
        }
    });
});