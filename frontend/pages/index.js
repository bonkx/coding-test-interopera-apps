import { useState, useEffect } from "react";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import RepList from "../components/RepList";
import DashboardCharts from "../components/DashboardCharts";
import AIChat from "../components/AIChat";

export default function Home() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true); // aktifkan loading
      setError(null); // reset error state

      // Delay 1 detik
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const res = await fetch("http://localhost:8000/api/sales-reps");
      const json = await res.json();
      // console.log(json);
      if (!res.ok) throw new Error(json['error']);

      setData(json.salesReps || []);     // simpan data ke state
    } catch (err) {
      setError(err.message || "Unexpected error occurred");
    } finally {
      setLoading(false); // loading selesai
    }
  };


  useEffect(() => {
    fetchData();  // panggil fetchData saat komponen pertama kali dimuat
  }, []);


  return (

    <div style={{ padding: "2rem" }}>
      <h1>Next.js + FastAPI Sample</h1>

      <section style={{ marginBottom: "2rem" }}>

        <div className="min-h-screen bg-gray-100 p-8">
          <h1 className="text-3xl font-bold mb-6">Sales Representatives</h1>

          {loading ? <Loading /> : error ? <ErrorMessage message={error} onRetry={fetchData} /> : <RepList reps={data} />}

        </div>
      </section>

      <section style={{ marginBottom: "2rem" }}>

        <div className="bg-gray-100 p-8">
          <h1 className="text-3xl font-bold mb-6">Sales Dashboard</h1>

          <DashboardCharts />

        </div>
      </section>

      <section>
        <div className="min-h-screen bg-gray-100 p-8">
          <h2>Ask a Question (AI Endpoint)</h2>

          <AIChat />

        </div>

      </section>
    </div>

  );
}
