"""
Entry point for backward compatibility.
This file now just imports and uses the modular app structure.
"""

from app.main import app

# This allows running the app directly with `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 