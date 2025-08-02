# Python DevOps Project

This project demonstrates a robust Python application setup with a focus on modern DevOps practices, including containerization, local development orchestration, and continuous integration/continuous deployment (CI/CD).

## Features

*   **FastAPI Application:** A lightweight and high-performance web framework for building APIs.
*   **System Monitoring:** Includes agents for monitoring system health and processes.
*   **Containerization with Docker:** Ensures consistent environments across development, testing, and production.
*   **Local Development with Docker Compose:** Simplifies running the application and its dependencies locally.
*   **CI/CD Pipeline with GitHub Actions:** Automates testing and Docker image building upon code changes.

## DevOps Explained

This project is engineered with a strong emphasis on DevOps principles to streamline development, testing, and deployment.

### 1. Containerization (Docker)

The `Dockerfile` defines the environment for the application. It ensures that the application runs consistently regardless of where it's deployed.

*   **Base Image:** Uses `python:3.9-slim-buster` for a lightweight Python environment.
*   **Working Directory:** Sets `/app` as the working directory inside the container.
*   **PythonPath:** Configures `PYTHONPATH` to allow Python to find modules within the `src` directory.
*   **Dependency Management:** Installs all required Python packages from `requirements.txt`.
*   **Port Exposure:** Exposes port `8001` for the FastAPI application.
*   **Application Entrypoint:** Runs the FastAPI application using `uvicorn`.

### 2. Local Development Orchestration (Docker Compose)

The `docker-compose.yml` file simplifies the local development workflow by defining how the application's services should be run.

*   **Service Definition:** Defines a `web` service that builds from the `Dockerfile`.
*   **Port Mapping:** Maps host port `8001` to container port `8001`, making the application accessible locally.
*   **Volume Mounting:** Mounts the local project directory into the container, enabling live code changes without rebuilding the image.
*   **Command Override:** Explicitly sets the command to run `uvicorn`, ensuring the application starts correctly.

### 3. Continuous Integration/Continuous Deployment (CI/CD) with GitHub Actions

The `.github/workflows/ci-cd.yml` file defines an automated pipeline that triggers on `push` and `pull_request` events to the `main` branch.

*   **Checkout Code:** Fetches the repository content.
*   **Set up Python:** Configures the Python environment.
*   **Install Dependencies:** Installs both production (`requirements.txt`) and development (`requirements-dev.txt`) dependencies, including `pytest` and `httpx` for testing.
*   **Install Docker Compose CLI:** Downloads and installs the `docker-compose` CLI plugin, ensuring it's available in the runner environment.
*   **Run Tests:** Executes unit and integration tests using `pytest`. This step is crucial for maintaining code quality and catching regressions early.
*   **Build Docker Image:** Builds the Docker image for the application.
*   **Run Docker Compose (Optional for Integration Tests):** Starts the application using Docker Compose for potential integration testing within the CI environment.
*   **Stop Docker Compose (Optional):** Cleans up Docker Compose services after testing.

This pipeline ensures that every code change is automatically validated, and a deployable Docker image is built, ready for further deployment stages.

## How to Run Locally

To run this project locally using Docker Compose:

1.  **Ensure Docker is installed:** Make sure Docker and Docker Compose are installed on your system.
2.  **Navigate to the project root:**
    ```bash
    cd /path/to/your/project
    ```
3.  **Start the application:**
    ```bash
    docker-compose up --build -d
    ```
    This command will build the Docker image (if not already built or if changes are detected) and start the application in detached mode.
4.  **Access the application:**
    The application should be accessible in your web browser at `http://localhost:8001`.

## Testing

To run the tests locally:

1.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt -r requirements-dev.txt
    ```
2.  **Run pytest:**
    ```bash
    pytest tests/
    ```

## Project Structure

```
.
├── .github/                 # GitHub Actions CI/CD workflows
│   └── workflows/
│       └── ci-cd.yml        # CI/CD pipeline definition
├── src/                     # Application source code
│   ├── main.py              # Main FastAPI application entry point
│   ├── api/                 # API routes
│   ├── config/              # Application configuration
│   ├── monitoring/          # System monitoring agents and collectors
│   └── utils/               # Utility functions (e.g., logger)
├── tests/                   # Unit and integration tests
│   ├── test_agents.py
│   └── test_api.py
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Docker Compose configuration for local development
├── requirements.txt         # Production Python dependencies
├── requirements-dev.txt     # Development Python dependencies (for testing, linting, etc.)
└── README.md                # Project README (this file)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
