from dash import Input, Output
from table_config import PAGE_SIZE

def register_callbacks(app, df):
    """
    Register all callbacks for the Dash application.
    
    Args:
        app: Dash application instance
        df: pandas DataFrame containing the salary data
    """
    @app.callback(
        Output("tbl", "data"),
        Output("tbl", "tooltip_data"),
        Input("my-year-dropdown", "value"),
        Input("my-dynamic-input", "value"),
        Input("my-search-toggle", "value"),
        Input("tbl", "page_current")
    )
    def display_table(year_value, search_value, search_toggle, page_current):
        """
        Callback function for table filtering and displaying based on user inputs.
        Defaults to unfiltered data when nothing is inputted in the search bar

        Args:
            year_value: the year selected from the dropdown
            search_value: the user's inputted search value (text)
            search_toggle: Name, Title, or Organization
            page_current: The selected data page
            
        Returns:
            tuple: (filtered data records, tooltip data)
        """
        df_year = df[df['Fiscal Year'] == year_value]

        # If there's no search value, display everything
        if not search_value:
            dff = df_year
        # otherwise, filter based on the user's search
        elif search_toggle == "Name":
            dff = df_year[df_year['Name'].str.contains(search_value, case=False, regex=False)]
        elif search_toggle == "Title":
            dff = df_year[df_year['Title'].str.contains(search_value, case=False, regex=False)]
        elif search_toggle == "Organization":
            dff = df_year[df_year['Organization'].str.contains(search_value, case=False, regex=False)]

        # Filter dff to just the current page - huge performance improvements with backend pagination
        dff = dff.iloc[page_current*PAGE_SIZE:(page_current + 1)*PAGE_SIZE]

        # Generate a tooltip list for the currently displayed page
        new_tooltip_list = [
            {
                column: {'value': str(value), 'type': 'text'}
                for column, value in row.items()
            } for row in dff.to_dict('records')
        ]

        return dff.to_dict("records"), new_tooltip_list 