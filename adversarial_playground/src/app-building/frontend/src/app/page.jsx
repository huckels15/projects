'use client';

import Link from 'next/link';

export default function Home() {
    return (
        <div className="min-h-screen bg-black text-green-400">
            {/* Page Wrapper */}
            <div className="page-wrapper">
                {/* Hero Section */}
                <section className="hero-section">
                    <div className="hero-content">
                        <h1 className="hero-title">
                            Get Ready to Play on the Adversarial Playground
                        </h1>
                        <img
                            src="/assets/advplayground.png"
                            alt="Playground"
                            className="w-48 h-48 mx-auto rounded-full"
                        />
                        <p className="hero-description">
                            Explore what happens when adversarial attacks are deployed against image classification networks and how they can be defended against!
                        </p>
                    </div>
                </section>

                {/* Content Section */}
                <section className="content-section">
                    <div className="content-grid">
                        <Link href="/playground" className="block">
                            <div className="p-6 bg-gray-900 border border-green-500 rounded-lg shadow-md hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105">
                                <h3 className="feature-card-title">Adversarial Playground</h3>
                                <p className="feature-card-description">
                                    Play around on our playground to see the effect of adversarial attacks on image classification models!
                                </p>
                            </div>
                        </Link>

                        <Link href="/github" className="block">
                            <div className="p-6 bg-gray-900 border border-green-500 rounded-lg shadow-md hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105">
                                <h3 className="feature-card-title">GitHub Page</h3>
                                <p className="feature-card-description">
                                    Visit our GitHub Page!
                                </p>
                            </div>
                        </Link>

                        <Link href="/members" className="block">
                            <div className="p-6 bg-gray-900 border border-green-500 rounded-lg shadow-md hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105">
                                <h3 className="feature-card-title">Black Knights Members</h3>
                                <p className="feature-card-description">
                                    Want to know more about the developers of Adversarial Playground? Click below!
                                </p>
                            </div>
                        </Link>

                        <Link href="/attacks" className="block">
                            <div className="p-6 bg-gray-900 border border-green-500 rounded-lg shadow-md hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105">
                                <h3 className="feature-card-title">Attacks</h3>
                                <p className="feature-card-description">
                                    Want to learn more about the attacks implemented? Click below!
                                </p>
                            </div>
                        </Link>

                        <Link href="/upload" className="block">
                            <div className="p-6 bg-gray-900 border border-green-500 rounded-lg shadow-md hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105">
                                <h3 className="feature-card-title">Upload</h3>
                                <p className="feature-card-description">
                                    Want to upload a custom model and dataset to test? Click below!
                                </p>
                            </div>
                        </Link>
                    </div>
                </section>
            </div>
        </div>
    );
}
