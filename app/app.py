from dash import Dash
from aws_utils import initialize_s3_client, load_data_from_s3
from layout import create_layout
from callbacks import register_callbacks
import os

# Initialize S3 client and load data
print("Loading dataset from S3...")
s3_client = initialize_s3_client()
df = load_data_from_s3(s3_client)
if df is None:
    print("Failed to load data from S3. Please check your AWS credentials and S3 configuration.")
    exit(1)

# Create initial dataframe for display
df_init = df.query("`Fiscal Year` == 2024").iloc[0:16]

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[{
    "href": (
        "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap"
    ),
    "rel": "stylesheet",
}])
server = app.server

# Set app title
app.title = 'GA Salaries'

# Create layout
app.layout = create_layout(df_init)

# Register callbacks
register_callbacks(app, df)

if __name__ == '__main__':
    # Get port from environment variable or default to 8050
    port = int(os.getenv('PORT', 8050))
    # Get debug mode from environment variable
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Dash app server on port {port}...")
    app.run(debug=debug, host='0.0.0.0', port=port) 