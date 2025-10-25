"""initial tables

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Функция для обновления updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    # Таблица пользователей
    op.create_table('user_table',
        sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
        sa.Column('login', sa.Text(), nullable=False),
        sa.Column('password_hash', sa.LargeBinary(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('length(login) >= 6 AND length(login) <= 20', name='user_table_login_check'),
        sa.CheckConstraint('octet_length(password_hash) = 40', name='user_table_password_hash_check')
    )
    op.create_unique_constraint('user_login_unique', 'user_table', ['login'])
    
    # Таблица групп наблюдений
    op.create_table('observation_groups',
        sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), server_default=sa.text("'active'"), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("status IN ('active', 'processing', 'completed', 'error')", name='observation_groups_status_check')
    )
    
    # Таблица наблюдений
    op.create_table('observations',
        sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(), nullable=False),
        sa.Column('group_id', postgresql.UUID(), nullable=False),
        sa.Column('observation_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('right_ascension', sa.Double(), nullable=False),
        sa.Column('declination', sa.Double(), nullable=False),
        sa.Column('observer_name', sa.String(length=100), nullable=True),
        sa.Column('observation_notes', sa.Text(), nullable=True),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['observation_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user_table.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('declination >= -90 AND declination <= 90', name='valid_dec'),
        sa.CheckConstraint('right_ascension >= 0 AND right_ascension < 360', name='valid_ra')
    )
    
    # Таблица орбитальных параметров
    op.create_table('orbital_parameters',
        sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('group_id', postgresql.UUID(), nullable=False),
        sa.Column('semi_major_axis', sa.Double(), nullable=False),
        sa.Column('eccentricity', sa.Double(), nullable=False),
        sa.Column('inclination', sa.Double(), nullable=False),
        sa.Column('longitude_ascending_node', sa.Double(), nullable=False),
        sa.Column('argument_perihelion', sa.Double(), nullable=False),
        sa.Column('time_perihelion', sa.DateTime(timezone=True), nullable=False),
        sa.Column('calculation_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('used_observations_count', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['observation_groups.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('eccentricity >= 0', name='valid_eccentricity'),
        sa.CheckConstraint('inclination >= 0 AND inclination <= 180', name='valid_inclination'),
        sa.CheckConstraint('longitude_ascending_node >= 0 AND longitude_ascending_node < 360 AND argument_perihelion >= 0 AND argument_perihelion < 360', name='valid_angles'),
        sa.CheckConstraint('semi_major_axis > 0', name='positive_semi_major_axis')
    )
    
    # Таблица сближений
    op.create_table('close_approaches',
        sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('group_id', postgresql.UUID(), nullable=False),
        sa.Column('orbital_parameters_id', postgresql.UUID(), nullable=False),
        sa.Column('approach_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('distance_au', sa.Double(), nullable=False),
        sa.Column('distance_km', sa.Double(), nullable=False),
        sa.Column('calculation_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['observation_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['orbital_parameters_id'], ['orbital_parameters.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('distance_au > 0 AND distance_km > 0', name='positive_distance')
    )
    
    # Триггеры для обновления updated_at
    op.execute("""
        CREATE TRIGGER update_user_table_updated_at BEFORE UPDATE ON user_table
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)
    
    op.execute("""
        CREATE TRIGGER update_observation_groups_updated_at BEFORE UPDATE ON observation_groups
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    # Удаляем триггеры
    op.execute("DROP TRIGGER IF EXISTS update_observation_groups_updated_at ON observation_groups")
    op.execute("DROP TRIGGER IF EXISTS update_user_table_updated_at ON user_table")
    
    # Удаляем таблицы в обратном порядке
    op.drop_table('close_approaches')
    op.drop_table('orbital_parameters')
    op.drop_table('observations')
    op.drop_table('observation_groups')
    op.drop_table('user_table')
    
    # Удаляем функцию
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")