# CSV Question-Answering System

An intelligent CSV data analysis system powered by LLM technology that allows users to analyze CSV data through natural language questions and data visualization.

## Features

- **CSV File Upload**: Support for loading and parsing CSV files
- **Natural Language Queries**: Ask questions about your data in plain English
- **Interactive Data Visualization**: Create various types of plots:
    - Scatter plots with trend lines
    - Line charts for time series data
    - Bar charts for aggregated data 
    - Histograms for distributions
- **Data Preview**: View the loaded dataset in a tabular format
- **Error Handling**: Robust error handling and logging

## Technology Stack

- **Python 3.13**
- **Core Dependencies**:
    - gradio (5.20.1) - Web interface framework
    - pandas (2.2.3) - Data manipulation
    - plotly (6.0.0) - Interactive visualizations
    - ollama (0.4.7) - LLM integration
    - pydantic (2.10.6) - Data validation

## Project Structure

```
csv-qa-app/
├── src/
│   ├── agent/
│   │   └── llm_agent.py    # LLM integration
│   ├── data/
│   │   └── csv_handler.py  # CSV processing
│   ├── visualization/
│   │   └── plotter.py      # Plotting utilities
│   └── main.py            # Application entry point
├── tests/
│   └── test_plotter.py    # Unit tests
└── README.md
```

## Installation

1. Create a virtual environment:
```bash
conda create -n gradio_env python=3.13
conda activate gradio_env
```

2. Install dependencies:
```bash
pip install gradio pandas plotly ollama pydantic
```

## Usage

1. Start the application:
    -run the Gradio first:
        either download app or run on other terminal:
        using commands: ```gradio serve```
    -then
        ```python src/main.py```


2. Access the interface at `http://127.0.0.1:7860`

3. Upload a CSV file and:
     - Ask questions about your data
     - Create visualizations
     - Preview the dataset

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

