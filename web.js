const fileInput = document.getElementById('fileInput');
const runButton = document.getElementById('runButton');
const downloadButton = document.getElementById('downloadButton');
const outputEl = document.getElementById('output');

let pyodide;
let generatedRouteFiles = [];

function linkifyLine(line) {
  const parts = line.split(/(GC[0-9A-Z]+)/g);
  const fragment = document.createDocumentFragment();

  for (const part of parts) {
    if (/^GC[0-9A-Z]+$/.test(part)) {
      const anchor = document.createElement('a');
      anchor.href = `https://coord.info/${part}`;
      anchor.target = '_blank';
      anchor.rel = 'noopener noreferrer';
      anchor.textContent = part;
      fragment.appendChild(anchor);
    } else {
      fragment.appendChild(document.createTextNode(part));
    }
  }

  return fragment;
}

function renderOutput(output) {
  outputEl.textContent = '';
  const lines = output.split('\n');

  lines.forEach((line, idx) => {
    outputEl.appendChild(linkifyLine(line));
    if (idx < lines.length - 1) {
      outputEl.appendChild(document.createElement('br'));
    }
  });
}

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

async function runFinder() {
  const files = Array.from(fileInput.files || []);

  if (!files.length) {
    outputEl.textContent = 'Please upload at least one .loc or .gpx file.';
    downloadButton.disabled = true;
    return;
  }

  const py = await ensurePyodide();
  outputEl.textContent = 'Processing...';
  downloadButton.disabled = true;

  for (const file of files) {
    const content = new Uint8Array(await file.arrayBuffer());
    py.FS.writeFile(file.name, content);
  }

  py.globals.set('browser_queries', files.map((f) => f.name));

  try {
    await py.runPythonAsync(`
import os
import shutil

if os.path.isdir('routes'):
    shutil.rmtree('routes')

output, combos = gs.run(browser_queries, write_routes=True, output_dir='routes')
route_files = sorted(os.listdir('routes')) if os.path.isdir('routes') else []
`);

    const output = py.globals.get('output');
    const routeFilesProxy = py.globals.get('route_files');
    generatedRouteFiles = routeFilesProxy.toJs();

    renderOutput(output);
    downloadButton.disabled = generatedRouteFiles.length === 0;

    routeFilesProxy.destroy();
  } catch (error) {
    outputEl.textContent = `Error: ${error.message}`;
    generatedRouteFiles = [];
    downloadButton.disabled = true;
  }
}

async function downloadRoutesZip() {
  if (!generatedRouteFiles.length) {
    return;
  }

  const py = await ensurePyodide();
  const zip = new JSZip();

  for (const fileName of generatedRouteFiles) {
    const bytes = py.FS.readFile(`routes/${fileName}`, { encoding: 'binary' });
    zip.file(fileName, bytes);
  }

  const blob = await zip.generateAsync({ type: 'blob' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'Schmiederouten.zip';
  link.click();
  URL.revokeObjectURL(link.href);
}

runButton.addEventListener('click', runFinder);
downloadButton.addEventListener('click', downloadRoutesZip);
