#-----------------------
# BIBLIOTECAS
#-----------------------
import os
import re
import zipfile
from time import sleep
import concurrent.futures
import moviepy.editor as mp
from datetime import datetime
from src.tools.tools import to_async
from pytube import Playlist, YouTube
from typing import Coroutine, Any
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
    
    def remover(self,caminho_do_arquivo:str) -> None:
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
    def __remover_arquivo(caminho_do_arquivo:str) -> None:
        """Remover Arquivo

        Neste método iremos remover o arquivo baixado anteriormente.
        
        Args:
            caminho_do_arquivo (str): Caminho do arquivo baixado.
        """
        if(os.path.exists(caminho_do_arquivo)):
            os.remove(caminho_do_arquivo);
    
    @staticmethod
    def __remover_pasta(caminho_da_pasta:str) -> None:
        """Remover Pasta

        Neste método iremos remover uma pasta criada anteriormente.
        
        Args:
            caminho_do_arquivo (str): Caminho do arquivo baixado.
        """
        if(os.path.exists(caminho_da_pasta)):
            os.rmdir(caminho_da_pasta);
    
    def __pegar_video(self,url:str) -> tuple[YouTube,str]:
        """Pegar Video

        Args:
            url (str): Aqui deve conter o url do video do YouTube
            a ser baixado.

        Returns:
            Union[YouTube,str,None]: Aqui retornaremos o video e o 
            titulo do video
        """
        # Retorno padrão
        retorno:list = [None,None];
        # Verificar se é playlist
        verificado = re.findall(
            r"(/watch\?v=[\w-]*)|(/youtu.be/)",
            url
        );
        if(not verificado):
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
    
    @to_async(executor=None)
    def baixar_video(self,url:str,pasta:str=None) -> Coroutine[Any,Any,tuple[str,str]]:
        """Baixar Video

        Args:
            url (str): Aqui deve conter o url do video do YouTube
            a ser baixado.

        Returns:
            List[str|None]: Aqui retornaremos em primeiro o título do 
            video e por segundo o seu caminho ou Nulo.
        """
        return self.__baixar_video(url=url,pasta=pasta);
    
    def __baixar_video(self,url:str,pasta:str=None) -> tuple[str,str]:
        """Baixar Video

        Args:
            url (str): Aqui deve conter o url do video do YouTube
            a ser baixado.

        Returns:
            List[str|None]: Aqui retornaremos em primeiro o título do 
            video e por segundo o seu caminho ou Nulo.
        """
        # Verifica se precisa por em uma pasta especifica.
        if(not pasta):
            pasta = f"./data/video/{self.data()}";
        # Pega o video do YouTube
        [youtube,titulo] = self.__pegar_video(url);
        youtube: YouTube;
        titulo : str;
        # Baixa o video
        caminho_video = youtube.download(pasta);
        
        return titulo,caminho_video;
    
    @to_async(executor=None)
    def baixar_musica(self,url:str,pasta:str=None) -> Coroutine[Any,Any,tuple[str,str]]:
        """Baixar música

        Args:
            url (str): Aqui deve conter o url da música do YouTube
            a ser baixado.

        Returns:
            List[str|None]: Aqui retornaremos em primeiro o título da 
            música e por segundo o seu caminho ou Nulo.
        """
        return self.__baixar_musica(url=url,pasta=pasta);
    
    def __baixar_musica(self,url:str,pasta:str=None) -> tuple[str,str]:
        """Baixar música

        Args:
            url (str): Aqui deve conter o url da música do YouTube
            a ser baixado.

        Returns:
            List[str|None]: Aqui retornaremos em primeiro o título da 
            música e por segundo o seu caminho ou Nulo.
        """
        # Verifica se precisa por em uma pasta especifica.
        if(not pasta):
            pasta = f"./data/music/{self.data()}";
        # Pega o video do YouTube
        [youtube,titulo] = self.__pegar_video(url);
        youtube: YouTube;
        titulo : str;
        # Baixa o video
        caminho_video = youtube.download(pasta);
        # Transforma em música
        caminho_musica = self.__converter_para_mp3(caminho_video);
        
        return titulo,caminho_musica;
    
    def __converter_para_mp3(self,arq_video:str) -> str:
        """Converter video para música

        Args:
            arq_video (str): Caminho para o arquivo de video.

        Returns:
            str: Caminho para o arquivo de audio.
        """
        name, _ = os.path.splitext(arq_video);
        out_name = name + ".mp3";
        
        with mp.AudioFileClip(arq_video) as audioclip:
            audioclip.write_audiofile(out_name,logger=None);
        
        self.__remover_arquivo(arq_video);
        return out_name;
    
    def __pegar_playlist(self,url:str) -> tuple[str,str]:
        """Pegar Video

        Args:
            url (str): Aqui deve conter o url da playlist do YouTube
            a ser baixado.

        Returns:
            Union[YouTube,str,None]: Aqui retornaremos a playlist e o 
            titulo da playlist.
        """
        # Retorno padrão
        retorno:list = [None,None];
        # Verificar se é playlist
        verificado = re.findall(
            r"(/playlist\?list=[\w-]*)",
            url
        );
        if(not verificado):
            return retorno;
        # Pegar a playlist
        playlist   = Playlist(url);
        titulo:str = playlist.title;
        
        return playlist,titulo;
    
    def __zipar_playlist(self,pasta:str,arquivo_zip:str) -> None:
        """Zipar Playlist

        Args:
            pasta (str): Pasta para ser zipada.
            arquivo_zip (str): Nome do arquivo a ser zipada.

        Returns:
            NoReturn: Não retorna nada.
        """
        # Pega os arquivos
        arquivos = (
            arquivo
            for _, _, arquivos in os.walk(os.path.abspath(pasta))
                for arquivo in arquivos
                    if(".mp3" in arquivo or ".mp4" in arquivo)
        );
        # Cria o arquivo zip
        tipo = zipfile.ZIP_DEFLATED;
        with zipfile.ZipFile(arquivo_zip, 'w', tipo) as zipar:
            for arquivo in arquivos:
                zipar.write(f"{pasta}/{arquivo}",arquivo);
                self.__remover_arquivo(f"{pasta}/{arquivo}");
        self.__remover_pasta(pasta);
    
    @to_async(executor=None)
    def baixar_playlist_videos(self,url:str) -> Coroutine[Any,Any,tuple[str,str]]:
        """Baixar Playlist de Videos

        Args:
            url (str): Aqui deve conter o url da playlist do YouTube
            a ser baixado.

        Returns:
            List[Union[str,None]]: Aqui retornaremos em 
            primeiro o título da da playlist e por 
            segundo o seu caminho ou Nulo.
        """
        retorno:str = None,None;
        # Pegar a playlist
        [playlist,titulo] = self.__pegar_playlist(url);
        playlist: Playlist;
        titulo  : str;
        if((not titulo)or(not playlist)):
            return retorno;
        # Cria o caminho dos arquivos
        pasta_primaria:str = f"./data/playlist/video/{self.data()}";
        arquivo_zip   :str = f'{pasta_primaria}/{titulo}.zip';
        pasta         :str = f"{pasta_primaria}/{titulo}";
        # Cria as sub-rotinas
        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = (
                executor.submit(
                    self.__baixar_video,
                    video,
                    pasta
                )
                for video in playlist.video_urls
            )
            for _ in concurrent.futures.as_completed(tasks):
                pass;
        # Zipar os arquivos
        self.__zipar_playlist(pasta,arquivo_zip);
        return titulo,arquivo_zip;
    
    @to_async(executor=None)
    def baixar_playlist_musicas(self,url:str) -> Coroutine[Any,Any,tuple[str,str]]:
        """Baixar Playlist de Música

        Args:
            url (str): Aqui deve conter o url da playlist do YouTube
            a ser baixado.

        Returns:
            List[Union[str,None]]: Aqui retornaremos em 
            primeiro o título da da playlist e por 
            segundo o seu caminho ou Nulo.
        """
        retorno:str = None,None;
        # Pegar a playlist
        [playlist,titulo] = self.__pegar_playlist(url);
        playlist: Playlist;
        titulo  : str;
        if((not titulo)or(not playlist)):
            return retorno;
        # Cria o caminho dos arquivos
        pasta_primaria:str = f"./data/playlist/music/{self.data()}";
        arquivo_zip   :str = f'{pasta_primaria}/{titulo}.zip';
        pasta         :str = f"{pasta_primaria}/{titulo}";
        # Baixa os videos
        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = (
                executor.submit(self.__baixar_video,video,pasta)
                for video in playlist.video_urls
            )
            for _ in concurrent.futures.as_completed(tasks):
                pass;
        # Pega os videos
        videos = (
            f"{pasta}/{arquivo}"
            for _, _, arquivos in os.walk(os.path.abspath(pasta))
                for arquivo in arquivos
                    if(".mp4" in arquivo)
        );
        # Transforma em MP3
        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = (
                executor.submit(self.__converter_para_mp3,video)
                for video in videos
            )
            for _ in concurrent.futures.as_completed(tasks):
                pass;
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