// components/Skills.js
export default function Skills({ skills }) {
    return (
        <div>
            <h3 className="font-medium text-gray-800">Skills:</h3>
            <div className="flex flex-wrap gap-2 mt-1">
                {skills.map((skill, idx) => (
                    <span
                        key={idx}
                        className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full"
                    >
                        {skill}
                    </span>
                ))}
            </div>
        </div>
    );
}
