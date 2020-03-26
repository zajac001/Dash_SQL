import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import sqlite3
import os
from datetime import datetime
import datetime


company_1_capital = pd.read_csv("company_1.csv", delimiter= ";",engine="python")
company_1_capital.columns = ["Created", "Amount", "Number", "Extends_ID"]

company_1_capital['Created'] = pd.to_datetime(pd.to_datetime(company_1_capital['Created'], \
                                                           format='%d.%m.%Y %H:%M').dt.strftime('%Y-%m'))

company_1_conditions = [
    company_1_capital['Number'] + company_1_capital['Extends_ID'] == 1,
    company_1_capital['Number'] + company_1_capital['Extends_ID'] == company_1_capital['Number'],
]

company_1_outputs = ['Product_1', 'Product_2']

company_1_change = np.select(company_1_conditions, company_1_outputs, 'Product_3')
company_1_typ = pd.DataFrame(company_1_change)

company_1_typ = company_1_typ.rename(columns={0: 'Typ'})

company_1_typ['Typ'] = company_1_typ['Typ'].astype(str)
company_1_capital = pd.concat([company_1_capital, company_1_typ], axis=1, sort=False)

database = 'database_dashboard.db'
con = sqlite3.connect(os.path.join(os.getcwd(), database))

company_1_capital.to_sql("company_1_capital", con, if_exists='replace', index=False)


sql_company_1_product_1 = pd.read_sql_query("""
SELECT Distinct Created, SUM(Amount) AS Amount
From company_1_capital
WHERE Typ = "Product_1"
Group by Created
Order by Created ASC
""", con)

sql_company_1_product_2 = pd.read_sql_query("""
SELECT Distinct Created, SUM(Amount) AS Amount
From company_1_capital
WHERE Typ = "Product_2"
Group by Created
Order by Created ASC
""", con)

sql_company_1_product_3 = pd.read_sql_query("""
SELECT Distinct Created, SUM(Amount) AS Amount
From company_1_capital
WHERE Typ = "Product_3"
Group by Created
Order by Created ASC
""", con)


company_2_capital = pd.read_csv("company_2.csv", delimiter= ";",engine="python")
company_2_capital.columns = ["Created", "Amount", "Number", "Extends_ID"]


company_2_capital['Created'] = pd.to_datetime(pd.to_datetime(company_2_capital['Created'], \
                                                          format='%d.%m.%Y %H:%M').dt.strftime('%Y-%m'))


company_2_conditions = [
    company_2_capital['Number'] + company_2_capital['Extends_ID'] == 1,
    company_2_capital['Number'] + company_2_capital['Extends_ID'] == company_2_capital['Number'],
]

company_2_outputs = ['Product_1', 'Product_2']

company_2_change = np.select(company_2_conditions, company_2_outputs, 'Product_3')
company_2_typ = pd.DataFrame(company_2_change)

company_2_typ = company_2_typ.rename(columns={0: 'Typ'})

company_2_typ['Typ'] = company_2_typ['Typ'].astype(str)
company_2_capital = pd.concat([company_2_capital, company_2_typ], axis=1, sort=False)



company_2_capital.to_sql("company_2_capital", con, if_exists='replace', index=False)



sql_company_2_product_1 = pd.read_sql_query("""
SELECT Distinct Created, SUM(Amount) AS Amount
From company_2_capital
WHERE Typ = "Product_1"
Group by Created
Order by Created ASC
""", con)

sql_company_2_product_2 = pd.read_sql_query("""
SELECT Distinct Created, SUM(Amount) AS Amount
From company_2_capital
WHERE Typ = "Product_2"
Group by Created
Order by Created ASC
""", con)

sql_company_2_product_3 = pd.read_sql_query("""
SELECT Distinct Created, SUM(Amount) AS Amount
From company_2_capital
WHERE Typ = "Product_3"
Group by Created
Order by Created ASC
""", con)


colors={
    'background': '#111111',
    'text': '#7FDBFF'
}


app = dash.Dash("dashboard")


company_1_capital['month']=pd.to_datetime(company_1_capital['Created'])
company_1_capital.set_index(['month'],inplace=True)


company_1_capital_wykres = dcc.Graph(
        id='company_1_capital',
        figure={
            'data': [{'x': sql_company_1_product_1['Created'], 'y': sql_company_1_product_1['Amount'], 'type': 'line', 'name': 'Product_1'},
                {'x': sql_company_1_product_2['Created'], 'y': sql_company_1_product_2['Amount'], 'type': 'line', 'name': 'Product_2'},
                {'x': sql_company_1_product_3['Created'], 'y': sql_company_1_product_3['Amount'], 'type': 'line', 'name': 'Product_3'}
            ],
            'layout': {
                'title': 'Company 1 Total capital'
            }
        }
    )



company_2_capital['month']=pd.to_datetime(company_2_capital['Created'])
company_2_capital.set_index(['month'],inplace=True)


company_2_capital_wykres = dcc.Graph(
        id='company_2_capital',
        figure={
            'data': [{'x': sql_company_2_product_1['Created'], 'y': sql_company_2_product_1['Amount'], 'type': 'line', 'name': 'Product_1'},
                {'x': sql_company_2_product_2['Created'], 'y': sql_company_2_product_2['Amount'], 'type': 'line', 'name': 'Product_2'},
                {'x': sql_company_2_product_3['Created'], 'y': sql_company_2_product_3['Amount'], 'type': 'line', 'name': 'Product_3'}
            ],
            'layout': {
                'title': 'Company 2 Total capital'
            }
        }
    )

app.layout = html.Div([
    html.H1('Dashboard'),
    company_1_capital_wykres,
    company_2_capital_wykres,

])

app.run_server(debug=True)
