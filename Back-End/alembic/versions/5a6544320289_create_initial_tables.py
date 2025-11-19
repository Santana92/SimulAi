"""create_initial_tables

Revision ID: 5a6544320289
Revises: 
Create Date: 2025-11-19 05:45:21.353381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a6544320289'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ra', sa.String(length=20), nullable=True),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('senha', sa.String(length=255), nullable=False),
        sa.Column('tipo_usuario', sa.String(length=10), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ra'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)

    op.create_table(
        'materias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('id_professor', sa.Integer(), nullable=False),
        sa.Column('chave_inscricao', sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(['id_professor'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'simulados',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_materia', sa.Integer(), nullable=False),
        sa.Column('titulo', sa.String(length=150), nullable=False),
        sa.Column('texto_base', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['id_materia'], ['materias.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'questoes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_simulado', sa.Integer(), nullable=False),
        sa.Column('enunciado', sa.Text(), nullable=False),
        sa.Column('resposta_correta', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['id_simulado'], ['simulados.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'matriculas',
        sa.Column('id_aluno', sa.Integer(), nullable=False),
        sa.Column('id_materia', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id_aluno'], ['usuarios.id'], ),
        sa.ForeignKeyConstraint(['id_materia'], ['materias.id'], ),
        sa.PrimaryKeyConstraint('id_aluno', 'id_materia')
    )

    op.create_table(
        'respostas_alunos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_aluno', sa.Integer(), nullable=False),
        sa.Column('id_questao', sa.Integer(), nullable=False),
        sa.Column('resposta_aluno', sa.Text(), nullable=False),
        sa.Column('correta', sa.Boolean(), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['id_aluno'], ['usuarios.id'], ),
        sa.ForeignKeyConstraint(['id_questao'], ['questoes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'desempenho_simulados',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_aluno', sa.Integer(), nullable=False),
        sa.Column('id_simulado', sa.Integer(), nullable=False),
        sa.Column('nota', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['id_aluno'], ['usuarios.id'], ),
        sa.ForeignKeyConstraint(['id_simulado'], ['simulados.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('desempenho_simulados')
    op.drop_table('respostas_alunos')
    op.drop_table('matriculas')
    op.drop_table('questoes')
    op.drop_table('simulados')
    op.drop_table('materias')
    op.drop_index(op.f('ix_usuarios_email'), table_name='usuarios')
    op.drop_table('usuarios')