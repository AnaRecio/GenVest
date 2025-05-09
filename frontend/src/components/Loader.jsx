// Simple loading spinner with an optional message prop
const Loader = ({ message = "Generating your investment report…" }) => {
  return (
    <div className="flex flex-col justify-center items-center my-10 text-center">
      {/* Spinner animation using Tailwind utility classes */}
      <div className="animate-spin rounded-full h-10 w-10 border-t-4 border-blue-600 border-opacity-70 mb-3"></div>

      {/* Optional loading message below the spinner */}
      <p className="text-sm text-gray-700">{message}</p>
    </div>
  );
};

export default Loader;
