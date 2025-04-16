import { useEffect, useState } from "react";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";
import { Bar } from "react-chartjs-2";
import {
    Chart as ChartJS,
    BarElement,
    CategoryScale,
    LinearScale,
    Tooltip,
    Legend,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);


function ChartCard({ title, data, loading, error, onRetry }) {
    return (
        <div className="bg-white rounded-2xl shadow-md p-4 w-full">
            <h2 className="text-xl font-semibold mb-4">{title}</h2>
            {loading && (
                <div className="text-center py-8">
                    <Loading heightStyle="min-h-[300px]" />
                </div>
            )}
            {error && (
                <div className="text-center py-8 text-red-500">
                    <ErrorMessage message={error} heightStyle="min-h-[300px]" onRetry={onRetry} />
                </div>
            )}
            {!loading && !error && data && <Bar data={data} options={{ responsive: true, plugins: { legend: { display: false } } }} />}
        </div>
    );
}

export default function DashboardCharts() {
    const [dealValueData, setDealValueData] = useState(null);
    const [topClientsData, setTopClientsData] = useState(null);
    const [loadingDealValue, setLoadingDealValue] = useState(false);
    const [loadingTopClients, setLoadingTopClients] = useState(false);
    const [errorDealValue, setErrorDealValue] = useState(null);
    const [errorTopClients, setErrorTopClients] = useState(null);

    const fetchDealValueData = async () => {
        try {
            setLoadingDealValue(true);
            setErrorDealValue(null);

            // Delay 1 detik
            await new Promise((resolve) => setTimeout(resolve, 1000));

            const res = await fetch("http://localhost:8000/api/chart/deal-value-per-rep");
            const data = await res.json();

            if (!res.ok) throw new Error(data['error']);

            setDealValueData(data); // simpan data ke state
        } catch (err) {
            setErrorDealValue(err.message || "Unexpected error occurred");
        } finally {
            setLoadingDealValue(false); // loading selesai
        }
    };

    const fetchTopClientsData = async () => {
        try {
            setLoadingTopClients(true); // aktifkan loading
            setErrorTopClients(null); // reset error state

            // Delay 1 detik
            await new Promise((resolve) => setTimeout(resolve, 1000));

            const res = await fetch("http://localhost:8000/api/chart/top-clients");
            const data = await res.json();

            if (!res.ok) throw new Error(data['error']);

            setTopClientsData(data); // simpan data ke state
        } catch (err) {
            setErrorTopClients(err.message || "Unexpected error occurred");
        } finally {
            setLoadingTopClients(false); // loading selesai
        }
    };

    useEffect(() => {
        fetchDealValueData();
        fetchTopClientsData();
    }, []);

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ChartCard
                title="Total Deal Value per Sales Rep"
                data={dealValueData}
                loading={loadingDealValue}
                error={errorDealValue}
                onRetry={fetchDealValueData}
            />
            <ChartCard
                title="Top Clients by Deal Value"
                data={topClientsData}
                loading={loadingTopClients}
                error={errorTopClients}
                onRetry={fetchTopClientsData}
            />
        </div>
    );
}
