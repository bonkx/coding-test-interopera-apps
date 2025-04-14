// components/Clients.js
export default function Clients({ clients }) {
    return (
        <div>
            <h3 className="font-medium text-gray-800 text-lg mb-2">Clients:</h3>
            <ul className="space-y-2 text-gray-700">
                {clients.map((client) => (
                    <li
                        key={client.contact}
                        className="flex justify-between items-center bg-gray-50 p-2 rounded"
                    >
                        <div>
                            <span className="block">{client.name}</span>
                            <span className="block text-sm text-gray-500">{client.contact}</span>
                        </div>
                        <span className="font-semibold text-green-600">
                            {client.industry}
                        </span>
                    </li>
                ))}
            </ul>
        </div>
    );
}
