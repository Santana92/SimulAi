from sqlalchemy import (
    Column, String, Integer, Text, ForeignKey, TIMESTAMP,
    DECIMAL, BOOLEAN, JSON, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

class Professor(Base):
    __tablename__ = 'professores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    materias = relationship("Materia", back_populates="professor", cascade="all, delete-orphan")

class Materia(Base):
    __tablename__ = 'materias'
    id = Column(Integer, primary_key=True, autoincrement=True)
    professor_id = Column(Integer, ForeignKey('professores.id', ondelete='CASCADE'), nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    senha_acesso = Column(String(50), nullable=False)
    texto_base = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    ativa = Column(BOOLEAN, default=True)
    
    professor = relationship("Professor", back_populates="materias")
    inscricoes = relationship("Inscricao", back_populates="materia", cascade="all, delete-orphan")
    avaliacoes = relationship("Avaliacao", back_populates="materia", cascade="all, delete-orphan")
    questoes = relationship("Questao", back_populates="materia", cascade="all, delete-orphan")

class Aluno(Base):
    __tablename__ = 'alunos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ra = Column(String(20), unique=True, nullable=False)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    inscricoes = relationship("Inscricao", back_populates="aluno", cascade="all, delete-orphan")
    respostas = relationship("RespostaAluno", back_populates="aluno", cascade="all, delete-orphan")
    desempenhos = relationship("Desempenho", back_populates="aluno", cascade="all, delete-orphan")

class Inscricao(Base):
    __tablename__ = 'inscricoes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id', ondelete='CASCADE'), nullable=False)
    materia_id = Column(Integer, ForeignKey('materias.id', ondelete='CASCADE'), nullable=False)
    data_inscricao = Column(TIMESTAMP, server_default=func.now())
    
    aluno = relationship("Aluno", back_populates="inscricoes")
    materia = relationship("Materia", back_populates="inscricoes")
    
    __table_args__ = (UniqueConstraint('aluno_id', 'materia_id', name='_aluno_materia_uc'),)

class Questao(Base):
    __tablename__ = 'questoes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    materia_id = Column(Integer, ForeignKey('materias.id', ondelete='CASCADE'), nullable=False)
    pergunta = Column(Text, nullable=False)
    tipo = Column(String(20), default='multipla_escolha')
    opcoes = Column(JSONB)
    resposta_correta = Column(String(10), nullable=False)
    nivel_dificuldade = Column(String(20), default='medio')
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    materia = relationship("Materia", back_populates="questoes")
    respostas_aluno = relationship("RespostaAluno", back_populates="questao", cascade="all, delete-orphan")

class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    materia_id = Column(Integer, ForeignKey('materias.id', ondelete='CASCADE'), nullable=False)
    titulo = Column(String(100), nullable=False)
    descricao = Column(Text)
    quantidade_questoes = Column(Integer, default=10)
    tempo_limite = Column(Integer) # em minutos
    disponivel_ate = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    materia = relationship("Materia", back_populates="avaliacoes")
    respostas_aluno = relationship("RespostaAluno", back_populates="avaliacao", cascade="all, delete-orphan")
    desempenhos = relationship("Desempenho", back_populates="avaliacao", cascade="all, delete-orphan")

class RespostaAluno(Base):
    __tablename__ = 'respostas_alunos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id', ondelete='CASCADE'), nullable=False)
    questao_id = Column(Integer, ForeignKey('questoes.id', ondelete='CASCADE'), nullable=False)
    avaliacao_id = Column(Integer, ForeignKey('avaliacoes.id', ondelete='CASCADE'), nullable=False)
    resposta_aluno = Column(String(500), nullable=False)
    correta = Column(BOOLEAN, default=False)
    nota = Column(DECIMAL(5, 2), default=0)
    feedback_ia = Column(Text)
    tempo_resposta = Column(Integer) # em segundos
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    aluno = relationship("Aluno", back_populates="respostas")
    questao = relationship("Questao", back_populates="respostas_aluno")
    avaliacao = relationship("Avaliacao", back_populates="respostas_aluno")

class Desempenho(Base):
    __tablename__ = 'desempenho'
    id = Column(Integer, primary_key=True, autoincrement=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id', ondelete='CASCADE'), nullable=False)
    avaliacao_id = Column(Integer, ForeignKey('avaliacoes.id', ondelete='CASCADE'), nullable=False)
    materia_id = Column(Integer, ForeignKey('materias.id', ondelete='CASCADE'), nullable=False)
    total_questoes = Column(Integer, default=0)
    acertos = Column(Integer, default=0)
    nota_final = Column(DECIMAL(5, 2), default=0)
    tempo_total = Column(Integer, default=0) # em segundos
    data_conclusao = Column(TIMESTAMP, server_default=func.now())

    aluno = relationship("Aluno", back_populates="desempenhos")
    avaliacao = relationship("Avaliacao", back_populates="desempenhos")