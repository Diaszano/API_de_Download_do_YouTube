""""""
#-----------------------
# BIBLIOTECAS
#-----------------------
from typing import List
from fastapi.responses import (
    StreamingResponse, FileResponse
)
from fastapi import (
    APIRouter, BackgroundTasks, status, HTTPException
)
from src.jobs.download_youtube import DownloadYouTube
#-----------------------
# CONSTANTES
#-----------------------
router = APIRouter(prefix="/youtube");
#-----------------------
# CLASSES
#-----------------------
#-----------------------
# FUNÇÕES()
#-----------------------
@router.get("/download/video/",response_class=FileResponse,status_code=status.HTTP_200_OK,tags=["Baixar"])
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
        background_tasks.add_task(DownloadYouTube().remover,arquivo);
        return retorno;
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );

@router.get("/download/musica/",response_class=FileResponse,status_code=status.HTTP_200_OK,tags=["Baixar"])
async def download_musica(link:str,background_tasks: BackgroundTasks):
    """Baixar a música

    Args:
        link (str): Deve ser um link existente no youtube.
    Returns:
        MP4: retorna a música.
    """
    try:
        nome,arquivo = await DownloadYouTube().baixar_musica(link);
        retorno = FileResponse(arquivo,media_type=".mp3",filename=f"{nome}.mp3");
        background_tasks.add_task(DownloadYouTube().remover,arquivo);
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