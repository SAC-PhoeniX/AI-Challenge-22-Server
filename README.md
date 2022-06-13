# PhoeniX AI Challenge 2022 Backend

The server used to run Keras models from the AI Challenge participant teams.

## Requirements

This uses the latest (?) versions of:
- tensorflow
- aiohttp
with Python 3

## Running
0. Clone using `git clone --recurse-submodules https://github.com/SAC-PhoeniX/AI-Challenge-22-Server.git`
1. Make a copy of example.conf and enter team names and models like in the example
2. Run `conda env create -f environment.yml` to download the requirements
3. Run `server.py`

### Running without TensorFlow

If you need to run the server to test the endpoints, you can set the `MODELS` environment variable to `NO_TF` before running `server.py`. To do so, use these commands:

on Linux/OSX:
```bash
MODELS=NO_TF python server.py
```

on Windows in [PowerShell](https://stackoverflow.com/questions/1420719/powershell-setting-an-environment-variable-for-a-single-command-only):
```powershell
$env:MODELS='NO_TF'
python server.py

# do after testing:
$env:MODELS="TF"
```
