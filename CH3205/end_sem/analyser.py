import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats

def load_and_analyze_results(filename='simulation_results.csv'):
    """
    Load simulation results and perform comprehensive analysis to determine which
    Ru complex (surface vs core) has higher quantum yield under different conditions.
    """
    try:
        # Load the CSV file
        df = pd.read_csv(filename)
        print(f"Successfully loaded {len(df)} simulation results.")
        print(f"Columns: {df.columns.tolist()}")
        
        # Basic statistics
        print("\n=== Basic Statistics ===")
        print(df.describe())
        
        # Calculate QY difference (positive means Ru1 has higher QY)
        df['QY_Difference'] = df['Simulated_QY_Ru1'] - df['Simulated_QY_Ru2']
        df['Higher_QY'] = df.apply(lambda row: 'Ru1 (surface)' if row['QY_Difference'] > 0 
                                 else 'Ru2 (core)' if row['QY_Difference'] < 0 
                                 else 'Equal', axis=1)
        
        # Count which complex typically has higher QY
        qy_counts = df['Higher_QY'].value_counts()
        print("\n=== Overall Winner Analysis ===")
        print(qy_counts)
        winner = qy_counts.idxmax() if len(qy_counts) > 0 else "No clear winner"
        print(f"Overall winner: {winner}")
        
        # T-test to see if the difference is statistically significant
        t_stat, p_val = stats.ttest_rel(df['Simulated_QY_Ru1'], df['Simulated_QY_Ru2'])
        print(f"Paired t-test: t={t_stat:.4f}, p={p_val:.4f}")
        if p_val < 0.05:
            print(f"The difference is statistically significant (p<0.05).")
            if t_stat > 0:
                print("Ru1 (surface) has significantly higher QY overall.")
            else:
                print("Ru2 (core) has significantly higher QY overall.")
        else:
            print("No statistically significant difference overall.")
        
        # Analyze the influence of each parameter
        print("\n=== Parameter Influence Analysis ===")
        analyze_parameter_influence(df)
        
        # Create visualizations
        create_visualizations(df)
        
        # Create detailed parameter interaction analysis
        analyze_parameter_interactions(df)
        
        # Final conclusion
        print("\n=== Conclusion ===")
        provide_conclusion(df)
        
        return df
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found. Please run the simulation first.")
        return None
    except Exception as e:
        print(f"Error analyzing results: {e}")
        return None

def analyze_parameter_influence(df):
    """Analyze how each parameter influences the quantum yield difference."""
    parameters = ['NUM_O2', 'DENSITY_STEEPNESS', 'O2_MOVE_PROB_MIN', 'EXCITED_LIFETIME']
    
    for param in parameters:
        if param in df.columns:
            print(f"\nAnalyzing influence of {param}:")
            param_values = df[param].unique()
            param_values.sort()
            
            print(f"  {'Value':<10} {'Avg QY Ru1':<12} {'Avg QY Ru2':<12} {'Avg Diff':<12} {'Winner'}")
            print(f"  {'-'*10} {'-'*12} {'-'*12} {'-'*12} {'-'*10}")
            
            for val in param_values:
                subset = df[df[param] == val]
                avg_qy1 = subset['Simulated_QY_Ru1'].mean()
                avg_qy2 = subset['Simulated_QY_Ru2'].mean()
                avg_diff = subset['QY_Difference'].mean()
                winner = 'Ru1' if avg_diff > 0 else 'Ru2' if avg_diff < 0 else 'Equal'
                
                print(f"  {val:<10} {avg_qy1:<12.4f} {avg_qy2:<12.4f} {avg_diff:<+12.4f} {winner}")

def create_visualizations(df):
    """Create visualizations to illustrate the relationship between parameters and QY."""
    # Set up the figure for all plots
    plt.figure(figsize=(15, 12))
    
    # 1. Box plot comparing QY of Ru1 vs Ru2
    plt.subplot(2, 2, 1)
    box_data = pd.melt(df[['Simulated_QY_Ru1', 'Simulated_QY_Ru2']], 
                        var_name='Complex Type', value_name='Quantum Yield')
    box_data['Complex Type'] = box_data['Complex Type'].map({
        'Simulated_QY_Ru1': 'Ru1 (surface)', 
        'Simulated_QY_Ru2': 'Ru2 (core)'
    })
    sns.boxplot(x='Complex Type', y='Quantum Yield', data=box_data)
    plt.title('Quantum Yield Comparison: Surface vs Core', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # 2. Heatmap showing QY difference vs two most influential parameters
    # Find two most influential parameters
    parameters = ['NUM_O2', 'DENSITY_STEEPNESS', 'O2_MOVE_PROB_MIN', 'EXCITED_LIFETIME']
    param_influences = {}
    
    for param in parameters:
        if param in df.columns:
            # Calculate eta squared (effect size)
            groups = [df[df[param] == val]['QY_Difference'] for val in df[param].unique()]
            if len(groups) > 1:  # Need at least 2 groups
                f_val, p_val = stats.f_oneway(*groups)
                param_influences[param] = f_val
    
    # Sort parameters by influence
    sorted_params = sorted(param_influences.items(), key=lambda x: x[1], reverse=True)
    top_params = [p[0] for p in sorted_params[:2]] if len(sorted_params) >= 2 else parameters[:2]
    
    # Create the heatmap
    if len(top_params) >= 2:
        plt.subplot(2, 2, 2)
        pivot_data = df.pivot_table(
            values='QY_Difference', 
            index=top_params[0], 
            columns=top_params[1],
            aggfunc='mean'
        )
        
        # Custom colormap: blue for negative (Ru2 wins), red for positive (Ru1 wins)
        cmap = LinearSegmentedColormap.from_list(
            'RuDifference', 
            ['blue', 'lightgray', 'red'], 
            N=256
        )
        
        sns.heatmap(pivot_data, annot=True, cmap=cmap, center=0, fmt='.3f')
        plt.title(f'QY Difference (Ru1-Ru2) by {top_params[0]} and {top_params[1]}', fontsize=14)
    
    # 3. Line plot showing QY vs oxygen concentration
    if 'NUM_O2' in df.columns:
        plt.subplot(2, 2, 3)
        o2_values = sorted(df['NUM_O2'].unique())
        ru1_means = [df[df['NUM_O2'] == val]['Simulated_QY_Ru1'].mean() for val in o2_values]
        ru2_means = [df[df['NUM_O2'] == val]['Simulated_QY_Ru2'].mean() for val in o2_values]
        
        plt.plot(o2_values, ru1_means, 'ro-', label='Ru1 (surface)')
        plt.plot(o2_values, ru2_means, 'bo-', label='Ru2 (core)')
        plt.xlabel('Number of O2 Molecules', fontsize=12)
        plt.ylabel('Average Quantum Yield', fontsize=12)
        plt.title('Effect of O2 Concentration on Quantum Yield', fontsize=14)
        plt.legend()
        plt.grid(True, alpha=0.3)
    
    # 4. Bar chart showing QY at different density steepness
    if 'DENSITY_STEEPNESS' in df.columns:
        plt.subplot(2, 2, 4)
        steepness_values = sorted(df['DENSITY_STEEPNESS'].unique())
        x = np.arange(len(steepness_values))
        width = 0.35
        
        ru1_means = [df[df['DENSITY_STEEPNESS'] == val]['Simulated_QY_Ru1'].mean() for val in steepness_values]
        ru2_means = [df[df['DENSITY_STEEPNESS'] == val]['Simulated_QY_Ru2'].mean() for val in steepness_values]
        
        plt.bar(x - width/2, ru1_means, width, label='Ru1 (surface)', color='red', alpha=0.7)
        plt.bar(x + width/2, ru2_means, width, label='Ru2 (core)', color='blue', alpha=0.7)
        
        plt.xlabel('Density Steepness', fontsize=12)
        plt.ylabel('Average Quantum Yield', fontsize=12)
        plt.title('Effect of Polymer Density Profile on Quantum Yield', fontsize=14)
        plt.xticks(x, steepness_values)
        plt.legend()
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('qy_analysis_results.png', dpi=300, bbox_inches='tight')
    print("\nCreated visualizations and saved to 'qy_analysis_results.png'")

def analyze_parameter_interactions(df):
    """Analyze how parameters interact to influence QY difference."""
    print("\n=== Parameter Interaction Analysis ===")
    
    # Create a column to identify optimal conditions for each complex
    df['Optimal_For'] = df.apply(
        lambda row: 'Ru1' if row['QY_Difference'] > 0.1 else 
                   'Ru2' if row['QY_Difference'] < -0.1 else 
                   'Both Similar', axis=1
    )
    
    # Analyze optimal conditions for each complex
    for complex_type in ['Ru1', 'Ru2']:
        optimal_subset = df[df['Optimal_For'] == complex_type]
        if len(optimal_subset) > 0:
            print(f"\nOptimal conditions for {complex_type} (higher QY):")
            for param in ['NUM_O2', 'DENSITY_STEEPNESS', 'O2_MOVE_PROB_MIN', 'EXCITED_LIFETIME']:
                if param in df.columns:
                    values = optimal_subset[param].value_counts().sort_index()
                    most_common = values.idxmax() if not values.empty else "N/A"
                    print(f"  {param}: Most common value {most_common}")
                    
            # Get the best case scenario
            if complex_type == 'Ru1':
                best_case = df.loc[df['QY_Difference'].idxmax()]
                qy_diff = best_case['QY_Difference']
            else:
                best_case = df.loc[df['QY_Difference'].idxmin()]
                qy_diff = -best_case['QY_Difference']
                
            print(f"  Best case scenario (QY diff: {qy_diff:.4f}):")
            for param in ['NUM_O2', 'DENSITY_STEEPNESS', 'O2_MOVE_PROB_MIN', 'EXCITED_LIFETIME']:
                if param in df.columns:
                    print(f"    {param}: {best_case[param]}")

def provide_conclusion(df):
    """Provide a concise conclusion based on the analysis."""
    # Overall statistics
    ru1_wins = (df['QY_Difference'] > 0).sum()
    ru2_wins = (df['QY_Difference'] < 0).sum()
    ties = (df['QY_Difference'] == 0).sum()
    
    # Average QY values
    avg_qy1 = df['Simulated_QY_Ru1'].mean()
    avg_qy2 = df['Simulated_QY_Ru2'].mean()
    
    # Maximum advantage scenarios
    max_ru1_adv = df['QY_Difference'].max()
    max_ru2_adv = -df['QY_Difference'].min()
    
    # Print conclusion
    print(f"Based on {len(df)} simulation runs:")
    
    if ru1_wins > ru2_wins:
        print(f"Ru1 (surface) shows higher quantum yield in {ru1_wins} scenarios ({ru1_wins/len(df)*100:.1f}%)")
        print(f"compared to Ru2 (core) with {ru2_wins} scenarios ({ru2_wins/len(df)*100:.1f}%).")
    elif ru2_wins > ru1_wins:
        print(f"Ru2 (core) shows higher quantum yield in {ru2_wins} scenarios ({ru2_wins/len(df)*100:.1f}%)")
        print(f"compared to Ru1 (surface) with {ru1_wins} scenarios ({ru1_wins/len(df)*100:.1f}%).")
    else:
        print(f"Both complexes show equivalent performance across scenarios.")
    
    print(f"Average QY: Ru1={avg_qy1:.4f}, Ru2={avg_qy2:.4f}")
    
    # Key influencing factors
    if 'NUM_O2' in df.columns:
        low_o2 = df[df['NUM_O2'] == df['NUM_O2'].min()]
        high_o2 = df[df['NUM_O2'] == df['NUM_O2'].max()]
        lo_diff = low_o2['QY_Difference'].mean()
        hi_diff = high_o2['QY_Difference'].mean()
        
        print("\nKey insights:")
        if abs(lo_diff - hi_diff) > 0.05:  # If meaningful difference
            if lo_diff > hi_diff:
                print(f"- At lower O2 concentrations, Ru1 (surface) has greater advantage")
            else:
                print(f"- At higher O2 concentrations, Ru2 (core) has greater advantage")
    
    # Physical interpretation
    print("\nPhysical interpretation:")
    if avg_qy1 > avg_qy2:
        print("Surface-located complexes (Ru1) generally show higher quantum yield, likely due to:")
        print("- Less exposure to oxygen molecules that can diffuse through the polymer matrix")
        print("- The polymer density gradient creates a partial barrier for oxygen diffusion")
    else:
        print("Core-located complexes (Ru2) generally show higher quantum yield, likely due to:")
        print("- Additional protection from oxygen provided by the surrounding polymer matrix")
        print("- Restricted mobility of oxygen molecules in the denser core region")

# Run the analysis
if __name__ == "__main__":
    print("=== Ruthenium Complex Quantum Yield Analysis ===")
    df = load_and_analyze_results()
    
    # Additional command to show interactive plots if needed
    plt.show()