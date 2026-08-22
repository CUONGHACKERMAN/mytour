import { useState, useEffect } from 'react';
import { SignInPage } from './pages/SignInPage';
import { SignUpPage } from './pages/SignUpPage';
import { DashboardPage } from './pages/DashboardPage';

type ViewMode = 'signin' | 'signup' | 'dashboard';

export function App() {
  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem('mytour_access_token');
  });

  const [currentView, setCurrentView] = useState<ViewMode>(() => {
    // If token exists, show dashboard; otherwise signin
    const savedToken = localStorage.getItem('mytour_access_token');
    return savedToken ? 'dashboard' : 'signin';
  });

  // Keep state in sync with URL hash if present
  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.replace('#/', '').replace('#', '');
      if (hash === 'signup') {
        setCurrentView('signup');
      } else if (hash === 'signin') {
        setCurrentView('signin');
      } else if (hash === 'dashboard' && token) {
        setCurrentView('dashboard');
      }
    };

    window.addEventListener('hashchange', handleHashChange);
    handleHashChange();

    return () => window.removeEventListener('hashchange', handleHashChange);
  }, [token]);

  const handleSignInSuccess = (newToken: string) => {
    setToken(newToken);
    setCurrentView('dashboard');
    window.location.hash = '#/dashboard';
  };

  const handleSignUpSuccess = () => {
    setCurrentView('signin');
    window.location.hash = '#/signin';
  };

  const handleLogout = () => {
    localStorage.removeItem('mytour_access_token');
    setToken(null);
    setCurrentView('signin');
    window.location.hash = '#/signin';
  };

  const navigateToSignUp = () => {
    setCurrentView('signup');
    window.location.hash = '#/signup';
  };

  const navigateToSignIn = () => {
    setCurrentView('signin');
    window.location.hash = '#/signin';
  };

  if (currentView === 'dashboard' && token) {
    return (
      <DashboardPage
        accessToken={token}
        onLogout={handleLogout}
      />
    );
  }

  if (currentView === 'signup') {
    return (
      <SignUpPage
        onNavigateSignIn={navigateToSignIn}
        onSuccess={handleSignUpSuccess}
      />
    );
  }

  return (
    <SignInPage
      onNavigateSignUp={navigateToSignUp}
      onSuccess={handleSignInSuccess}
    />
  );
}

export default App;
