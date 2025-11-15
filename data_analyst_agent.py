"""
Simple Data Analyst Agent MVP
Analyzes CSV data and provides insights
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path


class DataAnalystAgent:
    """A simple AI agent for data analysis tasks"""

    def __init__(self, data_path=None):
        """Initialize the agent with optional data file"""
        self.data = None
        self.data_path = data_path
        if data_path:
            self.load_data(data_path)

    def load_data(self, file_path):
        """Load CSV data file"""
        try:
            self.data = pd.read_csv(file_path)
            self.data_path = file_path
            print(f"✓ Data loaded successfully from {file_path}")
            print(f"  Shape: {self.data.shape[0]} rows, {self.data.shape[1]} columns")
            return True
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return False

    def get_summary(self):
        """Get basic statistical summary of the data"""
        if self.data is None:
            print("✗ No data loaded")
            return None

        print("\n" + "="*60)
        print("DATA SUMMARY")
        print("="*60)

        print(f"\nDataset: {self.data_path}")
        print(f"Rows: {self.data.shape[0]}")
        print(f"Columns: {self.data.shape[1]}")

        print("\nColumn Types:")
        print(self.data.dtypes)

        print("\nMissing Values:")
        missing = self.data.isnull().sum()
        if missing.sum() > 0:
            print(missing[missing > 0])
        else:
            print("  No missing values")

        print("\nNumerical Statistics:")
        print(self.data.describe())

        return self.data.describe()

    def analyze_column(self, column_name):
        """Analyze a specific column"""
        if self.data is None:
            print("✗ No data loaded")
            return None

        if column_name not in self.data.columns:
            print(f"✗ Column '{column_name}' not found")
            print(f"  Available columns: {', '.join(self.data.columns)}")
            return None

        col_data = self.data[column_name]

        print("\n" + "="*60)
        print(f"ANALYSIS: {column_name}")
        print("="*60)

        print(f"\nData Type: {col_data.dtype}")
        print(f"Non-null Count: {col_data.count()}/{len(col_data)}")

        if pd.api.types.is_numeric_dtype(col_data):
            print("\nNumerical Statistics:")
            print(f"  Mean: {col_data.mean():.2f}")
            print(f"  Median: {col_data.median():.2f}")
            print(f"  Std Dev: {col_data.std():.2f}")
            print(f"  Min: {col_data.min():.2f}")
            print(f"  Max: {col_data.max():.2f}")
        else:
            print("\nCategorical Statistics:")
            print(f"  Unique Values: {col_data.nunique()}")
            print(f"\nTop 5 Values:")
            print(col_data.value_counts().head())

        return col_data

    def visualize_column(self, column_name, output_path=None):
        """Create visualization for a column"""
        if self.data is None:
            print("✗ No data loaded")
            return False

        if column_name not in self.data.columns:
            print(f"✗ Column '{column_name}' not found")
            return False

        col_data = self.data[column_name].dropna()

        plt.figure(figsize=(10, 6))

        if pd.api.types.is_numeric_dtype(col_data):
            # Histogram for numerical data
            plt.subplot(1, 2, 1)
            plt.hist(col_data, bins=30, edgecolor='black', alpha=0.7)
            plt.title(f'Distribution of {column_name}')
            plt.xlabel(column_name)
            plt.ylabel('Frequency')

            # Box plot
            plt.subplot(1, 2, 2)
            plt.boxplot(col_data)
            plt.title(f'Box Plot of {column_name}')
            plt.ylabel(column_name)
        else:
            # Bar chart for categorical data
            value_counts = col_data.value_counts().head(10)
            plt.bar(range(len(value_counts)), value_counts.values)
            plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, ha='right')
            plt.title(f'Top Values in {column_name}')
            plt.xlabel(column_name)
            plt.ylabel('Count')

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✓ Visualization saved to {output_path}")
        else:
            output_path = f"{column_name}_plot.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✓ Visualization saved to {output_path}")

        plt.close()
        return True

    def find_correlations(self, threshold=0.5):
        """Find correlations between numerical columns"""
        if self.data is None:
            print("✗ No data loaded")
            return None

        numerical_cols = self.data.select_dtypes(include=[np.number]).columns

        if len(numerical_cols) < 2:
            print("✗ Not enough numerical columns for correlation analysis")
            return None

        print("\n" + "="*60)
        print("CORRELATION ANALYSIS")
        print("="*60)

        corr_matrix = self.data[numerical_cols].corr()

        # Find strong correlations
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) >= threshold:
                    strong_corr.append({
                        'col1': corr_matrix.columns[i],
                        'col2': corr_matrix.columns[j],
                        'correlation': corr_matrix.iloc[i, j]
                    })

        if strong_corr:
            print(f"\nStrong correlations (|r| >= {threshold}):")
            for corr in sorted(strong_corr, key=lambda x: abs(x['correlation']), reverse=True):
                print(f"  {corr['col1']} <-> {corr['col2']}: {corr['correlation']:.3f}")
        else:
            print(f"\nNo strong correlations found (threshold: {threshold})")

        # Create heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                    square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        plt.title('Correlation Matrix')
        plt.tight_layout()
        plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
        print(f"\n✓ Correlation matrix saved to correlation_matrix.png")
        plt.close()

        return corr_matrix

    def get_insights(self):
        """Generate automated insights from the data"""
        if self.data is None:
            print("✗ No data loaded")
            return None

        print("\n" + "="*60)
        print("AUTOMATED INSIGHTS")
        print("="*60)

        insights = []

        # Check data quality
        missing_pct = (self.data.isnull().sum() / len(self.data) * 100)
        if missing_pct.max() > 10:
            worst_col = missing_pct.idxmax()
            insights.append(f"⚠ High missing data: '{worst_col}' has {missing_pct.max():.1f}% missing values")

        # Check for duplicates
        dup_count = self.data.duplicated().sum()
        if dup_count > 0:
            insights.append(f"⚠ Found {dup_count} duplicate rows ({dup_count/len(self.data)*100:.1f}%)")

        # Analyze numerical columns
        numerical_cols = self.data.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            col_data = self.data[col].dropna()
            if len(col_data) > 0:
                # Check for outliers
                q1, q3 = col_data.quantile([0.25, 0.75])
                iqr = q3 - q1
                outliers = ((col_data < q1 - 1.5*iqr) | (col_data > q3 + 1.5*iqr)).sum()
                if outliers > len(col_data) * 0.05:
                    insights.append(f"📊 '{col}' has {outliers} potential outliers ({outliers/len(col_data)*100:.1f}%)")

        # Analyze categorical columns
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            unique_count = self.data[col].nunique()
            if unique_count == len(self.data):
                insights.append(f"🔑 '{col}' appears to be a unique identifier (all values unique)")
            elif unique_count < 10:
                insights.append(f"📋 '{col}' has {unique_count} categories")

        if insights:
            for insight in insights:
                print(f"\n  {insight}")
        else:
            print("\n  ✓ No major issues detected")

        return insights


if __name__ == "__main__":
    print("Data Analyst Agent MVP")
    print("Usage: python data_analyst_agent.py")
    print("\nOr use CLI: python cli.py <data_file.csv>")
