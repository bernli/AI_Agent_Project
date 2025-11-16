#!/usr/bin/env python3
"""
Visualisierung der verschiedenen Agent-Architekturen
Single-Agent vs Multi-Agent Systeme
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np


def visualize_single_agent():
    """Visualisiere Single-Agent Architektur (Data Analyst Agent)"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Titel
    ax.text(5, 9.5, 'Single-Agent System\n(Data Analyst Agent)',
            ha='center', va='top', fontsize=16, fontweight='bold')

    # Hauptagent
    agent_box = FancyBboxPatch((2, 6), 6, 2,
                               boxstyle="round,pad=0.1",
                               edgecolor='blue', facecolor='lightblue',
                               linewidth=2)
    ax.add_patch(agent_box)
    ax.text(5, 7, 'DataAnalystAgent', ha='center', va='center',
            fontsize=14, fontweight='bold')

    # Tools
    tools = [
        ('load_data()', 1, 4),
        ('get_summary()', 3, 4),
        ('analyze_column()', 5, 4),
        ('visualize_column()', 7, 4),
        ('find_correlations()', 2, 2),
        ('get_insights()', 8, 2)
    ]

    for tool_name, x, y in tools:
        tool_box = FancyBboxPatch((x-0.8, y-0.3), 1.6, 0.6,
                                  boxstyle="round,pad=0.05",
                                  edgecolor='green', facecolor='lightgreen',
                                  linewidth=1.5)
        ax.add_patch(tool_box)
        ax.text(x, y, tool_name, ha='center', va='center',
                fontsize=9, fontweight='bold')

        # Pfeile vom Agent zu Tools
        arrow = FancyArrowPatch((5, 6), (x, y+0.3),
                               arrowstyle='->', mutation_scale=20,
                               color='gray', linewidth=1, linestyle='--')
        ax.add_patch(arrow)

    # User Input
    ax.text(5, 9, 'User: "Analyze data.csv"', ha='center',
            fontsize=10, style='italic', bbox=dict(boxstyle='round',
            facecolor='yellow', alpha=0.5))

    # Output
    ax.text(5, 0.5, 'Output: Statistics + Visualizations + Insights',
            ha='center', fontsize=10, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

    plt.tight_layout()
    plt.savefig('single_agent_architecture.png', dpi=300, bbox_inches='tight')
    print("✓ Single-Agent Diagramm gespeichert: single_agent_architecture.png")
    plt.close()


def visualize_multi_agent():
    """Visualisiere Multi-Agent Architektur (Agent Shutton Style)"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Titel
    ax.text(7, 11.5, 'Multi-Agent System\n(Agent Shutton Style)',
            ha='center', va='top', fontsize=16, fontweight='bold')

    # Orchestrator
    orch_box = FancyBboxPatch((4, 9), 6, 1.5,
                              boxstyle="round,pad=0.1",
                              edgecolor='red', facecolor='lightcoral',
                              linewidth=3)
    ax.add_patch(orch_box)
    ax.text(7, 9.75, 'Orchestrator Agent\n(BloggerAgent)',
            ha='center', va='center', fontsize=12, fontweight='bold')

    # Sub-Agents
    sub_agents = [
        ('Planner\nAgent', 1, 6, 'Plans structure'),
        ('Writer\nAgent', 5, 6, 'Creates content'),
        ('Editor\nAgent', 9, 6, 'Refines text'),
        ('Social Media\nAgent', 13, 6, 'Marketing posts')
    ]

    colors = ['lightyellow', 'lightgreen', 'lightblue', 'lavender']

    for i, (name, x, y, desc) in enumerate(sub_agents):
        # Sub-Agent Box
        agent_box = FancyBboxPatch((x-1.2, y-0.6), 2.4, 1.2,
                                   boxstyle="round,pad=0.1",
                                   edgecolor='darkblue', facecolor=colors[i],
                                   linewidth=2)
        ax.add_patch(agent_box)
        ax.text(x, y+0.2, name, ha='center', va='center',
                fontsize=10, fontweight='bold')
        ax.text(x, y-0.3, desc, ha='center', va='center',
                fontsize=7, style='italic')

        # Pfeil vom Orchestrator zu Sub-Agent
        arrow = FancyArrowPatch((7, 9), (x, y+0.6),
                               arrowstyle='->', mutation_scale=20,
                               color='red', linewidth=2)
        ax.add_patch(arrow)

        # Tools für jeden Sub-Agent
        if i == 0:  # Planner
            tools = ['analyze_codebase()', 'validate_outline()']
        elif i == 1:  # Writer
            tools = ['write_section()', 'add_code_examples()']
        elif i == 2:  # Editor
            tools = ['check_grammar()', 'improve_style()']
        else:  # Social Media
            tools = ['create_tweet()', 'linkedin_post()']

        for j, tool in enumerate(tools):
            tool_y = 4 - j*0.8
            tool_box = FancyBboxPatch((x-1, tool_y-0.25), 2, 0.5,
                                      boxstyle="round,pad=0.05",
                                      edgecolor='green', facecolor='lightgreen',
                                      linewidth=1)
            ax.add_patch(tool_box)
            ax.text(x, tool_y, tool, ha='center', va='center',
                    fontsize=7)

            # Pfeil von Sub-Agent zu Tool
            arrow = FancyArrowPatch((x, y-0.6), (x, tool_y+0.25),
                                   arrowstyle='->', mutation_scale=15,
                                   color='gray', linewidth=1, linestyle='--')
            ax.add_patch(arrow)

    # Workflow Pfeile zwischen Sub-Agents
    for i in range(len(sub_agents)-1):
        x1 = sub_agents[i][1]
        x2 = sub_agents[i+1][1]
        y = 6
        arrow = FancyArrowPatch((x1+1.2, y), (x2-1.2, y),
                               arrowstyle='->', mutation_scale=25,
                               color='orange', linewidth=2.5)
        ax.add_patch(arrow)

    # User Input
    ax.text(7, 11, 'User: "Write blog about Python async/await"',
            ha='center', fontsize=10, style='italic',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

    # Output
    ax.text(7, 1.5, 'Output: Blog Post + Social Media Posts + Images',
            ha='center', fontsize=10, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

    # Feedback Loop
    feedback_arrow = FancyArrowPatch((13, 5), (9, 5),
                                    arrowstyle='<->', mutation_scale=20,
                                    color='purple', linewidth=2,
                                    linestyle='dotted')
    ax.add_patch(feedback_arrow)
    ax.text(11, 5.3, 'Feedback Loop', ha='center',
            fontsize=8, color='purple', style='italic')

    plt.tight_layout()
    plt.savefig('multi_agent_architecture.png', dpi=300, bbox_inches='tight')
    print("✓ Multi-Agent Diagramm gespeichert: multi_agent_architecture.png")
    plt.close()


def visualize_comparison():
    """Vergleich zwischen Single-Agent und Multi-Agent"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Single-Agent (links)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('Single-Agent\n(Einfach, Fokussiert)', fontsize=14,
                  fontweight='bold', pad=20)

    # Agent
    agent1 = FancyBboxPatch((2, 5), 6, 2, boxstyle="round,pad=0.1",
                            edgecolor='blue', facecolor='lightblue', linewidth=2)
    ax1.add_patch(agent1)
    ax1.text(5, 6, 'Agent', ha='center', va='center',
             fontsize=12, fontweight='bold')

    # Tools
    for i, tool in enumerate(['Tool 1', 'Tool 2', 'Tool 3']):
        y = 3 - i*1.2
        box = FancyBboxPatch((2, y-0.4), 6, 0.8, boxstyle="round,pad=0.05",
                            edgecolor='green', facecolor='lightgreen', linewidth=1.5)
        ax1.add_patch(box)
        ax1.text(5, y, tool, ha='center', va='center', fontsize=10)
        arrow = FancyArrowPatch((5, 5), (5, y+0.4),
                               arrowstyle='->', mutation_scale=15,
                               color='gray', linewidth=1)
        ax1.add_patch(arrow)

    # Eigenschaften
    props1 = [
        '✓ Schnell zu entwickeln',
        '✓ Einfach zu testen',
        '✓ Klarer Workflow',
        '✓ Niedrige Komplexität'
    ]
    for i, prop in enumerate(props1):
        ax1.text(1, 9-i*0.6, prop, fontsize=9, style='italic')

    # Multi-Agent (rechts)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('Multi-Agent\n(Komplex, Spezialisiert)', fontsize=14,
                  fontweight='bold', pad=20)

    # Orchestrator
    orch = FancyBboxPatch((2, 7), 6, 1.5, boxstyle="round,pad=0.1",
                         edgecolor='red', facecolor='lightcoral', linewidth=2)
    ax2.add_patch(orch)
    ax2.text(5, 7.75, 'Orchestrator', ha='center', va='center',
             fontsize=12, fontweight='bold')

    # Sub-Agents
    sub_positions = [(1.5, 5), (4.5, 5), (7.5, 5)]
    sub_names = ['Agent 1', 'Agent 2', 'Agent 3']
    colors = ['lightyellow', 'lightgreen', 'lightblue']

    for (x, y), name, color in zip(sub_positions, sub_names, colors):
        box = FancyBboxPatch((x-0.8, y-0.5), 1.6, 1, boxstyle="round,pad=0.05",
                            edgecolor='darkblue', facecolor=color, linewidth=2)
        ax2.add_patch(box)
        ax2.text(x, y, name, ha='center', va='center',
                fontsize=9, fontweight='bold')
        arrow = FancyArrowPatch((5, 7), (x, y+0.5),
                               arrowstyle='->', mutation_scale=15,
                               color='red', linewidth=1.5)
        ax2.add_patch(arrow)

        # Tools
        for i in range(2):
            tool_y = 3.5 - i*0.8
            tool_box = FancyBboxPatch((x-0.6, tool_y-0.25), 1.2, 0.5,
                                     boxstyle="round,pad=0.03",
                                     edgecolor='green', facecolor='lightgreen',
                                     linewidth=1)
            ax2.add_patch(tool_box)
            ax2.text(x, tool_y, f'T{i+1}', ha='center', va='center', fontsize=7)

    # Workflow arrows
    for i in range(len(sub_positions)-1):
        x1, y1 = sub_positions[i]
        x2, y2 = sub_positions[i+1]
        arrow = FancyArrowPatch((x1+0.8, y1), (x2-0.8, y2),
                               arrowstyle='->', mutation_scale=20,
                               color='orange', linewidth=2)
        ax2.add_patch(arrow)

    # Eigenschaften
    props2 = [
        '✓ Hohe Qualität',
        '✓ Spezialisierung',
        '✓ Feedback-Loops',
        '✓ Skalierbar'
    ]
    for i, prop in enumerate(props2):
        ax2.text(1, 9-i*0.6, prop, fontsize=9, style='italic')

    plt.tight_layout()
    plt.savefig('agent_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Vergleichs-Diagramm gespeichert: agent_comparison.png")
    plt.close()


def create_workflow_diagram():
    """Erstelle detaillierten Workflow-Vergleich"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Titel
    ax.text(7, 11.5, 'Workflow Comparison: Single vs Multi-Agent',
            ha='center', va='top', fontsize=16, fontweight='bold')

    # Left side: Single-Agent Workflow
    ax.text(3.5, 10.5, 'Single-Agent Workflow', ha='center',
            fontsize=12, fontweight='bold', color='blue')

    steps_single = [
        ('Input', 9.5),
        ('Load Data', 8.5),
        ('Analyze', 7.5),
        ('Visualize', 6.5),
        ('Report', 5.5),
        ('Output', 4.5)
    ]

    for i, (step, y) in enumerate(steps_single):
        box = FancyBboxPatch((2, y-0.3), 3, 0.6,
                            boxstyle="round,pad=0.05",
                            edgecolor='blue', facecolor='lightblue',
                            linewidth=2)
        ax.add_patch(box)
        ax.text(3.5, y, step, ha='center', va='center',
                fontsize=10, fontweight='bold')

        if i < len(steps_single) - 1:
            arrow = FancyArrowPatch((3.5, y-0.3), (3.5, steps_single[i+1][1]+0.3),
                                   arrowstyle='->', mutation_scale=20,
                                   color='blue', linewidth=2)
            ax.add_patch(arrow)

    ax.text(3.5, 3.5, 'Linear Workflow\n↓\nEinfach & Schnell',
            ha='center', fontsize=9, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

    # Right side: Multi-Agent Workflow
    ax.text(10.5, 10.5, 'Multi-Agent Workflow', ha='center',
            fontsize=12, fontweight='bold', color='red')

    steps_multi = [
        ('Input', 9.5),
        ('Orchestrator', 8.5),
        ('Agent 1: Plan', 7.5),
        ('Agent 2: Execute', 6.5),
        ('Agent 3: Review', 5.5),
        ('Feedback Loop', 4.8),
        ('Output', 4)
    ]

    for i, (step, y) in enumerate(steps_multi):
        color = 'lightcoral' if 'Orchestrator' in step else 'lightyellow'
        box = FancyBboxPatch((9, y-0.3), 3, 0.6,
                            boxstyle="round,pad=0.05",
                            edgecolor='red', facecolor=color,
                            linewidth=2)
        ax.add_patch(box)
        ax.text(10.5, y, step, ha='center', va='center',
                fontsize=9, fontweight='bold')

        if i < len(steps_multi) - 1:
            if 'Feedback' in step:
                # Feedback arrow zurück
                arrow = FancyArrowPatch((9, y), (9, steps_multi[3][1]),
                                       arrowstyle='<->', mutation_scale=20,
                                       color='purple', linewidth=2,
                                       linestyle='dotted')
            else:
                arrow = FancyArrowPatch((10.5, y-0.3),
                                       (10.5, steps_multi[i+1][1]+0.3),
                                       arrowstyle='->', mutation_scale=20,
                                       color='red', linewidth=2)
            ax.add_patch(arrow)

    ax.text(10.5, 2.5, 'Iterative Workflow\n↓\nHohe Qualität',
            ha='center', fontsize=9, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))

    # Comparison arrow
    comparison_arrow = FancyArrowPatch((5.5, 7), (8.5, 7),
                                      arrowstyle='<->', mutation_scale=25,
                                      color='green', linewidth=3)
    ax.add_patch(comparison_arrow)
    ax.text(7, 7.5, 'VS', ha='center', fontsize=14,
            fontweight='bold', color='green')

    plt.tight_layout()
    plt.savefig('workflow_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Workflow-Diagramm gespeichert: workflow_comparison.png")
    plt.close()


if __name__ == "__main__":
    print("🎨 Erstelle Agent-Architektur Visualisierungen...\n")

    visualize_single_agent()
    visualize_multi_agent()
    visualize_comparison()
    create_workflow_diagram()

    print("\n✅ Alle Diagramme erfolgreich erstellt!")
    print("\nErstelte Dateien:")
    print("  1. single_agent_architecture.png")
    print("  2. multi_agent_architecture.png")
    print("  3. agent_comparison.png")
    print("  4. workflow_comparison.png")
    print("\nÖffne die PNG-Dateien, um die Architekturen zu verstehen!")
