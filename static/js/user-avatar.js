document.addEventListener("DOMContentLoaded", function () {
    fetch("/user/user_info")
        .then(response => response.json())
        .then(data => {
            const userAvatar = document.getElementsByClassName("user-avatar")[0];
            const userInitials = document.getElementsByClassName("initials")[0];
            const [nickname, link] = Object.entries(data)[0];

            userInitials.textContent = nickname; // 显示用户昵称
            userAvatar.onclick = function () {
                window.open(link);
            };
        })
        .catch(error => {
            console.error("Error fetching user info:", error);
        });
});