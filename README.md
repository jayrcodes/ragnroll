
Demo

https://www.youtube.com/watch?v=-40SDvznhzg

### Dec 28, 2024 - Start API

```
uvicron main:app --port 8100 --reload
```

Available API

```
POST /embed/webpage
POST /chat
```

### Dec 11, 2024 - PDF embedding 

Add pdf on data folder

```
data/article1.pdf
```

Embed and store in Qdrant

```
python test_qdrant_embed_pdf.py
```

Ask questions based on the stored data in Qdrant.

```
python test_chat.py
```

### Dec 8, 2024 - Webpage embedding 

Enter website url, fetch content, chunk it, embed and store in Qdrant.

```
python test_qdrant_embed_webpage.py
```

Ask questions based on the stored data in Qdrant.

```
python test_chat.py
```

## Trying out Poetry

Add to .zshrc

```
export VENV_PATH="$HOME/.virtualenvs/venv"
```

Install poetry into virtual environment

```
python -m venv $VENV_PATH 
$VENV_PATH/bin/pip install -U pip setuptools
$VENV_PATH/bin/pip install poetry
```

Add poetry to zsh

```
alias poetry="$VENV_PATH/bin/poetry"
```

Initialize poetry project

```
~/Developer/ragnroll
poetry init
```

How to activate poetry project

```
poetry shell
```

How to add package

```
poetry add langchain
```

Install packages if there's new update on pyproject.toml

```
poetry install --no-root
```

VSCode settings

```
{
    "python.defaultInterpreterPath": "home/jayrpc/.cache/pypoetry/virtualenvs/ragnroll-J6asQ6za-py3.1/bin/python"
}
```

## Installation/Setup

How to create venv and activate it (Non-poetry way)

```
python -m venv venv
source venv/bin/activate
```


How to verify what venv is activated

```
echo $VIRTUAL_ENV
```

How to install pip packages

```
pip install -r requirements.txt
```

How to freeze pip packages

```
pip install pipreqs
pipreqs . --force
```

## Usage

How to store knowledge and ask questions

```
# add new knowledge under data folder
data/article3.txt

# embed and store knowledge in Qdrant
python test_qdrant_embed.py

# ask questions
python test_chat.py
```

How to store data and search it using Qdrant

```
python test_qdrant_embed.py
python test_qdrant_search.py
```

## Qdrant Database Cheatsheet

How to create Qdrant instance

```
docker run --name qdrant_instance -d -p 6333:6333 qdrant/qdrant
```

Useful Qdrant commands

```
# create a new collection
PUT collections/acme
{
  "vectors": {
    "size": 768,
    "distance": "Cosine"
  }
}

# delete a collection
DELETE collections/acme

# list all points in a collection
POST collections/acme/points/scroll
{
  "with_vector": true
}

# list all collections
GET collections

# search by: filter must match
POST /collections/acme/points/scroll
{
    "filter": {
        "must": [
            { "key": "metadata_title", "match": { "value": "AMD Preps Ryzen 9 9955HX3D \"Fire Range\" CPU For Enthusiast Laptops, Arrow Lake-HX Doesn't Bring Big Performance Jump" } }
        ]
    }
}

# delete by: filter must match
POST /collections/acme/points/delete
{
    "filter": {
        "must": [
            { "key": "metadata_title", "match": { "value": "AMD Preps Ryzen 9 9955HX3D \"Fire Range\" CPU For Enthusiast Laptops, Arrow Lake-HX Doesn't Bring Big Performance Jump" } }
        ]
    }
}

```

## ffmpeg

Convert video to audio

```
ffmpeg -i input_video.mp4 -q:a 0 -map a output_audio.mp3
```