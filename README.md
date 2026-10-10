# Secure Minimum-Cost Computer Network Design

This project implements a web application for designing the minimum-cost communication network that connects all offices in an organization.

## Overview

The application allows the user to enter:
- the number of offices
- the available communication links
- the installation cost for each link
- optional bandwidth information

It then compares the two required MST algorithms:
- Prim's Minimum Spanning Tree
- Kruskal's Minimum Spanning Tree
- Disjoint Set / Union-Find

The system also reports a comparison of the algorithms in terms of:
- number of vertices
- number of edges
- execution time
- number of operations

## Features

- Interactive web interface built with Flask
- Parsing of office-link data from user input
- Prim's MST implementation
- Kruskal's MST implementation
- Union-Find / Disjoint Set structure
- Real-time comparison of algorithm performance
- Render-ready deployment configuration

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://localhost:5000
```

## Input format

Use one edge per line:

```text
1 2 10 50
2 3 5 80
3 4 8 35
```

Format:

```text
office1 office2 cost [bandwidth]
```

The bandwidth value is optional.

## Deployment on Render

This repository includes a `render.yaml` file for easy deployment to Render.

Steps:
1. Connect the repository to Render.
2. Use the included `render.yaml` configuration.
3. Deploy the web service.

## Project structure

```text
app.py
requirements.txt
render.yaml
templates/
  index.html
static/
  styles.css
README.md
```

## Example result

The app will compute the MST cost and display a side-by-side comparison of Prim's and Kruskal's algorithms.

## License

This project is intended for academic and demonstration use.
