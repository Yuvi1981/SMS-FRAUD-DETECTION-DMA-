import React, { useEffect, useState } from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  ResponsiveContainer, 
  CartesianGrid, 
  Legend 
} from 'recharts';
import { Search, Filter, Layers, BookOpen } from 'lucide-react';
import { api } from '../services/api';

interface EdaViewProps {
  activeSubTab?: string;
  onTabChange?: (tab: string) => void;
  globalSearch?: string;
}

export const EdaView: React.FC<EdaViewProps> = ({ 
  activeSubTab = 'length', 
  onTabChange, 
  globalSearch = '' 
}) => {
  const [activeTab, setActiveTab] = useState<'balance' | 'length' | 'words' | 'samples'>(
    (activeSubTab as any) || 'length'
  );
  const [edaData, setEdaData] = useState<any>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [classFilter, setClassFilter] = useState('All');
  const [searchQuery, setSearchQuery] = useState(globalSearch);
  const [loadingMessages, setLoadingMessages] = useState(false);

  useEffect(() => {
    if (activeSubTab && ['balance', 'length', 'words', 'samples'].includes(activeSubTab)) {
      setActiveTab(activeSubTab as any);
    }
  }, [activeSubTab]);

  useEffect(() => {
    if (globalSearch !== undefined && globalSearch !== searchQuery) {
      setSearchQuery(globalSearch);
      if (globalSearch.trim() && activeTab !== 'samples') {
        handleTabSelect('samples');
      }
    }
  }, [globalSearch]);

  const handleTabSelect = (tab: 'balance' | 'length' | 'words' | 'samples') => {
    setActiveTab(tab);
    if (onTabChange) onTabChange(tab);
  };

  useEffect(() => {
    api.getEda().then(res => setEdaData(res));
  }, []);

  const loadMessages = async () => {
    setLoadingMessages(true);
    try {
      const res = await api.getMessages(classFilter, searchQuery, 20);
      setMessages(res.messages || []);
    } finally {
      setLoadingMessages(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'samples') {
      loadMessages();
    }
  }, [activeTab, classFilter, searchQuery]);

  const lengthData = edaData?.length_distribution || [
    { range: '0-40', ham: 2150, spam: 12 },
    { range: '40-80', ham: 1420, spam: 45 },
    { range: '80-120', ham: 620, spam: 110 },
    { range: '120-140', ham: 180, spam: 165 },
    { range: '140-160', ham: 110, spam: 248 },
    { range: '160-200', ham: 25, spam: 58 },
    { range: '200-300', ham: 11, spam: 15 }
  ];

  return (
    <div className="flex flex-col gap-5">
      {/* Tab Pills */}
      <div className="flex items-center gap-2 bg-white p-1.5 rounded-xl border border-[#E6E6EF] shadow-2xs self-start">
        {[
          { id: 'length', label: '📏 Message Length Distribution' },
          { id: 'balance', label: '📊 Class Balance Summary' },
          { id: 'words', label: '🔤 Chi² Top Terms' },
          { id: 'samples', label: '🔍 Sample Messages Explorer' },
        ].map((t) => (
          <button
            key={t.id}
            onClick={() => handleTabSelect(t.id as any)}
            className={`px-3 py-1.5 rounded-lg text-[12.5px] font-semibold transition-all ${
              activeTab === t.id
                ? 'bg-[#6045F5] text-white shadow-xs'
                : 'text-[#77778D] hover:text-[#19153F] hover:bg-gray-50'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Tab 1: Length Distribution */}
      {activeTab === 'length' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
          <div className="lg:col-span-8 bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card">
            <div className="flex items-center justify-between pb-3 border-b border-gray-100">
              <h2 className="text-[16px] font-bold text-[#19153F]">Character Length Distribution by Class</h2>
              <span className="text-[11px] text-[#77778D]">Binned Counts (Chars)</span>
            </div>

            <div className="w-full h-[260px] mt-3">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={lengthData} margin={{ top: 15, right: 15, left: -10, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F0F0F5" />
                  <XAxis dataKey="range" tick={{ fill: '#77778D', fontSize: 11 }} />
                  <YAxis tick={{ fill: '#9E9EA7', fontSize: 11 }} />
                  <Tooltip 
                    content={({ active, payload, label }) => {
                      if (active && payload && payload.length) {
                        return (
                          <div className="bg-[#19153F] text-white text-[11px] p-2 rounded-md shadow-md">
                            <div className="font-bold border-b border-white/20 pb-1">{label} chars</div>
                            <div className="text-emerald-400 mt-1">Ham: {payload[0]?.value}</div>
                            <div className="text-red-400">Spam: {payload[1]?.value}</div>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Legend />
                  <Bar dataKey="ham" fill="#10B981" name="Ham (Legitimate)" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="spam" fill="#EF4444" name="Spam" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="lg:col-span-4 bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card">
            <h3 className="text-[15px] font-bold text-[#19153F] mb-3">Key Text Length Insights</h3>
            <div className="space-y-3 text-[12.5px] text-[#47475A] leading-relaxed">
              <div className="p-3 bg-[#FEF2F2] rounded-xl border border-[#FCA5A5]/40">
                <span className="font-bold text-[#B91C1C] block mb-1">🚨 Distinct 140–160 Character Spike:</span>
                Spam messages cluster aggressively around 130–160 characters to maximize the 160-char SMS limit with marketing links and phone numbers.
              </div>
              <div className="p-3 bg-[#F0FDF4] rounded-xl border border-[#86EFAC]/40">
                <span className="font-bold text-[#15803D] block mb-1">✅ Concise Conversational Ham:</span>
                Legitimate SMS are substantially briefer with a median length of <strong>40 characters</strong> (9 words) and a long, dispersed tail.
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Class Balance */}
      {activeTab === 'balance' && (
        <div className="bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card">
          <div className="flex items-center justify-between pb-3 border-b border-gray-100">
            <div>
              <h2 className="text-[16px] font-bold text-[#19153F]">Corpus Summary Statistics</h2>
              <p className="text-[11.5px] text-[#77778D] mt-0.5">Statistical profile of 5,169 deduplicated SMS messages from raw dataset</p>
            </div>
            <span className="text-[11px] font-semibold bg-[#DCFCE7] text-[#15803D] px-2.5 py-0.5 rounded-full">
              Full Corpus Profiled
            </span>
          </div>

          <div className="overflow-x-auto mt-3">
            <table className="w-full text-left text-[12.5px] border-collapse">
              <thead>
                <tr className="border-b border-gray-200 text-[#77778D] font-medium text-[11px]">
                  <th className="pb-2">Class</th>
                  <th className="pb-2">Count</th>
                  <th className="pb-2">Prevalence</th>
                  <th className="pb-2">Avg Chars</th>
                  <th className="pb-2">Avg Words</th>
                  <th className="pb-2">% Digits</th>
                  <th className="pb-2">% URLs</th>
                  <th className="pb-2">% Money/Prize</th>
                  <th className="pb-2">% Phone Numbers</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {edaData?.summary && edaData.summary.length > 0 ? (
                  edaData.summary.map((row: any, idx: number) => {
                    const isSpam = row.class === 'spam';
                    const isTotal = row.class === 'total';
                    return (
                      <tr 
                        key={idx} 
                        className={`hover:bg-gray-50 ${isTotal ? 'bg-[#FAF9FD] font-semibold' : ''}`}
                      >
                        <td className={`py-3 font-bold ${
                          isTotal ? 'text-[#6045F5]' : (isSpam ? 'text-[#EF4444]' : 'text-[#10B981]')
                        }`}>
                          {isTotal ? 'Total Corpus' : (isSpam ? 'Spam' : 'Ham (Legitimate)')}
                        </td>
                        <td className="py-3 font-semibold text-[#19153F]">{Number(row.count).toLocaleString()}</td>
                        <td className="py-3 text-[#19153F]">{row.percentage}%</td>
                        <td className="py-3 text-[#47475A]">{row.avg_chars} chars</td>
                        <td className="py-3 text-[#47475A]">{row.avg_words} words</td>
                        <td className="py-3 text-[#47475A]">{row.pct_has_digits}%</td>
                        <td className="py-3 text-[#47475A]">{row.pct_has_url}%</td>
                        <td className="py-3 text-[#47475A]">{row.pct_has_money}%</td>
                        <td className="py-3 text-[#47475A]">{row.pct_has_phone}%</td>
                      </tr>
                    );
                  })
                ) : (
                  <>
                    <tr className="hover:bg-gray-50">
                      <td className="py-2.5 font-bold text-[#10B981]">Ham (Legitimate)</td>
                      <td className="py-2.5 font-semibold text-[#19153F]">4,516</td>
                      <td className="py-2.5 font-medium text-[#19153F]">87.37%</td>
                      <td className="py-2.5 text-[#47475A]">71.0 chars</td>
                      <td className="py-2.5 text-[#47475A]">14.2 words</td>
                      <td className="py-2.5 text-[#47475A]">15.8%</td>
                      <td className="py-2.5 text-[#47475A]">0.02%</td>
                      <td className="py-2.5 text-[#47475A]">2.55%</td>
                      <td className="py-2.5 text-[#47475A]">0.07%</td>
                    </tr>
                    <tr className="hover:bg-gray-50">
                      <td className="py-2.5 font-bold text-[#EF4444]">Spam</td>
                      <td className="py-2.5 font-semibold text-[#19153F]">653</td>
                      <td className="py-2.5 font-medium text-[#19153F]">12.63%</td>
                      <td className="py-2.5 text-[#47475A]">138.1 chars</td>
                      <td className="py-2.5 text-[#47475A]">23.7 words</td>
                      <td className="py-2.5 text-[#47475A]">94.0%</td>
                      <td className="py-2.5 text-[#47475A]">13.8%</td>
                      <td className="py-2.5 text-[#47475A]">41.7%</td>
                      <td className="py-2.5 text-[#47475A]">51.6%</td>
                    </tr>
                    <tr className="hover:bg-gray-50 bg-[#FAF9FD] font-semibold">
                      <td className="py-2.5 text-[#6045F5]">Total Corpus</td>
                      <td className="py-2.5 text-[#19153F]">5,169</td>
                      <td className="py-2.5 text-[#19153F]">100.0%</td>
                      <td className="py-2.5 text-[#47475A]">79.5 chars</td>
                      <td className="py-2.5 text-[#47475A]">15.4 words</td>
                      <td className="py-2.5 text-[#47475A]">25.7%</td>
                      <td className="py-2.5 text-[#47475A]">1.76%</td>
                      <td className="py-2.5 text-[#47475A]">7.49%</td>
                      <td className="py-2.5 text-[#47475A]">6.58%</td>
                    </tr>
                  </>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 3: Top Chi-2 Terms */}
      {activeTab === 'words' && (
        <div className="bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card">
          <div className="flex items-center justify-between pb-3 border-b border-gray-100">
            <div>
              <h2 className="text-[16px] font-bold text-[#19153F]">Top Discriminative Features by Chi-Square (χ²) Statistic</h2>
              <p className="text-[11.5px] text-[#77778D] mt-0.5">Top rank-ordered n-grams selected for modeling based on independence testing against class labels</p>
            </div>
            <span className="text-[11px] font-semibold bg-[#EDE9FE] text-[#6045F5] px-2.5 py-0.5 rounded-full">
              p &lt; 0.0001
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 mt-4">
            {(edaData?.top_chi2 && edaData.top_chi2.length > 0 ? edaData.top_chi2 : [
              { term: 'numtoken', chi2_score: 2450.8, p_value: 0.0 },
              { term: 'phonetoken', chi2_score: 2190.2, p_value: 0.0 },
              { term: 'claim', chi2_score: 1254.2, p_value: 0.0 },
              { term: 'free', chi2_score: 1089.4, p_value: 0.0 },
              { term: 'prize', chi2_score: 982.6, p_value: 0.0 },
              { term: 'call', chi2_score: 876.1, p_value: 0.0 },
              { term: 'txt', chi2_score: 792.5, p_value: 0.0 },
              { term: 'won', chi2_score: 745.3, p_value: 0.0 },
              { term: 'urgent', chi2_score: 682.0, p_value: 0.0 },
              { term: 'stop', chi2_score: 612.4, p_value: 0.0 },
              { term: 'cash', chi2_score: 584.8, p_value: 0.0 },
              { term: 'moneytoken', chi2_score: 531.6, p_value: 0.0 },
            ]).map((item: any, idx: number) => {
              const score = typeof item.chi2_score === 'number' ? item.chi2_score.toLocaleString(undefined, { maximumFractionDigits: 1 }) : (item.chi2 || '0');
              const pVal = item.p_value !== undefined ? (Number(item.p_value) < 0.0001 ? '< 0.0001' : String(item.p_value)) : '< 0.0001';
              return (
                <div key={idx} className="bg-[#FAF9FD] p-3 rounded-xl border border-[#E6E6EF] flex items-center justify-between hover:border-[#6045F5]/40 transition-colors">
                  <div>
                    <span className="text-[13px] font-bold text-[#19153F]">"{item.term}"</span>
                    <span className="text-[11px] text-[#77778D] block">p-value: {pVal}</span>
                  </div>
                  <span className="text-[12px] font-bold text-[#6045F5] bg-[#EDE9FE] px-2 py-0.5 rounded-lg font-mono">
                    χ² {score}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Tab 4: Sample Messages */}
      {activeTab === 'samples' && (
        <div className="bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-gray-100">
            <h2 className="text-[16px] font-bold text-[#19153F]">Interactive Corpus Explorer</h2>

            <div className="flex items-center gap-2">
              <select
                value={classFilter}
                onChange={(e) => setClassFilter(e.target.value)}
                className="bg-[#F4F4F8] border border-[#E6E6EF] rounded-lg px-2.5 py-1 text-[12px] font-semibold text-[#19153F]"
              >
                <option value="All">All Messages</option>
                <option value="Spam">Spam Only</option>
                <option value="Ham">Ham Only</option>
              </select>

              <div className="relative w-48">
                <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Filter messages..."
                  className="w-full bg-[#FAF9FD] border border-[#E6E6EF] rounded-lg pl-8 pr-2.5 py-1 text-[12px] text-[#19153F] focus:outline-none focus:ring-1 focus:ring-[#6045F5]"
                />
              </div>
            </div>
          </div>

          <div className="overflow-x-auto mt-3">
            <table className="w-full text-left text-[12px] border-collapse">
              <thead>
                <tr className="border-b border-gray-200 text-[#77778D] font-medium text-[11px]">
                  <th className="pb-2 w-12">#</th>
                  <th className="pb-2 w-20">Class</th>
                  <th className="pb-2">Message Content</th>
                  <th className="pb-2 w-16">Length</th>
                  <th className="pb-2 w-16">Words</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {messages.length > 0 ? (
                  messages.map((msg) => (
                    <tr key={msg.id} className="hover:bg-gray-50">
                      <td className="py-2.5 text-gray-400">{msg.id}</td>
                      <td className="py-2.5">
                        <span className={`px-2 py-0.5 rounded text-[10.5px] font-bold ${
                          msg.is_spam ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-700'
                        }`}>
                          {msg.label}
                        </span>
                      </td>
                      <td className="py-2.5 font-medium text-[#19153F] pr-4">{msg.text}</td>
                      <td className="py-2.5 text-[#77778D]">{msg.n_chars}</td>
                      <td className="py-2.5 text-[#77778D]">{msg.n_words}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={5} className="py-6 text-center text-gray-400">
                      {loadingMessages ? 'Loading messages...' : 'No messages match search.'}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
