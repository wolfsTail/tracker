import os
from uvicorn.workers import UvicornWorker
from dotenv import load_dotenv

load_dotenv()

environment = os.getenv("ENVIRONMENT")

env = os.path.join(os.getcwd(), f".{environment}.env")

if os.path.exists(env):
    load_dotenv(env)

bind = "127.0.0.1:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
