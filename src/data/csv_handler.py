import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class CSVHandler:
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.max_file_size = 25 * 1024 * 1024  # 25MB

    def load_csv(self, file_path: str) -> bool:
        try:
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if path.stat().st_size > self.max_file_size:
                raise ValueError(f"File size exceeds {self.max_file_size/1024/1024}MB limit")
            
            self.df = pd.read_csv(file_path)
            logger.info(f"Successfully loaded CSV with {len(self.df)} rows")
            return True
            
        except Exception as e:
            logger.error(f"Error loading CSV: {str(e)}")
            self.df = None
            return False

    def get_dataframe(self) -> Optional[pd.DataFrame]:
        return self.df

    def get_column_info(self) -> Dict[str, Any]:
        if self.df is None:
            return {}
            
        try:
            return {
                'columns': list(self.df.columns),
                'dtypes': self.df.dtypes.astype(str).to_dict(),
                'summary': self.df.describe().to_dict(),
                'row_count': len(self.df),
                'missing_values': self.df.isnull().sum().to_dict()
            }
        except Exception as e:
            logger.error(f"Error getting column info: {str(e)}")
            return {}