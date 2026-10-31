import React, { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { DashboardHeader } from './components/DashboardHeader';
import { AnalyticsTabs } from './components/AnalyticsTabs';
import { OverviewView } from './views/OverviewView';
import { LivePredictionView } from './views/LivePredictionView';
import { EdaView } from './views/EdaView';
import { ModelBenchmarkView } from './views/ModelBenchmarkView';
import { WordInsightsView } from './views/WordInsightsView';
import { BayesianNetworkView } from './views/BayesianNetworkView';
import { TimeSeriesView } from './views/TimeSeriesView';

export const App: React.FC = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeNav, setActiveNav] = useState('overview');
  const [activeSubTab, setActiveSubTab] = useState('summary');
  const [searchQuery, setSearchQuery] = useState('');

  const renderActiveView = () => {
    switch (activeNav) {
      case 'overview':
        return <OverviewView onNavigateToPrediction={() => setActiveNav('prediction')} activeSubTab={activeSubTab} />;
      case 'prediction':
        return <LivePredictionView activeSubTab={activeSubTab} globalSearch={searchQuery} />;
      case 'eda':
        return <EdaView activeSubTab={activeSubTab} onTabChange={setActiveSubTab} globalSearch={searchQuery} />;
      case 'models':
        return <ModelBenchmarkView activeSubTab={activeSubTab} />;
      case 'words':
        return <WordInsightsView activeSubTab={activeSubTab} globalSearch={searchQuery} />;
      case 'bayesian':
        return <BayesianNetworkView activeSubTab={activeSubTab} />;
      case 'timeseries':
        return <TimeSeriesView activeSubTab={activeSubTab} />;
      default:
        return <OverviewView onNavigateToPrediction={() => setActiveNav('prediction')} activeSubTab={activeSubTab} />;
    }
  };

  return (
    <div className="min-h-screen bg-[#E8E7EC] flex items-center justify-center p-2 sm:p-4 lg:p-6 font-sans antialiased text-[#19153F]">
      {/* Centered Dashboard Window Container Matching Reference Mockup */}
      <div className="w-full max-w-[1440px] min-h-[920px] bg-[#FCFCFE] rounded-[20px] shadow-2xl flex overflow-hidden border border-[#D9D8E0] relative items-stretch">
        
        {/* Left Fixed Sidebar (216px) */}
        <Sidebar 
          mobileOpen={mobileMenuOpen} 
          setMobileOpen={setMobileMenuOpen} 
          activeNav={activeNav}
          setActiveNav={(nav) => {
            setActiveNav(nav);
            // Default sub-tab
            setActiveSubTab(nav === 'overview' ? 'summary' : (nav === 'prediction' ? 'classifier' : 'length'));
          }}
        />

        {/* Main Content Area */}
        <main className="flex-1 flex flex-col p-4 sm:p-6 lg:p-[28px] overflow-y-auto">
          
          {/* Top Header */}
          <DashboardHeader 
            onMenuToggle={() => setMobileMenuOpen(true)}
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            activeNav={activeNav}
          />

          {/* Navigation Tabs */}
          <AnalyticsTabs 
            activeNav={activeNav}
            activeSubTab={activeSubTab}
            setActiveSubTab={setActiveSubTab}
          />

          {/* Dynamic Active Feature View */}
          <div className="animate-in fade-in duration-200">
            {renderActiveView()}
          </div>

        </main>
      </div>
    </div>
  );
};

export default App;
