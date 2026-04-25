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
- After the `x combinations found` line, each combination is printed on its own line as comma-separated `GC...` codes.

## GitHub Pages web UI

A simple static website is included (`index.html`, `web.js`, `styles.css`) so non-coders can use the tool in a browser:

1. Enable **GitHub Pages** in your repository settings (deploy from the root on `main`, or use Actions).
2. Open the published site.
3. Upload one or more `.loc` / `.gpx` files.
4. Click **Run Finder**.
5. Read the output and click **Download .loc ZIP** to download generated route files.

The page uses Pyodide and JSZip client-side, so no server is needed.
