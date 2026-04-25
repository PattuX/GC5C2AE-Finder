# GC5C2AE-Finder

Finds seven caches fitting GC5C2AE from GPX or LOC files.

## Command-line usage

Run `gs.py` with one or more input files:

```bash
python3 gs.py geocaching.loc
python3 gs.py file1.loc file2.gpx --no-route-files
```

- Input files are passed as arguments.
- By default, route files `Schmiederoute*.loc` are written when combinations are found.
- Use `--no-route-files` to only print terminal output.

## GitHub Pages web UI

A simple static website is included under https://pattux.github.io/GC5C2AE-Finder/.

1. Upload one or more `.loc` / `.gpx` files.
2. Click **Run Finder**.
3. Read the output and click **Download .loc ZIP** to download generated route files.

The page uses Pyodide and JSZip client-side, so no installatoin is needed.
