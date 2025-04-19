const ReportViewer = ({ report }) => {
  if (!report) return null;

  const marketData = report.marketData || {};
  const news = report.news || {};
  const swot = report.swot || "No SWOT analysis available.";
  const recommendation = report.recommendation || "No recommendation generated.";

  function formatMarketCap(value) {
    if (!value || isNaN(value)) return "N/A";
    const num = Number(value);
  
    if (num >= 1_000_000_000_000) return (num / 1_000_000_000_000).toFixed(1) + "T";
    if (num >= 1_000_000_000) return (num / 1_000_000_000).toFixed(1) + "B";
    if (num >= 1_000_000) return (num / 1_000_000).toFixed(1) + "M";
    return num.toLocaleString(); // fallback
  }
  

  return (
    <div className="space-y-6 mt-8">
      <div className="bg-white rounded-2xl shadow-md p-6">
        <h2 className="text-2xl font-bold text-blue-900 mb-2">
          {report.company ?? "Unknown Company"} ({report.ticker ?? "N/A"})
        </h2>
        <div className="grid grid-cols-2 gap-4 text-sm text-gray-700">
          <div>📈 Current Price: <strong>${marketData.currentPrice ?? "N/A"}</strong></div>
          <div>🏛️ Market Cap: {formatMarketCap(report.marketData.marketCap) ?? "N/A"}</div>
          <div>📊 P/E Ratio: {marketData.trailingPE ?? "N/A"}</div>
          <div>📉 52-Week Low: {marketData.fiftyTwoWeekLow ?? "N/A"}</div>
          <div>📈 52-Week High: {marketData.fiftyTwoWeekHigh ?? "N/A"}</div>
          <div>📦 Sector: {marketData.sector ?? "N/A"}</div>
        </div>
      </div>

      {report.priceChart && (
        <div className="bg-white rounded-2xl shadow-md p-6">
          <h3 className="text-xl font-semibold mb-2 text-blue-800">📊 Price Forecast</h3>
          <img src={`data:image/png;base64,${report.priceChart}`} alt="Chart" className="w-full max-w-3xl" />
        </div>
      )}

      {news.summary && (
        <div className="bg-white rounded-2xl shadow-md p-6">
          <h3 className="text-xl font-semibold mb-2 text-blue-800">📰 News Summary</h3>
          <p className="text-gray-800">{news.summary}</p>
        </div>
      )}

      <div className="bg-white rounded-2xl shadow-md p-6">
        <h3 className="text-xl font-semibold mb-2 text-blue-800">📋 SWOT & Investment Summary</h3>
        <pre className="bg-gray-100 p-4 rounded whitespace-pre-wrap text-sm">{swot}</pre>
      </div>

      <div className="bg-white rounded-2xl shadow-md p-6">
        <h3 className="text-xl font-semibold mb-2 text-blue-800">💡 AI Recommendation</h3>
        <p className="text-gray-900">{recommendation}</p>
      </div>
    </div>
  );
};

export default ReportViewer;

