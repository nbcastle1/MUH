# MUH Data Analysis Pipeline

A comprehensive Python pipeline for analyzing Motor Unit Habituation (MUH) gait data, including stride analysis, performance metrics calculation, and statistical modeling.

## Features

- **Data Processing**: Automated loading and preprocessing of trial data with fragment splicing
- **Performance Metrics**: Calculate success rates, stride variability, motor noise, and asymmetry measures
- **Statistical Analysis**: Regression modeling and binary classification for predictive analysis  
- **Visualization**: Rich plotting capabilities including correlation plots, noise analysis, and stride patterns
- **Export Options**: HTML tables, Excel files, and high-resolution figures

## Project Structure

```
muh_analysis/
├── processed_trial_data.py     # Core data processing and filtering
├── performance_metrics_db.py   # Metrics calculation and statistical analysis
├── plotter.py                  # Visualization and plotting functions
├── trial_splicer.py           # Fragment splicing utilities (optional)
├── main_analysis.py           # Main analysis pipeline
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── figures/                   # Output directory for plots
```

## Quick Start

### 1. Installation

```bash
# Clone or download the files
# Install dependencies
pip install -r requirements.txt
```

### 2. Data Setup

Update the paths in `main_analysis.py`:

```python
METADATA_PATH = 'path/to/your/muh_metadata.csv'
DATA_ROOT_DIR = 'path/to/your/muh_data/'
```

### 3. Run Analysis

```bash
python main_analysis.py
```

## Data Format

### Metadata File (CSV)
Expected columns:
- `ID`: Subject identifier
- `DOB`: Date of birth  
- `Session Date`: Session date
- `age_years`: Age in years
- `age_months`: Age in months

### Trial Data Files (TXT, tab-delimited)
Expected directory structure:
```
data_root/
├── SUBJECT_ID1/
│   ├── primer*.txt    # Mapped to 'vis1'
│   ├── trial*.txt     # Mapped to 'invis' 
│   ├── vis*.txt       # Mapped to 'vis2'
│   └── pref*.txt      # Preference trials
└── SUBJECT_ID2/
    └── ...
```

Required columns in trial files:
- `Stride Number`: Sequential stride identifier
- `Success`: Binary success indicator (0/1)
- `Constant`: Target constant value
- `Upper bound success`/`Lower bound success`: Target boundaries
- `Sum of gains and steps`: Primary outcome measure
- `Right step length`/`Left step length`: For asymmetry calculations

## Usage Examples

### Basic Analysis

```python
from processed_trial_data import ProcessedTrialData
from performance_metrics_db import PerformanceMetricsDB
from plotter import Plotter

# Load and process data
data_manager = ProcessedTrialData('metadata.csv', 'data/')
data_manager = data_manager.filter_trials(
    max_target_size=0.31,
    required_trial_types=['pref', 'invis']
)

# Calculate metrics
metrics_db = PerformanceMetricsDB()
metrics_db.update_metrics(data_manager)

# Create visualizations
plotter = Plotter(metrics_db, data_manager)
plotter.plot_metrics(trial_type='invis', metric='sr', color_by='age_years')
```

### Statistical Analysis

```python
# Regression analysis
results = metrics_db.perform_success_rate_regression(
    trial_type='invis',
    condition='max_const', 
    selected_condition_metrics=['asymmetry', 'msl']
)
plotter.plot_regression_results(results)

# Binary classification
classification = metrics_db.perform_binary_classification(
    trial_type='invis',
    threshold=0.68
)
plotter.plot_classification_results(classification)
```

### Advanced Filtering

```python
# Filter subjects and trials
filtered_data = data_manager.filter_trials(
    min_age=8,
    max_age=16,
    max_target_size=0.3,
    min_strides=50,
    max_strides=400,
    required_trial_types=['vis1', 'invis', 'vis2', 'pref']
)
```

## Key Classes

### ProcessedTrialData
- Loads and processes raw trial files
- Handles fragment splicing for interrupted trials
- Applies data filters and validation
- Detects and flags anomalous data points

### PerformanceMetricsDB  
- Calculates comprehensive performance metrics
- Stores results in structured database format
- Provides statistical analysis capabilities
- Exports results to various formats

### Plotter
- Creates publication-ready visualizations
- Supports multiple plot types and customization
- Handles age-based coloring and trend analysis
- Automatically saves figures with appropriate naming

## Metrics Calculated

### Trial Performance
- **Success Rate**: Proportion of successful strides
- **Mean Stride Length**: Average sum of gains and steps  
- **Stride Variability**: Standard deviation of stride lengths
- **Error**: Deviation from target constant
- **Asymmetry**: Step length asymmetry measure
- **Strides Between Success**: Average interval between successful strides

### Motor Control
- **Motor Noise**: Variability in normalized step lengths (from preference trials)
- **Preference Asymmetry**: Step length asymmetry during free walking

### Trial Characteristics
- **Target Size**: Minimum target window size
- **Constant Range**: Max/min constant values used
- **Trial Order**: Whether max or min constant appeared first

## Visualization Options

### Available Plot Types
- Success rate vs age (by trial type and condition)
- Motor noise analysis (vs success rate, vs target thresholds)
- Stride patterns over time (with age grouping)
- Correlation analysis between any metrics
- Regression results with feature importance
- Classification performance (ROC curves, confusion matrices)
- Change in stride length after success/failure

### Customization Options
- Color by any metric (age, motor noise, etc.)
- Multiple trial types and conditions
- Age binning and grouping
- Smoothing and filtering options
- Export formats (PNG, PDF, etc.)

## Configuration

### Analysis Parameters
Modify these in `main_analysis.py`:
- `MAX_TARGET_SIZE`: Maximum target size to include
- `MAX_STRIDES`: Maximum trial length
- `REQUIRED_TRIAL_TYPES`: Which trial types must be present

### Plot Settings
Customize in `Plotter.__init__()`:
- Figure sizes and DPI
- Color schemes and transparency
- Grid and styling options

## Troubleshooting

### Common Issues

1. **File Not Found Errors**
   - Check that metadata and data paths are correct
   - Ensure file permissions allow reading

2. **Missing Columns**
   - Verify trial files contain required columns
   - Check for consistent column naming across files

3. **Empty Results**
   - Filters may be too restrictive
   - Check that subjects have required trial types

4. **Memory Issues**
   - Large datasets may require chunked processing
   - Consider filtering data earlier in pipeline

### Debug Mode
Enable detailed logging:
```python
data_manager = ProcessedTrialData(
    metadata_path='metadata.csv',
    data_root_dir='data/',
    debug=True  # Enable verbose output
)
```

## Contributing

To extend the analysis pipeline:

1. **Add New Metrics**: Extend `calculate_performance_metrics()` in `PerformanceMetricsDB`
2. **Add New Plots**: Create new methods in `Plotter` class
3. **Add New Filters**: Extend `filter_trials()` in `ProcessedTrialData` 
4. **Add New Analysis**: Create new statistical methods in `PerformanceMetricsDB`

## License

This project is intended for research use. Please cite appropriately if used in publications.

## Support

For questions or issues, please check:
1. This README for common solutions
2. Code comments for implementation details
3. Example outputs in the `figures/` directory