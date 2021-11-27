# Table of contents

- [Environment variables](#environment-variables)
- [Docker](#docker)
  - [Docker build](#docker-build)
  - [Docker compose](#docker-compose)

## Environment variables

- `SERVICE_PORT` - Port of api .Default: 3333

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
      - "3333:3333"
```
