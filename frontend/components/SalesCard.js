// components/SalesCard.js
import Skills from "./Skills";
import Clients from "./Clients";
import Deals from "./Deals";

export default function SalesCard({ rep }) {
    return (
        <div className="bg-white p-6 rounded-2xl shadow-md space-y-4 transition hover:shadow-lg">
            <div>
                <h2 className="text-xl font-semibold text-blue-700">{rep.name}</h2>
                <p className="text-sm text-gray-500">{rep.email}</p>
                <p className="text-sm text-gray-600 mt-1">
                    <span className="font-medium">Role:</span> {rep.role}
                </p>
                <p className="text-sm text-gray-600">
                    <span className="font-medium">Region:</span> {rep.region}
                </p>
            </div>

            <Skills skills={rep.skills} />
            <Clients clients={rep.clients} />
            <Deals deals={rep.deals} />
        </div>
    );
}
