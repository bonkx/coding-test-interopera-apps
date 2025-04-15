// components/Deals.js

const getStatusBadge = (status) => {
    switch (status) {
        case "Closed Won":
            return "bg-green-200 text-green-800"; // Green for Closed Won
        case "In Progress":
            return "bg-yellow-200 text-yellow-800"; // Yellow for In Progress
        case "Closed Lost":
            return "bg-red-200 text-red-800"; // Red for Closed Lost
        default:
            return "bg-blue-200 text-blue-800"; // Default for undefined status
    }
};

export default function Deals({ deals }) {
    return (
        <div>
            <h3 className="font-medium text-gray-800 text-lg mb-2">Deals:</h3>
            <ul className="space-y-2 text-gray-700">
                {deals.map((deal) => (
                    <li
                        key={deal.client}
                        className="flex justify-between items-center bg-gray-50 p-2 rounded"
                    >
                        <div>
                            <span className="block">{deal.client}</span>
                            <span
                                className={`inline-block px-2 py-1 mt-1 text-xs font-semibold rounded-sm ${getStatusBadge(deal.status)}`}
                            >
                                {deal.status}
                            </span>
                        </div>
                        <span className="font-semibold text-green-600">
                            USD {deal.value.toLocaleString("en-US")}
                        </span>

                    </li>
                ))}
            </ul>
        </div>
    );
}
