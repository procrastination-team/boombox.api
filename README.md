# Table of contents

- [Environment variables](#environment-variables)
- [Docker](#docker)
  - [Docker build](#docker-build)
  - [Docker compose](#docker-compose)

## Environment variables

- `CLIENT_ID` - client id for spotify oauth
- `CLIENT_SECRET` - client secret spotify for oauth

## Docker

### Docker build

```bash
docker build -t boombox .
```

### Docker compose

```yaml
version: '3'
services:
  boombox:
    image: boombox
    ports:
      - "8888:8888"
    environment:
      CLIENT_ID: 123456789
      CLIENT_SECRET: abcdef
```
