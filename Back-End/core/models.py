import uuid
from sqlalchemy import Column, String, ForeignKey, Float, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=True)  # Senha pode ser nula para logins com Google
    tipo = Column(String, nullable=False, default="aluno") # 'aluno' ou 'professor'

    resultados = relationship("Resultado", back_populates="usuario")

class Materia(Base):
    __tablename__ = "materias"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, unique=True, nullable=False)

    simulados = relationship("Simulado", back_populates="materia")

class Simulado(Base):
    __tablename__ = "simulados"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(String, nullable=False)
    materia_id = Column(UUID(as_uuid=True), ForeignKey("materias.id"), nullable=False)
    
    # Armazenaremos a estrutura complexa das questões como um JSON.
    # Isso simplifica o modelo e é eficiente em PostgreSQL.
    questoes = Column(JSON, nullable=False)

    materia = relationship("Materia", back_populates="simulados")
    resultados = relationship("Resultado", back_populates="simulado")

class Resultado(Base):
    __tablename__ = "resultados"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    simulado_id = Column(UUID(as_uuid=True), ForeignKey("simulados.id"), nullable=False)
    
    usuario_nome = Column(String, nullable=False) # Mantido para facilitar a exibição
    nota = Column(Float, nullable=False)
    
    # Armazena as respostas do usuário, por exemplo: {"1": "a", "2": "c"}
    respostas = Column(JSON, nullable=False)

    usuario = relationship("Usuario", back_populates="resultados")
    simulado = relationship("Simulado", back_populates="resultados")
