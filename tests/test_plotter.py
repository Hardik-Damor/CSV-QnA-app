import unittest
import pandas as pd
import numpy as np
from src.visualization.plotter import Plotter
import plotly.graph_objects as go

class TestPlotter(unittest.TestCase):
    def setUp(self):
        # Create sample DataFrame for testing
        self.sample_df = pd.DataFrame({
            'x_values': [1, 2, 3, 4, 5],
            'y_values': [5, 4, 3, 2, 1],
            'category': ['A', 'B', 'A', 'B', 'A']
        })

    def test_create_scatter_plot(self):
        plot = Plotter.create_plot(
            df=self.sample_df,
            x_col='x_values',
            y_col='y_values',
            plot_type='scatter'
        )
        self.assertIsInstance(plot, go.Figure)
        
    def test_create_line_plot(self):
        plot = Plotter.create_plot(
            df=self.sample_df,
            x_col='x_values',
            y_col='y_values',
            plot_type='line'
        )
        self.assertIsInstance(plot, go.Figure)

    def test_create_bar_plot(self):
        plot = Plotter.create_plot(
            df=self.sample_df,
            x_col='category',
            y_col='x_values',
            plot_type='bar'
        )
        self.assertIsInstance(plot, go.Figure)

    def test_create_histogram(self):
        plot = Plotter.create_plot(
            df=self.sample_df,
            x_col='x_values',
            y_col=None,
            plot_type='histogram'
        )
        self.assertIsInstance(plot, go.Figure)

    def test_invalid_plot_type(self):
        with self.assertRaises(ValueError):
            Plotter.create_plot(
                df=self.sample_df,
                x_col='x_values',
                y_col='y_values',
                plot_type='invalid_type'
            )

    def test_invalid_column_names(self):
        with self.assertRaises(ValueError):
            Plotter.create_plot(
                df=self.sample_df,
                x_col='non_existent',
                y_col='y_values',
                plot_type='scatter'
            )

if __name__ == '__main__':
    unittest.main()