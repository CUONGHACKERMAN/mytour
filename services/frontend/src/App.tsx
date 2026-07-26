import React, { useState, useEffect } from 'react';
import {
    Lock,
    UserPlus,
    LogIn,
    User,
    Terminal,
    RefreshCw,
    Copy,
    Check,
    ShieldCheck,
    Globe,
    Layers,
    Users
} from 'lucide-react';

interface JwtPayload {
    id?: string;
    email?: string;
    first_name?: string;
    last_name?: string;
    phone?: string;
    iat?: number;
    exp?: number;
    [key: string]: any;
}

interface ApiLog {
    id: string;
    timestamp: string;
    method: string;
    url: string;
    status: number;
    data: any;
    timeMs: number;
}

export function App() {
    const [baseUrl, setBaseUrl] = useState('http://localhost:8005');

    // Auth Form State
    const [email, setEmail] = useState('john.doe@mytour.com');
    const [password, setPassword] = useState('SecurePass123!');
    const [firstName, setFirstName] = useState('John');
    const [lastName, setLastName] = useState('Doe');
    const [phone, setPhone] = useState('+1234567890');

    // Token State
    const [accessToken, setAccessToken] = useState<string | null>(() => localStorage.getItem('mytour_access_token'));
    const [decodedToken, setDecodedToken] = useState<JwtPayload | null>(null);
    const [copied, setCopied] = useState(false);

    const [activeTab, setActiveTab] = useState<'signin' | 'signup' | 'profile'>(() => {
        return localStorage.getItem('mytour_access_token') ? 'profile' : 'signin';
    });

    // Sync token with localStorage
    useEffect(() => {
        if (accessToken) {
            localStorage.setItem('mytour_access_token', accessToken);
        } else {
            localStorage.removeItem('mytour_access_token');
        }
    }, [accessToken]);

    // Status & Logs
    const [loading, setLoading] = useState(false);
    const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
    const [apiLogs, setApiLogs] = useState<ApiLog[]>([]);
    const [usersList, setUsersList] = useState<any[]>([]);

    // Decode JWT safely
    useEffect(() => {
        if (accessToken) {
            try {
                const parts = accessToken.split('.');
                if (parts.length === 3) {
                    const payloadJson = atob(parts[1].replace(/-/g, '+').replace(/_/g, '/'));
                    setDecodedToken(JSON.parse(payloadJson));
                } else {
                    setDecodedToken(null);
                }
            } catch {
                setDecodedToken(null);
            }
        } else {
            setDecodedToken(null);
        }
    }, [accessToken]);

    // Ping backend check
    const checkHealth = async () => {
        setApiStatus('checking');
        try {
            const res = await fetch(`${baseUrl}/docs`, { method: 'HEAD' });
            setApiStatus(res.ok || res.status < 500 ? 'online' : 'offline');
        } catch {
            setApiStatus('offline');
        }
    };

    useEffect(() => {
        checkHealth();
    }, [baseUrl]);

    const logRequest = (method: string, url: string, status: number, data: any, timeMs: number) => {
        const newLog: ApiLog = {
            id: Math.random().toString(36).substring(7),
            timestamp: new Date().toLocaleTimeString(),
            method,
            url,
            status,
            data,
            timeMs
        };
        setApiLogs(prev => [newLog, ...prev.slice(0, 9)]);
    };

    const handleSignIn = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        const start = performance.now();
        try {
            const response = await fetch(`${baseUrl}/auth/sign-in`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const data = await response.json();
            const elapsed = Math.round(performance.now() - start);

            logRequest('POST', '/auth/sign-in', response.status, data, elapsed);

            if (response.ok && data.access_token) {
                setAccessToken(data.access_token);
                localStorage.setItem('mytour_access_token', data.access_token);
                setActiveTab('profile');
            }
        } catch (err: any) {
            logRequest('POST', '/auth/sign-in', 500, { error: err.message || 'Connection failed' }, 0);
        } finally {
            setLoading(false);
        }
    };

    const handleSignUp = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        const start = performance.now();
        try {
            const response = await fetch(`${baseUrl}/auth/sign-up`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, first_name: firstName, last_name: lastName, phone })
            });
            const data = await response.json();
            const elapsed = Math.round(performance.now() - start);

            logRequest('POST', '/auth/sign-up', response.status, data, elapsed);

            if (response.ok) {
                setActiveTab('signin');
            }
        } catch (err: any) {
            logRequest('POST', '/auth/sign-up', 500, { error: err.message || 'Connection failed' }, 0);
        } finally {
            setLoading(false);
        }
    };

    const handleFetchUsers = async () => {
        setLoading(true);
        const start = performance.now();
        try {
            const response = await fetch(`${baseUrl}/user/users`, {
                headers: {
                    'Authorization': accessToken ? `Bearer ${accessToken}` : ''
                }
            });
            const data = await response.json();
            const elapsed = Math.round(performance.now() - start);

            logRequest('GET', '/user/users', response.status, data, elapsed);
            if (response.ok) {
                setUsersList(Array.isArray(data) ? data : [data]);
            }
        } catch (err: any) {
            logRequest('GET', '/user/users', 500, { error: err.message || 'Failed to fetch' }, 0);
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        setAccessToken(null);
        localStorage.removeItem('mytour_access_token');
        setActiveTab('signin');
    };

    const copyToken = () => {
        if (accessToken) {
            navigator.clipboard.writeText(accessToken);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }
    };

    return (
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '32px 16px' }}>

            {/* Header */}
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{ padding: '10px', background: 'rgba(99, 102, 241, 0.15)', borderRadius: '12px', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
                        <ShieldCheck size={28} color="#6366f1" />
                    </div>
                    <div>
                        <h1 style={{ fontSize: '1.75rem', fontWeight: 700 }}>
                            MyTour <span className="gradient-text">Auth Tester</span>
                        </h1>
                        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                            FastAPI DDD Domain Authentication Demo
                        </p>
                    </div>
                </div>

                {/* Base URL & Status */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'rgba(0,0,0,0.3)', padding: '6px 12px', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
                        <Globe size={16} color="var(--text-muted)" />
                        <input
                            type="text"
                            value={baseUrl}
                            onChange={(e) => setBaseUrl(e.target.value)}
                            style={{ background: 'transparent', border: 'none', color: '#fff', fontSize: '0.85rem', width: '180px', outline: 'none', fontFamily: 'var(--font-mono)' }}
                        />
                    </div>
                    <button onClick={checkHealth} className="btn-secondary" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <RefreshCw size={14} className={apiStatus === 'checking' ? 'spin' : ''} />
                        <span className={`status-ping ${apiStatus === 'online' ? 'active' : 'inactive'}`} />
                        {apiStatus === 'online' ? 'API Online' : apiStatus === 'offline' ? 'API Offline' : 'Checking'}
                    </button>
                </div>
            </header>

            {/* Main Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>

                {/* Left Column: Interactive Form Panel */}
                <div className="glass-panel" style={{ padding: '24px' }}>

                    {/* Nav Tabs */}
                    <div style={{ display: 'flex', gap: '8px', marginBottom: '24px', background: 'rgba(0,0,0,0.3)', padding: '4px', borderRadius: '12px' }}>
                        <button
                            onClick={() => setActiveTab('signin')}
                            className="btn-secondary"
                            style={{ flex: 1, background: activeTab === 'signin' ? 'var(--accent-primary)' : 'transparent', border: 'none', color: '#fff' }}
                        >
                            <LogIn size={16} style={{ marginRight: 6 }} /> Sign In
                        </button>
                        <button
                            onClick={() => setActiveTab('signup')}
                            className="btn-secondary"
                            style={{ flex: 1, background: activeTab === 'signup' ? 'var(--accent-primary)' : 'transparent', border: 'none', color: '#fff' }}
                        >
                            <UserPlus size={16} style={{ marginRight: 6 }} /> Sign Up
                        </button>
                        <button
                            onClick={() => setActiveTab('profile')}
                            className="btn-secondary"
                            style={{ flex: 1, background: activeTab === 'profile' ? 'var(--accent-primary)' : 'transparent', border: 'none', color: '#fff' }}
                        >
                            <User size={16} style={{ marginRight: 6 }} /> Token Session
                        </button>
                    </div>

                    {/* Sign In Form */}
                    {activeTab === 'signin' && (
                        <form onSubmit={handleSignIn} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                            <h2 style={{ fontSize: '1.2rem', fontWeight: 600 }}>Sign In to MyTour</h2>
                            <div>
                                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 6, display: 'block' }}>Email Address</label>
                                <input
                                    type="email"
                                    className="input-field"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                            </div>
                            <div>
                                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 6, display: 'block' }}>Password</label>
                                <input
                                    type="password"
                                    className="input-field"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                />
                            </div>
                            <button type="submit" className="btn-primary" disabled={loading} style={{ marginTop: 8 }}>
                                {loading ? 'Authenticating...' : 'Sign In & Issue JWT'}
                            </button>
                        </form>
                    )}

                    {/* Sign Up Form */}
                    {activeTab === 'signup' && (
                        <form onSubmit={handleSignUp} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                            <h2 style={{ fontSize: '1.2rem', fontWeight: 600 }}>Create New User Account</h2>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                                <div>
                                    <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 4, display: 'block' }}>First Name</label>
                                    <input type="text" className="input-field" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
                                </div>
                                <div>
                                    <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 4, display: 'block' }}>Last Name</label>
                                    <input type="text" className="input-field" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
                                </div>
                            </div>
                            <div>
                                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 4, display: 'block' }}>Email</label>
                                <input type="email" className="input-field" value={email} onChange={(e) => setEmail(e.target.value)} required />
                            </div>
                            <div>
                                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 4, display: 'block' }}>Phone</label>
                                <input type="text" className="input-field" value={phone} onChange={(e) => setPhone(e.target.value)} />
                            </div>
                            <div>
                                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 4, display: 'block' }}>Password</label>
                                <input type="password" className="input-field" value={password} onChange={(e) => setPassword(e.target.value)} required />
                            </div>
                            <button type="submit" className="btn-primary" disabled={loading} style={{ marginTop: 8 }}>
                                {loading ? 'Creating Account...' : 'Sign Up (POST /auth/sign-up)'}
                            </button>
                        </form>
                    )}

                    {/* Profile / Token Session */}
                    {activeTab === 'profile' && (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <h2 style={{ fontSize: '1.2rem', fontWeight: 600 }}>Active Session Details</h2>
                                {accessToken && (
                                    <button onClick={handleLogout} className="btn-secondary" style={{ color: 'var(--accent-rose)', borderColor: 'rgba(244,63,94,0.3)' }}>
                                        Logout
                                    </button>
                                )}
                            </div>

                            {accessToken ? (
                                <>
                                    <div style={{ background: 'rgba(99,102,241,0.1)', padding: '16px', borderRadius: '12px', border: '1px solid rgba(99,102,241,0.2)' }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                                            <span style={{ fontSize: '0.8rem', textTransform: 'uppercase', color: 'var(--accent-primary)', fontWeight: 700 }}>Decoded AuthorizationContext</span>
                                            <span style={{ fontSize: '0.75rem', color: 'var(--accent-emerald)', background: 'rgba(16,185,129,0.15)', padding: '2px 8px', borderRadius: '6px' }}>Valid JWT</span>
                                        </div>
                                        <pre className="code-block" style={{ maxHeight: '180px' }}>
                                            {JSON.stringify(decodedToken, null, 2)}
                                        </pre>
                                    </div>

                                    <div>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                                            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Raw JWT Token</span>
                                            <button onClick={copyToken} className="btn-secondary" style={{ padding: '4px 8px', fontSize: '0.75rem' }}>
                                                {copied ? <Check size={12} color="var(--accent-emerald)" /> : <Copy size={12} />}
                                                {copied ? 'Copied' : 'Copy'}
                                            </button>
                                        </div>
                                        <div className="code-block" style={{ wordBreak: 'break-all', fontSize: '0.75rem', color: 'var(--accent-cyan)' }}>
                                            {accessToken}
                                        </div>
                                    </div>

                                    <button onClick={handleFetchUsers} className="btn-primary" style={{ marginTop: 8 }}>
                                        Test Authenticated Request (GET /user/users)
                                    </button>

                                    {usersList.length > 0 && (
                                        <div>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6, fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                                                <Users size={14} /> Response Data ({usersList.length} user records)
                                            </div>
                                            <pre className="code-block" style={{ maxHeight: '150px' }}>
                                                {JSON.stringify(usersList, null, 2)}
                                            </pre>
                                        </div>
                                    )}
                                </>
                            ) : (
                                <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--text-muted)' }}>
                                    <Lock size={40} style={{ marginBottom: 12, opacity: 0.5 }} />
                                    <p>No active token found. Please Sign In to issue a JWT session.</p>
                                </div>
                            )}
                        </div>
                    )}

                </div>

                {/* Right Column: Live API Console & Logs */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>

                    <div className="glass-panel" style={{ padding: '24px', flex: 1 }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
                            <Terminal size={20} color="var(--accent-cyan)" />
                            <h2 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Live API Inspector & Logs</h2>
                        </div>

                        {apiLogs.length === 0 ? (
                            <div style={{ textAlign: 'center', padding: '60px 20px', color: 'var(--text-subtle)', fontSize: '0.9rem' }}>
                                <Layers size={32} style={{ marginBottom: 8, opacity: 0.3 }} />
                                <p>No API requests executed yet.</p>
                                <p style={{ fontSize: '0.8rem', opacity: 0.6, marginTop: 4 }}>Interact with the form to test live endpoints.</p>
                            </div>
                        ) : (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxHeight: '550px', overflowY: 'auto' }}>
                                {apiLogs.map((log) => (
                                    <div
                                        key={log.id}
                                        style={{
                                            background: 'rgba(0, 0, 0, 0.4)',
                                            borderRadius: '12px',
                                            padding: '14px',
                                            borderLeft: `4px solid ${log.status >= 200 && log.status < 300 ? 'var(--accent-emerald)' : 'var(--accent-rose)'}`
                                        }}
                                    >
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                                <span style={{
                                                    fontSize: '0.75rem',
                                                    fontWeight: 700,
                                                    padding: '2px 6px',
                                                    borderRadius: '4px',
                                                    background: log.method === 'POST' ? 'rgba(99,102,241,0.2)' : 'rgba(6,182,212,0.2)',
                                                    color: log.method === 'POST' ? 'var(--accent-primary)' : 'var(--accent-cyan)'
                                                }}>
                                                    {log.method}
                                                </span>
                                                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}>{log.url}</span>
                                            </div>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                                <span style={{
                                                    fontSize: '0.75rem',
                                                    fontWeight: 700,
                                                    color: log.status >= 200 && log.status < 300 ? 'var(--accent-emerald)' : 'var(--accent-rose)'
                                                }}>
                                                    HTTP {log.status}
                                                </span>
                                                <span style={{ fontSize: '0.75rem', color: 'var(--text-subtle)' }}>{log.timeMs}ms</span>
                                            </div>
                                        </div>

                                        <pre className="code-block" style={{ fontSize: '0.78rem', maxHeight: '140px' }}>
                                            {JSON.stringify(log.data, null, 2)}
                                        </pre>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                </div>

            </div>

        </div>
    );
}

export default App;
