# Perforce archive server

## How to use
```
pip install -r requirement.txt
cp config.py.sample config.py
vi config.py
python archive.py
```

## Dockenize
```
docker build -t sulee/p4-archive .
vi config.py
docker run --rm -v $(pwd)/config.py:/opt/config.py -p 5000:5000 sulee/p4-archive
```
