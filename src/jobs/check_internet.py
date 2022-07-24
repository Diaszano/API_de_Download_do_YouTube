"""Checador de internet

Este módulo contêm o verificador de internet.
"""
#-----------------------
# BIBLIOTECAS
#-----------------------
import re
import requests
from typing import List, Union
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
class CheckInternet:
    """Checador de internet
    
    Esta classe tem o intuito de verificar
    se está com internet ou não.
    """
    def __compile_re(self) -> None:
        """Compilador regex
        
        Aqui nós compilaremos todos os 
        regex utilizados nessa classe.
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
        """Checador de internet
    
        Está classe tem o intuito de verificar
        se está com internet ou não.
        """
        self.__compile_re();
        self.__MIN:int = 1;
        self.__MAX:int = 100;
        self.__URL:str = r'https://www.google.com/';
    
    def pegar_url(self,url:str) -> Union[str,None]:
        """Pegar URL
        
        Aqui nós verificaremos se existe uma URL na string
        passada.

        Args:
            url (str): aqui deverá vir a string com 
            a URL de um site existente.

        Returns:
            Union[str,None]: retorna a URL se ela for 
            verdadeira ou senão None.
        """
        list_url = self.__regex_url.findall(url);
        if(list_url):
            return list_url[0][0];
    
    def verificar_link(self,url:str) -> bool:
        """Verificar Link
        
        Aqui nós verificaremos se tem conexão com a 
        URL passada.

        Args:
            url (str): aqui deverá vir a string com 
            a URL de um site existente.

        Returns:
            bool: Se tiver conexão ele irá retornar 
            True, mas caso contrario irá retornar False.
        """
        url = self.pegar_url(url);
        if(not url):
            return False;
        return self.__requisicao(url);
    
    def verificar_sync(self) -> bool:
        try:
            response = requests.get(self.__URL);
            return True;
        except:
            return False;
    
    def verificar(self,quantidade:int = 10) -> bool:
        """Verificar conexão
        
        Verificação de conexão com internet.

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
        lista = (
            req 
            for req in tasks
        );
        return self.__verificar_media(lista);
    
    @staticmethod
    def __requisicao(url:str) -> bool:
        """Requisição

        Aqui faremos a requisição para um site determinado
        e verificaremos se ele irá retornar algo.
        
        Args:
            url (str): aqui deverá vir a string com 
            a URL de um site existente.
        
        Returns:
            bool: retornamos True se tiver conexão com o site e
            False se não tiver.
        """
        try:
            response = requests.get(url);
            return True;
        except:
            return False;
    
    @staticmethod
    def __verificar_media(lista:List[bool]) -> bool:
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
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
#-----------------------