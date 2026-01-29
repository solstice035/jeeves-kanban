-- Migration: Add links column to kanban_tasks
-- Date: 2026-01-29
-- Description: Add support for linking Obsidian notes, images, and files to tasks

-- Add links column (JSONB array)
ALTER TABLE kanban_tasks
ADD COLUMN IF NOT EXISTS links JSONB DEFAULT '[]'::jsonb;

-- Add index for better query performance
CREATE INDEX IF NOT EXISTS idx_kanban_tasks_links ON kanban_tasks USING GIN (links);

-- Example link structure:
-- [
--   {
--     "url": "obsidian://open?vault=MyVault&file=Notes/MyNote",
--     "type": "obsidian",
--     "title": "My Note"
--   },
--   {
--     "url": "/path/to/image.png",
--     "type": "image",
--     "title": "Screenshot"
--   }
-- ]

COMMENT ON COLUMN kanban_tasks.links IS 'Array of linked resources (Obsidian notes, files, images, URLs)';
