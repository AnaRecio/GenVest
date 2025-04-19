import { useState } from "react";
import InputForm from "../components/InputForm";
import ReportViewer from "../components/ReportViewer";
import DownloadButton from "../components/DownloadButton";
import Loader from "../components/Loader";
import { generateReport } from "../utils/api";

const Home = () => {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async (ticker, openaiKey, serperKey) => {
    setLoading(true);
    try {
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
        <h1 className="text-4xl font-bold text-center text-blue-900 mb-4">
          💼 GenVest: AI-Powered Investment Reports
        </h1>
        <InputForm onSubmit={handleGenerate} />
        {loading && <Loader />}
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

