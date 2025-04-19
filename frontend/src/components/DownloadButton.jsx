import { downloadPDF } from "../utils/api";

const DownloadButton = ({ report }) => {
    return (
      <div className="flex justify-center">
        <button
          onClick={() => downloadPDF(report)}
          className="bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-2 mt-6 rounded-lg transition"
        >
          📥 Download PDF Report
        </button>
      </div>
    );
  };
  

export default DownloadButton;
