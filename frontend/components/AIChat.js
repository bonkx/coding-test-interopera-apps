"use client";

import { useState } from "react";

export default function AIChat() {
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setAnswer("");
        setError("");

        try {
            const res = await fetch("http://localhost:8000/api/ai", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question }),
            });

            const data = await res.json();

            if (!res.ok) throw new Error(data.error || "Something went wrong");

            setAnswer(data.answer);
        } catch (err) {
            setError(err.message || "Unexpected error");
        } finally {
            setLoading(false);
        }
    };


    return (
        <div className="max-w-2xl mt-10 p-4 bg-white rounded-xl shadow">
            <form onSubmit={handleSubmit} className="flex flex-col gap-2 mb-4">
                <div className="flex items-center gap-2">
                    <input
                        type="text"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        placeholder="Ask something..."
                        className="flex-1 p-2 border rounded"
                    />
                    <button
                        type="submit"
                        disabled={loading || !question}
                        className="bg-blue-500 text-white px-4 py-2 rounded"
                    >
                        {loading ? "..." : "Ask"}
                    </button>
                </div>
                <p className="text-xs text-gray-400 pl-1">
                    e.g. "Tell me a joke", "What's the time?", "What's the weather like?", or "Can you help me?"
                </p>
            </form>

            {error && <p className="text-red-500 text-sm">{error}</p>}
            {answer && (
                <div className="bg-gray-50 p-4 rounded-xl shadow-md">
                    <p className="text-gray-800 whitespace-pre-line">{answer}</p>
                </div>
            )}
        </div>
    );
}
