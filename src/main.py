#-----------------------
# BIBLIOTECAS
#-----------------------
import os
import re
import aiohttp
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

# def converter_to_mp3_moviepy(arq_video):
#     name, ext = os.path.splitext(arq_video);
#     out_name = name + ".mp3";
    
#     with mp.AudioFileClip(arq_video) as audioclip:
#         audioclip.write_audiofile(out_name,logger=None);
    
# converter_to_mp3_moviepy(arquivo_audio);
# # convert_to_mp3_ffmpeg(arquivo_audio);
# end = time.time();
# print(end - start);
#-----------------------
# CLASSES
#-----------------------    
class CheckInternet:
    """Checador de internet
    
    Está classe tem o intuito de verificar
    se está com internet ou não.
    """
    def __compile_re(self) -> None:
        """_summary_
        """
        regex:str = (
            r"(?i)\b((?:https?://|"
            r"www\d{0,3}[.]|"
            r"[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|"
            r"\(([^\s()<>]+|"
            r"(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|"
            r"(\([^\s()<>]+\)))*\)|"
            r"[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        );
        self.__regex_url = re.compile(
            regex,
            re.MULTILINE |
            re.IGNORECASE
        );
    
    def __init__(self) -> None:
        """_summary_
        """
        self.__compile_re();
        self.__MIN:int = 1;
        self.__MAX:int = 100;
        self.__URL:str = r'https://www.google.com/';
    
    async def pegar_url(self,url:str) -> Union[str,None]:
        """_summary_

        Args:
            url (str): _description_

        Returns:
            Union[str,None]: _description_
        """
        list_url = self.__regex_url.findall(url);
        if(list_url):
            return list_url[0][0];
    
    async def verificar_link(self,url:str) -> bool:
        """_summary_

        Args:
            url (str): _description_

        Returns:
            bool: _description_
        """
        url = await self.pegar_url(url);
        if(not url):
            return False;
        return await self.__requisicao(url);
    
    async def verificar(self,quantidade:int = 10) -> bool:
        """Verificar conexão

        Args:
            quantidade (int, optional): Tu podes informar a quantidade
            de pings que vai querer fazer entre 1 até 100.

        Returns:
            bool:   retorna um boolean dizendo
            como está a conexão com a internet
            sendo True para conectado e False
            para não conectado.
        """
        if(quantidade < self.__MIN):
            quantidade = self.__MIN;
        elif(quantidade > self.__MAX):
            quantidade = self.__MAX;
        
        tasks = (
            self.__requisicao(self.__URL)
            for _ in range(quantidade)
        )
        lista = await asyncio.gather(*tasks);
        return await(self.__verificar_media(lista));
    
    @staticmethod
    async def __requisicao(url:str) -> bool:
        """Requisição

        Aqui faremos a requisição para um site determinado
        e verificaremos se ele irá retornar algo.
        
        Returns:
            bool: retornamos True se tiver conexão com o site e
            False se não tiver.
        """
        try:
            async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        pass;
            return True;
        except Exception as error:
            return False;
    
    @staticmethod
    async def __verificar_media(lista:List[bool]) -> bool:
        """Verificar Média
        
        Aqui fazemos a verificação da média dos resultados 
        do ping feitos.

        Args:
            lista (List[bool]): Recebemos uma lista com os 
            resultados dos pings feitos. 

        Returns:
            bool: Se a média for maior ou igual a 90%
            retornamos verdadeiro, mas caso contrário
            iremos retornar False.
        """
        tamanho_total:int = len(lista);
        conectados:int = 0;
        for index in lista:
            if(index):
                conectados += 1;
        media:int = int((conectados/tamanho_total)*100);
        if(media >= 90):
            return True;
        return False;

class DownloadYouTube:
    def __init__(self) -> None:
        """_summary_
        """
        self.__check_internet = CheckInternet();

    async def __verificacao(self,link:str) -> Union[None,str]:
        """_summary_

        Args:
            link (str): _description_

        Returns:
            Union[None,str]: _description_
        """
        url = await self.__check_internet.pegar_url(url=link);
        
        if(not url):
            return None;
        
        conexao = await self.__check_internet.verificar_link(url);
        
        if(not conexao):
            return None;
        
        return url;
    
    async def baixar_video(self,link:str) -> Union[None,int]:
        """_summary_

        Args:
            link (str): _description_

        Returns:
            Union[None,int]: _description_
        """
        url = await self.__verificacao(link=link);
        
        if(not url):
            return None;
        
        youtube = YouTube(url);
        
        video = youtube.streams.filter(
            progressive=True, 
            file_extension='mp4'
        ).order_by(
            'resolution'
        ).desc().first();
        now = datetime.now();
        time = now.strftime("%d-%m-%Y_%H:%M:%S")
        caminho_video = video.download(f"./data/{time}");
        return youtube.title,caminho_video;
        
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