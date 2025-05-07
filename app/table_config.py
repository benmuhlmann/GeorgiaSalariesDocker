from dash import dash_table

# Constants
PAGE_SIZE = 15
YEARS = list(range(2024, 2012, -1))  # values for the year dropdown

# Table formatting
money = dash_table.FormatTemplate.money(0)

# Table styling
TABLE_STYLE = {
    'style_table': {'overflowX': 'auto'},
    'style_cell': {
        'textAlign': 'left',
        'font-family': '"Lato", sans-serif',
        'fontSize': 12,
        'textOverflow': 'ellipsis',
        'maxWidth': 0,
    },
    'style_cell_conditional': [
        {'if': {'column_id': 'Name'}, 'width': '15%'},
        {'if': {'column_id': 'Title'}, 'width': '30%'},
        {'if': {'column_id': 'Organization'}, 'width': '30%'},
        {'if': {'column_id': 'Salary'}, 'width': '15%'},
        {'if': {'column_id': 'Fiscal Year'}, 'width': '10%'},
    ],
    'style_data_conditional': [
        {'if': {'row_index': 'odd'}, 'backgroundColor': 'RGB(200, 220, 240)'}  # stripe rows
    ]
}

# Table columns configuration
TABLE_COLUMNS = [
    dict(id='Name', name='Name'),
    dict(id='Title', name='Title'),
    dict(id='Organization', name='Organization'),
    dict(id='Salary', name='Salary', type='numeric', format=money),
    dict(id='Fiscal Year', name='Fiscal Year', type='numeric')
] 