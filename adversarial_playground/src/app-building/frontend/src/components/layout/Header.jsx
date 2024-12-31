'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Menu, Close, GitHub, People, BugReport, DirectionsRun } from '@mui/icons-material';

export default function Header() {
    // Component States
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const pathname = usePathname();

    const navItems = [
        { name: 'Home', path: '/', icon: <Home sx={{ fontSize: 20 }} /> },
        { name: 'GitHub', path: '/github', icon: <GitHub fontSize="small" /> },
        { name: 'Team Members', path: '/members', icon: <People fontSize="small" /> },
        { name: 'Attacks', path: '/attacks', icon: <BugReport fontSize="small" /> },
        { name: 'Playground', path: '/playground', icon: <DirectionsRun fontSize="small" /> },
        { name: 'Upload', path: '/upload', icon: <DirectionsRun fontSize="small" /> }
    ];

    // UI View
    return (
        <>
            <header className="header-wrapper">
                <div className="header-container">
                    <div className="header-content">
                        <Link href="/" className="header-logo">
                            <span className="text-2xl">
                                <img
                                    src="/assets/advplayground.png"
                                    alt="Playground"
                                    className="w-12 h-12 mx-auto rounded-full shadow-sm"
                                />
                            </span>
                            <h1 className="text-xl font-bold font-montserrat">Adversarial Playground</h1>
                        </Link>

                        <nav className="nav-desktop">
                            {navItems.map((item) => (
                                <Link
                                    key={item.name}
                                    href={item.path}
                                    className={`nav-link ${pathname === item.path ? 'nav-link-active' : ''}`}
                                >
                                    <div className="nav-icon-wrapper">{item.icon}</div>
                                    <span className="nav-text">{item.name}</span>
                                </Link>
                            ))}
                        </nav>

                        <button
                            className="mobile-menu-button"
                            onClick={() => setIsMenuOpen(!isMenuOpen)}
                            aria-label="Toggle menu"
                        >
                            {isMenuOpen ? <Close className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                        </button>
                    </div>
                </div>

                {/* Mobile Menu Dropdown */}
                <div
                    className={`mobile-menu transition-transform duration-300 ease-in-out ${
                        isMenuOpen ? 'translate-y-0 max-h-screen opacity-100' : '-translate-y-full max-h-0 opacity-0'
                    } overflow-hidden bg-gray-900 text-green-400 shadow-lg p-4 absolute w-full top-16 z-50`}
                >
                    <ul className="flex flex-col space-y-4">
                        {navItems.map((item) => (
                            <li key={item.name}>
                                <Link
                                    href={item.path}
                                    onClick={() => setIsMenuOpen(false)} // Close menu on selection
                                    className={`block px-4 py-2 rounded hover:bg-green-700 hover:text-black ${
                                        pathname === item.path ? 'bg-green-600 text-black' : ''
                                    }`}
                                >
                                    <div className="flex items-center gap-2">
                                        {item.icon}
                                        <span>{item.name}</span>
                                    </div>
                                </Link>
                            </li>
                        ))}
                    </ul>
                </div>
            </header>
            {isMenuOpen && (
                <div
                    className="mobile-menu-overlay fixed inset-0 bg-black/50 z-40"
                    onClick={() => setIsMenuOpen(false)}
                ></div>
            )}
        </>
    );
}
