import { useState } from "react";
import { searchTickers } from "../utils/api";

const InputForm = ({ onSubmit }) => {
  const [ticker, setTicker] = useState("");
  const [openaiKey, setOpenaiKey] = useState("");
  const [serperKey, setSerperKey] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  const handleTickerSearch = async () => {
    if (ticker.length < 2) return;
    try {
      const results = await searchTickers(ticker);
      setSuggestions(results.slice(0, 10));
      setShowSuggestions(true);
    } catch (err) {
      console.error("Ticker search failed:", err);
    }
  };

  const handleSuggestionClick = (symbol) => {
    setTicker(symbol);
    setShowSuggestions(false);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!ticker || !openaiKey || !serperKey) return;
    onSubmit(ticker, openaiKey, serperKey);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded-xl shadow-md relative">
      {/* Ticker Search */}
      <div className="relative">
        <label className="block mb-1 text-sm font-medium text-gray-700">Stock Ticker</label>
        <div className="flex space-x-2">
          <input
            type="text"
            placeholder="e.g. AAPL or Tesla"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="button"
            onClick={handleTickerSearch}
            className="bg-blue-600 text-white px-3 py-1 rounded-md hover:bg-blue-700 text-sm"
          >
            🔍 Search
          </button>
        </div>
        {showSuggestions && suggestions.length > 0 && (
          <ul className="absolute z-10 mt-1 w-full bg-white border border-gray-300 rounded-lg shadow-lg max-h-48 overflow-y-auto">
            {suggestions.map((item) => (
              <li
                key={item.symbol}
                onClick={() => handleSuggestionClick(item.symbol)}
                className="px-4 py-2 hover:bg-blue-100 cursor-pointer text-sm"
              >
                <strong>{item.symbol}</strong> — {item.name}
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* OpenAI Key */}
      <div>
        <label className="block mb-1 text-sm font-medium text-gray-700">OpenAI API Key</label>
        <input
          type="password"
          placeholder="sk-..."
          value={openaiKey}
          onChange={(e) => setOpenaiKey(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <p className="text-xs text-gray-500 mt-1">
          Get your key from{" "}
          <a
            href="https://platform.openai.com/account/api-keys"
            target="_blank"
            rel="noreferrer"
            className="text-blue-600 underline"
          >
            OpenAI API Dashboard ↗
          </a>
        </p>
      </div>

      {/* Serper Key */}
      <div>
        <label className="block mb-1 text-sm font-medium text-gray-700">Serper API Key</label>
        <input
          type="password"
          placeholder="serper-..."
          value={serperKey}
          onChange={(e) => setSerperKey(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <p className="text-xs text-gray-500 mt-1">
          Create a free key at{" "}
          <a
            href="https://serper.dev"
            target="_blank"
            rel="noreferrer"
            className="text-blue-600 underline"
          >
            serper.dev ↗
          </a>
        </p>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition"
      >
        🚀 Generate Report
      </button>
    </form>
  );
};

export default InputForm;