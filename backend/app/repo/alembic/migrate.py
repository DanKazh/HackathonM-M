#!/usr/bin/env python3
import sys
from pathlib import Path
from dotenv import load_dotenv
from alembic import context
from alembic.config import Config
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory

# Добавляем путь к корню проекта
current_file = Path(__file__)
project_root = current_file.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Загружаем .env
load_dotenv(project_root / '.env')

def run_migrations():
    # Указываем путь к alembic.ini
    alembic_ini_path = Path(__file__).parent / 'alembic.ini'
    alembic_cfg = Config(str(alembic_ini_path))
    
    script = ScriptDirectory.from_config(alembic_cfg)
    
    def upgrade(rev, context: context):
        return script._upgrade_revs("head", rev)
    
    with EnvironmentContext(
        alembic_cfg,
        script,
        fn=upgrade,
        starting_rev=None,
        destination_rev="head",
        tag=None,
    ):
        script.run_env()

if __name__ == "__main__":
    run_migrations()