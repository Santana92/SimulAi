from sqlalchemy import Column, String, ForeignKey, Float, Text, Integer, BOOLEAN
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ra = Column(String(20), unique=True, nullable=True)  # RA para alunos
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)
    tipo_usuario = Column(String(10), nullable=False, default='aluno')  # 'aluno' ou 'professor'
    avatar_url = Column(String(255), nullable=True) # URL para a foto do usuário

    materias_criadas = relationship("Materia", back_populates="professor")
    respostas = relationship("RespostaAluno", back_populates="aluno")
    desempenhos = relationship("DesempenhoSimulado", back_populates="aluno")
    matriculas = relationship("Matricula", back_populates="aluno")


class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    id_professor = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    chave_inscricao = Column(String(50), nullable=False)

    professor = relationship("Usuario", back_populates="materias_criadas")
    simulados = relationship("Simulado", back_populates="materia", cascade="all, delete-orphan")
    matriculas = relationship("Matricula", back_populates="materia", cascade="all, delete-orphan")


class Matricula(Base):
    __tablename__ = "matriculas"

    id_aluno = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    id_materia = Column(Integer, ForeignKey("materias.id"), primary_key=True)

    aluno = relationship("Usuario", back_populates="matriculas")
    materia = relationship("Materia", back_populates="matriculas")


class Simulado(Base):
    __tablename__ = "simulados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_materia = Column(Integer, ForeignKey("materias.id"), nullable=False)
    titulo = Column(String(150), nullable=False)
    texto_base = Column(Text, nullable=True)

    materia = relationship("Materia", back_populates="simulados")
    questoes = relationship("Questao", back_populates="simulado", cascade="all, delete-orphan")
    desempenhos = relationship("DesempenhoSimulado", back_populates="simulado", cascade="all, delete-orphan")


class Questao(Base):
    __tablename__ = "questoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_simulado = Column(Integer, ForeignKey("simulados.id"), nullable=False)
    enunciado = Column(Text, nullable=False)
    resposta_correta = Column(Text, nullable=True)  # Gabarito para a IA

    simulado = relationship("Simulado", back_populates="questoes")
    respostas = relationship("RespostaAluno", back_populates="questao", cascade="all, delete-orphan")


class RespostaAluno(Base):
    __tablename__ = "respostas_alunos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_aluno = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_questao = Column(Integer, ForeignKey("questoes.id"), nullable=False)
    resposta_aluno = Column(Text, nullable=False)
    correta = Column(BOOLEAN, nullable=True)
    feedback = Column(Text, nullable=True)

    aluno = relationship("Usuario", back_populates="respostas")
    questao = relationship("Questao", back_populates="respostas")


class DesempenhoSimulado(Base):
    __tablename__ = "desempenho_simulados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_aluno = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_simulado = Column(Integer, ForeignKey("simulados.id"), nullable=False)
    nota = Column(Float, nullable=True)

    aluno = relationship("Usuario", back_populates="desempenhos")
    simulado = relationship("Simulado", back_populates="desempenhos")
