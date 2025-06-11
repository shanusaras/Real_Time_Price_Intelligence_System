"""
EDA Analyzer Module
==================

This module provides functions for performing exploratory data analysis on Jumia product data.
It includes functions for statistical analysis, visualization, and report generation.

Functions:
    - load_data: Load and validate the dataset
    - get_basic_stats: Get basic dataset statistics
    - analyze_prices: Perform price analysis
    - analyze_categories: Analyze category distribution
    - create_visualizations: Generate EDA visualizations
    - generate_report: Generate a comprehensive EDA report
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class EDAAnalyzer:
    """Class for performing EDA on Jumia product data"""
    
    def __init__(self, data_path: str = '../etl/output/jumia_products_clean.csv'):
        """
        Initialize the EDA analyzer
        
        Args:
            data_path: Path to the cleaned data CSV file
        """
        self.data_path = Path(data_path)
        self.df = None
        self.output_dir = Path('../etl/output')
        
    def load_data(self) -> pd.DataFrame:
        """
        Load and validate the dataset
        
        Returns:
            pd.DataFrame: Loaded dataset
        
        Raises:
            FileNotFoundError: If the data file is not found
            ValueError: If required columns are missing
        """
        try:
            self.df = pd.read_csv(self.data_path)
            required_columns = ['name', 'brand', 'price', 'discount_pct', 'rating', 'reviews', 'in_stock', 'category', 'link']
            missing_cols = [col for col in required_columns if col not in self.df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            return self.df
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Data file not found at {self.data_path}") from e

    def get_basic_stats(self) -> dict:
        """
        Get basic statistics about the dataset
        
        Returns:
            dict: Dictionary containing basic statistics
        """
        stats = {
            'total_records': len(self.df),
            'unique_categories': self.df['category'].nunique(),
            'price_stats': self.df['price'].describe().to_dict(),
            'category_distribution': self.df['category'].value_counts().to_dict()
        }
        return stats

    def analyze_prices(self) -> dict:
        """
        Perform price analysis
        
        Returns:
            dict: Dictionary containing price analysis results
        """
        price_analysis = {
            'price_stats': self.df['price'].describe().to_dict(),
            'price_by_category': self.df.groupby('category')['price'].mean().sort_values(ascending=False).to_dict(),
            'price_percentiles': {
                f'p{p}': np.percentile(self.df['price'], p) for p in [10, 25, 50, 75, 90]
            }
        }
        return price_analysis

    def create_visualizations(self, save_path: str = None):
        """
        Create EDA visualizations
        
        Args:
            save_path: Path to save the visualization file
        """
        plt.figure(figsize=(12, 8))
        
        # Price distribution
        plt.subplot(2, 2, 1)
        sns.histplot(self.df['price'], bins=50)
        plt.title('Price Distribution')
        plt.xlabel('Price')
        plt.ylabel('Frequency')
        plt.yscale('log')

        # Category distribution
        plt.subplot(2, 2, 2)
        category_dist = self.df['category'].value_counts()
        category_dist.plot(kind='bar')
        plt.title('Category Distribution')
        plt.xlabel('Category')
        plt.ylabel('Number of Products')
        plt.xticks(rotation=45)

        # Price by category
        plt.subplot(2, 2, 3)
        sns.boxplot(x='category', y='price', data=self.df)
        plt.title('Price Distribution by Category')
        plt.xticks(rotation=45)
        plt.yscale('log')

        # Rating distribution
        plt.subplot(2, 2, 4)
        sns.histplot(self.df['rating'], bins=10)
        plt.title('Rating Distribution')
        plt.xlabel('Rating')
        plt.ylabel('Frequency')

        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
        plt.close()

    def generate_report(self, output_dir: str = None):
        """
        Generate a comprehensive EDA report
        
        Args:
            output_dir: Directory to save the report and visualizations
        """
        if output_dir:
            self.output_dir = Path(output_dir)
            self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create visualizations
        self.create_visualizations(self.output_dir / 'eda_visualizations.png')
        
        # Get all analysis results
        results = {
            'basic_stats': self.get_basic_stats(),
            'price_analysis': self.analyze_prices()
        }
        
        return results


def main():
    """Main function to run EDA analysis"""
    try:
        analyzer = EDAAnalyzer()
        df = analyzer.load_data()
        print("\n=== EDA Analysis Report ===")
        print("\nBasic Statistics:")
        print(analyzer.get_basic_stats())
        print("\nPrice Analysis:")
        print(analyzer.analyze_prices())
        
        print("\nGenerating visualizations...")
        analyzer.create_visualizations()
        print("\nAnalysis complete. Check the output directory for visualizations.")
        
    except Exception as e:
        print(f"Error during EDA analysis: {str(e)}")

if __name__ == "__main__":
    main()
