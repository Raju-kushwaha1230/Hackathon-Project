document.addEventListener("DOMContentLoaded", () => {
    const radioButtons = document.querySelectorAll("input[type='radio']");
    const labels = document.querySelectorAll(".option");

    // Hover effect for labels
    labels.forEach(label => {
        label.addEventListener("mouseenter", () => {
            label.style.transform = "scale(1.05)";
        });
        label.addEventListener("mouseleave", () => {
            label.style.transform = "scale(1)";
        });
    });

    // Highlight the selected option
    radioButtons.forEach(button => {
        button.addEventListener("change", () => {
            const selected = document.querySelector("input[type='radio']:checked");
            if (selected) {
                selected.nextElementSibling.style.transform = "scale(1.2)";
            }
        });
    });
});
