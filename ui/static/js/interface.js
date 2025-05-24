// static/js/interface.js
// Combina Monaco Editor y lógica de interfaz previa (highlight, tokens, AST)

const reservedTypes = ['IF','ELSE','WHILE','FOR','INT','RETURN','CHAR'];

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
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

// Configuración de Monaco Editor vía CDN
require.config({ paths: { 'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.33.0/min/vs' } });
require(['vs/editor/editor.main'], function() {
  // Crear instancia de Monaco en #code-input
  const editor = monaco.editor.create(document.getElementById('code-input'), {
    value: `#include <iostream>\nint main() { std::cout << \"Hola Mundo!\"; return 0; }`,
    language: 'cpp',
    theme: 'vs-dark',
    readOnly: false,
    automaticLayout: true,
    dragAndDrop: true,
    contextmenu: true,
    mouseWheelZoom: true,
    wordWrap: 'on',
    scrollBeyondLastLine: false,
    minimap: { enabled: false },
    fontSize: 14,
    multiCursorModifier: 'ctrlCmd'
  });

  // Almacenar IDs de decoraciones para eliminarlas en cada compilación
  let decorationIds = [];

  // Atajo Ctrl+A para seleccionar todo
  editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyA, function() {
    editor.trigger('keyboard', 'selectAll');
  });

  // Compilar y resaltar tokens dentro de Monaco
  document.getElementById('btn-compile').addEventListener('click', () => {
    const code = editor.getValue();
    fetch('/api/compile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code })
    })
    .then(res => res.json())
    .then(({ tokens, errors }) => {
      renderTokens(tokens);
      document.getElementById('errors').textContent = errors.join('\n') || 'Sin errores.';
      // Crear decoraciones para tokens y reemplazar las anteriores
      const decorations = tokens.map(tok => ({
        range: new monaco.Range(tok.line, tok.column + 1, tok.line, tok.column + String(tok.value).length + 1),
        options: {
          inlineClassName: tok.type === 'error'
            ? 'token-error'
            : reservedTypes.includes(tok.type)
              ? 'token-reserved'
              : `token-${tok.type.toLowerCase()}`
        }
      }));
      decorationIds = editor.deltaDecorations(decorationIds, decorations);
    })
    .catch(err => console.error(err));
  });

  // Mostrar AST
  document.getElementById('btn-show-ast').addEventListener('click', () => {
    const code = editor.getValue();
    fetch('/api/ast', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
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
      document.getElementById('btn-download-ast').onclick = () => {
        const svgData = new XMLSerializer().serializeToString(svgElement);
        const blob    = new Blob([svgData], { type: 'image/svg+xml' });
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

  // Cerrar modal AST
  document.getElementById('close-ast').addEventListener('click', () => {
    document.getElementById('ast-modal').classList.add('hidden');
  });
});
