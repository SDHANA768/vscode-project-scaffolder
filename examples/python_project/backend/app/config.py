import os

DEBUG = os.getenv("DEBUG", True)
HOST  = os.getenv("HOST", "0.0.0.0")
PORT  = int(os.getenv("PORT", 8000))
