'use client';
'use client';

import Header from '@/components/layout/Header';

export default function MembersPage() {
    return (
        <div className="min-h-screen bg-black text-green-400 relative overflow-hidden">
            {/* Header */}
            <Header />

            {/* Main Content */}
            <div className="relative z-10 flex flex-col items-center justify-center text-center py-20">
                {/* Header Spot */}
                <div className="mb-12">
                    <h1 className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 via-green-500 to-green-600 font-mono">
                        Black Knights Members
                    </h1>
                    <p className="mt-4 text-lg text-green-500">
                        Meet the creators of Adversarial Playground and learn about their roles.
                    </p>
                </div>

                {/* Members Section */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 container mx-auto max-w-6xl px-4">
                    {/* Jacob */}
                    <div className="p-6 bg-gray-900 border border-green-500 rounded-lg shadow-md hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105">
                        <img
                            src="/assets/jacob.jpg"
                            alt="Jacob Huckelberry"
                            className="w-24 h-24 mx-auto rounded-full shadow-lg border-2 border-green-500"
                        />
                        <h2 className="text-xl font-bold text-green-400 mt-4">Jacob Huckelberry</h2>
                        <p className="text-green-500 mt-2">Role: Developer</p>
                        <p className="text-green-600 mt-2 italic">Hailing from Discovery Bay, CA, Jacob is in the second year of getting his Masters Degree in Data Science. Following his time at Harvard, he will go on to serve as a Cyber Officer within the United States Army.</p>
                    </div>

                    {/* Eli */}
                    <div className="p-6 bg-gray-900 border border-green-500 rounded-lg shadow-md hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105">
                        <img
                            src="/assets/eli.jpg"
                            alt="Elijah Dabkowski"
                            className="w-24 h-24 mx-auto rounded-full shadow-lg border-2 border-green-500"
                        />
                        <h2 className="text-xl font-bold text-green-400 mt-4">Elijah Dabkowski</h2>
                        <p className="text-green-500 mt-2">Role: Developer</p>
                        <p className="text-green-600 mt-2 italic">From Tucson, AZ, Elijah is in the second year of getting his Masters Degree in Data Science. As an active duty Army officer, he will go on to serve as a 1LT in the Engineer Branch following his time at Harvard.</p>
                    </div>

                    {/* Ed */}
                    <div className="p-6 bg-gray-900 border border-green-500 rounded-lg shadow-md hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105">
                        <img
                            src="/assets/ed.jpeg"
                            alt="Ed Tang"
                            className="w-24 h-24 mx-auto rounded-full shadow-lg border-2 border-green-500"
                        />
                        <h2 className="text-xl font-bold text-green-400 mt-4">Ed Tang</h2>
                        <p className="text-green-500 mt-2">Role: Developer</p>
                        <p className="text-green-600 mt-2 italic">Originally from Palo Alto, CA, ED is a second year Masters student getting a degree in Data Science. He will serve as a Cyber Officer within the United States Army following his time at Harvard.</p>
                    </div>
                </div>
            </div>

        </div>
    );
}
