#!/usr/bin/env python3
"""
Jeeves Kanban Board - Flask Backend with PostgreSQL

Serves the Kanban board with persistent database storage.
"""

import os
import socket
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from flask import Flask, jsonify, request, send_from_directory
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
PORT = int(os.environ.get('PORT', 8888))
DIRECTORY = Path(__file__).parent.absolute()
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 5432)),
    'database': os.environ.get('DB_NAME', 'nick'),
}

# Valid column names
VALID_COLUMNS = {'backlog', 'ready', 'in-progress', 'review', 'done'}

# Field validation limits
MAX_TITLE_LENGTH = 255
MAX_DESCRIPTION_LENGTH = 10000
MAX_TAGS = 20
MAX_TAG_LENGTH = 50
MAX_LINKS = 50
MAX_LINK_URL_LENGTH = 2000
MAX_LINK_TITLE_LENGTH = 200

app = Flask(__name__, static_folder=str(DIRECTORY))

# Connection pool
connection_pool = None


def init_connection_pool():
    """Initialize the database connection pool"""
    global connection_pool
    try:
        connection_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            cursor_factory=RealDictCursor,
            **DB_CONFIG
        )
        logger.info("Database connection pool created successfully")
    except psycopg2.Error as e:
        logger.error(f"Failed to create connection pool: {e}")
        raise


def get_db():
    """Get database connection from pool"""
    try:
        if connection_pool:
            return connection_pool.getconn()
        else:
            # Fallback to direct connection if pool not initialized
            return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    except psycopg2.Error as e:
        logger.error(f"Failed to get database connection: {e}")
        raise


def return_db(conn):
    """Return database connection to pool"""
    try:
        if connection_pool and conn:
            connection_pool.putconn(conn)
    except psycopg2.Error as e:
        logger.error(f"Failed to return connection to pool: {e}")


def task_to_dict(task: Dict[str, Any]) -> Dict[str, Any]:
    """Convert database task row to API response dictionary"""
    return {
        'id': task['id'],
        'title': task['title'],
        'description': task['description'] or '',
        'tags': task['tags'] or [],
        'links': task.get('links', []) or [],
        'column': task['column_name'],
        'position': task['position'],
        'created_at': task['created_at'].isoformat() if task['created_at'] else None,
        'updated_at': task['updated_at'].isoformat() if task['updated_at'] else None,
    }


def validate_task_data(data: Dict[str, Any], require_title: bool = True) -> Optional[str]:
    """
    Validate task data.
    Returns error message if invalid, None if valid.
    """
    # Validate title
    if require_title:
        if 'title' not in data or not data['title']:
            return "Title is required"
        if not isinstance(data['title'], str):
            return "Title must be a string"
        if len(data['title']) > MAX_TITLE_LENGTH:
            return f"Title must be {MAX_TITLE_LENGTH} characters or less"

    # Validate description
    if 'description' in data and data['description']:
        if not isinstance(data['description'], str):
            return "Description must be a string"
        if len(data['description']) > MAX_DESCRIPTION_LENGTH:
            return f"Description must be {MAX_DESCRIPTION_LENGTH} characters or less"

    # Validate tags
    if 'tags' in data and data['tags']:
        if not isinstance(data['tags'], list):
            return "Tags must be an array"
        if len(data['tags']) > MAX_TAGS:
            return f"Maximum {MAX_TAGS} tags allowed"
        for tag in data['tags']:
            if not isinstance(tag, str):
                return "All tags must be strings"
            if len(tag) > MAX_TAG_LENGTH:
                return f"Each tag must be {MAX_TAG_LENGTH} characters or less"

    # Validate column
    if 'column' in data:
        if not isinstance(data['column'], str):
            return "Column must be a string"
        if data['column'] not in VALID_COLUMNS:
            return f"Column must be one of: {', '.join(VALID_COLUMNS)}"

    # Validate position
    if 'position' in data:
        if not isinstance(data['position'], int):
            return "Position must be an integer"
        if data['position'] < 0:
            return "Position must be non-negative"

    # Validate links
    if 'links' in data and data['links']:
        if not isinstance(data['links'], list):
            return "Links must be an array"
        if len(data['links']) > MAX_LINKS:
            return f"Maximum {MAX_LINKS} links allowed"
        for link in data['links']:
            if not isinstance(link, dict):
                return "All links must be objects"
            if 'url' not in link or not isinstance(link['url'], str):
                return "Each link must have a 'url' string field"
            if len(link['url']) > MAX_LINK_URL_LENGTH:
                return f"Link URL must be {MAX_LINK_URL_LENGTH} characters or less"
            if 'type' in link and not isinstance(link['type'], str):
                return "Link 'type' must be a string"
            if 'title' in link:
                if not isinstance(link['title'], str):
                    return "Link 'title' must be a string"
                if len(link['title']) > MAX_LINK_TITLE_LENGTH:
                    return f"Link title must be {MAX_LINK_TITLE_LENGTH} characters or less"

    return None


def get_local_ip():
    """Get the local network IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


# Static files
@app.route('/')
def serve_index():
    return send_from_directory(DIRECTORY, 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(DIRECTORY, filename)


# API Routes
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    conn = None
    cur = None
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, title, description, tags, links, column_name, position,
                   created_at, updated_at
            FROM kanban_tasks
            ORDER BY column_name, position, id
        """)
        tasks = cur.fetchall()

        # Convert to list of dicts with proper field names
        result = [task_to_dict(task) for task in tasks]

        return jsonify(result)
    except psycopg2.Error as e:
        logger.error(f"Database error in get_tasks: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logger.error(f"Unexpected error in get_tasks: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            return_db(conn)


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    conn = None
    cur = None
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate input
        validation_error = validate_task_data(data, require_title=True)
        if validation_error:
            return jsonify({'error': validation_error}), 400

        conn = get_db()
        cur = conn.cursor()

        # Get max position for the column
        column = data.get('column', 'backlog')
        cur.execute("""
            SELECT COALESCE(MAX(position), -1) + 1 as next_pos
            FROM kanban_tasks
            WHERE column_name = %s
        """, (column,))
        next_pos = cur.fetchone()['next_pos']

        cur.execute("""
            INSERT INTO kanban_tasks (title, description, tags, links, column_name, position)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, title, description, tags, links, column_name, position, created_at, updated_at
        """, (
            data['title'],
            data.get('description', ''),
            data.get('tags', []),
            data.get('links', []),
            column,
            next_pos
        ))

        task = cur.fetchone()
        conn.commit()

        logger.info(f"Created task {task['id']}: {task['title']}")
        return jsonify(task_to_dict(task)), 201

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error in create_task: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Unexpected error in create_task: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            return_db(conn)


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    conn = None
    cur = None
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        # Validate input
        validation_error = validate_task_data(data, require_title=False)
        if validation_error:
            return jsonify({'error': validation_error}), 400

        conn = get_db()
        cur = conn.cursor()

        # Build update query with whitelisted fields only (prevents SQL injection)
        allowed_fields = {
            'title': 'title',
            'description': 'description',
            'tags': 'tags',
            'links': 'links',
            'column': 'column_name',
            'position': 'position'
        }

        updates = []
        values = []

        for data_key, db_column in allowed_fields.items():
            if data_key in data:
                updates.append(f'{db_column} = %s')
                values.append(data[data_key])

        if not updates:
            return jsonify({'error': 'No valid fields to update'}), 400

        updates.append('updated_at = NOW()')
        values.append(task_id)

        query = f"""
            UPDATE kanban_tasks
            SET {', '.join(updates)}
            WHERE id = %s
            RETURNING id, title, description, tags, links, column_name, position, created_at, updated_at
        """

        cur.execute(query, values)
        task = cur.fetchone()
        conn.commit()

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        logger.info(f"Updated task {task_id}")
        return jsonify(task_to_dict(task))

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error in update_task: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Unexpected error in update_task: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            return_db(conn)


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    conn = None
    cur = None
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute('DELETE FROM kanban_tasks WHERE id = %s RETURNING id', (task_id,))
        deleted = cur.fetchone()
        conn.commit()

        if not deleted:
            return jsonify({'error': 'Task not found'}), 404

        logger.info(f"Deleted task {task_id}")
        return jsonify({'deleted': True, 'id': task_id})

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error in delete_task: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Unexpected error in delete_task: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            return_db(conn)


@app.route('/api/tasks/import', methods=['POST'])
def import_tasks():
    """Import tasks from localStorage migration"""
    conn = None
    cur = None
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        tasks = data.get('tasks', [])
        if not isinstance(tasks, list):
            return jsonify({'error': 'Tasks must be an array'}), 400

        if len(tasks) > 1000:
            return jsonify({'error': 'Cannot import more than 1000 tasks at once'}), 400

        conn = get_db()
        cur = conn.cursor()

        imported = 0
        errors = []

        for idx, task in enumerate(tasks):
            # Validate each task
            validation_error = validate_task_data(task, require_title=True)
            if validation_error:
                errors.append(f"Task {idx}: {validation_error}")
                continue

            try:
                cur.execute("""
                    INSERT INTO kanban_tasks (title, description, tags, links, column_name, position)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    task['title'],
                    task.get('description', ''),
                    task.get('tags', []),
                    task.get('links', []),
                    task.get('column', 'backlog'),
                    task.get('position', 0)
                ))
                imported += 1
            except psycopg2.Error as e:
                errors.append(f"Task {idx}: Database error")
                logger.error(f"Error importing task {idx}: {e}")

        conn.commit()
        logger.info(f"Imported {imported} tasks with {len(errors)} errors")

        response = {'imported': imported}
        if errors:
            response['errors'] = errors

        return jsonify(response)

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error in import_tasks: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Unexpected error in import_tasks: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            return_db(conn)


if __name__ == '__main__':
    try:
        # Initialize connection pool
        init_connection_pool()

        local_ip = get_local_ip()

        print("\n" + "=" * 60)
        print("🎯 Jeeves Kanban Board Server (Flask + PostgreSQL)")
        print("=" * 60)
        print(f"\n✅ Server starting...\n")
        print(f"📱 Access from this computer:")
        print(f"   http://localhost:{PORT}/")
        print(f"   http://127.0.0.1:{PORT}/\n")
        print(f"🌐 Access from other devices on your network:")
        print(f"   http://{local_ip}:{PORT}/\n")
        print(f"🛑 Press Ctrl+C to stop the server\n")
        print("=" * 60 + "\n")

        app.run(host='0.0.0.0', port=PORT, debug=False)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        print(f"\n❌ Failed to start server: {e}")
    finally:
        # Close connection pool
        if connection_pool:
            connection_pool.closeall()
            logger.info("Connection pool closed")
