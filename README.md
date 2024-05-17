# DomJudge-Tool-Standalone

## Environmental Requirements
- python = "^3.12"
- poetry

## How to implement
```
python -m streamlit run home.py --server.port=8000 --server.address=0.0.0.0
```

## Use Example
```
$ domjudge-tool-cli general config https://domjudge.example.dev
$ domjudge-tool-cli general check                
Success connect API v4.

$ domjudge-tool-cli users user-list
```