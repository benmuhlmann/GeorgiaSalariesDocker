from dash import html, dcc, dash_table
from table_config import TABLE_COLUMNS, TABLE_STYLE, PAGE_SIZE, YEARS

def create_layout(df_init):
    """
    Create the Dash application layout.
    
    Args:
        df_init: Initial DataFrame to display in the table
        
    Returns:
        html.Div: The complete application layout
    """
    return html.Div(
        children=[
            # header
            html.Div(
                children=html.H1(
                    children='Georgia Employee Salaries By Year',
                    className='header-title'
                ),
                className='header'
            ),
            # main content
            html.Div(
                children=[
                    # filters
                    html.Div(
                        children=[
                            # search bar and text tip
                            html.Div(
                                children=[
                                    html.Div('Search Salaries', className='search-tip'),
                                    dcc.Input(
                                        type='text',
                                        debounce=False,
                                        id='my-dynamic-input',
                                        className='search-bar'
                                    )
                                ],
                                className='search-filter'
                            ),
                            # year dropdown and text above
                            html.Div(
                                children=[
                                    html.Div("Year"),
                                    dcc.Dropdown(
                                        value=2024,
                                        options=YEARS,
                                        id='my-year-dropdown',
                                        maxHeight=200,
                                        searchable=False,
                                        className='year-dropdown'
                                    )
                                ],
                                className="year-filter"
                            ),
                            dcc.RadioItems(
                                options=['Name', 'Title', 'Organization'],
                                value='Name',
                                id='my-search-toggle',
                                className="search-toggle"
                            )
                        ],
                        className='filters'
                    ),
                    # table
                    html.Div(
                        children=dash_table.DataTable(
                            id='tbl',
                            page_size=PAGE_SIZE,
                            page_action='custom',
                            page_current=0,
                            columns=TABLE_COLUMNS,
                            data=df_init.to_dict("records"),
                            tooltip_data=[
                                {
                                    column: {'value': str(value), 'type': 'markdown'}
                                    for column, value in row.items()
                                } for row in df_init.to_dict('records')
                            ],
                            tooltip_delay=0,
                            tooltip_duration=None,
                            **TABLE_STYLE
                        ),
                        className='table'
                    )
                ],
                className='main-content'
            ),
            # footer
            html.Footer(
                children=[
                    html.A(
                        "Ben Muhlmann",
                        href="https://github.com/benmuhlmann/GeorgiaSalaries",
                        target="_blank"
                    ),
                    html.Span(" 2025")
                ],
                className='footer'
            )
        ]
    ) 