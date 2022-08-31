""""""
#-----------------------
# BIBLIOTECAS
#-----------------------
from fastapi.responses import ( 
    FileResponse
)
from fastapi import (
    APIRouter, BackgroundTasks, status, HTTPException
)
from src.jobs.download_youtube import DownloadYouTube
#-----------------------
# CONSTANTES
#-----------------------
router = APIRouter(prefix="/youtube");
download_youtube = DownloadYouTube();
#-----------------------
# CLASSES
#-----------------------
#-----------------------
# FUNÇÕES()
#-----------------------
@router.get(
    "/download/video/",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    tags=["Video"]
)
async def download_video(
    link:str,
    background_tasks: BackgroundTasks
):
    """Baixar o video

    Args:
        link (str): Deve ser um link existente no youtube.
    Returns:
        MP4: retorna o video.
    """
    try:
        nome,arquivo = await download_youtube.baixar_video(link);
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );
    if((not nome)or(not arquivo)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Requisição incorreta"
    );
    try:
        retorno = FileResponse(
            arquivo,
            media_type=".mp4",
            filename=f"{nome}.mp4"
        );
        background_tasks.add_task(
            download_youtube.remover,
            arquivo
        );
        return retorno;
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );

@router.get(
    "/download/musica/",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    tags=["Música"]
)
async def download_musica(
    link:str,
    background_tasks: BackgroundTasks
):
    try:
        nome,arquivo = await download_youtube.baixar_musica(link);
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );
    if((not nome)or(not arquivo)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Requisição incorreta"
    );
    try:
        retorno = FileResponse(
            arquivo,
            media_type=".mp3",
            filename=f"{nome}.mp3"
        );
        background_tasks.add_task(
            download_youtube.remover,
            arquivo
        );
        return retorno;
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );

@router.get(
    "/download/video/playlist/",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    tags=["Playlist","Video"]
)
async def download_playlist_videos(
    link:str,
    background_tasks: BackgroundTasks
):
    try:
        nome,arquivo = await download_youtube.baixar_playlist_videos(link);
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );
    if((not nome)or(not arquivo)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Requisição incorreta"
    );
    try:
        retorno = FileResponse(
            arquivo,
            media_type=".zip",
            filename=f"{nome}.zip"
        );
        background_tasks.add_task(
            download_youtube.remover,arquivo
        );
        return retorno;
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );

@router.get(
    "/download/musica/playlist/",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    tags=["Playlist","Música"]
)
async def download_playlist_musicas(
    link:str,
    background_tasks: BackgroundTasks
):
    try:
        
        nome,arquivo = await download_youtube.baixar_playlist_musicas(link);
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );
    if((not nome)or(not arquivo)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Requisição incorreta"
    );
    try:
        retorno = FileResponse(
            arquivo,
            media_type=".zip",
            filename=f"{nome}.zip"
        );
        background_tasks.add_task(
            download_youtube.remover,
            arquivo
        );
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