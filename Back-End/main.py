from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Annotated, Optional, Union
from datetime import timedelta

from . import models, schemas, crud, security
from .database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine) # Removido, pois estamos usando Alembic para migrações

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Autenticação e Autorização ---
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        user_type: str = payload.get("user_type") # Get user_type from token
        if email is None or user_type is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email, user_type=user_type) # Use schemas.TokenData
    except security.JWTError:
        raise credentials_exception

    if token_data.user_type == "professor":
        user = crud.get_professor_by_email(db, email=token_data.email)
    elif token_data.user_type == "aluno":
        user = crud.get_aluno_by_email(db, email=token_data.email)
    else:
        raise credentials_exception # Invalid user_type
    
    if user is None:
        raise credentials_exception # User not found
    return user

async def get_current_professor(current_user: Annotated[models.Professor, Depends(get_current_user)]):
    if not isinstance(current_user, models.Professor):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Apenas professores podem acessar este recurso")
    return current_user

async def get_current_aluno(current_user: Annotated[models.Aluno, Depends(get_current_user)]):
    if not isinstance(current_user, models.Aluno):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Apenas alunos podem acessar este recurso")
    return current_user

# --- Endpoints de Autenticação ---
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    user = crud.get_professor_by_email(db, email=form_data.username)
    user_type = "professor"
    if not user:
        user = crud.get_aluno_by_email(db, email=form_data.username)
        user_type = "aluno"
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou senha incorretos")

    if not security.verify_password(form_data.password, user.senha_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou senha incorretos")
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "user_type": user_type}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=Union[schemas.ProfessorResponse, schemas.AlunoResponse])
async def read_users_me(current_user: Annotated[Union[models.Professor, models.Aluno], Depends(get_current_user)]):
    return current_user

@app.post("/professores/register", response_model=schemas.ProfessorResponse)
def register_professor(professor: schemas.ProfessorCreate, db: Session = Depends(get_db)):
    db_professor = crud.get_professor_by_email(db, email=professor.email)
    if db_professor:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud.create_professor(db=db, professor=professor)

@app.post("/alunos/register", response_model=schemas.AlunoResponse)
def register_aluno(aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    db_aluno = crud.get_aluno_by_email(db, email=aluno.email)
    if db_aluno:
        raise HTTPException(status_code=400, detail="Email já registrado")
    db_aluno = crud.get_aluno_by_ra(db, ra=aluno.ra)
    if db_aluno:
        raise HTTPException(status_code=400, detail="RA já registrado")
    return crud.create_aluno(db=db, aluno=aluno)

# --- Endpoints para Professores ---
@app.post("/materias/", response_model=schemas.MateriaResponse)
def create_materia_for_professor(
    materia: schemas.MateriaCreate,
    current_professor: Annotated[models.Professor, Depends(get_current_professor)],
    db: Session = Depends(get_db)
):
    return crud.create_materia(db=db, materia=materia, professor_id=current_professor.id)

@app.get("/professores/me/materias", response_model=List[schemas.MateriaResponse])
def get_my_materias(
    current_professor: Annotated[models.Professor, Depends(get_current_professor)],
    db: Session = Depends(get_db)
):
    return crud.get_materias_by_professor(db=db, professor_id=current_professor.id)

@app.get("/materias/{materia_id}", response_model=schemas.MateriaResponse)
def get_materia(materia_id: int, db: Session = Depends(get_db)):
    db_materia = crud.get_materia_by_id(db, materia_id=materia_id)
    if db_materia is None:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")
    return db_materia

@app.put("/materias/{materia_id}", response_model=schemas.MateriaResponse)
def update_materia(
    materia_id: int,
    materia_update: schemas.MateriaCreate,
    current_professor: Annotated[models.Professor, Depends(get_current_professor)],
    db: Session = Depends(get_db)
):
    db_materia = crud.get_materia_by_id(db, materia_id=materia_id)
    if db_materia is None:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")
    if db_materia.professor_id != current_professor.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para editar esta matéria")
    return crud.update_materia(db=db, materia_id=materia_id, materia_update=materia_update)

@app.delete("/materias/{materia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_materia(
    materia_id: int,
    current_professor: Annotated[models.Professor, Depends(get_current_professor)],
    db: Session = Depends(get_db)
):
    db_materia = crud.get_materia_by_id(db, materia_id=materia_id)
    if db_materia is None:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")
    if db_materia.professor_id != current_professor.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para deletar esta matéria")
    crud.delete_materia(db=db, materia_id=materia_id)
    return

@app.get("/materias/{materia_id}/alunos", response_model=List[schemas.AlunoResponse])
def get_alunos_matriculados_em_materia(
    materia_id: int,
    current_professor: Annotated[models.Professor, Depends(get_current_professor)],
    db: Session = Depends(get_db)
):
    db_materia = crud.get_materia_by_id(db, materia_id=materia_id)
    if db_materia is None:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")
    if db_materia.professor_id != current_professor.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para ver os alunos desta matéria")
    
    inscricoes = crud.get_inscricoes_by_materia(db, materia_id=materia_id)
    # Explicitly convert SQLAlchemy Aluno models to schemas.AlunoResponse
    alunos = [schemas.AlunoResponse.model_validate(inscricao.aluno) for inscricao in inscricoes]
    return alunos

# --- Endpoints para Alunos ---
@app.post("/materias/join", response_model=schemas.InscricaoResponse)
def join_materia(
    senha_acesso: str,
    current_aluno: Annotated[models.Aluno, Depends(get_current_aluno)],
    db: Session = Depends(get_db)
):
    db_materia = crud.get_materia_by_senha_acesso(db, senha_acesso=senha_acesso)
    if db_materia is None:
        raise HTTPException(status_code=404, detail="Matéria não encontrada ou senha de acesso incorreta")
    
    if crud.get_inscricao(db, aluno_id=current_aluno.id, materia_id=db_materia.id):
        raise HTTPException(status_code=409, detail="Aluno já inscrito nesta matéria")
    
    inscricao = crud.create_inscricao(db=db, aluno_id=current_aluno.id, materia_id=db_materia.id)
    if inscricao is None:
         raise HTTPException(status_code=500, detail="Erro ao realizar inscrição na matéria")
    return inscricao

@app.get("/alunos/me/materias", response_model=List[schemas.MateriaResponse])
def get_my_enrolled_materias(
    current_aluno: Annotated[models.Aluno, Depends(get_current_aluno)],
    db: Session = Depends(get_db)
):
    inscricoes = crud.get_inscricoes_by_aluno(db, aluno_id=current_aluno.id)
    # Explicitly convert SQLAlchemy Materia models to schemas.MateriaResponse
    materias_inscritas = [schemas.MateriaResponse.model_validate(inscricao.materia) for inscricao in inscricoes]
    return materias_inscritas

# --- Placeholder para IA (Gerar e Corrigir Questões) ---
@app.post("/ai/generate_questoes/{materia_id}", response_model=List[schemas.QuestaoResponse])
async def generate_questoes_ai(
    materia_id: int,
    num_questoes: int = 5,
    current_professor: Annotated[models.Professor, Depends(get_current_professor)],
    db: Session = Depends(get_db)
):
    db_materia = crud.get_materia_by_id(db, materia_id=materia_id)
    if not db_materia:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")
    if db_materia.professor_id != current_professor.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para gerar questões para esta matéria")
    
    # Lógica para chamar a IA para gerar questões baseadas em db_materia.texto_base
    # Placeholder: Retorna algumas questões de exemplo
    questoes_geradas = []
    for i in range(num_questoes):
        questao_data = schemas.QuestaoCreate(
            materia_id=materia_id,
            pergunta=f"Questão {i+1} gerada pela IA sobre {db_materia.nome}?",
            tipo="multipla_escolha",
            opcoes={"A": "Opção A", "B": "Opção B", "C": "Opção C", "D": "Opção D"},
            resposta_correta="A",
            nivel_dificuldade="medio"
        )
        db_questao = crud.create_questao(db, questao=questao_data)
        questoes_geradas.append(db_questao)
    return questoes_geradas

@app.post("/ai/correct_resposta/{resposta_id}", response_model=schemas.RespostaAlunoResponse)
async def correct_resposta_ai(
    resposta_id: int,
    current_aluno: Annotated[models.Aluno, Depends(get_current_aluno)],
    db: Session = Depends(get_db)
):
    # Lógica para chamar a IA para corrigir a resposta
    # Placeholder: Marca como correta e adiciona feedback
    # TODO: Implementar lógica de correção da IA real
    pass # Remova este pass e adicione a implementação real aqui

# --- Endpoints para Avaliações e Respostas ---
@app.post("/avaliacoes/", response_model=schemas.AvaliacaoResponse)
def create_avaliacao(
    avaliacao: schemas.AvaliacaoCreate,
    current_professor: Annotated[models.Professor, Depends(get_current_professor)],
    db: Session = Depends(get_db)
):
    db_materia = crud.get_materia_by_id(db, materia_id=avaliacao.materia_id)
    if not db_materia or db_materia.professor_id != current_professor.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para criar avaliações para esta matéria")
    return crud.create_avaliacao(db=db, avaliacao=avaliacao)

@app.get("/avaliacoes/{avaliacao_id}/questoes", response_model=List[schemas.QuestaoResponse])
def get_questoes_for_avaliacao(
    avaliacao_id: int,
    current_user: Annotated[Union[models.Professor, models.Aluno], Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    db_avaliacao = crud.get_avaliacao_by_id(db, avaliacao_id=avaliacao_id)
    if not db_avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    
    # Verificar se o usuário tem permissão (professor da matéria ou aluno inscrito)
    if isinstance(current_user, models.Professor) and db_avaliacao.materia.professor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para ver estas questões")
    
    if isinstance(current_user, models.Aluno) and not crud.get_inscricao(db, aluno_id=current_user.id, materia_id=db_avaliacao.materia_id):
        raise HTTPException(status_code=403, detail="Você não está inscrito nesta matéria para ver esta avaliação")
    
    return crud.get_questoes_by_materia(db, materia_id=db_avaliacao.materia_id)

@app.post("/avaliacoes/{avaliacao_id}/submit_resposta", response_model=schemas.RespostaAlunoResponse)
def submit_resposta_avaliacao(
    avaliacao_id: int,
    resposta: schemas.RespostaAlunoCreate,
    current_aluno: Annotated[models.Aluno, Depends(get_current_aluno)],
    db: Session = Depends(get_db)
):
    if resposta.aluno_id != current_aluno.id:
        raise HTTPException(status_code=403, detail="Você não pode submeter respostas por outro aluno")
    
    db_avaliacao = crud.get_avaliacao_by_id(db, avaliacao_id=avaliacao_id)
    if not db_avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")

    if not crud.get_inscricao(db, aluno_id=current_aluno.id, materia_id=db_avaliacao.materia_id):
        raise HTTPException(status_code=403, detail="Você não está inscrito nesta matéria")
    
    # Placeholder para IA de correção
    # A IA corrigiria a resposta e preencheria 'correta', 'nota', 'feedback_ia'
    # Por enquanto, apenas cria a resposta com valores padrão
    db_resposta = crud.create_resposta_aluno(db=db, resposta=resposta)
    return db_resposta

@app.get("/alunos/me/desempenho", response_model=List[schemas.DesempenhoResponse])
def get_my_desempenho(
    current_aluno: Annotated[models.Aluno, Depends(get_current_aluno)],
    db: Session = Depends(get_db)
):
    return current_aluno.desempenhos # Assumindo que o relationship 'desempenhos' está carregado

@app.get("/materias/{materia_id}/relatorio-geral", response_model=schemas.RelatorioGeralTurma)
def get_relatorio_geral_turma(
    materia_id: int,
    current_professor: Annotated[models.Professor, Depends(get_current_professor)],
    db: Session = Depends(get_db)
):
    db_materia = crud.get_materia_by_id(db, materia_id=materia_id)
    if not db_materia or db_materia.professor_id != current_professor.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para ver este relatório")
    
    relatorio = crud.get_relatorio_geral_turma(db, materia_id)
    if relatorio is None:
        raise HTTPException(status_code=404, detail="Relatório não encontrado ou matéria sem dados")
    
    return relatorio # Pydantic's from_attributes will handle mapping the Row object

@app.get("/materias/{materia_id}/desempenho-individual", response_model=List[schemas.DesempenhoIndividualAluno])
def get_desempenho_individual_alunos(
    materia_id: int,
    current_professor: Annotated[models.Professor, Depends(get_current_professor)],
    db: Session = Depends(get_db)
):
    db_materia = crud.get_materia_by_id(db, materia_id=materia_id)
    if not db_materia or db_materia.professor_id != current_professor.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para ver este relatório")
    
    desempenho_alunos = crud.get_desempenho_individual_alunos(db, materia_id)
    return desempenho_alunos # Pydantic's from_attributes will handle mapping the Row objects
