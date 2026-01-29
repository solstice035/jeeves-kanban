#!/usr/bin/env python3
"""
Run database migrations for Jeeves Kanban Board
"""
import os
import psycopg2
from pathlib import Path

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 5432)),
    'database': os.environ.get('DB_NAME', 'nick'),
}

def run_migration(migration_file):
    """Run a single migration file"""
    print(f"Running migration: {migration_file.name}")

    with open(migration_file, 'r') as f:
        sql = f.read()

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    try:
        cur.execute(sql)
        conn.commit()
        print(f"✅ {migration_file.name} completed successfully")
        return True
    except Exception as e:
        conn.rollback()
        print(f"❌ {migration_file.name} failed: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def main():
    migrations_dir = Path(__file__).parent / 'migrations'

    print("🔄 Running database migrations...")
    print(f"Database: {DB_CONFIG['database']} on {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print()

    if not migrations_dir.exists():
        print("❌ Migrations directory not found")
        return

    # Get all .sql files in migrations directory
    migration_files = sorted(migrations_dir.glob('*.sql'))

    if not migration_files:
        print("No migration files found")
        return

    success_count = 0
    for migration_file in migration_files:
        if run_migration(migration_file):
            success_count += 1
        print()

    print(f"Completed {success_count}/{len(migration_files)} migrations")

if __name__ == '__main__':
    main()
