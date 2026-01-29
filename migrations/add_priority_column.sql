-- Migration: Add priority column to kanban_tasks
-- Date: 2026-01-29
-- Description: Add priority flag to tasks (1=Low, 2=Medium, 3=High, 4=Urgent)

-- Add priority column (integer, default to 2=Medium)
ALTER TABLE kanban_tasks
ADD COLUMN IF NOT EXISTS priority INTEGER DEFAULT 2;

-- Add constraint to ensure priority is between 1-4
ALTER TABLE kanban_tasks
ADD CONSTRAINT priority_range CHECK (priority >= 1 AND priority <= 4);

-- Add index for filtering by priority
CREATE INDEX IF NOT EXISTS idx_kanban_tasks_priority ON kanban_tasks (priority);

COMMENT ON COLUMN kanban_tasks.priority IS 'Task priority: 1=Low, 2=Medium, 3=High, 4=Urgent';
