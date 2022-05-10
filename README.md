# H&M demo

This repository contains a source code of the demo using H&M data to create
an ecommerce recommendation system. 

## Dependencies

The application may be launched in a container, but requires an external Qdrant
server for vector search.

## Building and running the image

The basic version of the image might be built with the following command:

```
docker build -t qdrant/demo-hmm .
docker run -p "8501:8501" \
    qdrant/demo-hmm
```

The application should be exposed at http://localhost:8501

However, setting the project properly requires providing Qdrant hostname and
optionally port, if it's not the default one (6333).

```
docker build -t qdrant/demo-hmm .
docker run \
    -p "8501:8501" \
    -e QDRANT_HOST=qdrant.server.local \
    -e QDRANT_PORT=6321 \
    qdrant/demo-hmm
```
