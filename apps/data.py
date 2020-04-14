import numpy as np
import pandas as pd

file_data = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_datos_isciii.csv'
population = 'https://raw.githubusercontent.com/codeforspain/ds-poblacion/master/data/poblacion-autonomias.csv'


class Dataset:
    def __init__(self, url):
        self.df = pd.read_csv(url)
        self.df['Fecha'] = pd.to_datetime(self.df['Fecha'])
        self.compute_today_df()
        self.df_spain = self.df.groupby('Fecha').sum()
        self.df_spain = self.df_spain.drop(columns=['cod_ine'])

    def last_update(self):
        return self.df['Fecha'].max()

    def compute_today_df(self):
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

    def metrics(self):
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
        cols = ['Casos', 'Fallecidos', 'Recuperados']

        for col in cols:
            self.df_spain['inc_{}'.format(
                col)] = self.df_spain[col].diff()
            self.df_spain['inc_pct_{}'.format(
                col)] = self.df_spain[col].pct_change().replace(np.inf, np.nan).dropna()


dataset = Dataset(file_data)
dataset.compute_today_df()
dataset.metrics()
dataset.dict_metrics()
dataset.calculate_increment_columns()
