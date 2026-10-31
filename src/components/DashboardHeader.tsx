import React, { useState, useRef, useEffect } from 'react';
import { Search, Bell, Settings, Menu, X, CheckCircle, Shield, Globe, Cpu } from 'lucide-react';

interface DashboardHeaderProps {
  onMenuToggle: () => void;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  activeNav: string;
}

export const DashboardHeader: React.FC<DashboardHeaderProps> = ({
  onMenuToggle,
  searchQuery,
  setSearchQuery,
  activeNav
}) => {
  const [showNotifications, setShowNotifications] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  const notifRef = useRef<HTMLDivElement>(null);
  const settingsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (notifRef.current && !notifRef.current.contains(e.target as Node)) {
        setShowNotifications(false);
      }
      if (settingsRef.current && !settingsRef.current.contains(e.target as Node)) {
        setShowSettings(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const titles: Record<string, { title: string, subtitle: string }> = {
    overview: { title: 'Overview & Key Metrics', subtitle: 'SMS Spam Classifier + Daily Volume Forecast' },
    prediction: { title: 'Live Prediction & Explainability', subtitle: 'Real-Time SMS Classification with Word Odds Ratios' },
    eda: { title: 'Exploratory Data Analysis (EDA)', subtitle: 'Corpus Profiling, Text Length Distributions & Vocabulary' },
    models: { title: 'Cross-Model Benchmark', subtitle: 'Evaluation on Stratified 20% Test Split (1,034 SMS)' },
    words: { title: 'Word-Level Odds Ratio Insights', subtitle: 'Interpretable Logistic Regression Coefficients (exp(β))' },
    bayesian: { title: 'Bayesian Network (DAG)', subtitle: 'Probabilistic Graphical Modeling & Exact Belief Updating' },
    timeseries: { title: 'Time-Series Volume Forecast', subtitle: '365-Day Daily Counts & 30-Day ARIMA(1,1,1) Projections' }
  };

  const current = titles[activeNav] || titles.overview;

  return (
    <header className="shrink-0 flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 select-none">
      {/* Title & Mobile Toggle */}
      <div className="flex items-center gap-3">
        <button
          onClick={onMenuToggle}
          className="lg:hidden p-2 text-[#19153F] hover:bg-black/5 rounded-lg transition-colors"
          aria-label="Toggle navigation menu"
        >
          <Menu size={20} />
        </button>
        <div>
          <h1 className="text-2xl sm:text-[25px] font-bold tracking-tight text-[#19153F] leading-tight">
            {current.title}
          </h1>
          <p className="text-[11.5px] text-[#77778D] font-medium hidden sm:block mt-0.5">
            {current.subtitle}
          </p>
        </div>
      </div>

      {/* Controls on the Right */}
      <div className="flex items-center gap-2.5 self-end sm:self-auto">
        {/* Model Engine Status Tag */}
        <div className="hidden md:flex items-center gap-1.5 bg-[#FAF9FD] border border-[#E6E6EF] px-2.5 py-1.5 rounded-xl text-[11px] font-semibold text-[#19153F] shadow-xs">
          <Cpu size={13} className="text-[#6045F5]" />
          <span>4 Models Ready</span>
          <span className="w-1.5 h-1.5 rounded-full bg-[#10B981]"></span>
        </div>

        {/* Search input */}
        <div className="relative w-44 sm:w-56">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#77778D]" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search keywords..."
            className="w-full bg-white border border-[#E6E6EF] rounded-xl pl-8 pr-3 py-1.5 text-[12.5px] text-[#19153F] placeholder-[#9E9EA7] focus:outline-none focus:ring-2 focus:ring-[#6045F5]/30 focus:border-[#6045F5] transition-all shadow-xs"
          />
          {searchQuery && (
            <button 
              onClick={() => setSearchQuery('')}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              <X size={12} />
            </button>
          )}
        </div>

        {/* Notification Bell Button */}
        <div className="relative" ref={notifRef}>
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="w-9 h-9 rounded-xl bg-white border border-[#E6E6EF] flex items-center justify-center text-[#19153F] hover:bg-gray-50 transition-colors shadow-xs relative"
            title="Notifications"
          >
            <Bell size={16} />
            <span className="w-2 h-2 rounded-full bg-[#10B981] absolute top-2 right-2 ring-2 ring-white"></span>
          </button>

          {/* Notifications Dropdown */}
          {showNotifications && (
            <div className="absolute right-0 mt-2 w-72 bg-white rounded-xl shadow-dropdown border border-[#E6E6EF] py-3 px-3.5 z-50 text-[12.5px] flex flex-col gap-2.5 animate-in fade-in duration-150">
              <div className="flex items-center justify-between border-b border-gray-100 pb-2">
                <span className="font-semibold text-[#19153F]">Model System Logs</span>
                <span className="text-[11px] text-[#6045F5] font-medium cursor-pointer">Live</span>
              </div>
              <div className="flex gap-2.5 items-start p-1.5 hover:bg-gray-50 rounded-lg">
                <div className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center shrink-0 mt-0.5">
                  <CheckCircle size={12} />
                </div>
                <div className="flex flex-col">
                  <span className="text-[#19153F] font-semibold text-[11.5px]">Champion Model Evaluated</span>
                  <span className="text-[#77778D] text-[10.5px]">Logistic Regression achieved 0.9653 F1-Score.</span>
                </div>
              </div>
              <div className="flex gap-2.5 items-start p-1.5 hover:bg-gray-50 rounded-lg">
                <div className="w-5 h-5 rounded-full bg-purple-100 text-[#6045F5] flex items-center justify-center shrink-0 mt-0.5">
                  <Bell size={12} />
                </div>
                <div className="flex flex-col">
                  <span className="text-[#19153F] font-semibold text-[11.5px]">FastAPI Backend Connected</span>
                  <span className="text-[#77778D] text-[10.5px]">Serving on http://127.0.0.1:8000</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Settings Button (Dark Purple) */}
        <div className="relative" ref={settingsRef}>
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="w-9 h-9 rounded-xl bg-[#2B2257] hover:bg-[#342A68] flex items-center justify-center text-white transition-colors shadow-xs"
            title="Settings & Info"
          >
            <Settings size={16} />
          </button>

          {/* Settings Dropdown */}
          {showSettings && (
            <div className="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-dropdown border border-[#E6E6EF] py-3 px-3.5 z-50 text-[12px] flex flex-col gap-2 animate-in fade-in duration-150">
              <span className="font-semibold text-[#19153F] border-b border-gray-100 pb-2">Pipeline Settings</span>
              <div className="p-1.5 text-[#19153F]">
                <div className="font-medium text-[11px] text-[#77778D]">Corpus Size</div>
                <div className="font-bold">5,169 distinct SMS messages</div>
              </div>
              <div className="p-1.5 text-[#19153F]">
                <div className="font-medium text-[11px] text-[#77778D]">Features</div>
                <div className="font-bold">TF-IDF (1,2) + Top 500 Chi²</div>
              </div>
              <div className="p-1.5 text-[#19153F]">
                <div className="font-medium text-[11px] text-[#77778D]">Decision Threshold</div>
                <div className="font-bold">0.50 Probability</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
