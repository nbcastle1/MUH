#!/usr/bin/env python3
"""
Main analysis script for MUH (Motor Unit Habituation) data analysis.

This script loads and processes gait data, calculates performance metrics,
and generates various plots and analyses.

Usage:
    python main_analysis.py

Dependencies:
    - processed_trial_data.py
    - performance_metrics_db.py  
    - plotter.py
    - trial_splicer.py (optional)
"""

import os
import sys
from pathlib import Path

# Add current directory to path so we can import our modules
sys.path.append(str(Path(__file__).parent))

from processed_trial_data import ProcessedTrialData
from performance_metrics_db import PerformanceMetricsDB
from plotter import Plotter


def main():
    """Main analysis pipeline"""
    
    # ======================
    # Configuration
    # ======================
    
    # Update these paths to match your data location
    METADATA_PATH = 'muh_metadata.csv'  # Update this path
    DATA_ROOT_DIR = 'muh_data/'         # Update this path
    
    # Analysis parameters
    MAX_TARGET_SIZE = 0.31
    MAX_STRIDES = 415
    REQUIRED_TRIAL_TYPES = ['pref', 'invis']
    
    print("🚀 Starting MUH Data Analysis Pipeline")
    print("=" * 50)
    
    # ======================
    # Data Loading & Processing
    # ======================
    
    print("\n📊 Loading and processing data...")
    
    # Load raw data
    data_manager_pre = ProcessedTrialData(
        metadata_path=METADATA_PATH,
        data_root_dir=DATA_ROOT_DIR, 
        force_reprocess=False,
        debug=True
    )
    
    # Apply filters
    print(f"\n🔍 Applying filters:")
    print(f"  - Max target size: {MAX_TARGET_SIZE}")
    print(f"  - Max strides: {MAX_STRIDES}")
    print(f"  - Required trial types: {REQUIRED_TRIAL_TYPES}")
    
    data_manager = data_manager_pre.filter_trials(
        max_target_size=MAX_TARGET_SIZE,
        max_strides=MAX_STRIDES,
        required_trial_types=REQUIRED_TRIAL_TYPES
    )
    
    print(f"✅ Processed {len(data_manager.processed_data)} subjects")
    
    # ======================
    # Metrics Calculation
    # ======================
    
    print("\n📈 Calculating performance metrics...")
    
    # Initialize metrics database
    metrics_db = PerformanceMetricsDB()
    
    # Calculate and store metrics
    success = metrics_db.update_metrics(data_manager)
    if success:
        print("✅ Metrics calculated and stored successfully")
    else:
        print("❌ Error calculating metrics")
        return
    
    # Display summary
    print(f"📋 Metrics summary:")
    print(f"  - Total subjects: {len(metrics_db.get_subject_ids())}")
    
    # ======================
    # Initialize Plotter
    # ======================
    
    print("\n🎨 Initializing plotter...")
    plotter = Plotter(metrics_db, data_manager)
    print("✅ Plotter initialized")
    
    # ======================
    # Statistical Analysis
    # ======================
    
    print("\n📊 Running statistical analyses...")
    
    # Success rate regression
    print("  - Success rate regression (all trials)")
    regression_model = metrics_db.run_success_rate_regression()
    if regression_model:
        print("    ✅ Regression completed")
        print(f"    📈 R² = {regression_model.rsquared:.3f}")
    
    # Plot regression betas
    metrics_db.plot_success_rate_regression_betas(use_abs=False, trial_mode='all')
    
    # ======================
    # Generate Plots
    # ======================
    
    print("\n📊 Generating plots...")
    
    # 1. Success rate plots by trial type
    print("  - Success rate plots...")
    for trial_type in ['vis1', 'invis', 'vis2']:
        try:
            plotter.plot_metrics(
                trial_type=trial_type, 
                metric='sr', 
                color_by='mot_noise', 
                show_trendline=True
            )
            print(f"    ✅ {trial_type} success rate plot")
        except Exception as e:
            print(f"    ❌ {trial_type} success rate plot failed: {e}")
    
    # 2. Motor noise analysis
    print("  - Motor noise analysis...")
    try:
        plotter.plot_noise_analysis(
            trial_type='invis',
            color_by='age_years',
            analysis_type='vs_success'
        )
        print("    ✅ Noise vs success plot")
    except Exception as e:
        print(f"    ❌ Noise analysis failed: {e}")
    
    # 3. Sum of gains and steps visualization
    print("  - Sum of gains and steps plots...")
    try:
        plotter.plot_sum_of_gains_steps(trial_type='invis')
        print("    ✅ Sum of gains and steps plot")
    except Exception as e:
        print(f"    ❌ Sum of gains and steps plot failed: {e}")
    
    # 4. Stride change after success analysis
    print("  - Stride change after success analysis...")
    for trial_type in ['vis1', 'invis', 'vis2']:
        try:
            plotter.plot_sl_change_after_success(
                trial_type=trial_type,
                use_entire_period=True
            )
            print(f"    ✅ {trial_type} stride change plot")
        except Exception as e:
            print(f"    ❌ {trial_type} stride change plot failed: {e}")
    
    # ======================
    # Advanced Analysis
    # ======================
    
    print("\n🔬 Advanced analysis...")
    
    # Binary classification example
    print("  - Binary classification...")
    try:
        classification_results = metrics_db.perform_binary_classification(
            trial_type='invis',
            condition='min_const',
            model_type='logistic',
            threshold=0.68
        )
        plotter.plot_classification_results(classification_results)
        print("    ✅ Classification analysis completed")
    except Exception as e:
        print(f"    ❌ Classification analysis failed: {e}")
    
    # Regression analysis with specific metrics
    print("  - Regression analysis...")
    try:
        regression_results = metrics_db.perform_success_rate_regression(
            selected_condition_metrics=['asymmetry'],
            trial_type='vis1',
            condition='min_const',
            model_type='linear'
        )
        plotter.plot_regression_results(regression_results)
        print("    ✅ Regression analysis completed")
    except Exception as e:
        print(f"    ❌ Regression analysis failed: {e}")
    
    # ======================
    # Export Results
    # ======================
    
    print("\n💾 Exporting results...")
    
    # Display metrics table in browser
    try:
        styled_table = metrics_db.display_pretty_table(open_in_browser=True)
        print("    ✅ Metrics table opened in browser")
    except Exception as e:
        print(f"    ❌ Table export failed: {e}")
    
    # Export to Excel (optional)
    try:
        metrics_db.export_to_excel('muh_analysis_results.xlsx')
        print("    ✅ Results exported to Excel")
    except Exception as e:
        print(f"    ❌ Excel export failed: {e}")
    
    # ======================
    # Summary
    # ======================
    
    print("\n" + "=" * 50)
    print("🎉 Analysis Pipeline Complete!")
    print("=" * 50)
    
    print(f"📊 Summary:")
    print(f"  - Subjects processed: {len(data_manager.processed_data)}")
    print(f"  - Metrics calculated: {len(metrics_db.get_subject_ids())}")
    print(f"  - Figures saved to: {plotter.figures_dir}")
    
    # Print subject ages for reference
    print("\n👥 Participant Summary:")
    data_manager.print_participant_ages()
    
    print("\n✨ All done! Check the 'figures' directory for plots.")


def run_example_analyses():
    """
    Example function showing various analysis options.
    Call this if you want to see more analysis examples.
    """
    
    print("\n🔬 Running example analyses...")
    
    # Load data (you would replace this with your actual data loading)
    data_manager = ProcessedTrialData('metadata.csv', 'data/')
    metrics_db = PerformanceMetricsDB()
    metrics_db.update_metrics(data_manager)
    plotter = Plotter(metrics_db, data_manager)
    
    # Example 1: Correlation analysis
    print("  - Correlation analysis example...")
    try:
        plotter.plot_correlation_analysis(
            x_col='age_years',
            y_col='mot_noise',
            color_by='invis_sr_max_const',
            show_trendline=True
        )
    except Exception as e:
        print(f"    ❌ Correlation analysis failed: {e}")
    
    # Example 2: All regression combinations
    print("  - All regression combinations...")
    try:
        plotter.plot_all_regression_condition_combinations(
            selected_condition_metrics=['asymmetry', 'msl'],
            model_type='linear'
        )
    except Exception as e:
        print(f"    ❌ All regression combinations failed: {e}")
    
    # Example 3: Flexible noise analysis
    print("  - Flexible noise analysis...")
    try:
        plotter.plot_noise_analysis(
            trial_type='invis',
            color_by='age',
            analysis_type='flexible'
        )
    except Exception as e:
        print(f"    ❌ Flexible noise analysis failed: {e}")


if __name__ == "__main__":
    # Update these paths before running
    if not Path('muh_metadata.csv').exists():
        print("❌ Error: Please update METADATA_PATH and DATA_ROOT_DIR in the script")
        print("   Currently looking for: muh_metadata.csv and muh_data/")
        print("   Update the paths at the top of main() function")
        sys.exit(1)
    
    # Run main analysis
    main()
    
    # Uncomment to run additional examples
    # run_example_analyses()