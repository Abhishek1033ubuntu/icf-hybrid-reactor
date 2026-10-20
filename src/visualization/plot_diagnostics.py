"""
Diagnostic Plotting Utilities
Lead Author: Abhishek Singh (ORCID: 0009-0004-6913-096X)
Technical Collaboration: Google Gemini AI
"""

import matplotlib.pyplot as plt

def setup_plot_style():
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    plt.rcParams['axes.edgecolor'] = '#333333'
    plt.rcParams['axes.linewidth'] = 0.8

def format_dual_axis(ax1, ax2, title, x_label, y1_label, y2_label):
    ax1.set_title(title, fontweight='bold', fontsize=12)
    ax1.set_xlabel(x_label, fontsize=10)
    ax1.set_ylabel(y1_label, color='b', fontsize=10)
    ax2.set_ylabel(y2_label, color='g', fontsize=10)
    ax1.grid(True, alpha=0.3)
