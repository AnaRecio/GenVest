import matplotlib.pyplot as plt
import io
import base64

def plot_predictions(historical_df, forecast_df):
    """
    Generates a plot showing historical and predicted stock prices.
    Returns a base64-encoded PNG.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(historical_df.index, historical_df['price'], label='Historical')
    plt.plot(forecast_df['date'], forecast_df['predicted_price'], label='Forecast', linestyle='--')
    
    plt.title("Stock Price Prediction")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()

    # Save plot to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()

    return image_base64
