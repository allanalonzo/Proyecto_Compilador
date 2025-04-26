// ui/static/js/interface.js

// Función que pinta la tabla de tokens
function renderTokens(tokens) {
    const tbody = document.querySelector('#tokens-table tbody');
    tbody.innerHTML = ''; 
    tokens.forEach(tok => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
        <td>${tok.type}</td>
        <td>${tok.value}</td>
        <td>[${tok.line}, ${tok.column}]</td>
    `;
    tbody.appendChild(tr);
    });
}

  // Cuando hagan clic en Compilar…
document.getElementById('btn-compile').addEventListener('click', () => {
    const code = document.getElementById('code-input').value;

    fetch('/api/compile', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code })
    })
    .then(res => res.json())
    .then(({ tokens, errors }) => {
    renderTokens(tokens);
    document.getElementById('errors').textContent = errors.join('\n') || 'Sin errores.';
    })
    .catch(console.error);
});