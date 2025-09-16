#!/bin/bash

# EduSync Setup Script
# This script helps you set up the EduSync application quickly

echo "🎓 EduSync - Smart Attendance & Learning Platform Setup"
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo "✅ Prerequisites check passed!"
echo ""

# Setup Backend
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

echo "✅ Backend setup complete!"
echo ""

# Setup Frontend
echo "🔧 Setting up Frontend..."
cd ../frontend

# Install Node.js dependencies
npm install

echo "✅ Frontend setup complete!"
echo ""

echo "🎉 Setup completed successfully!"
echo ""
echo "To start the application:"
echo "1. Start Backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "2. Start Frontend: cd frontend && npm start"
echo ""
echo "Or use Docker: docker-compose up --build"
echo ""
echo "Access the app at: http://localhost:3000"
echo "API docs at: http://localhost:8000/docs"