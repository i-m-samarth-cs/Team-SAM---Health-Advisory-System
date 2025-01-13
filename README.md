# Team Sam - Health Advisory System

A real-time health monitoring and advisory system built with Pathway and Streamlit.

PPT - https://my.visme.co/view/ojk38097-health-advisory-system-using-pathway-and-rag-model
Video demo - https://drive.google.com/file/d/18fBcBoBcjEKW0PABYutXmMzzAlyfvLO1/view?usp=drive_link
Github Repo Link -  
## Features

- Real-time health data monitoring
- Personalized health recommendations using RAG
- Interactive dashboard with real-time updates
- Anomaly detection and alerts
- Multi-user support
- Historical data visualization

## Setup Options

You can run this application in two ways:
1. Direct installation (Recommended for beginners)
2. Docker installation (Optional, for containerized deployment)

### Option 1: Direct Installation

1. Ensure Python 3.9+ is installed:
```bash
python --version
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/health-advisory.git
cd health-advisory
```

3. Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a .env file:
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your OpenAI API key
# OPENAI_API_KEY=your_api_key_here
```

6. Run the application:
```bash
streamlit run src/ui/app.py
```

The application will be available at http://localhost:8501

### Option 2: Docker Installation (Optional)

If you prefer using Docker:

1. Install Docker from [Docker's official website](https://docs.docker.com/get-docker/)
2. Follow Docker setup instructions in DOCKER.md

## Project Structure

```
health_advisory/
├── src/
│   ├── data/
│   │   ├── mock_data_generator.py
│   │   └── health_guidelines.json
│   ├── pathway_processing/
│   │   ├── stream_processor.py
│   │   └── rag_pipeline.py
│   ├── ui/
│   │   ├── app.py
│   │   └── components/
│   └── utils/
│       └── helpers.py
├── .env
├── requirements.txt
└── README.md
```

## Troubleshooting Common Issues

### Package Installation Issues

If you encounter package installation issues:

1. Upgrade pip:
```bash
python -m pip install --upgrade pip
```

2. Install packages individually:
```bash
pip install streamlit
pip install pathway
pip install openai
# ... and so on
```

3. If you get permission errors:
- On Windows: Run command prompt as administrator
- On Linux/Mac: Use `sudo pip install` or add `--user` flag

### Application Won't Start

1. Check Python version:
```bash
python --version  # Should be 3.9+
```

2. Verify environment variables:
```bash
# On Windows
echo %OPENAI_API_KEY%

# On Linux/Mac
echo $OPENAI_API_KEY
```

3. Check port availability:
- Ensure nothing else is running on port 8501
- To use a different port:
```bash
streamlit run src/ui/app.py --server.port 8502
```

### Performance Issues

If the application runs slowly:

1. Close other resource-intensive applications
2. Monitor system resources:
   - CPU usage
   - Memory usage
   - Network connectivity

3. Reduce data retention period in the application settings

## Development Setup

For developers:

1. Install additional development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Set up pre-commit hooks:
```bash
pre-commit install
```

3. Run tests:
```bash
pytest tests/
```

## Deployment Options

1. Local Machine (Development):
- Follow the direct installation instructions above
- Suitable for development and testing

2. Cloud Platforms (Production):
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Platform
- Azure App Service

Deployment guides for each platform are available in the `docs/deployment` directory.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For support:
1. Check the [FAQ](docs/FAQ.md)
2. Create an issue in the repository
3. Contact the maintainers

## License

This project is licensed under the MIT License - see the LICENSE file for details.