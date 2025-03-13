from pathlib import Path
import pandas as pd
from typing import Union, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

def validate_csv_file(file_path: Union[str, Path]) -> pd.DataFrame:
    """Validate and load a CSV file."""
    try:
        file_path = Path(file_path)
        
        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if file_path.suffix.lower() != '.csv':
            raise ValueError(f"Invalid file format. Expected .csv, got {file_path.suffix}")
        
        if file_path.stat().st_size > 25_000_000:  # 25MB limit
            raise ValueError("File size exceeds 25MB limit")
        
        df = pd.read_csv(file_path)
        
        if df.empty:
            raise ValueError("CSV file is empty")
            
        if len(df.columns) < 2:
            raise ValueError("CSV must have at least 2 columns")
            
        return df
        
    except Exception as e:
        logger.error(f"Error validating CSV: {str(e)}")
        raise ValueError(f"Error reading CSV: {str(e)}")

def validate_plot_params(
    df: pd.DataFrame,
    x_col: str,
    y_col: Optional[str] = None,
    plot_type: str = 'scatter'
) -> bool:
    """Validate plotting parameters."""
    valid_plot_types = ['scatter', 'line', 'bar', 'box', 'histogram']
    
    if plot_type not in valid_plot_types:
        raise ValueError(f"Invalid plot type. Must be one of: {valid_plot_types}")
        
    if x_col not in df.columns:
        raise ValueError(f"Column '{x_col}' not found in DataFrame")
        
    if plot_type != 'histogram' and y_col not in df.columns:
        raise ValueError(f"Column '{y_col}' not found in DataFrame")
        
    return True