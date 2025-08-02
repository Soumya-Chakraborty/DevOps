# Python DevOps Project 🚀

[![CI/CD Status](https://github.com/Soumya-Chakraborty/DevOps/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Soumya-Chakraborty/DevOps/actions/workflows/ci-cd.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project showcases a robust Python application setup, emphasizing modern DevOps practices for seamless development, testing, and deployment. ✨

## 🌟 Features

*   **FastAPI Application:** A lightweight and high-performance web framework for building APIs. ⚡
*   **System Monitoring:** Includes agents for monitoring system health and processes. 📊
*   **Containerization with Docker:** Ensures consistent environments across development, testing, and production. 🐳
*   **Local Development with Docker Compose:** Simplifies running the application and its dependencies locally. 🛠️
*   **CI/CD Pipeline with GitHub Actions:** Automates testing and Docker image building upon code changes. 🚀

## 🌐 DevOps Philosophy

This project is meticulously engineered with a strong emphasis on DevOps principles to streamline the entire software development lifecycle.

### 1. Containerization (Docker) 📦

The `Dockerfile` serves as the blueprint for creating a consistent and isolated environment for the application. This ensures that the application behaves identically across various stages, from development to production.

*   **Base Image:** Utilizes `python:3.9-slim-buster` for a lean and efficient Python runtime. 🐍
*   **Working Directory:** Sets `/app` as the primary working directory within the container.
*   **PythonPath:** Configures `PYTHONPATH` to enable seamless module imports from the `src` directory.
*   **Dependency Management:** Installs all necessary Python packages as specified in `requirements.txt`.
*   **Port Exposure:** Exposes port `8001`, making the FastAPI application accessible.
*   **Application Entrypoint:** Defines the command to run the FastAPI application using `uvicorn`.

### 2. Local Development Orchestration (Docker Compose) 🏡

The `docker-compose.yml` file simplifies the local development experience by defining and orchestrating the application's services.

*   **Service Definition:** Declares a `web` service that is built from the `Dockerfile`.
*   **Port Mapping:** Maps host port `8001` to the container's port `8001`, allowing easy access to the application from your local machine.
*   **Volume Mounting:** Mounts the local project directory into the container, enabling instant code changes without requiring image rebuilds.
*   **Command Override:** Explicitly sets the `uvicorn` command to ensure the application starts correctly within the Docker environment.

### 3. Continuous Integration/Continuous Deployment (CI/CD) with GitHub Actions 🚀

The `.github/workflows/ci-cd.yml` file orchestrates an automated pipeline that springs into action on every `push` and `pull_request` to the `main` branch.

*   **Checkout Code:** Retrieves the latest code from the repository.
*   **Set up Python:** Configures the appropriate Python environment for the workflow.
*   **Install Dependencies:** Installs both production (`requirements.txt`) and development (`requirements-dev.txt`) dependencies, including essential testing libraries like `pytest` and `httpx`.
*   **Install Docker Compose CLI:** Downloads and installs the `docker-compose` CLI plugin, ensuring it's available for Docker operations within the runner.
*   **Run Tests:** Executes comprehensive unit and integration tests using `pytest`. This critical step helps maintain code quality and identifies regressions early in the development cycle. ✅
*   **Build Docker Image:** Constructs the Docker image for the application, preparing it for deployment.
*   **Run Docker Compose (Optional for Integration Tests):** Optionally starts the application using Docker Compose within the CI environment for more extensive integration testing.
*   **Stop Docker Compose (Optional):** Cleans up any running Docker Compose services after the tests are complete.

This automated pipeline guarantees that every code change undergoes rigorous validation, and a deployable Docker image is always ready for subsequent deployment stages. 🌟

## 🏃‍♀️ How to Run Locally

To get this project up and running on your local machine using Docker Compose:

1.  **Ensure Docker is installed:** Verify that Docker and Docker Compose are installed on your system. If not, follow the official Docker installation guide. 🐳
2.  **Navigate to the project root:**
    ```bash
    cd /path/to/your/project
    ```
3.  **Start the application:**
    ```bash
    docker-compose up --build -d
    ```
    This command will build the Docker image (if necessary) and launch the application in detached mode (runs in the background).
4.  **Access the application:**
    Open your web browser and navigate to `http://localhost:8001`. You should see your FastAPI application running! 🎉

## 🧪 Testing

To execute the project's tests locally:

1.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt -r requirements-dev.txt
    ```
2.  **Run pytest:**
    ```bash
    pytest tests/
    ```

## 📂 Project Structure

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

## 👋 Contributing

Contributions are highly encouraged! Feel free to open an issue or submit a pull request. Your input helps make this project even better. 💖

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.