# Ember Homes AI Voice Agent Plan

## Project Overview
Create an AI voice agent for Ember Homes inbound call service to handle customers wanting to sell their property.

## Agent Behavior
- **Agent Name**: Aria
- **Voice Profile**: Female, Alpharetta Georgia accent
- **Scenario**: Property seller inquiry
- **Deployment**: Web UI testing → Twilio integration (future)
- **Flow**:
  1. Agent speaks first: "Thanks for calling Ember Homes, I am Aria, I am here to help you. Could I start by asking your name?"
  2. Ask for customer name
  3. Ask for property address to sell
  4. Ask for best phone number for follow-up
  5. Ask for email address
  6. Closing: "Thank you. Our team member will review your details and contact you in one business day."
  7. End call

## Project Structure & Architecture

### Clean Architecture Principles
- **Domain-Driven Design**: Separate business logic from infrastructure
- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Single Responsibility**: Each component has one reason to change
- **Interface Segregation**: Small, focused interfaces
- **Professional Industry Standards**: PEP 8 compliance, type hints, comprehensive testing

### Directory Structure
```
vapi-agent/
├── backend/
│   ├── .venv/                    # Virtual environment
│   ├── src/
│   │   ├── domain/              # Business logic & entities
│   │   │   ├── entities/
│   │   │   ├── services/
│   │   │   └── repositories/
│   │   ├── infrastructure/      # External integrations
│   │   │   ├── vapi/
│   │   │   ├── google_sheets/
│   │   │   └── websocket/
│   │   ├── application/         # Use cases & orchestration
│   │   │   ├── use_cases/
│   │   │   └── dto/
│   │   └── presentation/        # API layer
│   │       ├── api/
│   │       └── websockets/
│   ├── tests/                   # Comprehensive test suite
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   ├── requirements/            # Dependency management
│   │   ├── base.txt
│   │   ├── development.txt
│   │   └── production.txt
│   ├── pyproject.toml          # Modern Python packaging
│   ├── manage.py
│   └── .env.example
├── frontend/
│   ├── .venv/                  # Node.js virtual environment
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/             # Page components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── services/          # API services
│   │   ├── types/             # TypeScript definitions
│   │   └── utils/             # Utility functions
│   ├── tests/                 # Frontend test suite
│   ├── package.json
│   └── .env.example
├── scripts/                   # Development & deployment scripts
├── docker-compose.yml         # Local development environment
└── readme.md
```

### Documentation Files
- Documentation must be kept in the allowed set only:
  - `readme.md`
  - `overview.md`
  - `architecture.md`
  - `techstacks.md`
  - `setup.md`
  - `changes.md`

## Development Environment Setup

### Backend Setup
1. **Python Environment**:
   ```bash
   python -m venv backend/.venv
   source backend/.venv/bin/activate  # Linux/Mac
   # backend\.venv\Scripts\activate   # Windows
   pip install -r backend/requirements/development.txt
   ```

2. **Environment Configuration**:
   - Copy `backend/.env.example` to `backend/.env`
   - Configure Vapi API keys
   - Set up Google Sheets credentials
   - Database configuration (SQLite for development)

3. **Database Setup**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

### Frontend Setup
1. **Node.js Environment**:
   ```bash
   cd frontend
   npm install
   # or: npx create-next-app@latest . --typescript --tailwind --eslint
   ```

2. **Environment Configuration**:
   - Copy `frontend/.env.example` to `frontend/.env.local`
   - Configure API endpoints
   - Set up WebSocket connections
   - Add Vapi Web SDK keys:
     ```
     NEXT_PUBLIC_VAPI_PUBLIC_KEY=your_public_key
     NEXT_PUBLIC_VAPI_ASSISTANT_ID=your_assistant_id
     ```

### Webhook Forwarding (Local Development)
- **Recommended**: Use Vapi CLI to forward webhooks to localhost
  ```bash
  # Install Vapi CLI globally
  npm install -g @vapi-ai/cli
  
  # Forward webhooks to local Django endpoint
  vapi listen --forward-to http://127.0.0.1:8000/api/vapi/webhook/
  ```
- Configure webhook URL in Vapi Dashboard to the CLI-provided URL

### Development Tools
- **Code Quality**: Black, isort, flake8, mypy for backend
- **Testing**: pytest (backend), Jest + React Testing Library (frontend)
- **Pre-commit hooks**: husky + lint-staged
- **Documentation**: Sphinx for backend, Storybook for frontend
- **Containerization**: Docker for consistent development environment

## Technology Stack
- **Backend**: Python 3.12 + Django + SQLite
- **Voice API**: Vapi API for agent integration
- **Phone Service**: Twilio (future integration)
- **Data Storage**: Google Sheets for leads
- **Frontend**: Next.js + TypeScript + WebSockets
- **Development**: Docker, pre-commit hooks, comprehensive testing

## Architecture Components

### Backend (Django)
- Django REST API for lead management
- Vapi webhook handler for call events
- Google Sheets integration service
- Lead data model and validation
- WebSocket support for real-time updates
- SQLite database for local development

### Voice Agent (Vapi)
- Custom voice configuration
- Conversation flow management
- Real-time call handling
- Webhook integration with Django backend

### Data Layer
- Google Sheets API integration
- Lead data structure (name, property_address, phone, email, timestamp)
- Data validation and error handling

### Frontend (Next.js)
- **Home Page**: Start call button + live conversation text display
- **Calls Page** (/calls): Call list with detailed call view
- **Analytics Panel** (/analytics): Interactive charts and metrics
- Real-time WebSocket integration
- Live conversation transcription during calls
- Call history and management interface

## Implementation Steps

### Phase 1: Backend Setup 
1. Initialize Django project with Python 3.12 + SQLite
2. Set up Vapi API integration with existing account
3. Configure Google Sheets API for new spreadsheet creation
4. Create lead management models and serializers
5. Implement webhook handlers for call events
6. Set up WebSocket support for real-time updates

### Phase 2: Voice Agent Configuration 
1. Configure Aria voice profile (female, Alpharetta Georgia accent)
2. Set up web UI testing environment (no phone service initially)
3. Configure conversation flow script
4. Test agent behavior and call handling via web interface
5. Implement webhook integration with Django backend

### Phase 3: Frontend Development 
1. Initialize Next.js project with WebSocket support
2. Create home page with start call button and live conversation display
3. Implement /calls page with call list and detailed call views
4. Build /analytics panel with interactive charts
5. Add real-time conversation transcription during calls
6. Implement call history and management interface

### Phase 4: Integration & Testing (In Progress)
1. End-to-end testing of call flow via web UI (Vapi Web SDK)
2. Data pipeline validation (Django → Google Sheets)
3. WebSocket real-time updates testing
4. Performance optimization for localhost deployment
5. Prepare for future Twilio integration

### Phase 5: Webhook Reachability & Production Readiness (Current)
1. Set up Vapi CLI forwarding for local webhook testing
2. Verify bind flow: Vapi call ID ↔ local Call ID
3. Harden Django configuration (env vars, secrets, CORS)
4. Verify Google Sheets credentials and lead storage
5. Frontend production build verification

## Data Flow
1. User clicks start call → Frontend connects to backend `/ws/voice/` → Backend creates local Call
2. Frontend starts Vapi Web SDK session → Vapi call ID is returned
3. Frontend sends `{type:"bind", vapi_call_id}` to backend → Backend links Vapi call to local Call
4. Vapi agent handles conversation with customer
5. Real-time transcription displayed via Vapi Web SDK directly in UI
6. Vapi sends webhook → Django processes transcript events and stores them
7. Django broadcasts transcript events via Channels to the same WebSocket session
8. Frontend updates → Real-time call display and analytics
9. Lead data flows to Google Sheets (when structured lead data is captured)

## Deployment Environment
- **Development**: Localhost only
- **Database**: SQLite for local development
- **Future**: Twilio integration for telephony services

## Success Metrics
- Call completion rate
- Lead data accuracy
- Real-time transcription accuracy
- Response time for follow-up
- User interface responsiveness