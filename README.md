# Task List App - Django REST Framework + Vue

A task management application built with Django REST Framework backend and Vue + TypeScript frontend.

## Project Overview

This project is inspired by my [Flask-based task list API](https://github.com/imlyj5/task-list-api/tree/main) and a collaborative [React frontend project](https://github.com/daniellew712/task-list-front-end/tree/wave5_JL). The styling and design elements are inspired by another of my group project's [fansite](https://github.com/dniph/group-fansite).

For practice purpose, I tried to use Django REST Framework + Vue and maintain the same functionality as the original Flask + React version.

## Quick Start

### Backend Setup

1. **Navigate to backend:**
   ```bash
   cd backend
   ```

2. **Set up virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp env.example .env
   # Edit .env with your database settings and slack token
   ```

4. **Set up database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run Django server:**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

## API Endpoints

### Tasks
- `GET /api/tasks/` - Get all tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Get specific task
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `PATCH /api/tasks/{id}/mark_complete/` - Mark task complete
- `PATCH /api/tasks/{id}/mark_incomplete/` - Mark task incomplete

### Goals
- `GET /api/goals/` - Get all goals
- `POST /api/goals/` - Create new goal
- `GET /api/goals/{id}/` - Get specific goal
- `PUT /api/goals/{id}/` - Update goal
- `DELETE /api/goals/{id}/` - Delete goal
- `POST /api/goals/{id}/tasks/` - Assign tasks to goal
- `GET /api/goals/{id}/tasks_list/` - Get tasks for goal
