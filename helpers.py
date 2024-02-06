import requests
import pandas as pd



def co2_ppm_df():
        # df = pd.read_csv(dir+'co2_mm_mlo.csv', encoding='utf-8', comment='#')
        df = pd.read_csv('https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.csv', comment='#')
        df['date'] = df.apply(lambda row: pd.to_datetime(str(int(row.year)) + '-' + str(int(row.month)), format='%Y-%m'), axis=1)
        df = df[['date', 'average', 'deseasonalized']]
        # df['average_year_change'] = df.average.diff(12)
        df['deseasonalized_change'] = df.deseasonalized.diff(12)
        df = df[df.date > '1959-12-31']
        df = df.melt(id_vars='date')
        df['type_group'] = df.apply(lambda row: 'Actual values' if row.variable in ['average', 'deseasonalized'] else 'Annual Change', axis=1)
        df['variable'] = df.variable.map({
                'deseasonalized': 'Seasonally adjusted',
                'average': 'Month Average',
                'deseasonalized_change': 'Annual change in seasonally adjusted value'
        })
        # df['variable'] = df['variable'].apply(lambda x: x.replace('average_year_change', 'average').replace('deseasonalized_change', 'deseasonalized'))
        return df