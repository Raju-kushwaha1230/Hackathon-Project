// JavaScript for animations or interactivity
document.addEventListener("DOMContentLoaded", () => {
    const predictionElement = document.querySelector('.prediction');

    // Simple animation for the score appearance
    if (predictionElement) {
        predictionElement.style.opacity = 0;
        predictionElement.style.transform = "scale(0.8)";

        setTimeout(() => {
            predictionElement.style.transition = "all 0.5s ease";
            predictionElement.style.opacity = 1;
            predictionElement.style.transform = "scale(1)";
        }, 300);
    }
});
