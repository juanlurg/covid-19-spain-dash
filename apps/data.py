from datetime import datetime

import numpy as np
import pandas as pd

file_data = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_datos_isciii.csv'
population = 'https://raw.githubusercontent.com/codeforspain/ds-poblacion/master/data/poblacion-autonomias.csv'


class Dataset(object):
    '''
    The Dataset object contains all the data we need in the format we need

    Paremeters
    ----------
    url: str
        The url to the csv file with the data we are using

    '''

    def __init__(self, url):
        '''
        Read csv, transform str to datetime group df by date to have Spain overall
        drop innecesary column and call today's computing data
        '''
        self.df = pd.read_csv(url)
        self.df['Fecha'] = pd.to_datetime(self.df['Fecha'])
        self.df['Casos'] = self.df['PCR+'] + self.df['TestAc+']
        self.df['Casos Activos'] = self.df['Casos'] - \
            self.df['Fallecidos'] - self.df['Recuperados']
        self.compute_today_df()
        self.df_spain = self.df.groupby('Fecha').sum()
        self.df_spain = self.df_spain.drop(columns=['cod_ine'])

    def last_update(self):
        '''
        Returns last day's date
        '''
        return self.df['Fecha'].max()

    def compute_today_df(self):
        '''
        Make calculation to have last day's metrics
        also we join the population of every community
        and/to calculate metrics per million of inhabitants
        '''
        self.hoy = self.df[self.df['Fecha'] == self.last_update()]
        self.hoy['Casos Activos'] = self.hoy['Casos'] - \
            self.hoy['Fallecidos'] - self.hoy['Recuperados']
        self.hoy = self.hoy.drop(columns=['Hospitalizados', 'UCI'])
        pop = pd.read_csv(population)
        pop = pop[pop['year'] == 2015]

        self.hoy = pd.merge(self.hoy, pop, left_on='cod_ine',
                            right_on='ine_code', how='left')
        self.hoy['1k_population'] = self.hoy['value']/1000000
        self.hoy = self.hoy.drop(columns=['name', 'ine_code', 'year', 'value'])
        self.hoy['casos_1k'] = self.hoy['Casos'] / self.hoy['1k_population']
        self.hoy['casos_activos_1k'] = self.hoy['Casos Activos'] / \
            self.hoy['1k_population']
        self.hoy['fallecidos_1k'] = self.hoy['Fallecidos'] / \
            self.hoy['1k_population']
        self.hoy['recuperados_1k'] = self.hoy['Recuperados'] / \
            self.hoy['1k_population']
        self.hoy = self.hoy.sort_values(by='Casos', ascending=False)

    def metrics(self):
        '''
        Compute overall metrics
        '''
        self.df_grouped = self.df.groupby('Fecha').sum()
        self.infected = self.df_grouped['Casos'].iloc[-1].astype(np.int64)
        self.deseased = self.df_grouped['Fallecidos'].iloc[-1].astype(np.int64)
        self.recovered = self.df_grouped['Recuperados'].iloc[-1].astype(
            np.int64)
        self.active_cases = self.infected - self.deseased - self.recovered

        self.inc_infected = self.infected - self.df_grouped['Casos'].iloc[-2]
        self.inc_deseased = self.deseased - \
            self.df_grouped['Fallecidos'].iloc[-2]
        self.inc_recovered = self.recovered - \
            self.df_grouped['Recuperados'].iloc[-2]
        self.inc_active_cases = self.inc_infected - self.inc_recovered

    def dict_metrics(self):
        '''
        Make a dict for the metrics and for the increments
        (just to make it easier to plot it in the app)
        '''
        self.metrics_dict = {
            "Casos activos": self.active_cases,
            "Infectados": self.infected,
            "Fallecidos": self.deseased,
            "Recuperados": self.recovered
        }
        self.inc_dict = {
            "Casos activos": self.inc_active_cases,
            "Infectados": self.inc_infected,
            "Fallecidos": self.inc_deseased,
            "Recuperados": self.inc_recovered
        }

    def calculate_increment_columns(self):
        '''
        For 'Casos' 'Fallecidos' 'Recuperados' calculate difference and 
        pct change from one day to the next
        '''
        cols = ['Casos', 'Fallecidos', 'Recuperados']

        for col in cols:
            self.df_spain['inc_{}'.format(
                col)] = self.df_spain[col].diff()
            self.df_spain['inc_pct_{}'.format(
                col)] = self.df_spain[col].pct_change().replace(np.inf, np.nan).dropna()

    def data_proc(self):
        '''
        Make data for the stacked bar chart of communities and also add special dates
        this was made this way because otherwise we have a conflict between Plotly JS format and Python dictionaries
        '''
        self.data = []
        for comunidad in self.hoy['CCAA'].unique().tolist():
            self.data.append(
                {'x': pd.DatetimeIndex(self.df[self.df['CCAA'] == comunidad]['Fecha']).to_pydatetime(
                ), 'y': self.df[self.df['CCAA'] == comunidad]['Casos'], 'name': comunidad, 'type': 'bar'}
            )
        self.data.append(
            {'x': [datetime.strptime('2020-03-14 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-14 00:01', '%Y-%m-%d %H:%M')], 'y': [
                0, self.df_spain['Casos'].max()], 'type': 'line', 'name': 'Estado de alarma', 'line': {'color': 'rgb(100, 105, 109)', 'width': '4', 'dash': 'dot'}})
        self.data.append(
            {'x': [datetime.strptime('2020-03-29 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-29 00:01', '%Y-%m-%d %H:%M')], 'y': [
                0, self.df_spain['Casos'].max()], 'type': 'line', 'name': 'Confinamiento estricto', 'line': {'color': 'rgb(143, 147, 150)', 'width': '4', 'dash': 'dot'}})
        self.data.append(
            {'x': [datetime.strptime('2020-04-13 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-04-13 00:01', '%Y-%m-%d %H:%M')], 'y': [
                0, self.df_spain['Casos'].max()], 'type': 'line', 'name': 'Vuelta al trabajo', 'line': {'color': 'rgb(100, 105, 109)', 'width': '4', 'dash': 'dot'}})


# Create the object and call necessary methods
dataset = Dataset(file_data)
dataset.compute_today_df()
dataset.metrics()
dataset.dict_metrics()
dataset.calculate_increment_columns()
dataset.data_proc()
