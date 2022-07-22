#-----------------------
# BIBLIOTECAS
#-----------------------
import os
from time import sleep
import moviepy.editor as mp
from datetime import datetime
from typing import List, Union
from pytube import Playlist, YouTube
from src.jobs.check_internet import CheckInternet
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
class DownloadYouTube:
    """Download YouTube
    
    Esta classe tem o intuito de fazer o download dos 
    videos, músicas e playlist do YouTube.
    """
    def __init__(self,  dias:int=0,horas:int=0,
                        minutos:int=0,segundos:int=0) -> None:
        """Download YouTube

        Esta classe tem o intuito de fazer o download dos 
        videos, músicas e playlist do YouTube.
        
        Args:
            dias     (int, optional): Dias para remoção dos 
            arquivos baixados.
            horas    (int, optional): Dias para remoção dos 
            arquivos baixados.
            minutos  (int, optional): Dias para remoção dos 
            arquivos baixados.
            segundos (int, optional): Dias para remoção dos 
            arquivos baixados.
        """
        self.__dias    :int = dias;
        self.__horas   :int = horas;
        self.__minutos :int = minutos;
        self.__segundos:int = segundos;
        if((dias+horas+minutos+segundos) <= 0):
            self.__tempo_total:int = 1*60;
        else:
            self.__tempo_total:int = (
                (self.__segundos) +
                (60*self.__minutos) + 
                (60*60*self.__horas) + 
                (60*60*24*self.__dias)
            );
            if(self.__tempo_total <= 0):
                self.__tempo_total:int = 1*60;
        self.__check_internet = CheckInternet();
        
    def remover(self,caminho_do_arquivo:str) -> None:
        """Remover

        Neste método iremos remover o arquivo baixado anteriormente.
        
        Args:
            caminho_do_arquivo (str): Caminho do arquivo baixado.
        """
        sleep(self.__tempo_total);
        if(os.path.exists(caminho_do_arquivo)):
            os.remove(caminho_do_arquivo);
        if(os.path.exists(os.path.dirname(caminho_do_arquivo))):
            os.rmdir(os.path.dirname(caminho_do_arquivo));
    
    def __remover_arquivo(self,caminho_do_arquivo:str) -> None:
        """Remover

        Neste método iremos remover o arquivo baixado anteriormente.
        
        Args:
            caminho_do_arquivo (str): Caminho do arquivo baixado.
        """
        if(os.path.exists(caminho_do_arquivo)):
            os.remove(caminho_do_arquivo);

    async def __verificacao(self,link:str) -> Union[None,str]:
        """Verificação
        
        Aqui faremos a verificação do link.

        Args:
            link (str): Aqui deve conter uma string de um link
            válido.

        Returns:
            Union[None,str]: Se o link for verdadeiro irá retornar
            o próprio, mas se for falso irá retornar None.
        """
        url = await self.__check_internet.pegar_url(url=link);
        
        if(not url):
            return None;
        
        conexao = await self.__check_internet.verificar_link(url);
        
        if(not conexao):
            return None;
        
        return url;
    
    async def baixar_video(self,link:str) -> List[Union[str,None]]:
        """Baixar Video

        Args:
            link (str): Aqui deve conter o link do video do YouTube
            a ser baixado.

        Returns:
            List[str|None]: Aqui retornaremos em primeiro o título do 
            video e por segundo o seu caminho ou Nulo.
        """
        url = await self.__verificacao(link=link);
        
        if(not url):
            return None, None;
        
        youtube = YouTube(url);
        
        video = youtube.streams.filter(
            progressive=True, 
            file_extension='mp4'
        ).order_by(
            'resolution'
        ).desc().first();
        now = datetime.now();
        time = now.strftime("%d-%m-%Y_%H:%M:%S")
        caminho_video = video.download(f"./data/video/{time}");
        return youtube.title,caminho_video;
    
    async def baixar_musica(self,link:str) -> List[Union[str,None]]:
        """Baixar música

        Args:
            link (str): Aqui deve conter o link da música do YouTube
            a ser baixado.

        Returns:
            List[str|None]: Aqui retornaremos em primeiro o título da 
            música e por segundo o seu caminho ou Nulo.
        """
        url = await self.__verificacao(link=link);
        
        if(not url):
            return None, None;
        
        youtube = YouTube(url);
        
        video = youtube.streams.filter(
            progressive=True, 
            file_extension='mp4'
        ).order_by(
            'resolution'
        ).desc().first();
        
        now = datetime.now();
        time = now.strftime("%d-%m-%Y_%H:%M:%S")
        
        caminho_video = video.download(f"./data/music/{time}");
        caminho_musica = await self.converter_to_mp3(caminho_video);
        
        return youtube.title,caminho_musica;
    
    async def converter_to_mp3(self,arq_video:str):
        name, ext = os.path.splitext(arq_video);
        out_name = name + ".mp3";
        
        with mp.AudioFileClip(arq_video) as audioclip:
            audioclip.write_audiofile(out_name,logger=None);
        
        self.__remover_arquivo(arq_video);
        return out_name;
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
#-----------------------