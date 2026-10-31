import React from 'react';
import { 
  LayoutDashboard, 
  Zap,
  BarChart3, 
  Trophy,
  FileText, 
  Network,
  TrendingUp,
  ArrowRight,
  X,
  CheckCircle2
} from 'lucide-react';

interface SidebarProps {
  mobileOpen: boolean;
  setMobileOpen: (open: boolean) => void;
  activeNav: string;
  setActiveNav: (nav: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  mobileOpen, 
  setMobileOpen,
  activeNav,
  setActiveNav
}) => {
  const navItems = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'prediction', label: 'Live Prediction', icon: Zap, badge: 'LIVE', badgeColor: 'bg-[#10B981]' },
    { id: 'eda', label: 'EDA Insights', icon: BarChart3 },
    { id: 'models', label: 'Model Benchmark', icon: Trophy },
    { id: 'words', label: 'Word Insights', icon: FileText },
    { id: 'bayesian', label: 'Bayesian Net', icon: Network },
    { id: 'timeseries', label: 'Volume Forecast', icon: TrendingUp },
  ];

  return (
    <>
      {/* Mobile Backdrop */}
      {mobileOpen && (
        <div 
          className="fixed inset-0 bg-black/40 z-40 lg:hidden backdrop-blur-sm"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Sidebar Container */}
      <aside 
        className={`fixed lg:static top-0 left-0 h-screen lg:h-auto lg:self-stretch w-[216px] bg-[#30265F] text-white flex flex-col justify-between py-6 px-4 z-50 transition-transform duration-300 ease-in-out shrink-0 select-none ${
          mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Top Logo & Navigation */}
        <div className="flex flex-col gap-6">
          {/* Logo */}
          <div className="flex items-center justify-between px-2">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center shadow-md shrink-0">
                {/* Purple abstract logo glyph */}
                <div className="w-4 h-4 relative flex items-center justify-center">
                  <span className="w-2 h-2 rounded-full bg-[#6045F5] absolute top-0 left-0"></span>
                  <span className="w-2 h-2 rounded-full bg-[#6045F5] absolute bottom-0 right-0"></span>
                  <span className="w-2.5 h-1.5 rounded-sm bg-[#6045F5] rotate-45"></span>
                </div>
              </div>
              <div className="flex flex-col leading-none">
                <span className="font-bold text-[16.5px] tracking-tight text-white">Droitdash</span>
                <span className="text-[9.5px] text-[#A59FC1] font-medium tracking-wide uppercase mt-0.5">SpamShield ML</span>
              </div>
            </div>

            {/* Mobile close button */}
            <button 
              onClick={() => setMobileOpen(false)}
              className="lg:hidden text-white/70 hover:text-white p-1"
            >
              <X size={18} />
            </button>
          </div>

          {/* Navigation Items */}
          <nav className="flex flex-col gap-1 mt-1 text-[13px]">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeNav === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveNav(item.id);
                    setMobileOpen(false);
                  }}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl transition-all group font-medium ${
                    isActive 
                      ? 'bg-[#3F3572] text-white shadow-sm' 
                      : 'text-[#A59FC1] hover:text-white hover:bg-white/5'
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <Icon 
                      size={16} 
                      className={isActive ? 'text-[#A392F8]' : 'text-[#8C84B0] group-hover:text-white transition-colors'} 
                    />
                    <span>{item.label}</span>
                  </div>

                  {item.badge && (
                    <span className={`text-[9.5px] font-bold text-white px-1.5 py-0.5 rounded-full ${item.badgeColor || 'bg-[#6045F5]'}`}>
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Bottom Section: Backend Status & User Profile */}
        <div className="flex flex-col gap-3 mt-4">
          {/* Live Engine Status Badge */}
          <div className="bg-[#241D49] rounded-lg px-2.5 py-1.5 flex items-center justify-between text-[11px] text-[#A59FC1] border border-white/5">
            <span className="flex items-center gap-1.5 font-medium">
              <span className="w-2 h-2 rounded-full bg-[#10B981] animate-pulse"></span>
              Backend Live
            </span>
            <span className="text-[10px] text-white/60 font-mono">Port 8000</span>
          </div>

          {/* Profile Card */}
          <div className="bg-[#372E66] rounded-xl p-2.5 flex items-center justify-between shadow-inner hover:bg-[#3E3474] transition-colors cursor-pointer group">
            <div className="flex items-center gap-2.5 overflow-hidden">
              <div className="w-8 h-8 rounded-full overflow-hidden shrink-0 bg-amber-100 border border-white/20">
                <img 
                  src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100&auto=format&fit=crop&q=80" 
                  alt="WP.AR Pascal" 
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="flex flex-col truncate">
                <span className="text-[12px] font-semibold text-white leading-tight truncate">WP.AR Pascal</span>
                <span className="text-[10px] text-[#A59FC1] truncate">joepascal@gmail.com</span>
              </div>
            </div>
            <ArrowRight size={13} className="text-[#A59FC1] group-hover:text-white transition-colors shrink-0 mr-1" />
          </div>
        </div>
      </aside>
    </>
  );
};
