const BASE_URL = "http://localhost:5000/api";

/**
 * Sends user input to the backend to generate an investment report
 */
export async function generateReport(ticker, openaiKey, serperKey) {
  const res = await fetch(`${BASE_URL}/report`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ticker,
      openai_key: openaiKey,
      serper_key: serperKey,
    }),
  });

  if (!res.ok) {
    throw new Error("Failed to generate report");
  }

  return await res.json();
}

/**
 * Downloads a generated investment report as a PDF file
 */
export async function downloadPDF(report) {
  const res = await fetch(`${BASE_URL}/report/download`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ report }),
  });

  if (!res.ok) {
    throw new Error("Failed to download PDF");
  }

  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "genvest_report.pdf";
  document.body.appendChild(link);
  link.click();
  link.remove();
}

/**
 * Fetches stock ticker suggestions based on user query
 */
export async function searchTickers(query) {
  const res = await fetch(`http://localhost:5000/api/search?q=${query}`);

  if (!res.ok) {
    throw new Error("Failed to fetch ticker suggestions");
  }

  return await res.json(); // [{ symbol, name }]
}



