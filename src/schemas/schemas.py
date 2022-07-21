"""Schema"""
#-----------------------
# BIBLIOTECAS
#-----------------------
from pydantic import BaseModel
from typing import Optional, List
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
# **************
# Schema Retorno
# **************
class ProdutoRetorno(BaseModel):
    """Produto Retorno - Schema
    
    Neste schema nós criamos todos os dados 
    necessários para a criação de um produto
    no nosso programa.
    """
    nome      : str;
    detalhes  : str;
    preco     : float;
    disponivel: bool = False;
    tamanhos  : Optional[str] = "Não informado";
    
    class Config:
        orm_mode = True;

class PedidoRetorno(BaseModel):
    """Pedido Retorno - Schema
    
    Neste schema nós criamos todos os dados 
    necessários para a criação de um pedido
    no nosso programa.
    """
    id         : Optional[int] = None;
    quantidade : int;
    entrega    : bool = False;
    endereco   : str;
    observacoes: Optional[str] = "Sem observações";
    produto    : Optional[ProdutoRetorno] = None;
    
    class Config:
        orm_mode = True;
# **************
# Schema Simples
# **************
class UsuarioSimples(BaseModel):
    """Usuário Simples - Schema
    
    Neste schema nós criamos todos os dados 
    necessários para a criação de um usuários 
    no nosso programa.
    """
    id      : Optional[int] = None;
    nome    : str;
    telefone: str;

    class Config:
        orm_mode = True;

class ProdutoSimples(BaseModel):
    """Produto Simples - Schema
    
    Neste schema nós criamos todos os dados 
    necessários para a criação de um produto
    no nosso programa.
    """
    id        : Optional[int] = None;
    nome      : str;
    detalhes  : str;
    preco     : float;
    disponivel: bool = False;
    tamanhos  : Optional[str] = "Não informado";
    
    class Config:
        orm_mode = True;

class PedidoSimples(BaseModel):
    """Pedido Simples - Schema
    
    Neste schema nós criamos todos os dados 
    necessários para a criação de um pedido
    no nosso programa.
    """
    id         : Optional[int] = None;
    quantidade : int;
    entrega    : bool = False;
    endereco   : str;
    observacoes: Optional[str] = "Sem observações";

    class Config:
        orm_mode = True;
# **************
# Schema Completo
# **************
class Usuario(BaseModel):
    """Usuário - Schema
    
    Neste schema nós criamos todos os dados 
    necessários para a criação de um usuários 
    no nosso programa.
    """
    id      : Optional[int] = None;
    nome    : str;
    telefone: str;
    senha   : str;
    produtos: Optional[List[ProdutoSimples]] = None;
    pedidos : Optional[List[PedidoSimples]]  = None;

    class Config:
        orm_mode = True;

class Produto(BaseModel):
    """Produto - Schema
    
    Neste schema nós criamos todos os dados 
    necessários para a criação de um produto
    no nosso programa.
    """
    id        : Optional[int] = None;
    nome      : str;
    detalhes  : str;
    preco     : float;
    disponivel: bool = False;
    tamanhos  : Optional[str] = "Não informado";
    usuario_id: Optional[int] = None;
    usuario   : Optional[UsuarioSimples] = None;
    
    class Config:
        orm_mode = True;

class Pedido(BaseModel):
    """Pedido - Schema
    
    Neste schema nós criamos todos os dados 
    necessários para a criação de um pedido
    no nosso programa.
    """
    id         : Optional[int] = None;
    quantidade : int;
    entrega    : bool = False;
    endereco   : str;
    observacoes: Optional[str] = "Sem observações";
    usuario_id : Optional[int] = None;
    usuario    : Optional[UsuarioSimples] = None;
    produto_id : Optional[int] = None;
    produto    : Optional[Produto] = None;

    class Config:
        orm_mode = True;
# **************
# Schema Login
# **************
class LoginData(BaseModel):
    """Login - Schema
    
    Neste schema nós criamos todos os dados 
    necessários para o login
    no nosso programa.
    """
    senha   : str;
    telefone: str;

class LoginSucesso(BaseModel):
    """Token do Usuário - Schema
    
    Neste schema nós colocaremos o 
    token de acesso do usuário.
    """
    usuario     : UsuarioSimples;
    access_token: str;
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
#-----------------------