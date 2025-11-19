@app.get("/materias/{id_materia}/alunos", response_model=List[schemas.Usuario])
def get_enrolled_students(id_materia: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    """Retorna a lista de alunos matriculados em uma matéria."""
    materia = db.query(models.Materia).filter(models.Materia.id == id_materia).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")

    if current_user.id != materia.id_professor:
        raise HTTPException(status_code=403, detail="Não autorizado")

    alunos = [matricula.aluno for matricula in materia.matriculas]
    return alunos

@app.post("/materias/{id_materia}/adicionar-aluno", response_model=schemas.Usuario)
def add_student_by_ra(id_materia: int, student_data: schemas.AddStudentByRA, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    """Adiciona um aluno a uma matéria pelo RA (apenas para professores)."""
    materia = db.query(models.Materia).filter(models.Materia.id == id_materia).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")

    if current_user.id != materia.id_professor:
        raise HTTPException(status_code=403, detail="Não autorizado a adicionar alunos a esta matéria")

    aluno = crud.get_user_by_ra(db, ra=student_data.ra)
    if not aluno:
        raise HTTPException(status_code=404, detail="Não há um aluno com esse RA")
    
    if aluno.tipo_usuario != 'aluno':
        raise HTTPException(status_code=400, detail="O usuário encontrado não é um aluno")

    # Verifica se o aluno já está matriculado
    matricula_existente = db.query(models.Matricula).filter(
        models.Matricula.id_aluno == aluno.id,
        models.Matricula.id_materia == id_materia
    ).first()

    if matricula_existente:
        raise HTTPException(status_code=409, detail="Aluno já matriculado nesta matéria")

    nova_matricula = models.Matricula(id_aluno=aluno.id, id_materia=id_materia)
    db.add(nova_matricula)
    db.commit()
    db.refresh(aluno) # Refresh para garantir que o avatar_url está carregado
    
    return aluno