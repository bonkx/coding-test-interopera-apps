// components/ErrorMessage.js
export default function ErrorMessage({ message = "Something went wrong.", onRetry }) {
    return (
        <div className="min-h-[500px] flex items-center justify-center bg-red-50">
            <div className="text-center p-6 bg-white border border-red-300 rounded-xl shadow-md">
                <h2 className="text-xl font-semibold text-red-600 mb-2">Error</h2>
                <p className="text-gray-700 mb-4">{message}</p>
                <button
                    onClick={onRetry}
                    className="mt-2 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition"
                >
                    Reload
                </button>
            </div>
        </div>
    );
}
