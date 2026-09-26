# Binance Market TUI

A real-time cryptocurrency market monitoring application built with **Python**, **Binance WebSockets**, **Textual**, and **Docker**.

This project extends a basic object-oriented WebSocket client into an interactive terminal application. It demonstrates how asynchronous WebSocket communication can be integrated with a terminal user interface and packaged into a Docker container for deployment.

## Project Overview

The application connects to the Binance WebSocket API and displays live cryptocurrency market data inside an interactive Textual terminal interface.

Users can dynamically subscribe and unsubscribe from market streams using the interface while the application maintains the WebSocket connection and processes incoming market data asynchronously.

The project focuses on:

- Object-oriented WebSocket client design
- Asynchronous programming with `asyncio`
- Real-time market data streaming
- Dynamic stream subscription and unsubscription
- Integration of asynchronous networking with a Textual TUI
- Separation of application, GUI, and WebSocket logic
- Docker containerization and deployment

## Tech Stack

- **Python 3.14**
- **websockets 16.0**
- **Textual 8.2.8**
- **Binance WebSocket API**
- **Docker**

## Project Structure

```text
binance-market-tui/
├── config.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── gui/
│   ├── app.py
│   └── app.tcss
├── logs/
├── main.py
├── README.md
├── requirements.txt
└── src/
    ├── __init__.py
    └── binance_client.py
```

### `main.py`

Application entry point.

Starts the Textual application and initializes the project.

### `src/binance_client.py`

Contains the object-oriented Binance WebSocket client responsible for:

- Establishing the WebSocket connection
- Receiving real-time market data
- Managing subscriptions
- Managing unsubscriptions
- Handling WebSocket communication

### `gui/app.py`

Contains the Textual application and connects the user interface to the WebSocket client.

It manages:

- Market data display
- Symbol selection
- Subscription controls
- Connection state
- Stream state
- Interaction between the GUI and asynchronous WebSocket client

### `gui/app.tcss`

Defines the layout and styling of the Textual terminal interface.

### `config.py`

Contains application configuration such as the Binance WebSocket endpoint and other project settings.

## Architecture

The application separates WebSocket communication from presentation logic.

```text
                Binance WebSocket API
                         │
                         │
                         ▼
              BinanceWebSocketClient
                src/binance_client.py
                         │
                         │
                  Async market data
                         │
                         ▼
                   BinanceApp
                    gui/app.py
                         │
                         ▼
                   Textual TUI
```

This separation allows the WebSocket client to handle networking independently while the Textual application handles presentation and user interaction.

## Installation

Clone the repository:

```bash
git clone https://github.com/mahmoud8999/binance-market-tui
cd binance-market-tui
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Run:

```bash
python main.py
```

The Textual interface will open directly in the terminal.

## Running with Docker

Build the Docker image:

```bash
docker build -t binance-market-tui .
```

Run the container:

```bash
docker run --rm -it binance-market-tui
```

The `-it` options are required because Textual runs as an interactive terminal application.

`--rm` automatically removes the container after the application exits.

## Docker Deployment

The project can be deployed to a remote Linux server or VPS without installing the Python dependencies directly on the host.

Only Docker is required on the server.

```bash
git clone <repository-url>
cd binance-market-tui

docker build -t binance-market-tui .
docker run --rm -it binance-market-tui
```

This provides the same Python environment and application dependencies regardless of the host system.

## Dependencies

The primary Python dependencies are:

```text
websockets==16.0
textual==8.2.8
```

Install them using:

```bash
pip install -r requirements.txt
```

## Learning Objectives

This project was built as part of a Data Engineering project portfolio to practice the integration of several concepts in a single application:

- WebSocket communication
- Python object-oriented programming
- `asyncio`
- Event-driven programming
- Real-time data ingestion
- Terminal user interfaces
- Application modularization
- Dependency management
- Docker image creation
- Containerized deployment

## Project Progression

This project builds on an earlier **Binance WebSocket Client** project.

The first project focused primarily on understanding WebSocket communication and implementing a reusable object-oriented WebSocket client.

This project takes the next step by integrating that knowledge into a complete application with:

```text
WebSocket API
     ↓
Async Python Client
     ↓
Application Logic
     ↓
Textual TUI
     ↓
Docker Container
     ↓
VPS Deployment
```

The result is a small end-to-end real-time data application rather than a standalone WebSocket client.

## License

This project is intended for educational and portfolio purposes.
