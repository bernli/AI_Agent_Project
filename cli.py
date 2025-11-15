#!/usr/bin/env python3
"""
Command-line interface for Data Analyst Agent
"""

import argparse
import sys
from pathlib import Path
from data_analyst_agent import DataAnalystAgent


def main():
    parser = argparse.ArgumentParser(
        description='Data Analyst Agent - Automated data analysis tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s data.csv                          # Full analysis
  %(prog)s data.csv --summary                # Just summary statistics
  %(prog)s data.csv --column age             # Analyze specific column
  %(prog)s data.csv --correlations           # Find correlations
  %(prog)s data.csv --insights               # Get automated insights
        """
    )

    parser.add_argument('data_file', help='Path to CSV data file')
    parser.add_argument('--summary', action='store_true', help='Show data summary')
    parser.add_argument('--column', help='Analyze specific column')
    parser.add_argument('--visualize', help='Create visualization for column')
    parser.add_argument('--correlations', action='store_true', help='Find correlations')
    parser.add_argument('--corr-threshold', type=float, default=0.5,
                        help='Correlation threshold (default: 0.5)')
    parser.add_argument('--insights', action='store_true', help='Get automated insights')
    parser.add_argument('--all', action='store_true', help='Run all analyses')

    args = parser.parse_args()

    # Check if file exists
    if not Path(args.data_file).exists():
        print(f"✗ Error: File '{args.data_file}' not found")
        sys.exit(1)

    # Initialize agent
    print("🤖 Data Analyst Agent MVP")
    print("="*60)
    agent = DataAnalystAgent(args.data_file)

    if agent.data is None:
        sys.exit(1)

    # If no specific action, run all
    if not any([args.summary, args.column, args.visualize,
                args.correlations, args.insights, args.all]):
        args.all = True

    # Run requested analyses
    if args.all or args.summary:
        agent.get_summary()

    if args.all or args.insights:
        agent.get_insights()

    if args.all or args.correlations:
        agent.find_correlations(threshold=args.corr_threshold)

    if args.column:
        agent.analyze_column(args.column)
        if args.all or args.visualize:
            agent.visualize_column(args.column)

    if args.visualize and not args.column:
        # Visualize first numerical column if no column specified
        numerical_cols = agent.data.select_dtypes(include=['number']).columns
        if len(numerical_cols) > 0:
            agent.visualize_column(numerical_cols[0])
        else:
            print("✗ No numerical columns found for visualization")

    print("\n" + "="*60)
    print("✓ Analysis complete!")
    print("="*60)


if __name__ == "__main__":
    main()
