from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from . import models, schemas
from .security import get_password_hash # Importar a função de hash de senha

# --- Professor CRUD ---
def get_professor_by_email(db: Session, email: str):
    return db.query(models.Professor).filter(models.Professor.email == email).first()

def get_professor_by_id(db: Session, professor_id: int):
    return db.query(models.Professor).filter(models.Professor.id == professor_id).first()

def create_professor(db: Session, professor: schemas.ProfessorCreate):
    hashed_password = get_password_hash(professor.senha)
    db_professor = models.Professor(
        nome=professor.nome,
        email=professor.email,
        senha_hash=hashed_password
    )
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

# --- Aluno CRUD ---
def get_aluno_by_email(db: Session, email: str):
    return db.query(models.Aluno).filter(models.Aluno.email == email).first()

def get_aluno_by_ra(db: Session, ra: str):
    return db.query(models.Aluno).filter(models.Aluno.ra == ra).first()

def get_aluno_by_id(db: Session, aluno_id: int):
    return db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()

def create_aluno(db: Session, aluno: schemas.AlunoCreate):
    hashed_password = get_password_hash(aluno.senha)
    db_aluno = models.Aluno(
        ra=aluno.ra,
        nome=aluno.nome,
        email=aluno.email,
        senha_hash=hashed_password
    )
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

# --- Materia CRUD ---
def create_materia(db: Session, materia: schemas.MateriaCreate, professor_id: int):
    db_materia = models.Materia(
        **materia.model_dump(),
        professor_id=professor_id
    )
    db.add(db_materia)
    db.commit()
    db.refresh(db_materia)
    return db_materia

def get_materia_by_id(db: Session, materia_id: int):
    return db.query(models.Materia).filter(models.Materia.id == materia_id).first()

def get_materias_by_professor(db: Session, professor_id: int):
    return db.query(models.Materia).filter(models.Materia.professor_id == professor_id).all()

def get_materia_by_senha_acesso(db: Session, senha_acesso: str):
    return db.query(models.Materia).filter(models.Materia.senha_acesso == senha_acesso).first()

def update_materia(db: Session, materia_id: int, materia_update: schemas.MateriaCreate):
    db_materia = db.query(models.Materia).filter(models.Materia.id == materia_id).first()
    if db_materia:
        for key, value in materia_update.model_dump(exclude_unset=True).items():
            setattr(db_materia, key, value)
        db.commit()
        db.refresh(db_materia)
    return db_materia

def delete_materia(db: Session, materia_id: int):
    db_materia = db.query(models.Materia).filter(models.Materia.id == materia_id).first()
    if db_materia:
        db.delete(db_materia)
        db.commit()
    return db_materia

# --- Inscricao CRUD ---
def create_inscricao(db: Session, aluno_id: int, materia_id: int):
    db_inscricao = models.Inscricao(aluno_id=aluno_id, materia_id=materia_id)
    try:
        db.add(db_inscricao)
        db.commit()
        db.refresh(db_inscricao)
        return db_inscricao
    except IntegrityError:
        db.rollback()
        return None # Aluno já inscrito ou erro de integridade

def get_inscricao(db: Session, aluno_id: int, materia_id: int):
    return db.query(models.Inscricao).filter(
        models.Inscricao.aluno_id == aluno_id,
        models.Inscricao.materia_id == materia_id
    ).first()

def get_inscricoes_by_aluno(db: Session, aluno_id: int):
    return db.query(models.Inscricao).filter(models.Inscricao.aluno_id == aluno_id).all()

def get_inscricoes_by_materia(db: Session, materia_id: int):
    return db.query(models.Inscricao).filter(models.Inscricao.materia_id == materia_id).all()

# --- Questao CRUD ---
def create_questao(db: Session, questao: schemas.QuestaoCreate):
    db_questao = models.Questao(**questao.model_dump())
    db.add(db_questao)
    db.commit()
    db.refresh(db_questao)
    return db_questao

def get_questao_by_id(db: Session, questao_id: int):
    return db.query(models.Questao).filter(models.Questao.id == questao_id).first()

def get_questoes_by_materia(db: Session, materia_id: int):
    return db.query(models.Questao).filter(models.Questao.materia_id == materia_id).all()

def delete_questao(db: Session, questao_id: int):
    db_questao = db.query(models.Questao).filter(models.Questao.id == questao_id).first()
    if db_questao:
        db.delete(db_questao)
        db.commit()
    return db_questao

# --- Avaliacao CRUD ---
def create_avaliacao(db: Session, avaliacao: schemas.AvaliacaoCreate):
    db_avaliacao = models.Avaliacao(**avaliacao.model_dump())
    db.add(db_avaliacao)
    db.commit()
    db.refresh(db_avaliacao)
    return db_avaliacao

def get_avaliacao_by_id(db: Session, avaliacao_id: int):
    return db.query(models.Avaliacao).filter(models.Avaliacao.id == avaliacao_id).first()

def get_avaliacoes_by_materia(db: Session, materia_id: int):
    return db.query(models.Avaliacao).filter(models.Avaliacao.materia_id == materia_id).all()

def delete_avaliacao(db: Session, avaliacao_id: int):
    db_avaliacao = db.query(models.Avaliacao).filter(models.Avaliacao.id == avaliacao_id).first()
    if db_avaliacao:
        db.delete(db_avaliacao)
        db.commit()
    return db_avaliacao

# --- RespostaAluno CRUD ---
def create_resposta_aluno(db: Session, resposta: schemas.RespostaAlunoCreate):
    db_resposta = models.RespostaAluno(**resposta.model_dump())
    db.add(db_resposta)
    db.commit()
    db.refresh(db_resposta)
    return db_resposta

def get_respostas_by_aluno_and_avaliacao(db: Session, aluno_id: int, avaliacao_id: int):
    return db.query(models.RespostaAluno).filter(
        models.RespostaAluno.aluno_id == aluno_id,
        models.RespostaAluno.avaliacao_id == avaliacao_id
    ).all()

# --- Desempenho CRUD ---
def create_desempenho(db: Session, desempenho: schemas.DesempenhoCreate):
    db_desempenho = models.Desempenho(**desempenho.model_dump())
    db.add(db_desempenho)
    db.commit()
    db.refresh(db_desempenho)
    return db_desempenho

def get_desempenho_by_aluno_and_avaliacao(db: Session, aluno_id: int, avaliacao_id: int):
    return db.query(models.Desempenho).filter(
        models.Desempenho.aluno_id == aluno_id,
        models.Desempenho.avaliacao_id == avaliacao_id
    ).first()

# --- Relatórios para o Professor (baseados em etapa1.txt) ---
def get_relatorio_geral_turma(db: Session, materia_id: int):
    return db.query(
        models.Materia.nome.label("materia"),
        sa.func.count(sa.distinct(models.Inscricao.aluno_id)).label("total_alunos"),
        sa.func.avg(models.Desempenho.nota_final).label("media_turma"),
        sa.func.max(models.Desempenho.nota_final).label("maior_nota"),
        sa.func.min(models.Desempenho.nota_final).label("menor_nota")
    ).outerjoin(models.Inscricao, models.Materia.id == models.Inscricao.materia_id)\
    .outerjoin(models.Desempenho, models.Materia.id == models.Desempenho.materia_id)\
    .filter(models.Materia.id == materia_id)\
    .group_by(models.Materia.id, models.Materia.nome).first()

def get_desempenho_individual_alunos(db: Session, materia_id: int):
    return db.query(
        models.Aluno.nome.label("aluno"),
        models.Aluno.ra,
        models.Desempenho.nota_final,
        models.Desempenho.acertos,
        models.Desempenho.total_questoes,
        (sa.cast(models.Desempenho.acertos, sa.DECIMAL) / models.Desempenho.total_questoes * 100).label("percentual_acerto")
    ).join(models.Desempenho, models.Aluno.id == models.Desempenho.aluno_id)\
    .filter(models.Desempenho.materia_id == materia_id)\
    .order_by(models.Desempenho.nota_final.desc()).all()
