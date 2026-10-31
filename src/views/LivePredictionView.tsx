import React, { useState, useEffect } from 'react';
import { 
  Zap, 
  Trash2, 
  CheckCircle, 
  AlertTriangle, 
  HelpCircle, 
  Sparkles,
  Shield,
  Layers,
  Info
} from 'lucide-react';
import { api, PredictResult } from '../services/api';

interface LivePredictionViewProps {
  activeSubTab?: string;
  globalSearch?: string;
}

export const LivePredictionView: React.FC<LivePredictionViewProps> = ({
  activeSubTab = 'classifier',
  globalSearch = ''
}) => {
  const PRESETS = [
    {
      id: 'spam',
      label: '🚨 Example 1: Lottery Spam',
      text: 'WINNER! You have won a guaranteed £1,000 cash prize or a holiday! Call 09061701461 to claim now. Reply STOP to cancel.'
    },
    {
      id: 'ham1',
      label: '💬 Example 2: Study Meetup',
      text: 'Hey, are we still meeting at the library around 4pm to work on the DMA project?'
    },
    {
      id: 'ham2',
      label: '🏡 Example 3: Personal Update',
      text: 'Just arrived home safely, will call you in 10 minutes once I get settled.'
    }
  ];

  const [inputText, setInputText] = useState(PRESETS[0].text);
  const [selectedModel, setSelectedModel] = useState('Logistic Regression');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictResult | null>(null);

  useEffect(() => {
    if (globalSearch && globalSearch.trim()) {
      setInputText(globalSearch.trim());
      handleClassify(globalSearch.trim());
    }
  }, [globalSearch]);

  const handleClassify = async (textToClassify?: string) => {
    const text = textToClassify !== undefined ? textToClassify : inputText;
    if (!text.trim()) return;

    setLoading(true);
    try {
      const res = await api.predict(text, selectedModel);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Run initial classification on mount
  useEffect(() => {
    handleClassify(inputText);
  }, [selectedModel]);

  return (
    <div className="flex flex-col gap-5">
      {/* Top Input & Controls Card */}
      <div className="bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-gray-100">
          <div className="flex items-center gap-2">
            <h2 className="text-[16px] font-bold text-[#19153F]">Interactive SMS Classifier</h2>
            <span className="text-[10px] font-semibold bg-[#DCFCE7] text-[#15803D] px-2 py-0.5 rounded-full flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-[#10B981] animate-pulse"></span>
              Live ML Model Active
            </span>
          </div>

          {/* Model Selector Pill Dropdown */}
          <div className="flex items-center gap-2">
            <span className="text-[11.5px] font-medium text-[#77778D]">Classifier:</span>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="bg-[#F4F4F8] border border-[#E6E6EF] rounded-lg px-2.5 py-1 text-[12px] font-semibold text-[#19153F] focus:outline-none focus:ring-2 focus:ring-[#6045F5]/30 cursor-pointer"
            >
              <option value="Logistic Regression">Logistic Regression (L2)</option>
              <option value="Naive Bayes">Naive Bayes (Multinomial)</option>
              <option value="k-Nearest Neighbors">k-Nearest Neighbors (k=5)</option>
            </select>
          </div>
        </div>

        {/* Quick Example Presets */}
        <div className="mt-3.5">
          <span className="text-[11px] font-semibold text-[#77778D] uppercase tracking-wider block mb-2">
            One-Click Test Presets:
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
            {PRESETS.map((preset) => (
              <button
                key={preset.id}
                onClick={() => {
                  setInputText(preset.text);
                  handleClassify(preset.text);
                }}
                className={`text-left p-2.5 rounded-xl border text-[12px] transition-all flex flex-col justify-between ${
                  inputText === preset.text
                    ? 'border-[#6045F5] bg-[#F4F2FF] text-[#19153F] font-semibold shadow-xs'
                    : 'border-[#E6E6EF] hover:border-gray-300 bg-gray-50 text-[#47475A]'
                }`}
              >
                <span>{preset.label}</span>
                <span className="text-[10px] text-[#77778D] truncate mt-1">"{preset.text.slice(0, 36)}..."</span>
              </button>
            ))}
          </div>
        </div>

        {/* Text Area */}
        <div className="mt-4">
          <div className="flex items-center justify-between text-[11.5px] text-[#77778D] mb-1.5 font-medium">
            <span>Type or paste SMS text to evaluate:</span>
            <span>{inputText.length} characters • {inputText.split(/\s+/).filter(Boolean).length} words</span>
          </div>

          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows={3}
            placeholder="Type or paste any SMS message here..."
            className="w-full bg-[#FAF9FD] border border-[#E6E6EF] rounded-xl p-3 text-[13px] text-[#19153F] placeholder-[#9E9EA7] focus:outline-none focus:ring-2 focus:ring-[#6045F5]/30 focus:border-[#6045F5] transition-all resize-none shadow-xs font-sans"
          />

          <div className="flex items-center justify-between mt-3">
            <button
              onClick={() => {
                setInputText('');
                setResult(null);
              }}
              className="flex items-center gap-1.5 text-[12px] text-[#77778D] hover:text-[#EF4444] transition-colors py-1 px-2 rounded-lg"
            >
              <Trash2 size={13} />
              <span>Clear</span>
            </button>

            <button
              onClick={() => handleClassify()}
              disabled={loading || !inputText.trim()}
              className="flex items-center gap-2 bg-[#6045F5] hover:bg-[#4E34E0] disabled:bg-gray-300 text-white font-semibold text-[13px] px-5 py-2 rounded-xl shadow-sm transition-all"
            >
              <Zap size={15} />
              <span>{loading ? 'Evaluating...' : 'Classify SMS'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Result Card */}
      {result && (
        <div className="bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card">
          <div className="flex items-center justify-between pb-3 border-b border-gray-100">
            <h2 className="text-[16px] font-bold text-[#19153F]">Classification Verdict</h2>
            <span className="text-[11px] text-[#77778D]">Model: {result.model}</span>
          </div>

          {/* Verdict Banner */}
          <div className={`mt-4 p-4 rounded-xl border flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
            result.is_spam 
              ? 'bg-[#FEF2F2] border-[#FCA5A5]' 
              : 'bg-[#F0FDF4] border-[#86EFAC]'
          }`}>
            <div className="flex items-center gap-3">
              <div className={`w-12 h-12 rounded-xl flex items-center justify-center shrink-0 shadow-sm ${
                result.is_spam ? 'bg-[#EF4444] text-white' : 'bg-[#10B981] text-white'
              }`}>
                {result.is_spam ? <AlertTriangle size={24} /> : <CheckCircle size={24} />}
              </div>
              <div className="flex flex-col">
                <span className={`text-[19px] font-bold tracking-tight ${
                  result.is_spam ? 'text-[#B91C1C]' : 'text-[#15803D]'
                }`}>
                  {result.is_spam ? '🚨 SPAM DETECTED' : '✅ HAM (LEGITIMATE)'}
                </span>
                <span className="text-[12px] text-[#47475A]">
                  {result.is_spam 
                    ? `High spam probability detected (${result.probability}% likelihood)`
                    : `Message assessed as legitimate communication (${result.confidence}% confidence)`
                  }
                </span>
              </div>
            </div>

            {/* Probability Progress Gauge */}
            <div className="w-full sm:w-48 flex flex-col gap-1.5 shrink-0">
              <div className="flex items-center justify-between text-[11px] font-semibold text-[#19153F]">
                <span>Spam Probability:</span>
                <span className={result.is_spam ? 'text-[#B91C1C]' : 'text-[#15803D]'}>
                  {result.probability}%
                </span>
              </div>
              <div className="w-full h-2.5 bg-white rounded-full overflow-hidden border border-gray-200">
                <div 
                  className={`h-full rounded-full transition-all duration-500 ${
                    result.is_spam ? 'bg-[#EF4444]' : 'bg-[#10B981]'
                  }`}
                  style={{ width: `${result.probability}%` }}
                />
              </div>
            </div>
          </div>

          {/* Explainability Section ("Why?") */}
          <div className="mt-5 pt-4 border-t border-gray-100">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles size={16} className="text-[#6045F5]" />
              <h3 className="text-[14px] font-bold text-[#19153F]">
                Why did the model decide this? (Odds Ratio Explainability)
              </h3>
            </div>
            <p className="text-[12px] text-[#77778D] mb-3">
              Words extracted from this message are matched to their empirical <strong>Logistic Regression Odds Ratios (exp(β))</strong>. 
              Tokens that multiply spam likelihood appear in <strong className="text-[#EF4444]">red</strong>, while tokens lowering spam likelihood appear in <strong className="text-[#10B981]">green</strong>.
            </p>

            {result.why_chips && result.why_chips.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {result.why_chips.map((chip, idx) => (
                  <div
                    key={idx}
                    className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-[12px] font-semibold transition-all ${
                      chip.direction === 'spam'
                        ? 'bg-[#FEF2F2] border-[#FECACA] text-[#B91C1C]'
                        : 'bg-[#F0FDF4] border-[#BBF7D0] text-[#15803D]'
                    }`}
                  >
                    <span>{chip.word}</span>
                    <span className="text-[10px] px-1.5 py-0.2 rounded-md bg-white shadow-2xs font-mono">
                      {chip.badge}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-[12px] text-[#77778D] italic p-3 bg-gray-50 rounded-lg">
                No high-salience discriminatory tokens were found in this message. Classification relied on general length and unselected feature distribution.
              </div>
            )}
          </div>

          {/* Side-by-Side Model Consensus Table */}
          <div className="mt-5 pt-4 border-t border-gray-100">
            <h3 className="text-[14px] font-bold text-[#19153F] mb-3">
              Side-by-Side Model Consensus
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-[12px] border-collapse">
                <thead>
                  <tr className="border-b border-gray-200 text-[#77778D] font-medium text-[11px]">
                    <th className="pb-2 font-medium">Model</th>
                    <th className="pb-2 font-medium">Verdict</th>
                    <th className="pb-2 font-medium">Spam Probability</th>
                    <th className="pb-2 font-medium">Confidence</th>
                    <th className="pb-2 font-medium">Decision Threshold</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {result.consensus.map((item, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="py-2.5 font-semibold text-[#19153F]">{item.model}</td>
                      <td className="py-2.5">
                        <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold ${
                          item.verdict === 'SPAM' 
                            ? 'bg-red-100 text-red-700' 
                            : 'bg-emerald-100 text-emerald-700'
                        }`}>
                          {item.verdict === 'SPAM' ? '🚨 SPAM' : '✅ HAM'}
                        </span>
                      </td>
                      <td className="py-2.5 font-medium text-[#19153F]">{item.probability}%</td>
                      <td className="py-2.5 font-medium text-[#19153F]">{item.confidence}%</td>
                      <td className="py-2.5 text-[#77778D]">0.50</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
