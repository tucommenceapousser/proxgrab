document.addEventListener('DOMContentLoaded', () => {
    const flashyText = document.querySelector('.flashy-text');
    let colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff'];
    let currentColorIndex = 0;

    setInterval(() => {
        flashyText.style.color = colors[currentColorIndex];
        currentColorIndex = (currentColorIndex + 1) % colors.length;
    }, 500);
});