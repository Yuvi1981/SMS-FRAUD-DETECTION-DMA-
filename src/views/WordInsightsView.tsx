import React, { useState, useEffect } from 'react';
import { Search, Sparkles, AlertCircle, ArrowUpRight, ArrowDownRight, Sliders } from 'lucide-react';
import { api, WordLookupResult } from '../services/api';

interface WordInsightsViewProps {
  activeSubTab?: string;
  globalSearch?: string;
}

export const WordInsightsView: React.FC<WordInsightsViewProps> = ({ 
  activeSubTab = 'lookup', 
  globalSearch = '' 
}) => {
  const [searchWord, setSearchWord] = useState('prize');
  const [lookupResult, setLookupResult] = useState<WordLookupResult | null>(null);
  const [wordLimit, setWordLimit] = useState(10);
  const [wordsData, setWordsData] = useState<{ spam_drivers: any[], ham_drivers: any[] }>({
    spam_drivers: [],
    ham_drivers: []
  });

  const performLookup = async (word: string) => {
    if (!word.trim()) return;
    const res = await api.lookupWord(word.trim());
    setLookupResult(res);
  };

  useEffect(() => {
    performLookup('prize');
  }, []);

  useEffect(() => {
    if (globalSearch && globalSearch.trim()) {
      setSearchWord(globalSearch.trim());
      performLookup(globalSearch.trim());
    }
  }, [globalSearch]);

  useEffect(() => {
    api.getWords(wordLimit).then(res => setWordsData(res));
  }, [wordLimit]);

  return (
    <div className="flex flex-col gap-5">
      {/* Word Lookup Search Card */}
      <div className={`bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card transition-all ${
        activeSubTab === 'lookup' ? 'ring-2 ring-[#6045F5]/20' : ''
      }`}>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-gray-100">
          <div>
            <h2 className="text-[16px] font-bold text-[#19153F]">Word-Level Odds Ratio Lookup</h2>
            <p className="text-[11.5px] text-[#77778D] mt-0.5">Explore Logistic Regression coefficients ($e^\beta$) for any vocabulary token</p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-[11px] text-[#77778D] font-medium">Top Words to Display:</span>
            <span className="text-[12px] font-bold text-[#6045F5]">{wordLimit}</span>
            <input 
              type="range" 
              min={5} 
              max={30} 
              value={wordLimit} 
              onChange={(e) => setWordLimit(Number(e.target.value))}
              className="w-24 accent-[#6045F5] cursor-pointer"
            />
          </div>
        </div>

        {/* Search bar & quick chips */}
        <div className="mt-3.5 flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
          <div className="relative flex-1">
            <Search size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              value={searchWord}
              onChange={(e) => setSearchWord(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') performLookup(searchWord);
              }}
              placeholder="Search word (e.g. claim, prize, free, call, urgent, meet, home)..."
              className="w-full bg-[#FAF9FD] border border-[#E6E6EF] rounded-xl pl-9 pr-3.5 py-2 text-[13px] text-[#19153F] placeholder-[#9E9EA7] focus:outline-none focus:ring-2 focus:ring-[#6045F5]/30 focus:border-[#6045F5]"
            />
          </div>

          <button
            onClick={() => performLookup(searchWord)}
            className="bg-[#6045F5] hover:bg-[#4E34E0] text-white text-[12.5px] font-semibold px-4 py-2 rounded-xl transition-colors shadow-xs"
          >
            Lookup Token
          </button>
        </div>

        {/* Quick Suggestion Pills */}
        <div className="flex flex-wrap items-center gap-1.5 mt-2.5 text-[11px] text-[#77778D]">
          <span>Try quick words:</span>
          {['claim', 'prize', 'free', 'urgent', 'cash', 'call', 'meet', 'home', 'later', 'ok'].map((w) => (
            <button
              key={w}
              onClick={() => {
                setSearchWord(w);
                performLookup(w);
              }}
              className="bg-gray-100 hover:bg-gray-200 text-[#19153F] px-2 py-0.5 rounded-md font-medium transition-colors"
            >
              {w}
            </button>
          ))}
        </div>

        {/* Lookup Result Box */}
        {lookupResult && (
          <div className="mt-4 p-4 rounded-xl border border-[#E6E6EF] bg-[#FBFBFE] shadow-2xs">
            {lookupResult.found ? (
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold text-white shadow-xs ${
                    (lookupResult.odds_ratio || 1) >= 1 ? 'bg-[#EF4444]' : 'bg-[#10B981]'
                  }`}>
                    {(lookupResult.odds_ratio || 1) >= 1 ? <ArrowUpRight size={20} /> : <ArrowDownRight size={20} />}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-[17px] font-bold text-[#19153F]">"{lookupResult.word}"</span>
                      <span className={`text-[11px] font-bold px-2 py-0.5 rounded-md ${
                        (lookupResult.odds_ratio || 1) >= 1 ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-700'
                      }`}>
                        {lookupResult.factor_text}
                      </span>
                    </div>
                    <p className="text-[12px] text-[#47475A] mt-0.5">{lookupResult.explanation}</p>
                  </div>
                </div>

                <div className="flex items-center gap-4 text-[11.5px] border-t sm:border-t-0 sm:border-l border-gray-200 pt-2 sm:pt-0 sm:pl-4">
                  <div>
                    <span className="text-[#77778D] block">Coefficient (β):</span>
                    <span className="font-mono font-bold text-[#19153F]">{lookupResult.coef}</span>
                  </div>
                  <div>
                    <span className="text-[#77778D] block">95% CI Range:</span>
                    <span className="font-mono font-bold text-[#19153F]">[{lookupResult.ci_lower}, {lookupResult.ci_upper}]</span>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-2 text-[12px] text-gray-500">
                <AlertCircle size={15} />
                <span>{lookupResult.explanation}</span>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Dual Column: Top Spam Drivers vs Top Ham Drivers */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 items-start">
        {/* Spam Drivers */}
        <div className={`bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card transition-all ${
          activeSubTab === 'spam' ? 'ring-2 ring-[#EF4444]/20' : ''
        }`}>
          <div className="flex items-center justify-between pb-3 border-b border-gray-100">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-[#EF4444]"></span>
              <h3 className="text-[15px] font-bold text-[#19153F]">Top {wordLimit} Spam Drivers (Odds Ratio &gt; 1)</h3>
            </div>
            <span className="text-[11px] text-[#EF4444] font-semibold">Multiplies Spam Odds</span>
          </div>

          <div className="overflow-x-auto mt-2">
            <table className="w-full text-left text-[12px] border-collapse">
              <thead>
                <tr className="border-b border-gray-100 text-[#77778D] font-medium text-[11px]">
                  <th className="pb-2">Token</th>
                  <th className="pb-2">Odds Ratio ($e^\beta$)</th>
                  <th className="pb-2">Coefficient (β)</th>
                  <th className="pb-2">95% CI</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {wordsData.spam_drivers.map((w, idx) => (
                  <tr key={idx} className="hover:bg-red-50/40">
                    <td className="py-2 font-semibold text-[#19153F]">"{w.word}"</td>
                    <td className="py-2">
                      <span className="font-bold text-[#EF4444] bg-red-50 px-2 py-0.5 rounded font-mono">
                        {w.odds_ratio}x
                      </span>
                    </td>
                    <td className="py-2 text-[#47475A] font-mono">{w.coef}</td>
                    <td className="py-2 text-[#77778D] font-mono text-[11px]">[{w.ci_lower}, {w.ci_upper}]</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Ham Drivers */}
        <div className={`bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card transition-all ${
          activeSubTab === 'ham' ? 'ring-2 ring-[#10B981]/20' : ''
        }`}>
          <div className="flex items-center justify-between pb-3 border-b border-gray-100">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-[#10B981]"></span>
              <h3 className="text-[15px] font-bold text-[#19153F]">Top {wordLimit} Ham Drivers (Odds Ratio &lt; 1)</h3>
            </div>
            <span className="text-[11px] text-[#10B981] font-semibold">Lowers Spam Odds</span>
          </div>

          <div className="overflow-x-auto mt-2">
            <table className="w-full text-left text-[12px] border-collapse">
              <thead>
                <tr className="border-b border-gray-100 text-[#77778D] font-medium text-[11px]">
                  <th className="pb-2">Token</th>
                  <th className="pb-2">Odds Ratio ($e^\beta$)</th>
                  <th className="pb-2">Coefficient (β)</th>
                  <th className="pb-2">95% CI</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {wordsData.ham_drivers.map((w, idx) => (
                  <tr key={idx} className="hover:bg-emerald-50/40">
                    <td className="py-2 font-semibold text-[#19153F]">"{w.word}"</td>
                    <td className="py-2">
                      <span className="font-bold text-[#10B981] bg-emerald-50 px-2 py-0.5 rounded font-mono">
                        {w.odds_ratio}x
                      </span>
                    </td>
                    <td className="py-2 text-[#47475A] font-mono">{w.coef}</td>
                    <td className="py-2 text-[#77778D] font-mono text-[11px]">[{w.ci_lower}, {w.ci_upper}]</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
