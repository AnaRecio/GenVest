import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # Use a non-interactive backend suitable for servers

import io
import base64

def plot_predictions(historical_df, forecast_df):
    """
    Generates a matplotlib line plot comparing historical and forecasted stock prices.

    Parameters:
        historical_df (pd.DataFrame): DataFrame containing past prices with datetime index and 'price' column.
        forecast_df (pd.DataFrame): DataFrame containing forecasted prices with 'date' and 'predicted_price' columns.

    Returns:
        str: Base64-encoded PNG image of the plot for embedding in HTML or PDF.
    """
    # Initialize plot with fixed dimensions
    plt.figure(figsize=(10, 5))

    # Plot historical prices
    plt.plot(historical_df.index, historical_df['price'], label='Historical')

    # Plot forecasted prices with a dashed line
    plt.plot(forecast_df['date'], forecast_df['predicted_price'], label='Forecast', linestyle='--')

    # Configure chart labels and legend
    plt.title("Stock Price Prediction")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()

    # Save figure to a buffer in PNG format
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the image buffer to base64 string
    image_base64 = base64.b64encode(buffer.read()).decode()

    # Release memory associated with the figure
    plt.close()

    return image_base64
