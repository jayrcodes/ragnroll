
Demo

https://www.youtube.com/watch?v=-40SDvznhzg

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

How to create venv and activate it

```
python -m venv venv
source venv/bin/activate
```

How to verify what venv is activated

```
echo $VIRTUAL_ENV
# or 
which python
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
```
