#!/usr/bin/env python3
"""
Simple test script for Data Analyst Agent
"""

from data_analyst_agent import DataAnalystAgent


def test_basic_functionality():
    """Test basic agent functionality"""
    print("Testing Data Analyst Agent...")
    print("="*60)

    # Test 1: Load data
    print("\n[Test 1] Loading example data...")
    agent = DataAnalystAgent("example_data.csv")
    assert agent.data is not None, "Failed to load data"
    print("✓ Data loaded successfully")

    # Test 2: Get summary
    print("\n[Test 2] Getting data summary...")
    summary = agent.get_summary()
    assert summary is not None, "Failed to get summary"
    print("✓ Summary generated")

    # Test 3: Analyze column
    print("\n[Test 3] Analyzing column 'age'...")
    result = agent.analyze_column('age')
    assert result is not None, "Failed to analyze column"
    print("✓ Column analysis complete")

    # Test 4: Visualize column
    print("\n[Test 4] Creating visualization...")
    success = agent.visualize_column('salary', 'test_salary_plot.png')
    assert success, "Failed to create visualization"
    print("✓ Visualization created")

    # Test 5: Find correlations
    print("\n[Test 5] Finding correlations...")
    corr = agent.find_correlations(threshold=0.3)
    assert corr is not None, "Failed to find correlations"
    print("✓ Correlation analysis complete")

    # Test 6: Get insights
    print("\n[Test 6] Getting automated insights...")
    insights = agent.get_insights()
    assert insights is not None, "Failed to get insights"
    print("✓ Insights generated")

    print("\n" + "="*60)
    print("✓ All tests passed!")
    print("="*60)


if __name__ == "__main__":
    test_basic_functionality()
