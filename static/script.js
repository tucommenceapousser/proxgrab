document.addEventListener('DOMContentLoaded', () => {
    const flashyText = document.querySelector('.flashy-text');
    let colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff'];
    let currentColorIndex = 0;

    setInterval(() => {
        flashyText.style.color = colors[currentColorIndex];
        currentColorIndex = (currentColorIndex + 1) % colors.length;
    }, 500);
});

document.addEventListener('DOMContentLoaded', (event) => {
    const copyButton = document.getElementById('copy-button');
    const downloadButton = document.getElementById('download-button');
    const proxyList = document.getElementById('proxy-list');

    if (copyButton) {
        copyButton.addEventListener('click', () => {
            // Crée une plage de texte contenant les résultats
            let range = document.createRange();
            range.selectNode(proxyList);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);

            // Copie le texte sélectionné dans le presse-papiers
            document.execCommand('copy');
            window.getSelection().removeAllRanges();

            alert('Proxies copied to clipboard!');
        });
    }

    if (downloadButton) {
        downloadButton.addEventListener('click', () => {
            // Crée un blob avec les résultats
            let text = Array.from(proxyList.querySelectorAll('li')).map(li => li.textContent).join('\n');
            let blob = new Blob([text], { type: 'text/plain' });
            let url = URL.createObjectURL(blob);

            // Crée un lien pour télécharger le fichier
            let a = document.createElement('a');
            a.href = url;
            a.download = 'proxies.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    }
});
