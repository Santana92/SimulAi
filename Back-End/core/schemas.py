from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Shared
class Message(BaseModel):
    message: str

# Professores
class ProfessorBase(BaseModel):
    nome: str
    email: EmailStr

class ProfessorCreate(ProfessorBase):
    senha: str

class ProfessorResponse(ProfessorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Alunos
class AlunoBase(BaseModel):
    ra: str
    nome: str
    email: EmailStr

class AlunoCreate(AlunoBase):
    senha: str

class AlunoResponse(AlunoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Matérias
class MateriaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    senha_acesso: str
    texto_base: str
    ativa: Optional[bool] = True

class MateriaCreate(MateriaBase):
    pass

class MateriaResponse(MateriaBase):
    id: int
    professor_id: int
    created_at: datetime
    # Relacionamentos
    professor: Optional[ProfessorResponse] = None # Para incluir dados do professor
    questoes: List["QuestaoResponse"] = [] # Forward Ref
    inscricoes: List["InscricaoResponse"] = [] # Forward Ref
    avaliacoes: List["AvaliacaoResponse"] = [] # Forward Ref

    class Config:
        from_attributes = True

# Inscrições (Relacionamento Aluno-Matéria)
class InscricaoBase(BaseModel):
    aluno_id: int
    materia_id: int

class InscricaoCreate(InscricaoBase):
    pass

class InscricaoResponse(InscricaoBase):
    id: int
    data_inscricao: datetime
    aluno: Optional[AlunoResponse] = None
    materia: Optional[MateriaResponse] = None

    class Config:
        from_attributes = True

# Questões
class QuestaoBase(BaseModel):
    materia_id: int
    pergunta: str
    tipo: Optional[str] = "multipla_escolha"
    opcoes: Optional[dict] = None # {"A": "Opção A", "B": "Opção B", ...}
    resposta_correta: str
    nivel_dificuldade: Optional[str] = "medio"

class QuestaoCreate(QuestaoBase):
    pass

class QuestaoResponse(QuestaoBase):
    id: int
    created_at: datetime
    # materia: Optional[MateriaResponse] = None # Evitar recursão excessiva
    respostas_aluno: List["RespostaAlunoResponse"] = [] # Forward Ref

    class Config:
        from_attributes = True

# Avaliações (Sessões de Prova)
class AvaliacaoBase(BaseModel):
    materia_id: int
    titulo: str
    descricao: Optional[str] = None
    quantidade_questoes: Optional[int] = 10
    tempo_limite: Optional[int] = None # em minutos
    disponivel_ate: Optional[datetime] = None

class AvaliacaoCreate(AvaliacaoBase):
    pass

class AvaliacaoResponse(AvaliacaoBase):
    id: int
    created_at: datetime
    # materia: Optional[MateriaResponse] = None # Evitar recursão excessiva
    respostas_aluno: List["RespostaAlunoResponse"] = [] # Forward Ref
    desempenhos: List["DesempenhoResponse"] = [] # Forward Ref

    class Config:
        from_attributes = True

# Respostas dos Alunos
class RespostaAlunoBase(BaseModel):
    aluno_id: int
    questao_id: int
    avaliacao_id: int
    resposta_aluno: str
    correta: Optional[bool] = False
    nota: Optional[float] = 0.0
    feedback_ia: Optional[str] = None
    tempo_resposta: Optional[int] = None # em segundos

class RespostaAlunoCreate(RespostaAlunoBase):
    pass

class RespostaAlunoResponse(RespostaAlunoBase):
    id: int
    created_at: datetime
    # aluno: Optional[AlunoResponse] = None # Evitar recursão
    # questao: Optional[QuestaoResponse] = None
    # avaliacao: Optional[AvaliacaoResponse] = None

    class Config:
        from_attributes = True

# Desempenho (Resumo por Avaliação)
class DesempenhoBase(BaseModel):
    aluno_id: int
    avaliacao_id: int
    materia_id: int
    total_questoes: Optional[int] = 0
    acertos: Optional[int] = 0
    nota_final: Optional[float] = 0.0
    tempo_total: Optional[int] = 0 # em segundos

class DesempenhoCreate(DesempenhoBase):
    pass

class DesempenhoResponse(DesempenhoBase):
    id: int
    data_conclusao: datetime
    # aluno: Optional[AlunoResponse] = None
    # avaliacao: Optional[AvaliacaoResponse] = None
    # materia: Optional[MateriaResponse] = None

    class Config:
        from_attributes = True

# Forward references for relationships to avoid circular imports during definition
MateriaResponse.model_rebuild()
QuestaoResponse.model_rebuild()
AvaliacaoResponse.model_rebuild()
InscricaoResponse.model_rebuild()
RespostaAlunoResponse.model_rebuild()
DesempenhoResponse.model_rebuild()

# JWT
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_type: Optional[str] = None # 'aluno' ou 'professor'

# Report Schemas
class RelatorioGeralTurma(BaseModel):
    materia: str
    total_alunos: int
    media_turma: Optional[float] = None
    maior_nota: Optional[float] = None
    menor_nota: Optional[float] = None

    class Config:
        from_attributes = True

class DesempenhoIndividualAluno(BaseModel):
    aluno: str
    ra: str
    nota_final: Optional[float] = None
    acertos: Optional[int] = None
    total_questoes: Optional[int] = None
    percentual_acerto: Optional[float] = None

    class Config:
        from_attributes = True
