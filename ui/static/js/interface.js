function renderTokens(tokens) {
    const tbody = document.querySelector('#tokens-table tbody');
    tbody.innerHTML = '';
    tokens.forEach(t => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${t.type}</td><td>${t.value}</td><td>[${t.line}, ${t.column}]</td>`;
        tbody.appendChild(tr);
    });
}

document.getElementById('btn-compile').addEventListener('click', () => {
    const code = document.getElementById('code-input').value;
    fetch('/api/compile', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ code })
    })
    .then(res => res.json())
    .then(data => {
        renderTokens(data.tokens);
        document.getElementById('errors').textContent = data.errors.join('\n') || 'Sin errores.';
    });
});