# digital ema

a digital version of traditional japanese ema (絵馬) wooden plaques for writing wishes and prayers.

## features

- write and submit wishes
- view all submitted wishes
- persistent storage with sqlite
- deployed on fly.io

## tech

- fastapi backend
- sqlite database
- vanilla js frontend
- fly.io hosting

## local dev

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

visit `http://localhost:8000`

## deploy

```bash
fly deploy
```

live at [digital-ema.fly.dev](https://digital-ema.fly.dev)
