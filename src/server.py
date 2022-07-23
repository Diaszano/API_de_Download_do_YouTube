"""🐍 API de Download do YouTube

Funcionalidades:
    - Poderá baixar videos.
    - Poderá baixar playlists de videos.
    - Poderá baixar músicas.
    - Poderá baixar playlists de músicas.

Arquitetura e Ferramentas
    - [Utilizamos a linguagem Python](https://www.python.org/)
    - [Utilizamos FastAPI](https://fastapi.tiangolo.com/)
    - [Utilizamos moviepy](https://pypi.org/project/moviepy/)
    - [Utilizamos pytube](https://pytube.io/en/latest/)
"""
#-----------------------
# BIBLIOTECAS
#-----------------------
import sys
from fastapi import FastAPI
from src.routers import router_youtube
from src.jobs.check_internet import CheckInternet
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.httpsredirect import (
#     HTTPSRedirectMiddleware
# )
#-----------------------
# FastApi
#-----------------------
ping = CheckInternet();
result_ping = ping.verificar_sync();

if(not result_ping):
    sys.exit(0);
    
app = FastAPI();
#-----------------------
# CORS
#-----------------------
origins:str = [
    "http://localhost",
    "https://localhost",
    "http://localhost:8000",
    "https://localhost:8000",
];
# app.add_middleware(
#     HTTPSRedirectMiddleware
# );
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
);
#-----------------------
# Routers
#-----------------------
app.include_router(
    router = router_youtube.router,
    prefix = "/api"
);
#-----------------------