// components/Loading.js
export default function Loading() {
    return (
        <div className="min-h-[500px] flex items-center justify-center bg-gray-100">
            <div className="text-center">
                <div className="w-10 h-10 border-4 border-blue-500 border-dashed rounded-full animate-spin mx-auto mb-4"></div>
                <p className="text-gray-700 font-medium">Loading...</p>
            </div>
        </div>
    );
}
