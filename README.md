# MidiMaestro

MidiMaestro requires python3 and libsound to be installed.  Install with
```
sudo apt-get install -y python3-dev libasound2-dev
```

Set up the virtual environment with
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

You can either leave the virtual environment active, or run scripts with `./venv/bin/python ...`

====

After installing new python modules with `pip install ...` save these to `requirements.txt` with `pip freeze > requirements.txt`
