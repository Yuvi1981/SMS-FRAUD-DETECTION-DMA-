import React from 'react';
import { 
  Target, 
  Percent, 
  Sliders, 
  Filter, 
  Zap, 
  BarChart3, 
  Trophy, 
  FileText, 
  Network, 
  TrendingUp,
  LayoutDashboard,
  PieChart,
  Layers,
  Sparkles,
  ShieldCheck,
  Search,
  CheckCircle,
  Calendar
} from 'lucide-react';

interface AnalyticsTabsProps {
  activeNav: string;
  activeSubTab: string;
  setActiveSubTab: (tab: string) => void;
}

export const AnalyticsTabs: React.FC<AnalyticsTabsProps> = ({ 
  activeNav, 
  activeSubTab, 
  setActiveSubTab 
}) => {
  const tabsConfig: Record<string, Array<{ id: string, label: string, icon: any }>> = {
    overview: [
      { id: 'summary', label: 'Executive Summary', icon: LayoutDashboard },
      { id: 'balance', label: 'Corpus Balance', icon: PieChart },
      { id: 'pipeline', label: 'ML Pipeline', icon: Layers }
    ],
    prediction: [
      { id: 'classifier', label: 'Live Classifier', icon: Zap },
      { id: 'why', label: 'Explainability (Why?)', icon: Sparkles },
      { id: 'consensus', label: 'Multi-Model Consensus', icon: ShieldCheck }
    ],
    eda: [
      { id: 'length', label: 'Message Length', icon: BarChart3 },
      { id: 'balance', label: 'Class Balance', icon: PieChart },
      { id: 'words', label: 'Chi² Top Terms', icon: FileText },
      { id: 'samples', label: 'Sample Messages', icon: Search }
    ],
    models: [
      { id: 'benchmark', label: 'Performance Benchmark', icon: Trophy },
      { id: 'visualizer', label: 'Metric Visualizer', icon: BarChart3 },
      { id: 'rationale', label: 'Champion Rationale', icon: CheckCircle }
    ],
    words: [
      { id: 'lookup', label: 'Word Odds Lookup', icon: Search },
      { id: 'spam', label: 'Spam Drivers', icon: FileText },
      { id: 'ham', label: 'Ham Drivers', icon: FileText }
    ],
    bayesian: [
      { id: 'playground', label: 'Evidence Playground', icon: Network },
      { id: 'cpt', label: 'CPT Tables', icon: FileText },
      { id: 'dag', label: 'DAG Topology', icon: Layers }
    ],
    timeseries: [
      { id: 'volume', label: 'Daily Volume (365d)', icon: TrendingUp },
      { id: 'forecast', label: 'ARIMA Forecast (30d)', icon: Calendar },
      { id: 'metrics', label: 'Forecast Metrics', icon: Trophy }
    ]
  };

  const tabs = tabsConfig[activeNav] || tabsConfig.overview;
  const currentTab = tabs.find(t => t.id === activeSubTab) ? activeSubTab : tabs[0].id;

  return (
    <div className="shrink-0 w-full border-b border-[#E6E6EF] mb-5 overflow-x-auto select-none">
      <div className="flex items-center gap-6 sm:gap-8 min-w-max pb-0.5">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = currentTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveSubTab(tab.id)}
              className={`flex items-center gap-2 pb-3 pt-1 text-[13px] font-medium transition-all relative ${
                isActive 
                  ? 'text-[#19153F] font-semibold' 
                  : 'text-[#77778D] hover:text-[#19153F]'
              }`}
            >
              <Icon size={14} className={isActive ? 'text-[#6045F5]' : 'text-[#77778D]'} />
              <span>{tab.label}</span>
              
              {/* Signature Vivid Purple Underline Indicator */}
              {isActive && (
                <span className="absolute bottom-0 left-0 right-0 h-[2.5px] bg-[#6045F5] rounded-full animate-in fade-in duration-200" />
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};
