import { useState, useMemo } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Logo } from '../components/Logo';
import { AlertCircle, CheckCircle2 } from 'lucide-react';
import signupHero from '../assets/signup_hero.jpg';

export function SignUpPage() {
  const navigate = useNavigate();
  const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8005';

  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [agreeTerms, setAgreeTerms] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Calculate password strength (0 to 4)
  const passwordStrength = useMemo(() => {
    if (!password) return 0;
    let score = 0;
    if (password.length >= 8) score += 1;
    if (/[A-Z]/.test(password)) score += 1;
    if (/[0-9]/.test(password)) score += 1;
    if (/[^A-Za-z0-9]/.test(password)) score += 1;
    return score;
  }, [password]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);

    if (!agreeTerms) {
      setError('Please accept the Terms of Service and Privacy Policy.');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long.');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${baseUrl}/auth/sign-up`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          email: email.trim(),
          password,
          first_name: firstName.trim(),
          last_name: lastName.trim(),
          phone: phone.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || data.message || 'Account creation failed.');
      }

      setSuccessMessage('Account created successfully! Redirecting to sign in...');
      setTimeout(() => {
        navigate('/signin', { replace: true });
      }, 1200);
    } catch (err: any) {
      setError(err.message || 'Failed to create account. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex bg-[#F8FAFC] font-sans antialiased">
      {/* Left Column: Visual Hero Banner */}
      <div className="hidden lg:relative lg:flex lg:w-1/2 min-h-screen overflow-hidden p-6">
        <div className="relative w-full h-full rounded-2xl overflow-hidden shadow-2xl">
          <img
            src={signupHero}
            alt="Alpine Mountain Lake"
            className="absolute inset-0 w-full h-full object-cover object-center"
          />
          {/* Subtle gradient overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
        </div>
      </div>

      {/* Right Column: Centered Floating Card */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-4 sm:p-8 lg:p-10">
        <div className="w-full max-w-[460px] bg-white rounded-2xl shadow-[0_10px_35px_-5px_rgba(15,23,42,0.06),0_8px_16px_-6px_rgba(15,23,42,0.04)] border border-[#E2E8F0] p-6 sm:p-8 animate-fade-in my-auto">
          {/* Brand Header */}
          <div className="mb-6">
            <Logo subtitle="ADMIN TERMINAL" subtitleUppercase />
          </div>

          {/* Heading */}
          <div className="mb-6">
            <h1 className="text-2xl font-bold tracking-tight text-[#0f172a] mb-1">
              Join the Voyage
            </h1>
            <p className="text-xs sm:text-sm text-[#64748b]">
              Create your agent account to start managing tours.
            </p>
          </div>

          {/* Success Notification */}
          {successMessage && (
            <div className="mb-5 p-3 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center gap-2 text-xs text-emerald-700">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
              <span>{successMessage}</span>
            </div>
          )}

          {/* Inline Error Alert */}
          {error && (
            <div className="mb-5 p-3 bg-red-50 border border-red-200 rounded-xl flex items-start gap-2 text-xs text-red-700">
              <AlertCircle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          {/* Sign Up Form */}
          <form onSubmit={handleSubmit} className="space-y-3.5">
            {/* First Name & Last Name in 2 columns */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label
                  htmlFor="firstName"
                  className="block text-xs font-semibold text-[#334155] mb-1.5"
                >
                  First Name
                </label>
                <input
                  id="firstName"
                  type="text"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  placeholder="Jane"
                  required
                  className="w-full px-3.5 py-2 bg-[#f8fafc] hover:bg-[#f1f5f9]/80 focus:bg-white border border-[#e2e8f0] focus:border-[#0891b2] rounded-lg text-sm text-[#0f172a] placeholder-[#94a3b8] focus:outline-none focus:ring-2 focus:ring-[#0891b2]/20 transition-all"
                />
              </div>

              <div>
                <label
                  htmlFor="lastName"
                  className="block text-xs font-semibold text-[#334155] mb-1.5"
                >
                  Last Name
                </label>
                <input
                  id="lastName"
                  type="text"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  placeholder="Doe"
                  required
                  className="w-full px-3.5 py-2 bg-[#f8fafc] hover:bg-[#f1f5f9]/80 focus:bg-white border border-[#e2e8f0] focus:border-[#0891b2] rounded-lg text-sm text-[#0f172a] placeholder-[#94a3b8] focus:outline-none focus:ring-2 focus:ring-[#0891b2]/20 transition-all"
                />
              </div>
            </div>

            {/* Email Address */}
            <div>
              <label
                htmlFor="emailAddress"
                className="block text-xs font-semibold text-[#334155] mb-1.5"
              >
                Email Address
              </label>
              <input
                id="emailAddress"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="jane@example.com"
                required
                className="w-full px-3.5 py-2 bg-[#f8fafc] hover:bg-[#f1f5f9]/80 focus:bg-white border border-[#e2e8f0] focus:border-[#0891b2] rounded-lg text-sm text-[#0f172a] placeholder-[#94a3b8] focus:outline-none focus:ring-2 focus:ring-[#0891b2]/20 transition-all"
              />
            </div>

            {/* Phone Number */}
            <div>
              <label
                htmlFor="phoneNumber"
                className="block text-xs font-semibold text-[#334155] mb-1.5"
              >
                Phone Number
              </label>
              <input
                id="phoneNumber"
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+1 (555) 000-0000"
                required
                className="w-full px-3.5 py-2 bg-[#f8fafc] hover:bg-[#f1f5f9]/80 focus:bg-white border border-[#e2e8f0] focus:border-[#0891b2] rounded-lg text-sm text-[#0f172a] placeholder-[#94a3b8] focus:outline-none focus:ring-2 focus:ring-[#0891b2]/20 transition-all"
              />
            </div>

            {/* Password */}
            <div>
              <label
                htmlFor="signupPassword"
                className="block text-xs font-semibold text-[#334155] mb-1.5"
              >
                Password
              </label>
              <input
                id="signupPassword"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full px-3.5 py-2 bg-[#f8fafc] hover:bg-[#f1f5f9]/80 focus:bg-white border border-[#e2e8f0] focus:border-[#0891b2] rounded-lg text-sm text-[#0f172a] placeholder-[#94a3b8] focus:outline-none focus:ring-2 focus:ring-[#0891b2]/20 transition-all"
              />

              {/* Password strength meter bars */}
              <div className="grid grid-cols-4 gap-1.5 mt-2">
                {[1, 2, 3, 4].map((step) => (
                  <div
                    key={step}
                    className={`h-1 rounded-full transition-all duration-300 ${
                      passwordStrength >= step
                        ? passwordStrength <= 2
                          ? 'bg-amber-400'
                          : 'bg-[#67b0ce]'
                        : 'bg-[#e2e8f0]'
                    }`}
                  />
                ))}
              </div>
              <span className="block text-[11px] text-[#94a3b8] mt-1">
                Must be at least 8 characters.
              </span>
            </div>

            {/* Confirm Password */}
            <div>
              <label
                htmlFor="confirmPassword"
                className="block text-xs font-semibold text-[#334155] mb-1.5"
              >
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full px-3.5 py-2 bg-[#f8fafc] hover:bg-[#f1f5f9]/80 focus:bg-white border border-[#e2e8f0] focus:border-[#0891b2] rounded-lg text-sm text-[#0f172a] placeholder-[#94a3b8] focus:outline-none focus:ring-2 focus:ring-[#0891b2]/20 transition-all"
              />
            </div>

            {/* Terms and conditions */}
            <div className="flex items-start pt-1">
              <input
                id="agreeTerms"
                type="checkbox"
                checked={agreeTerms}
                onChange={(e) => setAgreeTerms(e.target.checked)}
                className="w-4 h-4 mt-0.5 rounded border-[#cbd5e1] text-[#0891b2] focus:ring-[#0891b2]/30 accent-[#0891b2] cursor-pointer"
              />
              <label
                htmlFor="agreeTerms"
                className="ml-2 text-xs text-[#64748b] leading-tight cursor-pointer select-none"
              >
                I agree to the{' '}
                <a
                  href="#terms"
                  onClick={(e) => e.preventDefault()}
                  className="font-medium text-[#0284c7] hover:underline"
                >
                  Terms of Service
                </a>{' '}
                and{' '}
                <a
                  href="#privacy"
                  onClick={(e) => e.preventDefault()}
                  className="font-medium text-[#0284c7] hover:underline"
                >
                  Privacy Policy
                </a>
                .
              </label>
            </div>

            {/* Create Account Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 px-4 bg-[#67b0ce] hover:bg-[#58a1be] active:bg-[#4991ae] text-white font-medium text-sm rounded-lg shadow-sm hover:shadow transition-all flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed cursor-pointer pt-2 mt-2"
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>

          {/* Footer Navigation */}
          <div className="mt-5 text-center text-xs text-[#64748b]">
            Already have an account?{' '}
            <Link
              to="/signin"
              className="font-semibold text-[#0891b2] hover:text-[#0e7490] transition-colors"
            >
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
