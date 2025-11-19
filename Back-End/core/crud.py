def get_user_by_ra(db: Session, ra: str):
    """Busca um usuário pelo RA."""
    return db.query(models.Usuario).filter(models.Usuario.ra == ra).first()