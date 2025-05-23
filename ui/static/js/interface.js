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

document.getElementById('btn-show-ast').addEventListener('click', () => {
  const code = document.getElementById('code-input').innerText;
  fetch('/api/ast', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ code })
  })
  .then(res => {
    if (!res.ok) throw new Error('Error al generar AST');
    return res.json();
  })
  .then(({ dot }) => {
    const viz = new Viz();
    return viz.renderSVGElement(dot);
  })
  .then(svgElement => {
    const container = document.getElementById('ast-container');
    container.innerHTML = '';            
    container.appendChild(svgElement);   
    document.getElementById('ast-modal').classList.remove('hidden');

    const exportBtn = document.getElementById('btn-download-ast');
    exportBtn.style.display = 'inline-block';

    exportBtn.onclick = () => {
      const svgData = new XMLSerializer().serializeToString(svgElement);
      const blob    = new Blob([svgData], {type: 'image/svg+xml'});
      const url     = URL.createObjectURL(blob);
      const a       = document.createElement('a');
      a.href        = url;
      a.download    = 'ast.svg';
      a.click();
      URL.revokeObjectURL(url);
    };
  })
  .catch(err => alert(err.message));
});

document.getElementById('close-ast').addEventListener('click', () => {
  document.getElementById('ast-modal').classList.add('hidden');
});

function mostrar3AC() {
  const codigo = document.getElementById('code-input').innerText;

  fetch('/api/compile', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({code: codigo})
  })
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById('ast-container');
    const modal = document.getElementById('ast-modal');
    container.innerHTML = '';

    document.getElementById('btn-download-ast').style.display = 'none';

    const pre = document.createElement('pre');

    if (data.intermediate_code && data.intermediate_code.length > 0) {
      pre.textContent = Array.isArray(data.intermediate_code)
        ? data.intermediate_code.join('\n')
        : data.intermediate_code;
    } else if (data.errors && data.errors.length > 0) {
      pre.textContent = "Errores:\n" + data.errors.join('\n');
    } else {
      pre.textContent = "No se generó código intermedio.";
    }

    container.appendChild(pre);
    modal.classList.remove('hidden');
  })
  .catch(error => {
    document.getElementById('intermediate-code').textContent =
      'Error al comunicarse con el servidor: ' + error.message;
  });
}

