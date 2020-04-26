# COVID-19 status in Spain

Exploring coronavirus pandemic data in Spain territory.

#### Project Status: [On Hold]

## Project Intro/Objective

The purpose of this project is to give clarity to the bunch of data we are exposed daily in this pandemic situation.

To reach this goal we will first create an interactive dashboard to see live status daily by community. Appart from that some relevant indicators will be plotted to monitorize historical information. The second step will be to use machine learning and deep learning to model our data in order to predict the evolution of the pandemic.

Step-by-step project building will be explained in the form of blog articles in my personal website. For more information please check the [Project Proposal](https://github.com/juanlurg/covid-19-spain-dash/blob/master/docs/proposal.pdf)

Final comments are availabel in [Project End Document](https://github.com/juanlurg/covid-19-spain-dash/blob/master/docs/Nanodegree%20Project.pdf)

### Methods Used

- Exploratory Data Analysis
- Data Visualization
- Dashboard building
- Machine Learning
  - Random Forest Regression
  - Gradient Boosting
- Deep Learning
  - ARIMA
  - Moving Averages
  - Exponential Smoothing
  - Double exponential smoothing
  - DeepAR
  - Facebook Prophet

### Technologies

- Python
- Dash
- pandas, matplotlib, plotly, seaborn, numpy
- Jupyter Notebook
- AWS for model training, deployment and batch transforming
- Heroku for dashboard deployment

## Project Description

We will be building our project based in [datadista COVID 19 Spain data repository](https://github.com/datadista/datasets/tree/master/COVID%2019) and for map visualization we will need GeoJSON data of Spain found in [this repository](https://github.com/deldersveld/topojson/blob/master/countries/spain/spain-comunidad-with-canary-islands.json).

The roadmap of the project is going to be:

1. Exploratory Data Analysis
2. Web dashboard developing
3. Feature Engineering and dimensionality reduction if needed.
4. Modeling
5. Evaluation, parameter tunning.
6. Deployment.

## Getting Started

1. Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).
2. Install requirements

```
pip install requirements.txt
```

3. Launch Dash application

```
python .\index.py
```

4. Go to http://127.0.0.1:8050/ to see the dashboard
5. For Jupyter Notebook, navigate to notebooks folder and then

```
jupyter notebook
```

## Featured Notebooks

- [Exploring COVID-19 Spain Data](https://github.com/juanlurg/covid-19-spain-dash/blob/master/notebooks/Exploring%20COVID-19%20Spain%20Data.ipynb)
- [Feature Engineering](https://github.com/juanlurg/covid-19-spain-dash/blob/master/notebooks/Feature%20Engineering.ipynb)
- [Models](https://github.com/juanlurg/covid-19-spain-dash/blob/master/notebooks/Models.ipynb)

## Contributing

**Project owner (Contact): [Juanlu RG](https://github.com/juanlurg/)**

## Contact

- Feel free to contact the repository owner by mail at _juanlu.rgarcia_ @ gmail.com
