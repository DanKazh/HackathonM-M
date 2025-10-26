"""seed data

Revision ID: 002
Revises: 001
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Данные для пользователей
    user_table_data = """
    ('11111111-1111-1111-1111-111111111111', 'astro_lab', decode('0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef', 'hex')),
    ('22222222-2222-2222-2222-222222222222', 'skywatcher', decode('fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210', 'hex')),
    ('33333333-3333-3333-3333-333333333333', 'observer_ru', decode('abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefab', 'hex'))
    """
    
    # Данные для групп наблюдений
    observation_groups_data = """
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '1P/Halley', 'Комета Галлея, исторические наблюдения', 'completed'),
    ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '2P/Encke', 'Короткопериодическая комета Энке', 'active'),
    ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'C/2025 R2 (SWAN)', 'Новая зелёная комета, открыта осенью 2025', 'processing')
    """
    
    # Данные для наблюдений
    observations_data = """
    ('11111111-1111-1111-1111-111111111111', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '1986-02-09 00:00:00+00', 320.5, -8.2, 'Э. Галлей', 'Максимальная яркость', NULL),
    ('11111111-1111-1111-1111-111111111111', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '1986-03-01 00:00:00+00', 338.2, -20.1, 'Э. Галлей', 'После перигелия', NULL),
    ('11111111-1111-1111-1111-111111111111', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '1986-04-01 00:00:00+00', 5.2, -28.3, 'Э. Галлей', 'Затухание яркости', NULL),
    ('22222222-2222-2222-2222-222222222222', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '2023-03-10 22:00:00+00', 120.3, 14.8, 'К. Мешен', 'Периодическое возвращение', NULL),
    ('22222222-2222-2222-2222-222222222222', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '2023-03-14 22:30:00+00', 121.5, 14.2, 'К. Мешен', 'Хорошее небо', NULL),
    ('22222222-2222-2222-2222-222222222222', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '2023-03-20 21:00:00+00', 122.7, 13.9, 'К. Мешен', 'Комета двигается на восток', NULL),
    ('33333333-3333-3333-3333-333333333333', 'cccccccc-cccc-cccc-cccc-cccccccccccc', '2025-10-10 19:00:00+00', 270.4, -15.7, 'В. Безуглый', 'Первое наблюдение кометы SWAN', NULL),
    ('33333333-3333-3333-3333-333333333333', 'cccccccc-cccc-cccc-cccc-cccccccccccc', '2025-10-15 20:30:00+00', 272.6, -16.3, 'В. Безуглый', 'Подтверждение движения', NULL),
    ('33333333-3333-3333-3333-333333333333', 'cccccccc-cccc-cccc-cccc-cccccccccccc', '2025-10-20 21:15:00+00', 275.1, -17.0, 'В. Безуглый', 'Приближение к Земле', NULL)
    """
    
    # Данные для орбитальных параметров
    orbital_parameters_data = """
    ('11111111-aaaa-bbbb-cccc-111111111111', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 17.834, 0.967, 162.3, 58.4, 111.3, '1986-02-09 12:00:00+00', 3),
    ('22222222-aaaa-bbbb-cccc-222222222222', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 2.217, 0.848, 11.8, 334.6, 186.5, '2023-03-10 00:00:00+00', 3),
    ('33333333-aaaa-bbbb-cccc-333333333333', 'cccccccc-cccc-cccc-cccc-cccccccccccc', 62.4, 0.999, 159.7, 80.2, 56.4, '2025-09-11 00:00:00+00', 3)
    """
    
    # Данные для сближений
    close_approaches_data = """
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-aaaa-bbbb-cccc-111111111111', '1986-04-11 06:00:00+00', 0.4166, 62300000),
    ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '22222222-aaaa-bbbb-cccc-222222222222', '2023-03-25 05:00:00+00', 0.266, 39800000),
    ('cccccccc-cccc-cccc-cccc-cccccccccccc', '33333333-aaaa-bbbb-cccc-333333333333', '2025-10-20 14:30:00+00', 0.26, 38900000)
    """

    # Вставляем пользователей (без version, т.к. есть DEFAULT 1)
    op.execute(f"""
        INSERT INTO user_table (id, login, password_hash) 
        VALUES {user_table_data}
    """)
    
    # Вставляем группы наблюдений
    op.execute(f"""
        INSERT INTO observation_groups (id, name, description, status) 
        VALUES {observation_groups_data}
    """)
    
    # Вставляем наблюдения
    op.execute(f"""
        INSERT INTO observations (
            user_id, group_id, observation_time, right_ascension, declination,
            observer_name, observation_notes, image_url
        ) VALUES {observations_data}
    """)
    
    # Вставляем орбитальные параметры
    op.execute(f"""
        INSERT INTO orbital_parameters (
            id, group_id, semi_major_axis, eccentricity, inclination,
            longitude_ascending_node, argument_perihelion, time_perihelion, used_observations_count
        ) VALUES {orbital_parameters_data}
    """)
    
    # Вставляем данные о сближениях
    op.execute(f"""
        INSERT INTO close_approaches (
            group_id, orbital_parameters_id, approach_time, distance_au, distance_km
        ) VALUES {close_approaches_data}
    """)


def downgrade() -> None:
    # Удаляем все данные в обратном порядке (с учетом foreign keys)
    op.execute("DELETE FROM close_approaches")
    op.execute("DELETE FROM orbital_parameters") 
    op.execute("DELETE FROM observations")
    op.execute("DELETE FROM observation_groups")
    op.execute("DELETE FROM user_table")