# Jeeves Kanban Board - PostgreSQL Backend Design

**Date:** 2026-01-29  
**Status:** Approved

## Overview

Add PostgreSQL backend and card editing to the Jeeves Kanban board.

## Features

1. **PostgreSQL Backend** - Replace localStorage with persistent database
2. **Edit Cards** - Click card to open modal with pre-filled values
3. **Delete Cards** - Delete button in edit modal

## Database Schema

Database: `nick` (local PostgreSQL 18 on port 5432)

```sql
CREATE TABLE kanban_tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    tags TEXT[],
    column_name VARCHAR(50) NOT NULL DEFAULT 'backlog',
    position INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## API Design

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /api/tasks | List all tasks |
| POST | /api/tasks | Create task |
| PUT | /api/tasks/:id | Update task |
| DELETE | /api/tasks/:id | Delete task |

## Backend (Flask)

- Replace `server.py` with Flask app
- Use `psycopg2` for PostgreSQL connection
- Serve static files from same server
- Port 8888 (unchanged)
- No authentication (local only)

## Frontend Changes

1. Replace localStorage calls with fetch API
2. Add click handler on cards to open edit modal
3. Reuse add modal for editing (pre-fill fields)
4. Add red "Delete" button to modal
5. Migration: offer to import localStorage data on first load

## File Changes

- `server.py` → Flask app with API routes
- `index.html` → Updated JavaScript for API + edit functionality
- `requirements.txt` → Flask, psycopg2-binary
