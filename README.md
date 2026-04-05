# Async Document Processing Workflow System

A production-style full-stack application for asynchronous document processing with real-time progress tracking, built with FastAPI, React, PostgreSQL, Redis, and Celery.

## 🚀 Features

- **Document Upload**: Upload one or more documents with drag-and-drop support
- **Background Processing**: Asynchronous document processing using Celery workers
- **Real-time Progress**: Live progress tracking via WebSocket connections
- **Job Management**: View, filter, search, and sort processing jobs
- **Review & Edit**: Review extracted data and make edits before finalization
- **Export Functionality**: Export processed data as JSON or CSV
- **Retry Mechanism**: Retry failed processing jobs
- **Responsive UI**: Modern, clean interface built with React and Tailwind CSS

## 🏗️ Architecture

### Backend
- **FastAPI**: Modern Python web framework for API development
- **PostgreSQL**: Primary database for storing documents and job metadata
- **Redis**: Message broker and caching layer
- **Celery**: Distributed task queue for background processing
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and serialization

### Frontend
- **Next.js**: React framework with TypeScript
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Icon library
- **WebSocket**: Real-time communication for progress updates

### Infrastructure
- **Docker**: Containerization for consistent deployment
- **Docker Compose**: Multi-container orchestration

## 📋 Requirements

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

## 🛠️ Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd document-processing-system
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database and Redis configurations
   ```

5. **Start PostgreSQL and Redis**
   ```bash
   # Using Docker
   docker run -d --name postgres -e POSTGRES_DB=document_processor -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15
   
   docker run -d --name redis -p 6379:6379 redis:7-alpine
   ```

6. **Run database migrations** (if using Alembic)
   ```bash
   alembic upgrade head
   ```

7. **Start the FastAPI server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

8. **Start Celery worker** (in a separate terminal)
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   celery -A app.workers.celery_app worker --loglevel=info
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set environment variables**
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

## 📖 API Documentation

### Document Endpoints

- `POST /api/v1/documents/upload` - Upload documents
- `GET /api/v1/documents` - List all documents
- `GET /api/v1/documents/{id}` - Get specific document
- `DELETE /api/v1/documents/{id}` - Delete document

### Job Endpoints

- `GET /api/v1/jobs` - List processing jobs with filtering and sorting
- `GET /api/v1/jobs/{id}` - Get specific job details
- `PUT /api/v1/jobs/{id}` - Update job (review and edit)
- `POST /api/v1/jobs/{id}/retry` - Retry failed job
- `POST /api/v1/jobs/{id}/finalize` - Finalize completed job
- `GET /api/v1/jobs/export/json` - Export jobs as JSON
- `GET /api/v1/jobs/export/csv` - Export jobs as CSV

### WebSocket Endpoint

- `WS /api/v1/ws/progress/{job_id}` - Real-time progress updates

## 🔄 Processing Workflow

1. **Document Upload**: User uploads one or more documents
2. **Job Creation**: System creates processing jobs and queues them
3. **Background Processing**: Celery workers process documents asynchronously
4. **Progress Tracking**: Real-time progress updates via Redis Pub/Sub and WebSocket
5. **Review & Edit**: Users can review and edit extracted data
6. **Finalization**: Users finalize the processed results
7. **Export**: Export finalized data in various formats

### Processing Stages

1. `document_received` - Document uploaded and job created
2. `parsing_started` - Document parsing initiated
3. `parsing_completed` - Document parsing finished
4. `extraction_started` - Field extraction initiated
5. `extraction_completed` - Field extraction finished
6. `storing_results` - Storing processed results
7. `job_completed` - Processing completed successfully

## 🧪 Testing

### Running Tests

#### Backend Tests
```bash
cd backend
pytest
```

#### Frontend Tests
```bash
cd frontend
npm test
```

## 📁 Project Structure

```
document-processing-system/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       └── api.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── redis_client.py
│   │   ├── models/
│   │   │   └── document.py
│   │   ├── schemas/
│   │   │   └── document.py
│   │   ├── services/
│   │   │   ├── document_service.py
│   │   │   └── job_service.py
│   │   ├── workers/
│   │   │   ├── celery_app.py
│   │   │   └── document_processor.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   │   ├── DocumentUpload.tsx
│   │   │   ├── JobsDashboard.tsx
│   │   │   └── JobDetail.tsx
│   │   └── lib/
│   │       └── api.ts
│   ├── package.json
│   ├── Dockerfile
│   └── next.config.js
├── docker-compose.yml
└── README.md
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/document_processor
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
UPLOAD_DIR=./uploads
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 🚀 Deployment

### Production Deployment

1. **Update environment variables** with production values
2. **Set up SSL certificates** for HTTPS
3. **Configure firewall rules** appropriately
4. **Set up monitoring and logging**
5. **Configure backup strategies** for database

### Docker Production Deployment

```bash
# Build and start production containers
docker-compose -f docker-compose.prod.yml up -d
```

## 📊 Monitoring

### Health Checks

- Backend: `GET /health`
- Database: Connection status via API
- Redis: Connection status via API
- Celery: Worker status via CLI or API

### Logs

- Backend logs: Available via Docker logs or application logging
- Celery logs: Worker process logs
- Frontend logs: Browser console and server logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in environment variables
   - Verify database exists

2. **Redis Connection Error**
   - Ensure Redis is running
   - Check REDIS_URL in environment variables

3. **Celery Worker Not Processing**
   - Check if Celery worker is running
   - Verify broker connection
   - Check worker logs for errors

4. **WebSocket Connection Issues**
   - Ensure backend is accessible from frontend
   - Check firewall settings
   - Verify WebSocket endpoint is correct

5. **File Upload Issues**
   - Check upload directory permissions
   - Verify file size limits
   - Ensure sufficient disk space

### Getting Help

- Check the logs for detailed error messages
- Verify all services are running correctly
- Ensure environment variables are set correctly
- Check network connectivity between services

## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] Advanced document parsing (PDF, DOCX, etc.)
- [ ] AI-powered content extraction
- [ ] Document versioning
- [ ] Batch processing capabilities
- [ ] Advanced filtering and search
- [ ] Email notifications
- [ ] Performance analytics and reporting
- [ ] Multi-language support
- [ ] Mobile application

## 📝 Notes

- AI tools were used during development for code generation and assistance
- The document processing logic is simulated for demonstration purposes
- In production, replace with actual parsing libraries and AI services
- Ensure proper security measures before deploying to production
- Regular updates and maintenance are recommended for production use
