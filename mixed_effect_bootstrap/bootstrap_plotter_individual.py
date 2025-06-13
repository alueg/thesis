import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Optional
import json
import os


def load_bootstrap_results(json_file: str) -> Dict:
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    if 'bootstrap_results' in data:
        return data['bootstrap_results']
    else:
        print("Warning: 'bootstrap_results' key not found in JSON file")
        return data


def prepare_plotting_data(bootstrap_results: Dict) -> pd.DataFrame:
    plot_data = []
    
    for trust_type, results in bootstrap_results.items():
        for factor, stats in results.items():
            plot_data.append({
                'trust_type': trust_type,
                'factor': factor,
                'coefficient': stats['mean'],
                'ci_lower': stats['ci_lower'],
                'ci_upper': stats['ci_upper'],
                'significant': stats['significant'],
                'std': stats['std']
            })
    
    return pd.DataFrame(plot_data)


# Configuration constants
COLOR_MAP = {
    'overtrust': '#FE6100',
    'undertrust': '#648FFF',
    'appropriate': '#DC267F'
}

TRUST_ORDER = ['overtrust', 'undertrust', 'appropriate']


def create_factor_group_plot(df: pd.DataFrame, 
                           factor_group: str,
                           width: int = 600, 
                           height: int = 300) -> Optional[go.Figure]:
    """Create a plot for a single factor group with all trust types"""
    
    # Filter for the specific factor group
    group_data = df[df['factor'].str[0] == factor_group].copy()
    
    if group_data.empty:
        print(f"Warning: No data available for factor group {factor_group}")
        return None
    
    # Prepare data
    group_data['factor_level'] = group_data['factor'].str[1]
    
    fig = go.Figure()
    
    # Set fixed x-axis range
    global_x_range = [-2, 2]
    
    all_trust_types = sorted(group_data['trust_type'].unique())
    all_trust_types = [t for t in TRUST_ORDER if t in all_trust_types]
    
    levels = sorted(group_data['factor_level'].unique())
    # Level 1 at top (higher y value)
    level_positions = {str(i): 2-i for i in range(1, len(levels) + 1)}
    
    trust_offset = 0.12
    
    for trust_idx, trust_type in enumerate(all_trust_types):
        trust_data = group_data[group_data['trust_type'] == trust_type].copy()
        
        if trust_data.empty:
            continue
        
        y_positions = []
        
        for _, data_row in trust_data.iterrows():
            level = data_row['factor_level']
            base_y = level_positions[level]
            offset_y = base_y + (trust_idx - len(all_trust_types)/2 + 0.5) * trust_offset
            y_positions.append(offset_y)
        
        # Add confidence intervals
        for i, (_, data_row) in enumerate(trust_data.iterrows()):
            y_pos = y_positions[i]
            
            fig.add_trace(go.Scatter(
                x=[data_row['ci_lower'], data_row['ci_upper']],
                y=[y_pos, y_pos],
                mode='lines',
                line=dict(color=COLOR_MAP[trust_type], width=3),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Add coefficient points
        marker_symbols = ['diamond' if sig else 'circle' for sig in trust_data['significant']]
        marker_sizes = [10 if sig else 8 for sig in trust_data['significant']]
        
        fig.add_trace(go.Scatter(
            x=trust_data['coefficient'],
            y=y_positions,
            mode='markers',
            marker=dict(
                color=COLOR_MAP[trust_type],
                size=marker_sizes,
                symbol=marker_symbols,
                line=dict(width=1, color='white')  
            ),
            showlegend=True, 
            name=trust_type.capitalize(),
            text=[f"Factor: {data_row['factor']}<br>"
                  f"Trust: {data_row['trust_type']}<br>"
                  f"Coefficient: {data_row['coefficient']:.3f}<br>"
                  f"CI: [{data_row['ci_lower']:.3f}, {data_row['ci_upper']:.3f}]<br>"
                  f"Significant: {'Yes' if data_row['significant'] else 'No'}"
                  for _, data_row in trust_data.iterrows()],
            hovertemplate='%{text}<extra></extra>'
        ))
    
    #Add zero line
    fig.add_vline(x=0, line_dash="dash", line_color="gray", line_width=2)
    
    #Update y-axis
    tick_positions = [level_positions[level] for level in levels]
    tick_labels = [f"{factor_group}{level}" for level in levels]
    
    sorted_pairs = sorted(zip(tick_positions, tick_labels), reverse=True)
    tick_positions = [pos for pos, _ in sorted_pairs]
    tick_labels = [label for _, label in sorted_pairs]
    
    fig.update_yaxes(
        tickmode='array',
        tickvals=tick_positions,
        ticktext=tick_labels,
        tickfont=dict(size=16, color='black', family='Arial Bold'),
        range=[-0.3, 1.3],
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        gridcolor="lightgray",
        gridwidth=0.3,
    )
    
    fig.update_xaxes(
        tickfont=dict(size=16, color='black', family='Arial Bold'),
        range=global_x_range,
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        gridcolor="lightgray",
        gridwidth=0.3,
        zeroline=True,
        zerolinecolor="gray",
        zerolinewidth=2,
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        width=width,
        height=height,
        margin=dict(l=80, r=40, t=60, b=50),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.0,
            xanchor="right",
            x=1.0,
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="gray",
            borderwidth=2,
            font=dict(size=14, color='black', family='Arial Bold')
        ),
        font=dict(size=12, color='black', family='Arial')
    )
    
    return fig


def main():
    try:
        bootstrap_results = load_bootstrap_results('bootstrap_results.json')
        df = prepare_plotting_data(bootstrap_results)
        
        if df.empty:
            print("No data available for plotting")
            return 1
        
        print(f"Found data for {len(df['factor'].unique())} factors")
        
    
        output_dir = "plots_individual"
        os.makedirs(output_dir, exist_ok=True)
        
        factor_groups = ['A', 'B', 'C', 'D']
        plots_created = 0
        
        print("Creating individual factor group plots...")
        
        for factor_group in factor_groups:
            print(f"  Creating {factor_group} factor group plot...")
            
            fig = create_factor_group_plot(df, factor_group)
            
            if fig:
                filename = f"factor_group_{factor_group.lower()}_all_trust_types.html"
                filepath = os.path.join(output_dir, filename)
                fig.write_html(filepath)
                print(f"    Saved: {filepath}")
                plots_created += 1
            else:
                print(f"    Skipped factor group {factor_group} - no data")
        
        if plots_created == 0:
            print("No plots could be created from the data.")
            return 1
        
        print(f"\nCreated {plots_created} factor group plots")
        print(f"All plots saved to '{output_dir}/' directory")
        return 0
        
    except Exception as e:
        print(f"Error creating plots: {e}")
        return 1


if __name__ == "__main__":
    exit(main())