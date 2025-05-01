# SHL Assessment Recommendation System - Solution Approach

## Overview
A FastAPI-based recommendation system that suggests appropriate SHL assessments based on natural language queries or job descriptions.

## Architecture
- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **AI Integration**: Google Gemini API
- **Deployment**: Gunicorn + Uvicorn

## Key Components

### 1. Core Recommendation Engine
- Implements weighted keyword matching system
- Considers multiple factors:
  - Test type relevance
  - Description matching
  - Query context
  - Duration preferences
  - Remote testing capability
  - Adaptive IRT support

### 2. API Layer
- RESTful endpoints for recommendations
- Health check monitoring
- CORS support for web integration
- Error handling and logging

### 3. Assessment Database
- Structured assessment metadata
- Key attributes:
  - Name and URL
  - Test type
  - Duration
  - Remote testing capability
  - Adaptive IRT support
  - Description

## Technical Implementation

### API Endpoint
```http
POST /api/recommend
Content-Type: application/json

{
    "query": "text query",
    "max_results": 10
}
```

### Scoring System
1. Test type match (highest weight)
2. Description keyword matching
3. Query context analysis
4. Duration optimization
5. Remote testing bonus
6. Adaptive IRT bonus

## Deployment
- Production-ready configuration
- Gunicorn worker management
- Environment variable support
- Logging and monitoring
- Health check endpoints

## Security
- CORS configuration
- Environment variable management
- Error handling
- Input validation

## Future Enhancements
1. Machine learning integration
2. User feedback loop
3. Performance analytics
4. A/B testing support
5. Multi-language support

## Usage Example
```python
import requests

response = requests.post(
    "http://localhost:8000/api/recommend",
    json={
        "query": "leadership assessment",
        "max_results": 5
    }
)
print(response.json())
``` 