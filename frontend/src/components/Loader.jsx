const Loader = () => {
    return (
      <div className="flex flex-col justify-center items-center my-10 text-center">
        <div className="animate-spin rounded-full h-10 w-10 border-t-4 border-blue-600 border-opacity-70 mb-3"></div>
        <p className="text-sm text-gray-700">Generating your investment report…</p>
      </div>
    );
  };

export default Loader;
