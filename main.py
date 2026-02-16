import random
import string
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/shorten")
def shorten_url(original_url: str, db: Session = Depends(get_db)):
    existing = db.query(models.URL).filter(
        models.URL.original_url == original_url
    ).first()

    if existing:
        return {"short_url": f"http://localhost:8000/{existing.short_code}"}

    code = generate_code()

    new_url = models.URL(
        original_url=original_url,
        short_code=code
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {"short_url": f"http://localhost:8000/{code}"}

@app.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    url_entry = db.query(models.URL).filter(models.URL.short_code == code).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")

    url_entry.clicks += 1
    db.commit()

    return RedirectResponse(url_entry.original_url)
@app.get("/stats/{code}")
def get_stats(code: str, db: Session = Depends(get_db)):
    url_entry = db.query(models.URL).filter(models.URL.short_code == code).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")

    return {
        "original_url": url_entry.original_url,
        "clicks": url_entry.clicks,
        "short_code": url_entry.short_code
    }
