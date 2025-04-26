const reservedTypes = ['IF','ELSE','WHILE','FOR','INT','RETURN','CHAR'];
function escapeHtml(str) {
  return str.replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
}

function highlightCode(code, tokens) {
  tokens.sort((a, b) => a.column - b.column);
  let result = '';
  let lastIndex = 0;

  tokens.forEach(tok => {
    const start = tok.column;
    const text  = tok.value.toString();

    result += escapeHtml(code.slice(lastIndex, start));

    let cls;
    if (tok.type === 'error') {
      cls = 'token-error';
    } else if (reservedTypes.includes(tok.type)) {
      cls = 'token-reserved';
    } else {
      cls = `token-${tok.type}`;
    }

    result += `<span class="${cls}">${escapeHtml(text)}</span>`;
    lastIndex = start + text.length;
  });

  result += escapeHtml(code.slice(lastIndex));
  return result;
}


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

document.getElementById('btn-compile').addEventListener('click', () => {
  const editor = document.getElementById('code-input');
  const code   = editor.innerText; 
  fetch('/api/compile', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code })
  })
  .then(res => res.json())
  .then(({ tokens, errors }) => {
    renderTokens(tokens);
    document.getElementById('errors').textContent =
      errors.join('\n') || 'Sin errores.';
    editor.innerHTML = highlightCode(code, tokens);
  })
  .catch(err => console.error(err));
});
