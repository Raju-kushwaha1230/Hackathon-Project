// Add a slight animation on button click
document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll("button");

    buttons.forEach(button => {
        button.addEventListener("click", (e) => {
            button.style.transform = "scale(0.95)";
            setTimeout(() => {
                button.style.transform = "scale(1)";
            }, 150);
        });
    });
});
