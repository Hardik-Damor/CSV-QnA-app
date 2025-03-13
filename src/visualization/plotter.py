import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Literal, Dict, Any
import pandas as pd
import logging
import numpy as np

logger = logging.getLogger(__name__)

class Plotter:
    PLOT_TYPES = Literal['scatter', 'line', 'bar', 'box', 'histogram']
    
    @staticmethod
    def create_plot(
        df: pd.DataFrame, 
        x_col: str, 
        y_col: str, 
        plot_type: str = 'scatter',
        custom_layout: Optional[Dict[str, Any]] = None
    ) -> Optional[go.Figure]:
        """
        Create a plotly figure based on the specified columns and plot type.
        
        Args:
            df: Input DataFrame with housing data
            x_col: Column name for x-axis
            y_col: Column name for y-axis (optional for histogram)
            plot_type: Type of visualization
            custom_layout: Optional custom layout parameters
            
        Returns:
            Optional[go.Figure]: Plotly figure object or None if error occurs
        """
        try:
            # Input validation
            if df is None or df.empty:
                raise ValueError("DataFrame is empty or None")
                
            if x_col not in df.columns:
                raise ValueError(f"Column {x_col} not found in DataFrame")
                
            # Handle missing values
            df_clean = df.dropna(subset=[x_col])
            if len(df_clean) < len(df):
                logger.warning(f"Removed {len(df) - len(df_clean)} rows with missing values")
                
            # Create appropriate plot
            if plot_type == 'histogram':
                fig = px.histogram(
                    df_clean, 
                    x=x_col, 
                    title=f'Distribution of {x_col}',
                    nbins=30,
                    marginal='box'
                )
            else:
                if y_col not in df.columns:
                    raise ValueError(f"Column {y_col} not found in DataFrame")
                    
                df_clean = df_clean.dropna(subset=[y_col])
                
                if plot_type == 'scatter':
                    fig = px.scatter(
                        df_clean, 
                        x=x_col, 
                        y=y_col,
                        title=f'{y_col} vs {x_col}',
                        trendline="ols",
                        trendline_color_override="red",
                        opacity=0.6
                    )
                elif plot_type == 'line':
                    fig = px.line(
                        df_clean, 
                        x=x_col, 
                        y=y_col,
                        title=f'{y_col} over {x_col}',
                        markers=True
                    )
                elif plot_type == 'bar':
                    fig = px.bar(
                        df_clean, 
                        x=x_col, 
                        y=y_col,
                        title=f'{y_col} by {x_col}',
                        color_discrete_sequence=['indianred']
                    )
                elif plot_type == 'box':
                    fig = px.box(
                        df_clean, 
                        x=x_col, 
                        y=y_col,
                        title=f'Distribution of {y_col} by {x_col}',
                        points="outliers"
                    )
                else:
                    raise ValueError(f"Unsupported plot type: {plot_type}")
            
            # Default layout settings
            default_layout = {
                'xaxis_title': x_col,
                'yaxis_title': y_col if plot_type != 'histogram' else 'Count',
                'template': 'plotly_white',
                'height': 600,
                'width': 800,
                'showlegend': True,
                'margin': dict(l=50, r=50, t=50, b=50),
                'font': dict(family="Arial, sans-serif", size=12),
                'hovermode': 'closest',
                'plot_bgcolor': 'white',
                'paper_bgcolor': 'white'
            }
            
            # Update with custom layout if provided
            if custom_layout:
                default_layout.update(custom_layout)
                
            fig.update_layout(**default_layout)
            
            # Add hover template
            hover_template = "<br>".join([
                f"{x_col}: %{{x}}",
                f"{y_col if plot_type != 'histogram' else 'Count'}: %{{y}}"
            ])
            fig.update_traces(hovertemplate=hover_template)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating plot: {str(e)}")
            return None
            
    @staticmethod
    def add_statistics(fig: go.Figure, df: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
        """Add statistical annotations to the plot."""
        if fig and isinstance(fig, go.Figure):
            stats_text = f"""
            Statistics:
            Mean {x_col}: {df[x_col].mean():.2f}
            Std {x_col}: {df[x_col].std():.2f}
            """
            if y_col in df.columns:
                stats_text += f"""
                Mean {y_col}: {df[y_col].mean():.2f}
                Std {y_col}: {df[y_col].std():.2f}
                Correlation: {df[x_col].corr(df[y_col]):.2f}
                """
            
            fig.add_annotation(
                text=stats_text,
                xref="paper",
                yref="paper",
                x=1.02,
                y=0.98,
                showarrow=False,
                font=dict(size=10),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="gray",
                borderwidth=1
            )
        return fig