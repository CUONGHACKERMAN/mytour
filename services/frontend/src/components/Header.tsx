import { useState } from 'react';
import { Logo } from './Logo';
import { LogOut } from 'lucide-react';

export interface UserProfile {
    id?: string;
    email?: string;
    first_name?: string;
    last_name?: string;
    phone?: string;
}

interface HeaderProps {
    user?: UserProfile | null;
    onLogout: () => void;
    baseUrl?: string;
}

export function Header({
    user,
    onLogout,
    baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8005',
}: HeaderProps) {
    const [loggingOut, setLoggingOut] = useState(false);

    const handleSignOut = async () => {
        setLoggingOut(true);
        try {
            await fetch(`${baseUrl}/auth/sign-out`, {
                method: 'POST',
                credentials: 'include',
            });
        } catch (err) {
            console.error('Sign-out error', err);
        } finally {
            setLoggingOut(false);
            onLogout();
        }
    };

    const displayName = user?.first_name
        ? `${user.first_name} ${user.last_name || ''}`.trim()
        : 'Authorized Agent';

    const avatarInitial = user?.first_name
        ? user.first_name[0].toUpperCase()
        : 'A';

    const displaySubtitle = user?.email || 'Cookie-authenticated Session';

    return (
        <header className="sticky top-0 z-30 bg-white border-b border-[#E2E8F0] shadow-xs">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                {/* Left: Brand Logo & Status */}
                <div className="flex items-center gap-6">
                    <Logo subtitle="Operations Portal" />
                    <div className="hidden md:flex items-center text-xs font-medium text-[#64748B] bg-[#F1F5F9] px-2.5 py-1 rounded-full border border-[#E2E8F0]">
                        <span className="w-2 h-2 rounded-full bg-emerald-500 mr-1.5 animate-pulse" />
                        VoyageERP Cloud Active
                    </div>
                </div>

                {/* Right: User Profile & Logout */}
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-3 pr-3 border-r border-[#E2E8F0]">
                        <div className="w-9 h-9 rounded-full bg-[#eef7fa] border border-[#74BDDA]/40 text-[#0891b2] font-semibold text-sm flex items-center justify-center shadow-xs">
                            {avatarInitial}
                        </div>
                        <div className="hidden sm:block text-left">
                            <p className="text-xs font-semibold text-[#0F172A] leading-tight">
                                {displayName}
                            </p>
                            <p className="text-[11px] text-[#64748B]">
                                {displaySubtitle}
                            </p>
                        </div>
                    </div>

                    <button
                        onClick={handleSignOut}
                        disabled={loggingOut}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors border border-transparent hover:border-red-200 cursor-pointer disabled:opacity-50"
                    >
                        <LogOut className="w-3.5 h-3.5" />
                        <span>{loggingOut ? 'Signing out...' : 'Logout'}</span>
                    </button>
                </div>
            </div>
        </header>
    );
}
