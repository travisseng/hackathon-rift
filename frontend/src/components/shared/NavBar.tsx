import { Link, useLocation } from 'react-router-dom';
import { Trophy, TrendingUp, MessageSquare } from 'lucide-react';

export default function NavBar() {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Year-End Recap', icon: Trophy },
    { path: '/progression', label: 'Progression', icon: TrendingUp },
    { path: '/coaching', label: 'AI Coaching', icon: MessageSquare },
  ];

  return (
    <nav className="bg-lol-dark-lighter border-b border-lol-gold/20 sticky top-0 z-50 backdrop-blur-sm bg-lol-dark-lighter/95">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-lol-gold to-lol-gold-dark rounded-lg flex items-center justify-center">
              <span className="text-lol-dark font-black text-xl">L</span>
            </div>
            <div>
              <h1 className="text-white font-bold text-lg leading-none">LoL Analytics</h1>
              <p className="text-lol-gold text-xs">AI-Powered</p>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="flex gap-1">
            {navItems.map(({ path, label, icon: Icon }) => {
              const isActive = location.pathname === path;
              return (
                <Link
                  key={path}
                  to={path}
                  className={`
                    flex items-center gap-2 px-4 py-2 rounded-lg transition-all
                    ${
                      isActive
                        ? 'bg-lol-gold text-lol-dark font-bold'
                        : 'text-white hover:bg-lol-dark-light hover:text-lol-gold'
                    }
                  `}
                >
                  <Icon size={18} />
                  <span className="hidden md:inline">{label}</span>
                </Link>
              );
            })}
          </div>

          {/* User Info (placeholder) */}
          <div className="flex items-center gap-2">
            <div className="text-right hidden md:block">
              <p className="text-white text-sm font-medium">Summoner123</p>
              <p className="text-gray-400 text-xs">Gold II</p>
            </div>
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-lol-blue to-lol-blue-dark" />
          </div>
        </div>
      </div>
    </nav>
  );
}
