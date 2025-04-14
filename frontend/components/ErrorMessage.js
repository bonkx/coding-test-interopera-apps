// components/ErrorMessage.js
export default function ErrorMessage({ message = "Something went wrong." }) {
    return (
        <div className="min-h-screen flex items-center justify-center bg-red-50">
            <div className="text-center p-6 bg-white border border-red-300 rounded-xl shadow-md">
                <h2 className="text-xl font-semibold text-red-600 mb-2">Error</h2>
                <p className="text-gray-700">{message}</p>
            </div>
        </div>
    );
}
