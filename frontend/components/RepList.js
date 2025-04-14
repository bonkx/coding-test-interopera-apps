import React, { useState } from "react";
import SalesCard from "../components/SalesCard";

const RepList = ({ reps }) => {
    const [searchTerm, setSearchTerm] = useState("");
    const [selectedRegion, setSelectedRegion] = useState("All");
    const [selectedSkill, setSelectedSkill] = useState("All");

    const regions = ["All", ...new Set(reps.map(rep => rep.region))];
    const skills = [...new Set(reps.flatMap((rep) => rep.skills))];

    // Filter based on search term, selected region and skill
    const filteredReps = reps.filter((rep) => {
        const matchesSearch =
            rep.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            rep.role.toLowerCase().includes(searchTerm.toLowerCase());

        const matchesRegion =
            selectedRegion === "All" || rep.region === selectedRegion;
        const matchesSkill = selectedSkill === "All" || rep.skills.includes(selectedSkill);

        return matchesSearch && matchesRegion && matchesSkill;
    });

    return (
        <div>

            <div className="mb-6 flex flex-wrap items-center gap-4">
                {/* Search by Name */}
                <div className="flex items-center space-x-2">
                    <label htmlFor="search" className="text-gray-700 font-medium min-w-[60px]">
                        Search:
                    </label>
                    <input
                        id="search"
                        type="text"
                        placeholder="Search by name or role..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="border p-2 rounded-md w-[400px]"
                    />
                </div>

                {/* Region Filter */}
                <div className="flex items-center space-x-2">
                    <label htmlFor="region" className="text-gray-700 font-medium min-w-[100px]">
                        Filter Region:
                    </label>
                    <select
                        id="region"
                        value={selectedRegion}
                        onChange={(e) => setSelectedRegion(e.target.value)}
                        className="border p-2 rounded-md w-[180px]"
                    >
                        {regions.map((region, index) => (
                            <option key={index} value={region}>
                                {region}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Skill Filter */}
                <div className="flex items-center space-x-2">
                    <label htmlFor="skill" className="text-gray-700 font-medium min-w-[100px]">
                        Filter Skill:
                    </label>
                    <select
                        id="skill"
                        value={selectedSkill}
                        onChange={(e) => setSelectedSkill(e.target.value)}
                        className="border p-2 rounded-md w-[180px]"
                    >
                        <option value="All">All Skills</option>
                        {skills.map((skill, index) => (
                            <option key={index} value={skill}>
                                {skill}
                            </option>
                        ))}
                    </select>
                </div>
            </div>



            {/* List of Representatives */}
            {filteredReps.length === 0 ? (
                <p className="text-gray-500">No representatives found.</p>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredReps.map((rep) => (
                        <SalesCard key={rep.id} rep={rep} />
                    ))}
                </div>
            )}

        </div>
    );
};

export default RepList;
