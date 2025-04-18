# Specification: Personal Task Manager App

This document outlines the specifications for a simple, personal task manager application designed to demonstrate vibe coding (AI-assisted development) using the Windsurf framework. The app will consist of a frontend, a database, and an API layer, providing a minimal yet functional task management system.

## My rules
1. Python
   1. The project uses conda for python environments so all package installations need to be done with that. The name of the environment is the same name as the project name / root folder
2. Structure
   1. There should be a src/api, src/db, and src/frontend folder for the respective layers of the app
   2. Each directory (src/api, src/db, src/frontend) should have its own requirements.txt file if it is using python
   3. Test folders should exist for src/frontend and src/api and src/db
   4. Create and modify code within the src folder and its children
   5. Avoid circular dependencies; the db should not import from the api, and the api should not import from the db
   6. Use relative imports instead of absolute imports
   7. The frontend shall not access the database directly; only access is through the API
3. DB
   1. Use PostgreSQL only for persistence. Do not degrade to SQLite
   2. Run PostgreSQL in a container
4. API
   1. Generate Python unit tests for validating the API
   2. Use pytest for Python unit tests
5. Frontend
   1. If there is a way to create unit tests for the frontend UI, do so
6. Management
   1. All stop, start, restart operations should take place with the manage.sh script
   2. When I ask for changes, focus on only those changes. I want to do small changes and small commits
7. Podman
   1. Use podman instead of docker
   2. Use podman-compose instead of docker-compose
   3. Use podman machine instead of docker machine
   4. Use podman machine ssh instead of docker machine ssh
   5. Use podman machine start instead of docker machine start
   6. Use podman machine stop instead of docker machine stop
   7. Use podman machine restart instead of docker machine restart
   8. Use podman machine rm instead of docker machine rm
   9. Use podman machine inspect instead of docker machine inspect
   10. Use podman machine list instead of docker machine list    
8.  No mocking. All real


## 1. Overview

The Personal Task Manager is a web-based application that allows users to create, view, update, and delete tasks. It emphasizes simplicity, clean design, and smooth developer experience using Windsurf for AI-assisted coding. The app is intended for personal use, focusing on core task management features without complex user authentication or collaboration.

### Objectives
- Demonstrate AI-assisted development with Windsurf.
- Build a functional, lightweight task manager.
- Showcase separation of concerns across frontend, API, and database layers.
- Ensure a responsive and intuitive user interface.

## 2. System Architecture

The application follows a three-tier architecture:
- **Frontend**: A reactive single-page application (SPA) built with a modern JavaScript framework (e.g., React or Vue.js).
- **API Layer**: A RESTful API built with Node.js and Express, handling business logic and communication between the frontend and database.
- **Database**: A lightweight relational database (i.e., PostgreSQL) for storing task data. run it containerized (podman)

### Tech Stack
- **Frontend**: React (with TypeScript) + Tailwind CSS for styling.
- **API**: Node.js + Express (TypeScript) for RESTful endpoints.

- **Framework**: Windsurf for AI-assisted coding (e.g., generating boilerplate, suggesting code, optimizing workflows).
- **Tools**: Vite (for frontend build), Prisma (for database ORM), ESLint + Prettier (for code quality).

## 3. Functional Requirements

### 3.1 Features
- **Task Creation**: Users can create a task with a title, optional description, due date, and priority (Low, Medium, High).
- **Task Listing**: Display all tasks in a list, sorted by due date or priority.
- **Task Update**: Edit task details (title, description, due date, priority, completion status).
- **Task Deletion**: Remove a task from the list.
- **Task Filtering**: Filter tasks by completion status (All, Completed, Pending).
- **Responsive Design**: The UI adapts to desktop and mobile devices.

### 3.2 Non-Functional Requirements
- **Performance**: API responses should be under 200ms for typical operations (assuming local DB).
- **Scalability**: While not critical, the API should handle up to 1,000 tasks efficiently.
- **Maintainability**: Code should be modular, typed, and documented, leveraging Windsurf’s AI suggestions for clean patterns.
- **Usability**: Intuitive UI with minimal learning curve.

## 4. Detailed Specifications

### 4.1 Frontend
The frontend is a React-based SPA, styled with Tailwind CSS for rapid development.

#### Components
- **TaskList**: Displays tasks in a table or card layout with columns for title, due date, priority, and status.
- **TaskForm**: A modal or inline form for creating/editing tasks.
- **FilterBar**: Dropdown or buttons to filter tasks by status.
- **Header**: Simple navigation with app title and optional theme toggle (light/dark mode).

#### Pages
- **Home**: Main page with TaskList, TaskForm, and FilterBar.

#### State Management
- Use React’s Context API or Zustand for lightweight state management.
- Store tasks locally in memory, synced with API calls.

#### Windsurf Integration
- Use Windsurf to generate component boilerplate, suggest Tailwind classes, and optimize React hooks.
- Leverage Windsurf’s AI to refactor repetitive code (e.g., form validation).

### 4.2 API Layer
The API is a RESTful service built with Express, providing endpoints for CRUD operations.

#### Endpoints
| Method | Endpoint           | Description                     | Request Body                              | Response                              |
|--------|--------------------|---------------------------------|-------------------------------------------|---------------------------------------|
| GET    | `/tasks`           | List all tasks                 | -                                         | `[{ id, title, description, dueDate, priority, completed }, ...]` |
| GET    | `/tasks/:id`       | Get a single task              | -                                         | `{ id, title, description, dueDate, priority, completed }` |
| POST   | `/tasks`           | Create a new task              | `{ title, description?, dueDate?, priority }` | `{ id, title, description, dueDate, priority, completed }` |
| PUT    | `/tasks/:id`       | Update a task                  | `{ title?,