![Python version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)
![PyPi version](https://img.shields.io/badge/pypi%20package-v0.2.1-green.svg)
![OS support](https://img.shields.io/badge/OS-Linux%20%7C%20Windows-red.svg)

# CSViewer-TUI (cvit)

![screenshot](https://github.com/user-attachments/assets/0920d4fc-cf43-48d1-aa65-f0cf49423ca9)

It is a CSV and Parquet file viewer built using Textual and textual-fastdatatable.
It can also be used in the Linux console.

## Usage

If you don't have uv installed, please install it.

### Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

```bash
uv tool install csviewer-tui
```

```bash
cvit example.csv
```
