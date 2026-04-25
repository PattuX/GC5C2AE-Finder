const fileInput = document.getElementById('fileInput');
const runButton = document.getElementById('runButton');
const outputEl = document.getElementById('output');

let pyodide;

async function ensurePyodide() {
  if (pyodide) return pyodide;
  outputEl.textContent = 'Loading Python runtime...';
  pyodide = await loadPyodide();

  const gsCode = await fetch('./gs.py').then((res) => res.text());
  pyodide.FS.writeFile('gs.py', gsCode);
  await pyodide.runPythonAsync(`
import importlib.util
spec = importlib.util.spec_from_file_location("gs", "gs.py")
gs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gs)
`);

  return pyodide;
}

runButton.addEventListener('click', async () => {
  const files = Array.from(fileInput.files || []);

  if (!files.length) {
    outputEl.textContent = 'Please upload at least one .loc or .gpx file.';
    return;
  }

  const py = await ensurePyodide();
  outputEl.textContent = 'Processing...';

  for (const file of files) {
    const content = new Uint8Array(await file.arrayBuffer());
    py.FS.writeFile(file.name, content);
  }

  const names = files.map((f) => f.name);
  py.globals.set('browser_queries', names);

  try {
    await py.runPythonAsync(`
output, combos = gs.run(browser_queries, write_routes=False)
`);
    const output = py.globals.get('output');
    outputEl.textContent = output;
  } catch (error) {
    outputEl.textContent = `Error: ${error.message}`;
  }
});
