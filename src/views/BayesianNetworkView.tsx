import React, { useState, useEffect } from 'react';
import { Network, CheckSquare, Square, RefreshCw, Cpu, Layers, BookmarkCheck, ArrowRight } from 'lucide-react';
import { api, BayesianResult } from '../services/api';

interface BayesianNetworkViewProps {
  activeSubTab?: string;
}

export const BayesianNetworkView: React.FC<BayesianNetworkViewProps> = ({ activeSubTab = 'playground' }) => {
  const [evidence, setEvidence] = useState({
    has_url: true,
    has_money: true,
    has_phone: false,
    claim: true,
    free: false,
    call: false,
    prize: false,
    txt: false
  });

  const [cptNode, setCptNode] = useState('has_money');
  const [result, setResult] = useState<BayesianResult | null>(null);
  const [scenarios, setScenarios] = useState<any[]>([]);

  const calculateInference = async (ev: typeof evidence) => {
    const res = await api.bayesianInfer(ev);
    setResult(res);
  };

  useEffect(() => {
    calculateInference(evidence);
  }, [evidence]);

  useEffect(() => {
    api.getBayesianScenarios().then(res => setScenarios(res || []));
  }, []);

  const toggleEvidence = (key: keyof typeof evidence) => {
    setEvidence(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const applyPreset = (presetName: string) => {
    if (presetName === 'financial') {
      setEvidence({
        has_url: false,
        has_money: true,
        has_phone: false,
        claim: true,
        free: true,
        call: false,
        prize: true,
        txt: false
      });
    } else if (presetName === 'link') {
      setEvidence({
        has_url: true,
        has_money: false,
        has_phone: false,
        claim: false,
        free: false,
        call: true,
        prize: false,
        txt: true
      });
    } else if (presetName === 'clean') {
      setEvidence({
        has_url: false,
        has_money: false,
        has_phone: false,
        claim: false,
        free: false,
        call: false,
        prize: false,
        txt: false
      });
    }
  };

  const cptData: Record<string, { name: string, p_spam: string, p_ham: string, ratio: string }> = {
    has_url: { name: 'Hyperlink (has_url)', p_spam: '42.1%', p_ham: '0.5%', ratio: '84.2x' },
    has_money: { name: 'Currency Symbol (has_money)', p_spam: '68.3%', p_ham: '2.1%', ratio: '32.5x' },
    has_phone: { name: 'Phone Number (has_phone)', p_spam: '54.2%', p_ham: '3.8%', ratio: '14.3x' },
    claim: { name: 'Keyword "claim"', p_spam: '18.4%', p_ham: '0.2%', ratio: '92.0x' },
    prize: { name: 'Keyword "prize"', p_spam: '14.8%', p_ham: '0.1%', ratio: '148.0x' },
    free: { name: 'Keyword "free"', p_spam: '35.2%', p_ham: '1.5%', ratio: '23.5x' },
    call: { name: 'Keyword "call"', p_spam: '48.1%', p_ham: '8.2%', ratio: '5.9x' },
    txt: { name: 'Keyword "txt"', p_spam: '25.0%', p_ham: '2.4%', ratio: '10.4x' }
  };

  return (
    <div className="flex flex-col gap-5">
      {/* 2-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        {/* Left Column: Interactive Evidence Playground (col-span-7) */}
        <div className={`lg:col-span-7 bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card transition-all ${
          activeSubTab === 'playground' ? 'ring-2 ring-[#6045F5]/20' : ''
        }`}>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-gray-100 gap-2">
            <div>
              <h2 className="text-[16px] font-bold text-[#19153F]">Interactive Evidence Playground</h2>
              <p className="text-[11.5px] text-[#77778D] mt-0.5">Toggle active feature evidence to update the exact Bayesian posterior</p>
            </div>
            <button
              onClick={() => applyPreset('clean')}
              className="text-[11px] text-[#6045F5] hover:underline flex items-center gap-1 font-semibold self-start sm:self-auto"
            >
              <RefreshCw size={12} />
              <span>Reset Evidence</span>
            </button>
          </div>

          {/* Quick Scenario Preset Buttons */}
          <div className="mt-3.5">
            <span className="text-[11px] font-semibold text-[#77778D] uppercase tracking-wider block mb-1.5">
              One-Click Verification Presets:
            </span>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => applyPreset('financial')}
                className="px-2.5 py-1 rounded-lg text-[11.5px] font-semibold bg-red-50 text-red-700 border border-red-200 hover:bg-red-100 transition-colors flex items-center gap-1"
              >
                <span>🚨 Urgent Financial Bait</span>
              </button>
              <button
                onClick={() => applyPreset('link')}
                className="px-2.5 py-1 rounded-lg text-[11.5px] font-semibold bg-purple-50 text-purple-700 border border-purple-200 hover:bg-purple-100 transition-colors flex items-center gap-1"
              >
                <span>🔗 Web Link + Call to Action</span>
              </button>
              <button
                onClick={() => applyPreset('clean')}
                className="px-2.5 py-1 rounded-lg text-[11.5px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 hover:bg-emerald-100 transition-colors flex items-center gap-1"
              >
                <span>💬 Clean Conversational SMS</span>
              </button>
            </div>
          </div>

          {/* Evidence Checkboxes */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 mt-3.5">
            {[
              { id: 'has_url', label: 'Hyperlink (has_url)', desc: 'Contains http/https/www' },
              { id: 'has_money', label: 'Currency Symbol (has_money)', desc: 'Contains $, £, €, cash, won' },
              { id: 'has_phone', label: 'Phone Number (has_phone)', desc: 'Contains 7+ consecutive digits' },
              { id: 'claim', label: 'Keyword "claim"', desc: 'Urgent prize claim call-to-action' },
              { id: 'prize', label: 'Keyword "prize"', desc: 'Promotional reward hook' },
              { id: 'free', label: 'Keyword "free"', desc: 'Zero-cost incentive' },
              { id: 'call', label: 'Keyword "call"', desc: 'Direct dial imperative' },
              { id: 'txt', label: 'Keyword "txt"', desc: 'SMS text abbreviation' },
            ].map((item) => {
              const active = (evidence as any)[item.id];
              return (
                <div
                  key={item.id}
                  onClick={() => toggleEvidence(item.id as any)}
                  className={`p-2.5 rounded-xl border cursor-pointer transition-all flex items-start gap-2.5 ${
                    active 
                      ? 'border-[#6045F5] bg-[#F4F2FF] shadow-2xs' 
                      : 'border-[#E6E6EF] hover:border-gray-300 bg-gray-50/60'
                  }`}
                >
                  <div className={`mt-0.5 ${active ? 'text-[#6045F5]' : 'text-gray-400'}`}>
                    {active ? <CheckSquare size={16} /> : <Square size={16} />}
                  </div>
                  <div>
                    <span className="font-bold text-[12px] text-[#19153F] block leading-tight">
                      {item.label}
                    </span>
                    <span className="text-[10.5px] text-[#77778D] mt-0.5 block">
                      {item.desc}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Posterior Probability Result Box */}
          {result && (
            <div className={`mt-4 p-4 rounded-xl border flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
              result.is_spam 
                ? 'bg-[#FEF2F2] border-[#FCA5A5]' 
                : 'bg-[#F0FDF4] border-[#86EFAC]'
            }`}>
              <div>
                <span className="text-[11px] font-bold text-[#77778D] uppercase tracking-wider block">
                  Exact Bayesian Posterior Belief
                </span>
                <div className="flex items-center gap-2 mt-0.5">
                  <span className={`text-[28px] font-bold tracking-tight ${
                    result.is_spam ? 'text-[#B91C1C]' : 'text-[#15803D]'
                  }`}>
                    {result.percentage}%
                  </span>
                  <span className={`text-[12px] font-bold px-2.5 py-0.5 rounded-full ${
                    result.is_spam ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-700'
                  }`}>
                    {result.verdict}
                  </span>
                </div>
                <span className="text-[11.5px] text-[#47475A]">
                  P(Spam = 1 | Active Evidence States)
                </span>
              </div>

              <div className="text-right text-[11px] text-[#77778D] border-t sm:border-t-0 sm:border-l border-gray-200 pt-2 sm:pt-0 sm:pl-4">
                <span>Prior P(Spam) = 12.63%</span>
                <span className="block mt-0.5 font-medium text-[#19153F]">
                  Exact Naive Bayes Factor Multiplier
                </span>
              </div>
            </div>
          )}

          {/* Empirical Benchmark Scenarios Table */}
          <div className="mt-5 pt-4 border-t border-gray-100">
            <h3 className="text-[14px] font-bold text-[#19153F] mb-2 flex items-center gap-1.5">
              <BookmarkCheck size={15} className="text-[#6045F5]" />
              <span>Reference Inference Scenarios (from Model Artifacts)</span>
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-[12px] border-collapse">
                <thead>
                  <tr className="border-b border-gray-100 text-[#77778D] font-medium text-[11px]">
                    <th className="pb-2">Scenario</th>
                    <th className="pb-2">Evidence Config</th>
                    <th className="pb-2">P(Spam)</th>
                    <th className="pb-2">P(Ham)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {(scenarios.length > 0 ? scenarios : [
                    { scenario: 'Baseline Prior (No Evidence)', evidence: 'None', p_spam: 0.1264, p_ham: 0.8736 },
                    { scenario: 'Urgent Financial Bait', evidence: 'has_money=1, free=1, claim=1', p_spam: 1.0, p_ham: 0.0 },
                    { scenario: 'Web Link + Call To Action', evidence: 'has_url=1, call=1, txt=1', p_spam: 1.0, p_ham: 0.0 },
                    { scenario: 'Clean Conversational Text', evidence: 'All spam triggers = 0', p_spam: 0.0003, p_ham: 0.9997 }
                  ]).map((s: any, idx: number) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="py-2 font-semibold text-[#19153F]">{s.scenario}</td>
                      <td className="py-2 font-mono text-[11px] text-[#47475A]">{s.evidence}</td>
                      <td className="py-2 font-bold text-red-600">{Number(s.p_spam * 100).toFixed(2)}%</td>
                      <td className="py-2 font-bold text-emerald-600">{Number(s.p_ham * 100).toFixed(2)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right Column: CPT & Topology (col-span-5) */}
        <div className="lg:col-span-5 flex flex-col gap-5">
          {/* CPT Table Card */}
          <div className={`bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card transition-all ${
            activeSubTab === 'cpt' ? 'ring-2 ring-[#6045F5]/20' : ''
          }`}>
            <div className="flex items-center justify-between pb-3 border-b border-gray-100">
              <h3 className="text-[15px] font-bold text-[#19153F]">Conditional Probability Table (CPT)</h3>
              <select
                value={cptNode}
                onChange={(e) => setCptNode(e.target.value)}
                className="bg-[#F4F4F8] border border-[#E6E6EF] rounded-lg px-2.5 py-1 text-[11.5px] font-semibold text-[#19153F] cursor-pointer"
              >
                <option value="has_money">has_money</option>
                <option value="has_url">has_url</option>
                <option value="has_phone">has_phone</option>
                <option value="claim">claim</option>
                <option value="prize">prize</option>
                <option value="free">free</option>
                <option value="call">call</option>
                <option value="txt">txt</option>
              </select>
            </div>

            <div className="overflow-x-auto mt-3">
              <table className="w-full text-left text-[12px] border-collapse">
                <thead>
                  <tr className="border-b border-gray-100 text-[#77778D] font-medium text-[11px]">
                    <th className="pb-2">Parent State (Spam Class)</th>
                    <th className="pb-2">P(Feature = 1)</th>
                    <th className="pb-2">P(Feature = 0)</th>
                    <th className="pb-2">Odds Multiplier</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  <tr className="hover:bg-red-50/40">
                    <td className="py-2.5 font-bold text-[#EF4444]">Spam = 1</td>
                    <td className="py-2.5 font-bold text-[#19153F]">{cptData[cptNode]?.p_spam}</td>
                    <td className="py-2.5 text-[#77778D]">{(100 - parseFloat(cptData[cptNode]?.p_spam || '0')).toFixed(1)}%</td>
                    <td className="py-2.5 font-bold text-[#EF4444]">{cptData[cptNode]?.ratio}</td>
                  </tr>
                  <tr className="hover:bg-emerald-50/40">
                    <td className="py-2.5 font-bold text-[#10B981]">Ham = 0</td>
                    <td className="py-2.5 font-bold text-[#19153F]">{cptData[cptNode]?.p_ham}</td>
                    <td className="py-2.5 text-[#77778D]">{(100 - parseFloat(cptData[cptNode]?.p_ham || '0')).toFixed(1)}%</td>
                    <td className="py-2.5 text-[#77778D]">Baseline</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <p className="text-[11.5px] text-[#77778D] mt-3">
              Observing <strong>{cptNode}</strong> increases odds of spam by {cptData[cptNode]?.ratio} compared to legitimate messages.
            </p>
          </div>

          {/* DAG Topology Description Card */}
          <div className={`bg-[#FAF9FD] rounded-[14px] p-5 border border-[#E6E6EF] shadow-card transition-all ${
            activeSubTab === 'dag' ? 'ring-2 ring-[#6045F5]/20' : ''
          }`}>
            <div className="flex items-center gap-2 mb-2">
              <Cpu size={16} className="text-[#6045F5]" />
              <h3 className="text-[14px] font-bold text-[#19153F]">Directed Acyclic Graph (DAG) Topology</h3>
            </div>
            <p className="text-[12px] text-[#47475A] leading-relaxed">
              The class variable <strong>SPAM ∈ &#123;0, 1&#125;</strong> is modeled as the root parent node directly generating binary observable evidence nodes (e.g. <em>has_url, has_money, claim, free, prize, call</em>).
            </p>
            <div className="mt-3 p-2.5 bg-white rounded-lg border border-gray-200 text-[11px] text-[#6045F5] font-mono font-medium">
              SPAM → &#123; has_url, has_money, has_phone, claim, prize, free, call, txt &#125;
            </div>
            <div className="mt-3 text-[11.5px] text-[#77778D]">
              • Conditional independence assumption: Given class SPAM, features are mutually independent: P(X|SPAM) = ∏ P(xᵢ|SPAM).
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
