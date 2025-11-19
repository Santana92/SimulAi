# --- Imports ---
import httpx
import json
import io
import google.generativeai as genai
from jose import jwt, JWTError

from fastapi import FastAPI, HTTPException, UploadFile, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict

# Imports da nova estrutura
from core import models, schemas
from core.database import engine, get_db
from core.config import GOOGLE_API_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

# Configura a API do Google Gemini
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# --- Instância da Aplicação FastAPI ---
app = FastAPI(title="SimulAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://*.vercel.app"],  # Permite acesso do localhost e da Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Eventos de Ciclo de Vida ---
@app.on_event("startup")
async def startup():
    # Esta função pode ser usada para criar as tabelas no banco de dados
    # No entanto, usaremos Alembic para um controle de versão mais robusto.
    # async with engine.begin() as conn:
    #     await conn.run_sync(models.Base.metadata.create_all)
    pass

# --- Endpoints ---

@app.get("/")
def read_root():
    """Endpoint inicial para verificar se a API está no ar."""
    return {"message": "API do SimulAI está no ar!"}

# --- Endpoints de Autenticação ---
@app.post("/usuarios", response_model=schemas.Usuario)
async def cadastrar_usuario(usuario: schemas.UsuarioCreate, db: AsyncSession = Depends(get_db)):
    pass

@app.post("/login", response_model=schemas.Usuario)
async def fazer_login(login_data: schemas.LoginData, db: AsyncSession = Depends(get_db)):
    pass

@app.post("/auth/google", response_model=schemas.Usuario)
async def auth_google(auth_code: schemas.GoogleAuthCode, db: AsyncSession = Depends(get_db)):
    pass

# --- Endpoints de Matérias e Simulados ---
@app.get("/materias", response_model=List[schemas.Materia])
async def get_materias(db: AsyncSession = Depends(get_db)):
    pass

@app.post("/materias", response_model=schemas.Materia)
async def create_materia(materia_data: schemas.MateriaCreate, db: AsyncSession = Depends(get_db)):
    pass

@app.get("/simulados/{id_simulado}", response_model=schemas.SimuladoCompleto)
async def get_simulado(id_simulado: str, db: AsyncSession = Depends(get_db)):
    pass

# --- Endpoints de Resultados ---
@app.post("/simulados/{simulado_id}/resultados", response_model=schemas.Resultado)
async def registrar_resultado(simulado_id: str, resultado: schemas.ResultadoCreate, db: AsyncSession = Depends(get_db)):
    pass

@app.get("/simulados/{simulado_id}/resultados", response_model=List[schemas.Resultado])
async def listar_resultados(simulado_id: str, db: AsyncSession = Depends(get_db)):
    pass

@app.get("/resultados/{usuario_id}", response_model=List[schemas.Resultado])
async def get_resultados_usuario(usuario_id: str, db: AsyncSession = Depends(get_db)):
    pass

@app.get("/resultados", response_model=List[schemas.Resultado])
async def get_todos_resultados(db: AsyncSession = Depends(get_db)):
    pass

# --- Geração de Simulados com IA (Gemini) ---
@app.post("/materias/{id_materia}/simulados", response_model=schemas.SimuladoCompleto)
async def create_simulado_from_gemini(
    id_materia: str,
    nome_simulado: str = Form(...),
    arquivo: UploadFile = Form(...),
    db: AsyncSession = Depends(get_db)
):
    pass