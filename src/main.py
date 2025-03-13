import gradio as gr
import pandas as pd
import plotly.express as px
from pathlib import Path
import logging
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

from data.csv_handler import CSVHandler
from agent.llm_agent import LLMAgent, QueryRequest

class CSVQAApp:
    def __init__(self):
        self.csv_handler = CSVHandler()
        self.llm_agent = LLMAgent()
        self.theme = gr.themes.Base()
        self.current_columns = []

    def create_interface(self):
        with gr.Blocks(theme=self.theme) as interface:
            gr.Markdown("# CSV Question Answering System")
            
            with gr.Row():
                file_input = gr.File(label="Upload CSV File")
                status = gr.Textbox(label="Status", interactive=False)
            
            with gr.Tabs():
                with gr.TabItem("Ask Questions"):
                    question = gr.Textbox(
                        label="Ask a question about your data",
                        placeholder="Example: What is the average price?"
                    )
                    submit_btn = gr.Button("Get Answer")
                    answer = gr.Textbox(label="Answer", interactive=False)
                
                with gr.TabItem("Data Preview"):
                    data_preview = gr.Dataframe()
                
                with gr.TabItem("Graph Plotting"):
                    with gr.Row():
                        with gr.Column():
                            x_col = gr.Dropdown(
                                label="X-axis Column",
                                choices=self.current_columns,  # Initialize empty
                                interactive=True,
                                value=None  # Explicitly set no default value
                            )
                            y_col = gr.Dropdown(
                                label="Y-axis Column",
                                choices=self.current_columns,  # Initialize empty
                                interactive=True,
                                value=None  # Explicitly set no default value
                            )
                            plot_type = gr.Dropdown(
                                label="Plot Type",
                                choices=["scatter", "line", "bar", "histogram"],
                                value="scatter",
                                interactive=True
                            )
                            plot_btn = gr.Button("Create Plot")
                    with gr.Row():
                        plot_output = gr.Plot(label="Visualization")

            def handle_file_upload(file):
                try:
                    if file is None:
                        return None, "Please upload a file", [], []
                    
                    success = self.csv_handler.load_csv(file.name)
                    if success:
                        df = self.csv_handler.get_dataframe()
                        self.current_columns = list(df.columns)  # Update stored columns
                        
                        # Return values for all outputs
                        return (
                            df.head(),  # Preview
                            "File loaded successfully",  # Status
                            gr.Dropdown(choices=self.current_columns),  # x_col update
                            gr.Dropdown(choices=self.current_columns)   # y_col update
                        )
                    return None, "Failed to load file", [], []
                except Exception as e:
                    logger.error(f"File upload error: {str(e)}")
                    return None, f"Error: {str(e)}", [], []

            async def handle_question(question_text):
                try:
                    if not question_text.strip():
                        return "Please enter a question"
                    
                    if self.csv_handler.df is None:
                        return "Please upload a CSV file first"
                    
                    context = self.csv_handler.get_column_info()
                    query = QueryRequest(question=question_text, context=context)
                    
                    response = await self.llm_agent.process_query(query)
                    return response
                except Exception as e:
                    logger.error(f"Question handling error: {str(e)}")
                    return f"Error: {str(e)}"

            def create_plot(x_col, y_col, plot_type):
                try:
                    if self.csv_handler.df is None:
                        return gr.Plot(visible=False)
                    
                    if not x_col:
                        return gr.Plot(visible=False)
                    
                    df = self.csv_handler.df
                    
                    # Configure common layout settings
                    layout_config = {
                        "template": "plotly_white",
                        "margin": dict(l=50, r=50, t=50, b=50),
                        "hoverlabel": dict(bgcolor="white", font_size=12)
                    }
                    
                    if plot_type == "histogram":
                        # Single column distribution
                        fig = px.histogram(
                            df, 
                            x=x_col,
                            title=f"Distribution of {x_col}",
                            opacity=0.7,
                            nbins=30  # Adjust number of bins
                        )
                        fig.update_layout(
                            **layout_config,
                            yaxis_title="Frequency",
                            bargap=0.1
                        )
                        
                    elif plot_type == "scatter":
                        # Relationship between two numeric columns
                        if not y_col:
                            return gr.Plot(visible=False)
                        fig = px.scatter(
                            df,
                            x=x_col,
                            y=y_col,
                            title=f"Relationship: {y_col} vs {x_col}",
                            opacity=0.6,
                            trendline="ols"  # Add trend line
                        )
                        fig.update_layout(**layout_config)
                        
                    elif plot_type == "bar":
                        # Aggregated bar chart
                        if not y_col:
                            return gr.Plot(visible=False)
                        agg_df = df.groupby(x_col)[y_col].mean().reset_index()
                        fig = px.bar(
                            agg_df,
                            x=x_col,
                            y=y_col,
                            title=f"Average {y_col} by {x_col}",
                            color=y_col  # Color bars by value
                        )
                        fig.update_layout(
                            **layout_config,
                            showlegend=False
                        )
                        
                    elif plot_type == "line":
                        # Time series or ordered data
                        if not y_col:
                            return gr.Plot(visible=False)
                        fig = px.line(
                            df.sort_values(x_col),  # Sort by x-axis
                            x=x_col,
                            y=y_col,
                            title=f"Trend: {y_col} over {x_col}",
                            markers=True  # Show points
                        )
                        fig.update_layout(**layout_config)
                    
                    # Common updates for all plots
                    fig.update_xaxes(title_text=x_col)
                    fig.update_yaxes(title_text=y_col if plot_type != "histogram" else "Frequency")
                    
                    return fig
                except Exception as e:
                    logger.error(f"Plot creation error: {str(e)}")
                    return gr.Plot(visible=False)

            file_input.change(
                fn=handle_file_upload,
                inputs=[file_input],
                outputs=[data_preview, status, x_col, y_col]
            )
            
            submit_btn.click(
                handle_question,
                inputs=[question],
                outputs=[answer]
            )
            
            plot_btn.click(
                create_plot,
                inputs=[x_col, y_col, plot_type],
                outputs=[plot_output]
            )

        return interface

if __name__ == "__main__":
    try:
        app = CSVQAApp()
        interface = app.create_interface()
        interface.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False
        )
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
        raise