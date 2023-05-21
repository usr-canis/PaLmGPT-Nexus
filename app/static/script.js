const text = "PaLmGPT-nexus , get responses from both the models at once";
const terminalText = document.getElementById("terminal-text");

function typeWriter(text, i) {
    if (i < text.length) {
        terminalText.innerHTML += text.charAt(i);
        i++;
        setTimeout(() => typeWriter(text, i), 50);
    }
}

typeWriter(text, 0);
