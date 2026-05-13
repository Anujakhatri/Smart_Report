# 🇳🇵 Smart Report NP

A civic issue reporting platform for Nepal. Citizens can report road potholes, water pipe leaks, street light outages, and other public infrastructure problems directly from their phone.

## Features

- 📷 Auto camera open to capture issue photo
- 📍 GPS auto-capture location (no typing address)
- 🎙 Voice to text for description
- 🗺 Add nearest landmark
- 📧 Email notification when issue is received
- ✅ Get notified when issue is fixed

## Tech Stack

**Backend**
- Python / Django
- Django REST Framework
- JWT Authentication
- PostgreSQL



## Project Structure

```
Smart-Report/
├── backend/          # Django REST API
│   ├── reports/      # Core app
│   ├── users/        # Auth
│   └── manage.py
└── frontend/         # React app(as planning)
    └── src/
```

## Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/subekshya-s/Smart_Report.git
cd Smart_Report

# Create and activate venv
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```


```

## Issue Categories

| Category | Description |
|----------|-------------|
| 🕳 Road | Pothole, road damage |
| 💧 Water | Pipe leak, supply issue |
| 💡 Street Light | Outage, damage |
| 🗑 Garbage | Waste, illegal dumping |
| ⚡ Electricity | Power line issue |

## Contributors

- [@subekshya-s](https://github.com/subekshya-s)
- [@anujakhatri](https://github.com/Anujakhatri)

## License

MIT
