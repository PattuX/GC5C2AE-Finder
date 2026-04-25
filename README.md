# GC5C2AE-Finder

Finds seven caches fitting GC5C2AE from GPX or LOC files.

## Command-line usage

Run `gs.py` with one or more input files:

```bash
python3 gs.py geocaching.loc
python3 gs.py file1.loc file2.gpx --no-route-files
```

- Input files are passed as arguments (no hardcoded `queries` list anymore).
- By default, route files `Schmiederoute*.loc` are written when combinations are found.
- Use `--no-route-files` to only print terminal output.

## GitHub Pages web UI

A simple static website is included (`index.html`, `web.js`, `styles.css`) so non-coders can use the script in a browser:

1. Enable **GitHub Pages** in your repository settings (deploy from the root on `main`, or use Actions).
2. Open the published site.
3. Upload one or more `.loc` / `.gpx` files.
4. Click **Run Finder**.
5. Read the terminal-like output in the output panel.

The page runs `gs.py` in-browser via Pyodide, so no server is needed.
