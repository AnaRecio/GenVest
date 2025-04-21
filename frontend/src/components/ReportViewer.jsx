const ReportViewer = ({ report }) => {
  if (!report) return null;

  const marketData = report.marketData || {};
  const news = report.news || {};
  const swot = report.swot || "No SWOT analysis available.";
  const recommendation = report.recommendation || "No recommendation generated.";
  const mae = report.mae ?? null;
  const forecast = report.forecast || [];

  function formatMarketCap(value) {
    if (!value || isNaN(value)) return "N/A";
    const num = Number(value);
    if (num >= 1_000_000_000_000) return (num / 1_000_000_000_000).toFixed(1) + "T";
    if (num >= 1_000_000_000) return (num / 1_000_000_000).toFixed(1) + "B";
    if (num >= 1_000_000) return (num / 1_000_000).toFixed(1) + "M";
    return num.toLocaleString();
  }

  function getForecastPrice(daysAhead) {
    const entry = forecast?.[daysAhead - 1];
    return entry?.predicted_price ?? null;
  }

  function getMAEColor(mae) {
    if (mae < 1) return "text-green-600";
    if (mae < 3) return "text-yellow-600";
    return "text-red-600";
  }

  return (
    <div className="space-y-6 mt-8">
      {/* Market Overview */}
      <div className="bg-white rounded-2xl shadow-md p-6">
        <h2 className="text-2xl font-bold text-blue-900 mb-2">
          {report.company ?? "Unknown Company"} ({report.ticker ?? "N/A"})
        </h2>
        <div className="grid grid-cols-2 gap-4 text-sm text-gray-700">
          <div>📈 Current Price: <strong>${marketData.currentPrice ?? "N/A"}</strong></div>
          <div>🏛️ Market Cap: {formatMarketCap(marketData.marketCap)}</div>
          <div>📊 P/E Ratio: {marketData.trailingPE ?? "N/A"}</div>
          <div>📉 52-Week Low: {marketData.fiftyTwoWeekLow ?? "N/A"}</div>
          <div>📈 52-Week High: {marketData.fiftyTwoWeekHigh ?? "N/A"}</div>
          <div>📦 Sector: {marketData.sector ?? "N/A"}</div>
          <div>🛒 Market: {marketData.exchange ?? "N/A"}</div>
        </div>
      </div>

      {/* Forecast Chart + Summary */}
      {report.priceChart && (
        <div className="bg-white rounded-2xl shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4 text-blue-800">📊 Price Forecast</h3>
          <img
            src={`data:image/png;base64,${report.priceChart}`}
            alt="Chart"
            className="w-full max-w-3xl"
          />

          {/* Forecast Summary Box */}
          <div className="mt-6 max-w-sm bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-semibold text-blue-800 mb-2 text-sm">📉 Forecast Summary</h4>
            <ul className="text-sm text-gray-800 space-y-1">

              {/* MAE Display */}
              {typeof mae === "number" && (
                <li className="mb-2">
                  📏 Model Validation MAE:{" "}
                  <strong className={`${getMAEColor(mae)}`}>
                    ${mae.toFixed(2)}
                  </strong>
                </li>
              )}

              {/* Forecasted Price and Change */}
              {[7, 14, 30].map((day) => {
                const predicted = getForecastPrice(day);
                const current = marketData.currentPrice;

                const change =
                  typeof predicted === "number" && typeof current === "number"
                    ? (((predicted - current) / current) * 100).toFixed(2)
                    : null;

                return (
                  <li key={day}>
                    Next {day} Days:{" "}
                    <strong>
                      {typeof predicted === "number" ? `$${predicted.toFixed(2)}` : "N/A"}
                    </strong>
                    {change && (
                      <span
                        className={`ml-2 font-medium ${
                          change >= 0 ? "text-green-600" : "text-red-600"
                        }`}
                      >
                        ({change > 0 ? "+" : ""}
                        {change}%)
                      </span>
                    )}
                  </li>
                );
              })}
            </ul>
          </div>
        </div>
      )}

      {/* News */}
      {news.summary && (
        <div className="bg-white rounded-2xl shadow-md p-6">
          <h3 className="text-xl font-semibold mb-2 text-blue-800">📰 News Summary</h3>
          <p className="text-gray-800">{news.summary}</p>
        </div>
      )}

      {/* SWOT */}
      <div className="bg-white rounded-2xl shadow-md p-6">
        <h3 className="text-xl font-semibold mb-2 text-blue-800">📋 SWOT & Investment Summary</h3>
        <pre className="bg-gray-100 p-4 rounded whitespace-pre-wrap text-sm">{swot}</pre>
      </div>

      {/* Recommendation */}
      <div className="bg-white rounded-2xl shadow-md p-6">
        <h3 className="text-xl font-semibold mb-2 text-blue-800">💡 AI Recommendation</h3>
        <p className="text-gray-900">{recommendation}</p>
      </div>
    </div>
  );
};

export default ReportViewer;
