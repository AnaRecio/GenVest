const BASE_URL = "https://genvest-production-ec2c.up.railway.app/api";

/**
 * Sends user input to the backend to generate an investment report
 */
export async function generateReport(ticker, openaiKey, serperKey) {
  const res = await fetch(`${BASE_URL}/report`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    // Send ticker and API keys to the backend
    body: JSON.stringify({
      ticker,
      openai_key: openaiKey,
      serper_key: serperKey,
    }),
  });

  // Throw an error if the backend response is not successful
  if (!res.ok) {
    throw new Error("Failed to generate report");
  }

  // Return parsed report JSON
  return await res.json();
}

/**
 * Downloads a generated investment report as a PDF file
 */
export const downloadPDF = async (report) => {
  try {
    // Send the report object to the backend for PDF generation
    const response = await fetch("http://localhost:5000/api/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ report }),
    });

    // Handle failed download attempt
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    // Convert response to blob and trigger file download in browser
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "genvest_report.pdf";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    // Log error and show fallback alert
    console.error("Download failed:", error);
    alert("❌ Failed to download PDF report.");
  }
};

/**
 * Fetches stock ticker suggestions based on user query
 */
export async function searchTickers(query) {
  // Call backend API with search query as query param
  const res = await fetch(`${BASE_URL}/search?q=${encodeURIComponent(query)}`);

  // Handle request failure
  if (!res.ok) {
    throw new Error("Failed to fetch ticker suggestions");
  }

  // Return the list of suggested tickers
  return await res.json(); // [{ symbol, name }]
}



