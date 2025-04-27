# Tic Tac Toe Web Application

A modern web-based Tic Tac Toe game built with Flask, featuring user authentication, real-time gameplay, and player statistics.

## Features

- User authentication (registration and login)
- Real-time multiplayer gameplay
- Game history tracking
- Player statistics and profiles
- Responsive design
- Modern UI/UX

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tic-tac-toe.git
   cd tic-tac-toe
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```bash
   flask db upgrade
   ```

## Running the Application

```bash
flask run
```

The application will be available at `http://localhost:5000`

## Project Structure

```
tic-tac-toe/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── user.py
│   │   └── game.py
│   ├── views/
│   │   ├── main.py
│   │   ├── auth.py
│   │   └── game.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── profile.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── game/
│   │       ├── lobby.html
│   │       └── play.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── game.js
├── tests/
├── config.py
├── requirements.txt
└── README.md
```

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_game.py

# Run with coverage
pytest --cov=app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 