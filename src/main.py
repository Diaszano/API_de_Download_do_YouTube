#-----------------------
# BIBLIOTECAS
#-----------------------
import os

import asyncio
from time import sleep
import moviepy.editor as mp
from datetime import datetime
from typing import List, Union
from pytube import Playlist, YouTube
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import (
    StreamingResponse, FileResponse
)
from fastapi import (
    FastAPI, BackgroundTasks, status, HTTPException
)
#-----------------------
# CONSTANTES
#-----------------------
DIAS_REMOCAO         :int = 0;
HORAS_REMOCAO        :int = 0;
MINUTOS_REMOCAO      :int = 15;
TEMPO_TOTAL_REMOVOCAO:int = (
    (60*MINUTOS_REMOCAO) + 
    (60*60*HORAS_REMOCAO) + 
    (60*60*24*DIAS_REMOCAO)
);
#-----------------------
app = FastAPI();


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://192.168.31.21",
    "http://192.168.31.21:8000",
    "http://192.168.31.*:8000",
    "http://192.168.31.*",
];

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
);
# VIDEO_URL = 'https://www.youtube.com/watch?v=xEukcvE63nk&ab_channel=Diolinux'
# start = time.time();
# yt = YouTube(VIDEO_URL)


# # video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first();
# audio = yt.streams.filter(only_audio=True)[-1];

# # print(video)
# print(audio)
# # print(video.download())

# arquivo_audio:str = audio.download();

# def convert_to_mp3_ffmpeg(arq_video):
#     name, ext = os.path.splitext(arq_video);
#     out_name = name + ".mp3";
#     ffmpeg.input(arq_video).output(out_name).run();

def converter_to_mp3_moviepy(arq_video):
    name, ext = os.path.splitext(arq_video);
    out_name = name + ".mp3";
    
    with mp.AudioFileClip(arq_video) as audioclip:
        audioclip.write_audiofile(out_name,logger=None);
    
# converter_to_mp3_moviepy(arquivo_audio);
# # convert_to_mp3_ffmpeg(arquivo_audio);
# end = time.time();
# print(end - start);
#-----------------------
# CLASSES
#-----------------------    
#-----------------------
# FUNÇÕES()
#-----------------------
def remover(arquivo) -> None:
    sleep(TEMPO_TOTAL_REMOVOCAO);
    os.remove(arquivo);
    os.rmdir(os.path.dirname(arquivo));

@app.get("/streaming/",response_class=StreamingResponse,status_code=status.HTTP_200_OK,tags=["Assistir"])
async def streaming_video(link:str,background_tasks: BackgroundTasks):
    """Assistir o video

    Args:
        link (str): Deve ser um link existente no youtube.
    Returns:
        MP4: retorna o video.
    """
    try:
        nome,arquivo = await DownloadYouTube().baixar_video(link);
        def iterfile():
            with open(arquivo,mode="rb") as file_like:
                yield from file_like
        retorno = StreamingResponse(iterfile(), media_type="video/mp4");
        background_tasks.add_task(remover,arquivo);
        return retorno;
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );

@app.get("/download/",response_class=FileResponse,status_code=status.HTTP_200_OK,tags=["Baixar"])
async def download_video(link:str,background_tasks: BackgroundTasks):
    """Baixar o video

    Args:
        link (str): Deve ser um link existente no youtube.
    Returns:
        MP4: retorna o video.
    """
    try:
        nome,arquivo = await DownloadYouTube().baixar_video(link);
        retorno = FileResponse(arquivo,media_type=".mp4",filename=f"{nome}.mp4");
        background_tasks.add_task(remover,arquivo);
        return retorno;
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );
#-----------------------
# Main()
#-----------------------
#-----------------------