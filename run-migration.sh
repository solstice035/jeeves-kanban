#!/bin/bash
# Run database migrations for Jeeves Kanban Board

# Default database connection
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-nick}"

echo "🔄 Running database migrations..."
echo "Database: $DB_NAME on $DB_HOST:$DB_PORT"
echo ""

# Run the links column migration
echo "Adding links column..."
psql -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -f migrations/add_links_column.sql

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Migration completed successfully!"
else
    echo ""
    echo "❌ Migration failed. Please check the error messages above."
    exit 1
fi
