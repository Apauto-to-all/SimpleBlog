document.addEventListener("DOMContentLoaded", function () {
  // 发送请求获取用户信息
  fetch("/user_info", {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      const userName = Object.keys(data)[0];
      const userLink = data[userName];

      // 更新用户信息
      document.getElementById("user-name").innerText = userName; // 更新用户名
      document.getElementById("user-avatar").href = userLink; // 更新用户头像链接

      // 如果用户未登录，隐藏用户菜单
      if (userLink === "/user_login") {
        document.getElementById("user-profile").style.display = "none"; // 隐藏用户中心按钮
        document.getElementById("user-logout").style.display = "none"; // 隐藏登出按钮
      } else {
        document.getElementById("user-profile").href = userLink; // 更新用户中心链接
        document.getElementById("user-login").style.display = "none"; // 隐藏登录按钮
      }
    })
    .catch((error) => {
      console.error("Error fetching user info:", error);
    });
});
