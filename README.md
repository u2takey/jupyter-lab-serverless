# jupyter-lab-serverless

Create And Run Serverless Function in JupyterLab

## Usage
### 1. Write a Function
![image](/doc/1.png)

### 2. Save Function
![image](/doc/2.png)

### 3. Test Function
![image](/doc/3.png)

### 4. Get Function Statistics
![image](/doc/4.png)

## Prerequisites

* JupyterLab

## Installation

```bash
pip install jupyter-lab-serverless
jupyter labextension install @u2takey/jupyter-lab-serverless
```

## Development

For a development install (requires npm version 4 or later), do the following in the repository directory:

```bash
pip install -e .
jlpm install
jupyter labextension install . --no-build
jupyter lab --debug
```

To rebuild the package and the JupyterLab app:

```bash
npm run build
jupyter lab build
```

