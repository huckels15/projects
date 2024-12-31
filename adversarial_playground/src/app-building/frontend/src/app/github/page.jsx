'use client';

export default function GitHubPage() {
    return (
        <div className="min-h-screen bg-black text-green-400 relative overflow-hidden">


            {/* Main Content */}
            <div className="relative z-10 flex flex-col items-center justify-center text-center min-h-screen">
                {/* Header Spot */}
                <div className="mb-8">
                    <h1 className="text-4xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 via-green-500 to-green-600 font-mono">
                        Want to See the Action Behind the Scenes?
                    </h1>
                    <p className="mt-4 text-lg text-green-500">
                        Dive into the source code that was used to develop our app!
                    </p>
                </div>

                {/* Button to GitHub Page */}
                <div className="mb-16">
                    <a 
                        href="https://github.com/huckels15/AC215_BlackKnights/tree/app_dev"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block px-12 py-5 bg-gradient-to-r from-green-600 to-green-800 text-black font-bold text-lg rounded-xl shadow-2xl border border-green-500 hover:border-green-400 hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105 relative"
                    >
                        Visit Our GitHub Repository
                        {/* Button Glow Effect */}
                        <span className="absolute inset-0 rounded-xl border-2 border-green-500 opacity-30 animate-pulse"></span>
                    </a>
                </div>

                {/* Decorative Sections */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 container mx-auto max-w-5xl px-4">
                    {/* Section 1 */}
                    <div className="p-6 bg-gray-900 border border-green-500 rounded-lg shadow-md hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105">
                        <h2 className="text-2xl font-bold mb-4 text-green-400">
                            Why Use GitHub?
                        </h2>
                        <p className="text-green-500">
                            GitHub has enabled our group to keep track of different versions of our project throughout
                            the span of working on our app over the course of the semester.
                        </p>
                    </div>

                    {/* Section 2 */}
                    <div className="p-6 bg-gray-900 border border-green-500 rounded-lg shadow-md hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105">
                        <h2 className="text-2xl font-bold mb-4 text-green-400">
                            Showcase Note
                        </h2>
                        <p className="text-green-500">
                            Unfortunately, our page is private due to course recommendations. Sorry!
                        </p>
                    </div>
                </div>
            </div>


        </div>
    );
}

