import { useState } from 'react';
import { Mail, Lock, Eye, EyeOff, ArrowRight, AlertCircle } from 'lucide-react';
import { Logo } from '../components/Logo';
import signinHero from '../assets/signin_hero.jpg';

interface SignInPageProps {
    onNavigateSignUp: () => void;
    onSuccess: (token: string) => void;
    baseUrl?: string;
}

export function SignInPage({
    onNavigateSignUp,
    onSuccess,
    baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8005',
}: SignInPageProps) {
    const [email, setEmail] = useState('agent@voyageerp.com');
    const [password, setPassword] = useState('SecurePass123!');
    const [showPassword, setShowPassword] = useState(false);
    const [rememberMe, setRememberMe] = useState(true);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        try {
            const response = await fetch(`${baseUrl}/auth/sign-in`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || data.message || 'Authentication failed. Please check your credentials.');
            }

            if (data.access_token) {
                localStorage.setItem('mytour_access_token', data.access_token);
                if (rememberMe) {
                    localStorage.setItem('mytour_remember_email', email);
                } else {
                    localStorage.removeItem('mytour_remember_email');
                }
                onSuccess(data.access_token);
            } else {
                throw new Error('No access token received from server.');
            }
        } catch (err: any) {
            setError(err.message || 'Failed to sign in. Please check your network connection.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen w-full flex bg-[#FFFFFF] font-sans antialiased">
            {/* Left Column: Visual Hero Banner */}
            <div className="hidden lg:relative lg:flex lg:w-1/2 min-h-screen overflow-hidden p-6">
                <div className="relative w-full h-full rounded-2xl overflow-hidden shadow-2xl">
                    <img
                        src={signinHero}
                        alt="Mediterranean Coastal Resort"
                        className="absolute inset-0 w-full h-full object-cover object-center"
                    />
                    {/* Subtle gradient overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />

                    {/* Hero Branding / Tagline at bottom */}
                    <div className="absolute bottom-10 left-10 right-10 text-white z-10">
                        <h2 className="text-3xl xl:text-4xl font-extrabold tracking-tight mb-2 drop-shadow-md">
                            Explore the Extraordinary
                        </h2>
                        <p className="text-white/90 text-sm xl:text-base font-normal max-w-md drop-shadow">
                            Your gateway to managing unforgettable journeys globally.
                        </p>
                    </div>
                </div>
            </div>

            {/* Right Column: Authentication Form */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-6 sm:p-12 lg:p-16">
                <div className="w-full max-w-[420px] flex flex-col justify-center animate-fade-in">
                    {/* Brand Header */}
                    <div className="mb-8">
                        <Logo subtitle="Admin Terminal" />
                    </div>

                    {/* Heading */}
                    <div className="mb-8">
                        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-[#0f172a] mb-1.5">
                            Welcome Back
                        </h1>
                        <p className="text-sm text-[#64748b]">
                            Sign in to access your dashboard.
                        </p>
                    </div>

                    {/* Inline Error Alert */}
                    {error && (
                        <div className="mb-6 p-3.5 bg-red-50/90 border border-red-200 rounded-xl flex items-start gap-2.5 text-xs text-red-700">
                            <AlertCircle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
                            <span>{error}</span>
                        </div>
                    )}

                    {/* Sign In Form */}
                    <form onSubmit={handleSubmit} className="space-y-5">
                        {/* Email Field */}
                        <div>
                            <label
                                htmlFor="email"
                                className="block text-xs font-semibold text-[#334155] mb-2"
                            >
                                Email Address
                            </label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-[#94a3b8]">
                                    <Mail className="w-4 h-4" />
                                </div>
                                <input
                                    id="email"
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="agent@voyageerp.com"
                                    required
                                    className="w-full pl-10 pr-4 py-2.5 bg-[#f8fafc] hover:bg-[#f1f5f9]/80 focus:bg-white border border-[#e2e8f0] focus:border-[#0891b2] rounded-lg text-sm text-[#0f172a] placeholder-[#94a3b8] focus:outline-none focus:ring-2 focus:ring-[#0891b2]/20 transition-all"
                                />
                            </div>
                        </div>

                        {/* Password Field */}
                        <div>
                            <div className="flex items-center justify-between mb-2">
                                <label
                                    htmlFor="password"
                                    className="block text-xs font-semibold text-[#334155]"
                                >
                                    Password
                                </label>
                                <a
                                    href="#forgot"
                                    onClick={(e) => {
                                        e.preventDefault();
                                        alert('Password reset instructions will be sent to your registered email.');
                                    }}
                                    className="text-xs font-medium text-[#0284c7] hover:text-[#0369a1] transition-colors"
                                >
                                    Forgot Password?
                                </a>
                            </div>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-[#94a3b8]">
                                    <Lock className="w-4 h-4" />
                                </div>
                                <input
                                    id="password"
                                    type={showPassword ? 'text' : 'password'}
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="••••••••"
                                    required
                                    className="w-full pl-10 pr-10 py-2.5 bg-[#f8fafc] hover:bg-[#f1f5f9]/80 focus:bg-white border border-[#e2e8f0] focus:border-[#0891b2] rounded-lg text-sm text-[#0f172a] placeholder-[#94a3b8] focus:outline-none focus:ring-2 focus:ring-[#0891b2]/20 transition-all"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-[#94a3b8] hover:text-[#475569] transition-colors"
                                >
                                    {showPassword ? (
                                        <EyeOff className="w-4 h-4" />
                                    ) : (
                                        <Eye className="w-4 h-4" />
                                    )}
                                </button>
                            </div>
                        </div>

                        {/* Remember Me Checkbox */}
                        <div className="flex items-center">
                            <input
                                id="remember-me"
                                type="checkbox"
                                checked={rememberMe}
                                onChange={(e) => setRememberMe(e.target.checked)}
                                className="w-4 h-4 rounded border-[#cbd5e1] text-[#0891b2] focus:ring-[#0891b2]/30 accent-[#0891b2] cursor-pointer"
                            />
                            <label
                                htmlFor="remember-me"
                                className="ml-2.5 text-xs text-[#64748b] cursor-pointer select-none"
                            >
                                Remember me for 30 days
                            </label>
                        </div>

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-2.5 px-4 bg-[#67b0ce] hover:bg-[#58a1be] active:bg-[#4991ae] text-white font-medium text-sm rounded-lg shadow-sm hover:shadow transition-all flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed group cursor-pointer"
                        >
                            <span>{loading ? 'Signing in...' : 'Sign In'}</span>
                            <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                        </button>
                    </form>

                    {/* Quick Sign Up link */}
                    <div className="mt-6 text-center text-xs text-[#64748b]">
                        Don't have an account?{' '}
                        <button
                            type="button"
                            onClick={onNavigateSignUp}
                            className="font-semibold text-[#0891b2] hover:text-[#0e7490] transition-colors cursor-pointer"
                        >
                            Sign Up
                        </button>
                    </div>

                    {/* Contact Support Footer */}
                    <div className="mt-8 text-center text-xs text-[#64748b]">
                        Having trouble logging in?{' '}
                        <a
                            href="mailto:support@voyageerp.com"
                            className="font-semibold text-[#0891b2] hover:text-[#0e7490] transition-colors"
                        >
                            Contact Support
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
};
