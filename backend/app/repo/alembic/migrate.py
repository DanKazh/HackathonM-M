#!/usr/bin/env python3
"""
Скрипт для управления миграциями базы данных
"""
import os
import sys
from alembic.config import Config
from alembic import command

def get_alembic_config():
    """Получить конфигурацию Alembic"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    alembic_ini_path = os.path.join(current_dir, 'alembic.ini')
    
    config = Config(alembic_ini_path)
    config.set_main_option('script_location', current_dir)
    
    return config

def run_migration():
    """Запустить миграции"""
    config = get_alembic_config()
    command.upgrade(config, 'head')

def create_migration(message):
    """Создать новую миграцию"""
    config = get_alembic_config()
    command.revision(config, message=message, autogenerate=True)

def downgrade_migration(revision):
    """Откатить миграцию"""
    config = get_alembic_config()
    command.downgrade(config, revision)

def show_history():
    """Показать историю миграций"""
    config = get_alembic_config()
    command.history(config, indicate_current=True)

def show_current():
    """Показать текущую версию"""
    config = get_alembic_config()
    command.current(config)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python migrate.py upgrade          - применить все миграции")
        print("  python migrate.py create <message> - создать новую миграцию")
        print("  python migrate.py downgrade <rev>  - откатить миграцию")
        print("  python migrate.py history          - показать историю")
        print("  python migrate.py current          - показать текущую версию")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == 'upgrade':
        run_migration()
        print("Миграции успешно применены")
    
    elif action == 'create' and len(sys.argv) > 2:
        message = sys.argv[2]
        create_migration(message)
        print(f"Миграция '{message}' создана")
    
    elif action == 'downgrade' and len(sys.argv) > 2:
        revision = sys.argv[2]
        downgrade_migration(revision)
        print(f"Откат до версии {revision} выполнен")
    
    elif action == 'history':
        show_history()
    
    elif action == 'current':
        show_current()
    
    else:
        print("Неизвестная команда")
        sys.exit(1)