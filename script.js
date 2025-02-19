document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".play-btn");

    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            const video = button.previousElementSibling;
            if (video.paused) {
                video.play();
                button.textContent = "Pause";
            } else {
                video.pause();
                button.textContent = "Play";
            }
        });
    });
});
