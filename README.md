# Data Plotting App
Web app for plot generation.

## Preparation

### For Linux

#### Prepare virtual environment

1. Create and activate virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```
2. Install required packages:

```
pip3 install -r requirements.txt
```

### For Windows

#### Prepare virtual environment

1. Create and activate virtual environment:

```
python -m venv .venv
.venv\Scripts\activate
```

2. Install required packages:

```
pip install -r requirements.txt
```

## Usage

### For Linux

Activate virtual environment: `source .venv/bin/activate`.

Run app: `python3 app.py`.

### For Windows

Activate virtual environment: `.venv\Scripts\activate`.

Run app: `python -m  ui.app`.

### General

Go to (http://127.0.0.1:8000/)[http://127.0.0.1:8000/] in your browser.

1. You can now plot the data by selecting columns, scales and color theme.
2. You can zoom the plot by selecting a rectangle area on the plot with the mouse.
3. Finally, you can download the plot in one of the following formats: PNG, JPG, SVG.
