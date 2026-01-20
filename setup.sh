#!/bin/bash

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Create .env file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please update with your credentials."
fi

echo "Backend setup complete!"

# Install frontend dependencies
cd ../frontend
npm install

echo "Frontend setup complete!"

echo "
Setup complete! To run the application:

1. Backend:
   cd backend
   python main.py

2. Frontend (in another terminal):
   cd frontend
   npm run dev

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
"
