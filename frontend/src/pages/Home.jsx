import { useState } from "react";
import InputForm from "../components/InputForm";
import ReportViewer from "../components/ReportViewer";
import DownloadButton from "../components/DownloadButton";
import Loader from "../components/Loader";
import { generateReport } from "../utils/api";

// Main page component for GenVest
const Home = () => {
  // State to hold the generated report object
  const [report, setReport] = useState(null);

  // State to handle loading spinner visibility
  const [loading, setLoading] = useState(false);

  // Message to display during loading (e.g. training status)
  const [loadingMessage, setLoadingMessage] = useState("");

  // Function to handle the form submission and trigger report generation
  const handleGenerate = async (ticker, openaiKey, serperKey) => {
    setLoadingMessage(`⏳ Training model for ${ticker.toUpperCase()}...`);
    setLoading(true);

    try {
      // Call API to generate the report
      const result = await generateReport(ticker, openaiKey, serperKey);
      setReport(result);
    } catch (error) {
      console.error("Error generating report:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 px-4 py-8">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Page Heading */}
        <h1 className="text-4xl font-bold text-center text-blue-900 mb-4">
          💼 GenVest: AI-Powered Investment Reports
        </h1>

        {/* Input Form for ticker and API keys */}
        <InputForm onSubmit={handleGenerate} />

        {/* Show loader while report is being generated */}
        {loading && <Loader message={loadingMessage} />}

        {/* Once loading is done and report exists, show report and download button */}
        {!loading && report && (
          <>
            <ReportViewer report={report} />
            <DownloadButton report={report} />
          </>
        )}
      </div>
    </div>
  );
};

export default Home;
