#!/usr/bin/env python3
"""
Jeeves Kanban Board - Flask Backend with PostgreSQL

Serves the Kanban board with persistent database storage.
"""

import os
import socket
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuration
PORT = 8888
DIRECTORY = Path(__file__).parent.absolute()
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'nick',
}

app = Flask(__name__, static_folder=str(DIRECTORY))


def get_db():
    """Get database connection"""
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    return conn


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
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, description, tags, column_name, position, 
               created_at, updated_at
        FROM kanban_tasks 
        ORDER BY column_name, position, id
    """)
    tasks = cur.fetchall()
    conn.close()
    
    # Convert to list of dicts with proper field names
    result = []
    for task in tasks:
        result.append({
            'id': task['id'],
            'title': task['title'],
            'description': task['description'] or '',
            'tags': task['tags'] or [],
            'column': task['column_name'],
            'position': task['position'],
            'created_at': task['created_at'].isoformat() if task['created_at'] else None,
            'updated_at': task['updated_at'].isoformat() if task['updated_at'] else None,
        })
    
    return jsonify(result)


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.json
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get max position for the column
    cur.execute("""
        SELECT COALESCE(MAX(position), -1) + 1 as next_pos 
        FROM kanban_tasks 
        WHERE column_name = %s
    """, (data.get('column', 'backlog'),))
    next_pos = cur.fetchone()['next_pos']
    
    cur.execute("""
        INSERT INTO kanban_tasks (title, description, tags, column_name, position)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, title, description, tags, column_name, position, created_at, updated_at
    """, (
        data['title'],
        data.get('description', ''),
        data.get('tags', []),
        data.get('column', 'backlog'),
        next_pos
    ))
    
    task = cur.fetchone()
    conn.commit()
    conn.close()
    
    return jsonify({
        'id': task['id'],
        'title': task['title'],
        'description': task['description'] or '',
        'tags': task['tags'] or [],
        'column': task['column_name'],
        'position': task['position'],
        'created_at': task['created_at'].isoformat() if task['created_at'] else None,
        'updated_at': task['updated_at'].isoformat() if task['updated_at'] else None,
    }), 201


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    data = request.json
    
    conn = get_db()
    cur = conn.cursor()
    
    # Build update query dynamically
    updates = []
    values = []
    
    if 'title' in data:
        updates.append('title = %s')
        values.append(data['title'])
    if 'description' in data:
        updates.append('description = %s')
        values.append(data['description'])
    if 'tags' in data:
        updates.append('tags = %s')
        values.append(data['tags'])
    if 'column' in data:
        updates.append('column_name = %s')
        values.append(data['column'])
    if 'position' in data:
        updates.append('position = %s')
        values.append(data['position'])
    
    updates.append('updated_at = NOW()')
    values.append(task_id)
    
    cur.execute(f"""
        UPDATE kanban_tasks 
        SET {', '.join(updates)}
        WHERE id = %s
        RETURNING id, title, description, tags, column_name, position, created_at, updated_at
    """, values)
    
    task = cur.fetchone()
    conn.commit()
    conn.close()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({
        'id': task['id'],
        'title': task['title'],
        'description': task['description'] or '',
        'tags': task['tags'] or [],
        'column': task['column_name'],
        'position': task['position'],
        'created_at': task['created_at'].isoformat() if task['created_at'] else None,
        'updated_at': task['updated_at'].isoformat() if task['updated_at'] else None,
    })


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('DELETE FROM kanban_tasks WHERE id = %s RETURNING id', (task_id,))
    deleted = cur.fetchone()
    conn.commit()
    conn.close()
    
    if not deleted:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({'deleted': True, 'id': task_id})


@app.route('/api/tasks/import', methods=['POST'])
def import_tasks():
    """Import tasks from localStorage migration"""
    data = request.json
    tasks = data.get('tasks', [])
    
    conn = get_db()
    cur = conn.cursor()
    
    imported = 0
    for task in tasks:
        cur.execute("""
            INSERT INTO kanban_tasks (title, description, tags, column_name, position)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            task['title'],
            task.get('description', ''),
            task.get('tags', []),
            task.get('column', 'backlog'),
            task.get('position', 0)
        ))
        imported += 1
    
    conn.commit()
    conn.close()
    
    return jsonify({'imported': imported})


if __name__ == '__main__':
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
