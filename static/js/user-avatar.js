document.addEventListener("DOMContentLoaded", function () {
  // 发送请求获取用户信息
  fetch('/user_info')
    .then(response => response.json())
    .then(data => {
      const [username, nickname, userLink] = data;

      // 更新用户信息
      document.getElementById("user-name").innerText = nickname; // 更新昵称
      document.getElementById("user-avatar").href = userLink; // 更新用户头像链接

      // 更新用户头像
      var avatarImg = document.getElementById('user-avatar-show');
      var timestamp = new Date().getTime(); // 防止浏览器缓存

      // 如果用户未登录，隐藏用户菜单
      if (userLink === "/user_login") {
        document.getElementById("user-profile").style.display = "none"; // 隐藏用户中心按钮
        document.getElementById("user-logout").style.display = "none"; // 隐藏登出按钮
      } else {
        document.getElementById("user-profile").href = userLink; // 更新用户中心链接
        document.getElementById("user-login").style.display = "none"; // 隐藏登录按钮
        document.getElementById("user-register").style.display = "none"; // 隐藏注册按钮
        avatarImg.src = `/img/user_avatar/${username}?t=${timestamp}`;
      }
    })
    .catch(error => {
      console.error('Error fetching user info:', error);
    });
});
