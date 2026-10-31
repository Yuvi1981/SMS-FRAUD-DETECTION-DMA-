import React, { useEffect, useState } from 'react';
import { 
  Mail, 
  AlertTriangle, 
  Trophy, 
  Target, 
  ArrowRight, 
  CheckCircle, 
  Layers, 
  TrendingUp, 
  Cpu, 
  ShieldCheck,
  Zap
} from 'lucide-react';
import { 
  PieChart, 
  Pie, 
  Cell, 
  ResponsiveContainer, 
  Tooltip 
} from 'recharts';
import { api, OverviewData } from '../services/api';

interface OverviewViewProps {
  onNavigateToPrediction: () => void;
  activeSubTab?: string;
}

export const OverviewView: React.FC<OverviewViewProps> = ({ onNavigateToPrediction, activeSubTab = 'summary' }) => {
  const [data, setData] = useState<OverviewData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getOverview().then(res => {
      setData(res);
      setLoading(false);
    });
  }, []);

  const donutData = data?.class_distribution || [
    { name: 'Ham (Legitimate)', count: 4516, percentage: 87.37, color: '#10B981' },
    { name: 'Spam', count: 653, percentage: 12.63, color: '#EF4444' }
  ];

  return (
    <div className="flex flex-col gap-5">
      {/* 4 Top KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Total Messages */}
        <div className="bg-[#DDE6FF] rounded-[14px] p-4 flex flex-col justify-between h-[115px] shadow-sm hover:-translate-y-0.5 transition-transform">
          <div className="flex items-center justify-between">
            <span className="text-[12px] font-semibold text-[#5468B0]">Total SMS Corpus</span>
            <div className="w-6 h-6 rounded-lg bg-white/80 flex items-center justify-center text-[#4C6EF5]">
              <Mail size={13} />
            </div>
          </div>
          <div className="text-[26px] font-bold text-[#19153F] tracking-tight leading-none">
            {data ? data.metrics.total_messages.toLocaleString() : '5,169'}
          </div>
          <div className="text-[11px] text-[#5468B0] font-medium flex items-center gap-1">
            <span>Deduplicated from 5,572 raw</span>
          </div>
        </div>

        {/* Card 2: Spam Prevalence */}
        <div className="bg-[#F9E1E4] rounded-[14px] p-4 flex flex-col justify-between h-[115px] shadow-sm hover:-translate-y-0.5 transition-transform">
          <div className="flex items-center justify-between">
            <span className="text-[12px] font-semibold text-[#B34A56]">Spam Prevalence</span>
            <div className="w-6 h-6 rounded-lg bg-white/80 flex items-center justify-center text-[#EF4444]">
              <AlertTriangle size={13} />
            </div>
          </div>
          <div className="text-[26px] font-bold text-[#19153F] tracking-tight leading-none">
            {data ? `${data.metrics.spam_prevalence}%` : '12.63%'}
          </div>
          <div className="text-[11px] text-[#B34A56] font-medium flex items-center gap-1">
            <span>Highly imbalanced (87:13)</span>
          </div>
        </div>

        {/* Card 3: Champion Model */}
        <div className="bg-[#DCEFEB] rounded-[14px] p-4 flex flex-col justify-between h-[115px] shadow-sm hover:-translate-y-0.5 transition-transform">
          <div className="flex items-center justify-between">
            <span className="text-[12px] font-semibold text-[#2C7A68]">Champion Classifier</span>
            <div className="w-6 h-6 rounded-lg bg-white/80 flex items-center justify-center text-[#10B981]">
              <Trophy size={13} />
            </div>
          </div>
          <div className="text-[20px] font-bold text-[#19153F] tracking-tight leading-tight truncate" title="Logistic Regression">
            Logistic Reg.
          </div>
          <div className="text-[11px] text-[#2C7A68] font-medium flex items-center gap-1">
            <span>L2 Balanced • Zero Leakage</span>
          </div>
        </div>

        {/* Card 4: Champion F1-Score */}
        <div className="bg-[#EDE9FE] rounded-[14px] p-4 flex flex-col justify-between h-[115px] shadow-sm hover:-translate-y-0.5 transition-transform">
          <div className="flex items-center justify-between">
            <span className="text-[12px] font-semibold text-[#6555AB]">Champion F1-Score</span>
            <div className="w-6 h-6 rounded-lg bg-white/80 flex items-center justify-center text-[#6045F5]">
              <Target size={13} />
            </div>
          </div>
          <div className="text-[26px] font-bold text-[#19153F] tracking-tight leading-none">
            {data ? data.metrics.champion_f1.toFixed(4) : '0.9653'}
          </div>
          <div className="text-[11px] text-[#6555AB] font-medium flex items-center gap-1">
            <span>ROC-AUC: 0.9971</span>
          </div>
        </div>
      </div>

      {/* Main 2-Column Content */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        {/* Left Column (col-span-7) */}
        <div className="lg:col-span-7 flex flex-col gap-5">
          {/* Executive Summary Card */}
          <div className="bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card">
            <div className="flex items-center justify-between pb-3 border-b border-gray-100">
              <h2 className="text-[16px] font-bold text-[#19153F]">Executive Summary</h2>
              <span className="text-[11px] font-semibold bg-[#EDE9FE] text-[#6045F5] px-2.5 py-0.5 rounded-full">
                DMA Academic Project
              </span>
            </div>

            <div className="space-y-3 mt-3.5 text-[13px] text-[#47475A] leading-relaxed">
              <p>
                • <strong className="text-[#19153F]">Class-Imbalanced Text Classification:</strong> Evaluated 4 distinct model architectures on 5,169 deduplicated SMS messages, strictly addressing the ~12.6% spam imbalance without synthetic leakage.
              </p>
              <p>
                • <strong className="text-[#19153F]">Transparent Explainability:</strong> Derived empirical word-level odds ratios (exp(β)) via Logistic Regression, enabling transparent auditing of which lexical tokens drive spam classifications.
              </p>
              <p>
                • <strong className="text-[#19153F]">Daily Volume Forecasting:</strong> Modeled 365 simulated daily spam counts with 7-day smoothing and an ARIMA(1,1,1) model over a 30-day holdout forecast.
              </p>
            </div>

            <div className="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between">
              <span className="text-[12px] text-[#77778D]">Ready to test live SMS messages?</span>
              <button 
                onClick={onNavigateToPrediction}
                className="flex items-center gap-1.5 bg-[#6045F5] hover:bg-[#4E34E0] text-white text-[12px] font-semibold px-3 py-1.5 rounded-lg shadow-sm transition-colors"
              >
                <span>Launch Live Classifier</span>
                <ArrowRight size={13} />
              </button>
            </div>
          </div>

          {/* 5-Step ML Pipeline Sequence */}
          <div className="bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card">
            <div className="flex items-center justify-between pb-3">
              <h2 className="text-[16px] font-bold text-[#19153F]">End-to-End ML Pipeline</h2>
              <span className="text-[11px] text-[#77778D] font-medium">5 Stages Verified</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-5 gap-2.5 mt-2">
              {[
                { step: '01', title: 'Preprocess', icon: Layers, desc: 'Regex & Stemming' },
                { step: '02', title: 'Features', icon: Cpu, desc: 'TF-IDF & Chi²' },
                { step: '03', title: 'Models', icon: Trophy, desc: 'NB, kNN, LR, BN' },
                { step: '04', title: 'Evaluate', icon: ShieldCheck, desc: 'F1: 0.9653' },
                { step: '05', title: 'Forecast', icon: TrendingUp, desc: 'ARIMA (30d)' }
              ].map((st) => {
                const Icon = st.icon;
                return (
                  <div key={st.step} className="bg-[#FAF9FD] border border-[#EBEBF2] rounded-xl p-3 flex flex-col justify-between hover:border-[#6045F5]/40 transition-colors">
                    <div className="flex items-center justify-between text-[10px] font-bold text-[#6045F5]">
                      <span>{st.step}</span>
                      <Icon size={12} />
                    </div>
                    <div className="font-bold text-[13px] text-[#19153F] mt-2 mb-0.5">{st.title}</div>
                    <div className="text-[10px] text-[#77778D]">{st.desc}</div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Right Column (col-span-5) */}
        <div className="lg:col-span-5 flex flex-col gap-5">
          {/* Class Distribution Donut Chart Card */}
          <div className="bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card">
            <div className="flex items-center justify-between pb-2">
              <h2 className="text-[16px] font-bold text-[#19153F]">Corpus Class Balance</h2>
              <span className="text-[11px] text-[#77778D]">5,169 SMS</span>
            </div>

            <div className="w-full h-[180px] relative">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={donutData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={75}
                    paddingAngle={4}
                    dataKey="count"
                  >
                    {donutData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const item = payload[0].payload;
                        return (
                          <div className="bg-[#19153F] text-white text-[11px] px-2.5 py-1 rounded-md shadow-md">
                            <span className="font-bold">{item.name}:</span> {item.count} ({item.percentage}%)
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>

              {/* Center Donut Label */}
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="text-[18px] font-bold text-[#19153F]">87 : 13</span>
                <span className="text-[10px] text-[#77778D]">Ham : Spam</span>
              </div>
            </div>

            {/* Donut Legend */}
            <div className="flex items-center justify-around pt-3 border-t border-gray-100 text-[12px]">
              {donutData.map((d) => (
                <div key={d.name} className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: d.color }}></span>
                  <span className="font-medium text-[#19153F]">{d.name}</span>
                  <span className="font-bold text-[#77778D]">({d.percentage}%)</span>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Action Interactive Card */}
          <div className="bg-[#EFF5FE] rounded-[14px] p-5 border border-[#DFE7FA] shadow-card flex items-center justify-between">
            <div className="flex flex-col">
              <span className="text-[14px] font-bold text-[#19153F]">Instant Inference Engine</span>
              <span className="text-[11px] text-[#77778D] mt-0.5">Test lottery, banking, and friend SMS</span>
            </div>
            <button
              onClick={onNavigateToPrediction}
              className="bg-[#2B2257] hover:bg-[#342A68] text-white p-2.5 rounded-xl shadow-sm transition-colors flex items-center gap-1.5 text-[12px] font-semibold"
            >
              <Zap size={14} className="text-[#A392F8]" />
              <span>Test Now</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
