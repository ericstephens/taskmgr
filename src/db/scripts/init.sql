-- Initialize database schema for Task Manager application

-- Create tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date TIMESTAMP,
    priority VARCHAR(20) CHECK (priority IN ('Low', 'Medium', 'High')),
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on due_date for faster sorting
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);

-- Create index on priority for faster filtering
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);

-- Create index on completed status for faster filtering
CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);

-- Add some sample tasks
INSERT INTO tasks (title, description, due_date, priority, completed)
VALUES 
('Complete project proposal', 'Write up the initial project proposal document', CURRENT_TIMESTAMP + INTERVAL '3 days', 'High', FALSE),
('Review code changes', 'Review pull requests from team members', CURRENT_TIMESTAMP + INTERVAL '1 day', 'Medium', FALSE),
('Update documentation', 'Update the API documentation with recent changes', CURRENT_TIMESTAMP + INTERVAL '5 days', 'Low', FALSE),
('Fix login bug', 'Address the issue with login timeout', CURRENT_TIMESTAMP + INTERVAL '2 days', 'High', FALSE),
('Weekly team meeting', 'Prepare agenda for weekly team sync', CURRENT_TIMESTAMP + INTERVAL '4 days', 'Medium', TRUE);
