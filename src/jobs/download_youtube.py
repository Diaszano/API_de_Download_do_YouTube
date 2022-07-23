#-----------------------
# BIBLIOTECAS
#-----------------------
import os
import re
import asyncio
import zipfile
from time import sleep
import moviepy.editor as mp
from datetime import datetime
from pytube import Playlist, YouTube
from typing import List, NoReturn, Union
from src.jobs.check_internet import CheckInternet
#-----------------------
# CONSTANTES
#-----------------------
NUMERO_MAXIMO_CONCORRENCIA:int = 10;
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
            horas    (int, optional): Horas para remoção dos 
            arquivos baixados.
            minutos  (int, optional): Minutos para remoção dos 
            arquivos baixados.
            segundos (int, optional): Segundos para remoção dos 
            arquivos baixados.
        """
        self.__dias    :int = dias;
        self.__horas   :int = horas;
        self.__minutos :int = minutos;
        self.__segundos:int = segundos;
        if((dias+horas+minutos+segundos) <= 0):
            self.tempo_total:int = 1*60;
        else:
            self.tempo_total:int = (
                (self.__segundos) +
                (60*self.__minutos) + 
                (60*60*self.__horas) + 
                (60*60*24*self.__dias)
            );
            if(self.tempo_total <= 0):
                self.tempo_total:int = 1*60;
        self.__check_internet = CheckInternet();
    
    @staticmethod
    def data() -> str:
        """Data
        
        Aqui nós pegaremos a data atual.

        Returns:
            str: retorna a data neste formato.
                Dia-Mês-Ano_Hora-Minutos-Segundos
        """
        now = datetime.now();
        time = now.strftime("%d-%m-%Y_%H:%M:%S");
        return time;
    
    def remover(self,caminho_do_arquivo:str) -> NoReturn:
        """Remover

        Neste método iremos remover o arquivo baixado anteriormente.
        
        Args:
            caminho_do_arquivo (str): Caminho do arquivo baixado.
        """
        sleep(self.tempo_total);
        if(os.path.exists(caminho_do_arquivo)):
            os.remove(caminho_do_arquivo);
        if(os.path.exists(os.path.dirname(caminho_do_arquivo))):
            os.rmdir(os.path.dirname(caminho_do_arquivo));
    
    @staticmethod
    def __remover_arquivo(caminho_do_arquivo:str) -> NoReturn:
        """Remover

        Neste método iremos remover o arquivo baixado anteriormente.
        
        Args:
            caminho_do_arquivo (str): Caminho do arquivo baixado.
        """
        if(os.path.exists(caminho_do_arquivo)):
            os.remove(caminho_do_arquivo);
    
    @staticmethod
    def __remover_pasta(caminho_da_pasta:str) -> NoReturn:
        """Remover

        Neste método iremos remover uma pasta criada anteriormente.
        
        Args:
            caminho_do_arquivo (str): Caminho do arquivo baixado.
        """
        if(os.path.exists(caminho_da_pasta)):
            os.rmdir(caminho_da_pasta);

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
    
    async def __pegar_video(self,link:str) -> Union[YouTube,str,None]:
        # Retorno padrão
        retorno:list = [None,None];
        # Verificar se é playlist
        verificado = re.findall(
            r"(/watch\?v=[\w-]*)",
            link
        );
        if(not verificado):
            return retorno;
        # Verificar a conexão com o link
        url = await self.__verificacao(link);
        if(not url):
            return retorno;
        # Pegar a playlist
        youtube = YouTube(url);
        titulo:str = youtube.title;
        video = youtube.streams.filter(
            progressive=True, 
            file_extension='mp4'
        ).order_by(
            'resolution'
        ).desc().first();
        
        return video,titulo;
    
    async def baixar_video(self,link:str,pasta:str=None) -> List[Union[str,None]]:
        """Baixar Video

        Args:
            link (str): Aqui deve conter o link do video do YouTube
            a ser baixado.

        Returns:
            List[str|None]: Aqui retornaremos em primeiro o título do 
            video e por segundo o seu caminho ou Nulo.
        """
        # Verifica se precisa por em uma pasta especifica.
        if(not pasta):
            pasta = f"./data/video/{self.data()}";
        # Pega o video do YouTube
        [youtube,titulo] = await self.__pegar_video(link);
        youtube: YouTube;
        titulo : str;
        # Baixa o video
        caminho_video = youtube.download(pasta);
        return titulo,caminho_video;
    
    async def baixar_musica(self,link:str,pasta:str=None) -> List[Union[str,None]]:
        """Baixar música

        Args:
            link (str): Aqui deve conter o link da música do YouTube
            a ser baixado.

        Returns:
            List[str|None]: Aqui retornaremos em primeiro o título da 
            música e por segundo o seu caminho ou Nulo.
        """
        # Verifica se precisa por em uma pasta especifica.
        if(not pasta):
            pasta = f"./data/music/{self.data()}";
        # Pega o video do YouTube
        [youtube,titulo] = await self.__pegar_video(link);
        youtube: YouTube;
        titulo : str;
        # Baixa o video
        caminho_video = youtube.download(pasta);
        # Transforma em música
        caminho_musica = await self.converter_to_mp3(caminho_video);
        
        return titulo,caminho_musica;
    
    async def converter_to_mp3(self,arq_video:str):
        name, ext = os.path.splitext(arq_video);
        out_name = name + ".mp3";
        
        with mp.AudioFileClip(arq_video) as audioclip:
            audioclip.write_audiofile(out_name,logger=None);
        
        self.__remover_arquivo(arq_video);
        return out_name;
    
    async def __pegar_playlist(self,link:str) -> Union[Playlist,str,None]:
        # Retorno padrão
        retorno:list = [None,None];
        # Verificar se é playlist
        verificado = re.findall(
            r"(/playlist\?list=[\w-]*)",
            link
        );
        if(not verificado):
            return retorno;
        # Verificar a conexão com o link
        url = await self.__verificacao(link);
        if(not url):
            return retorno;
        # Pegar a playlist
        playlist   = Playlist(url);
        titulo:str = playlist.title;
        
        return playlist,titulo;
    
    def __zipar_playlist(self,pasta:str,arquivo_zip:str) -> NoReturn:
        # Pega os arquivos
        arquivos = (
            arquivo
            for _, _, arquivos in os.walk(os.path.abspath(pasta))
                for arquivo in arquivos
                    if(".mp" in arquivo)
        );
        # Cria o arquivo zip
        with zipfile.ZipFile(arquivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipar:
            for arquivo in arquivos:
                zipar.write(f"{pasta}/{arquivo}",arquivo);
                self.__remover_arquivo(f"{pasta}/{arquivo}");
        self.__remover_pasta(pasta);
    
    @staticmethod
    async def __execute_coroutines(tasks:list,max:int = 10) -> NoReturn:
        dltasks = set();
        for task in tasks:
            if(len(dltasks) >= max):
                _done, dltasks = await asyncio.wait(
                    dltasks, 
                    return_when=asyncio.FIRST_COMPLETED
                );
            dltasks.add(asyncio.create_task(task));
        await asyncio.wait(dltasks);
    
    async def baixar_playlist_videos(self,link:str) -> str:
        retorno:str = None,None;
        # Pegar a playlist
        [playlist,titulo] = await self.__pegar_playlist(link);
        playlist: Playlist;
        titulo  : str;
        if((not titulo)or(not playlist)):
            return retorno;
        # Cria o caminho dos arquivos
        pasta_primaria:str = f"./data/playlist/video/{self.data()}";
        arquivo_zip   :str = f'{pasta_primaria}/{titulo}.zip';
        pasta         :str = f"{pasta_primaria}/{titulo}";
        # Cria as sub-rotinas
        tasks = (
            self.baixar_video(video,pasta)
            for video in playlist.video_urls
        )
        # Executa as sub-rotinas
        await self.__execute_coroutines(tasks);
        # Zipar os arquivos
        self.__zipar_playlist(pasta,arquivo_zip);
        return titulo,arquivo_zip;
    
    async def baixar_playlist_musicas(self,link:str) -> str:
        retorno:str = None,None;
        # Pegar a playlist
        [playlist,titulo] = await self.__pegar_playlist(link);
        playlist: Playlist;
        titulo  : str;
        if((not titulo)or(not playlist)):
            return retorno;
        # Cria o caminho dos arquivos
        pasta_primaria:str = f"./data/playlist/music/{self.data()}";
        arquivo_zip   :str = f'{pasta_primaria}/{titulo}.zip';
        pasta         :str = f"{pasta_primaria}/{titulo}";
        # Cria as sub-rotinas
        tasks = (
            self.baixar_musica(video,pasta)
            for video in playlist.video_urls
        )
        # Executa as sub-rotinas
        await self.__execute_coroutines(tasks);
        # Zipar os arquivos
        self.__zipar_playlist(pasta,arquivo_zip);
        return titulo,arquivo_zip;
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
#-----------------------