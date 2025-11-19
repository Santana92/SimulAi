from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
import uuid

# --- Schemas Base ---
# Usado para dados que vêm do cliente na criação

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: Optional[str] = None
    tipo: str

class LoginData(BaseModel):
    email: EmailStr
    senha: str

class GoogleAuthCode(BaseModel):
    code: str

class MateriaCreate(BaseModel):
    nome: str

class ResultadoCreate(BaseModel):
    usuario_id: uuid.UUID
    usuario_nome: str
    nota: float
    respostas: Dict[str, str]

# --- Schemas Completos ---
# Usado para dados que são retornados pela API

class OpcoesQuestao(BaseModel):
    a: str
    b: str
    c: str
    d: str
    e: str

class ExplicacoesQuestao(BaseModel):
    a: str
    b: str
    c: str
    d: str
    e: str

class Questao(BaseModel):
    id: int
    pergunta: str
    opcoes: OpcoesQuestao
    correta: str
    explicacoes: ExplicacoesQuestao

class SimuladoCompleto(BaseModel):
    id: uuid.UUID
    titulo: str
    questoes: List[Questao]

    class Config:
        orm_mode = True

class SimuladoInfo(BaseModel):
    id: uuid.UUID
    nome: str

    class Config:
        orm_mode = True

class Materia(BaseModel):
    id: uuid.UUID
    nome: str
    simulados: List[SimuladoInfo] = []

    class Config:
        orm_mode = True

class Usuario(BaseModel):
    id: uuid.UUID
    nome: str
    email: EmailStr
    tipo: str

    class Config:
        orm_mode = True

class Resultado(BaseModel):
    id: uuid.UUID
    usuario_id: uuid.UUID
    usuario_nome: str
    simulado_id: uuid.UUID
    nota: float
    respostas: Dict[str, str]

    class Config:
        orm_mode = True
