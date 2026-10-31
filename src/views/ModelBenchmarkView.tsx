import React, { useState, useEffect } from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  ResponsiveContainer, 
  CartesianGrid, 
  Cell 
} from 'recharts';
import { Trophy, CheckCircle, Clock, ShieldCheck, Zap } from 'lucide-react';
import { api } from '../services/api';

interface ModelBenchmarkViewProps {
  activeSubTab?: string;
}

export const ModelBenchmarkView: React.FC<ModelBenchmarkViewProps> = ({ activeSubTab = 'benchmark' }) => {
  const [selectedMetric, setSelectedMetric] = useState<'F1' | 'Precision' | 'Recall' | 'ROC-AUC' | 'Accuracy'>('F1');
  const [modelsData, setModelsData] = useState<any[]>([
    { model: 'Logistic Regression (L2 Balanced)', short: 'LogReg', F1: 0.9653, Precision: 0.9766, Recall: 0.9542, 'ROC-AUC': 0.9971, Accuracy: 0.9913, latency: 1.18, color: '#6045F5' },
    { model: 'Naive Bayes (Multinomial)', short: 'NaiveBayes', F1: 0.9375, Precision: 0.9600, Recall: 0.9160, 'ROC-AUC': 0.9954, Accuracy: 0.9845, latency: 1.64, color: '#10B981' },
    { model: 'k-Nearest Neighbors (k=5)', short: 'k-NN', F1: 0.8988, Precision: 0.9569, Recall: 0.8473, 'ROC-AUC': 0.9869, Accuracy: 0.9758, latency: 191.13, color: '#F59E0B' },
    { model: 'Bayesian Network (TAN/Naive)', short: 'BayesNet', F1: 0.8988, Precision: 0.9569, Recall: 0.8473, 'ROC-AUC': 0.9791, Accuracy: 0.9758, latency: 261.57, color: '#30265F' },
  ]);

  useEffect(() => {
    api.getModels().then(res => {
      if (res && res.comparison_table && res.comparison_table.length > 0) {
        const mapped = res.comparison_table.map((m: any) => {
          let short = 'Model';
          let color = '#6045F5';
          if (m.Model.includes('Logistic')) {
            short = 'LogReg';
            color = '#6045F5';
          } else if (m.Model.includes('Bayesian')) {
            short = 'BayesNet';
            color = '#30265F';
          } else if (m.Model.includes('Naive')) {
            short = 'NaiveBayes';
            color = '#10B981';
          } else if (m.Model.includes('k-Nearest') || m.Model.includes('k-NN') || m.Model.includes('KNN')) {
            short = 'k-NN';
            color = '#F59E0B';
          }

          const cleanNum = (v: any) => {
            if (typeof v === 'number') return v;
            return parseFloat(String(v).replace(/[^\d.-]/g, '')) || 0;
          };

          return {
            model: m.Model,
            short,
            F1: cleanNum(m.F1),
            Precision: cleanNum(m.Precision),
            Recall: cleanNum(m.Recall),
            'ROC-AUC': cleanNum(m['ROC-AUC']),
            Accuracy: cleanNum(m.Accuracy),
            latency: cleanNum(m['Prediction Time (ms/1k)']),
            color
          };
        });

        // Ensure champion (Logistic Regression) is sorted first
        mapped.sort((a: any, b: any) => b.F1 - a.F1);
        setModelsData(mapped);
      }
    });
  }, []);

  return (
    <div className="flex flex-col gap-5">
      {/* Benchmark Table Card */}
      <div className={`bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card transition-all ${
        activeSubTab === 'benchmark' ? 'ring-2 ring-[#6045F5]/20' : ''
      }`}>
        <div className="flex items-center justify-between pb-3 border-b border-gray-100">
          <div>
            <h2 className="text-[16px] font-bold text-[#19153F]">Cross-Model Benchmark (Test Split)</h2>
            <p className="text-[11.5px] text-[#77778D] mt-0.5">Identical stratified 20% holdout test evaluation (1,034 messages)</p>
          </div>
          <span className="text-[11px] font-semibold bg-[#EDE9FE] text-[#6045F5] px-2.5 py-0.5 rounded-full">
            Zero Data Leakage
          </span>
        </div>

        <div className="overflow-x-auto mt-3">
          <table className="w-full text-left text-[12.5px] border-collapse">
            <thead>
              <tr className="border-b border-gray-200 text-[#77778D] font-medium text-[11px]">
                <th className="pb-2">Model Architecture</th>
                <th className="pb-2">Accuracy</th>
                <th className="pb-2">Precision</th>
                <th className="pb-2">Recall</th>
                <th className="pb-2">F1-Score</th>
                <th className="pb-2">ROC-AUC</th>
                <th className="pb-2">Latency (ms/1k)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {modelsData.map((m, idx) => (
                <tr key={idx} className={`hover:bg-gray-50 ${idx === 0 ? 'bg-[#F9F8FE]' : ''}`}>
                  <td className="py-3 font-semibold text-[#19153F] flex items-center gap-1.5">
                    {idx === 0 && <Trophy size={14} className="text-[#6045F5]" />}
                    <span>{m.model}</span>
                  </td>
                  <td className="py-3 font-medium text-[#19153F]">{m.Accuracy.toFixed(4)}</td>
                  <td className="py-3 font-medium text-[#19153F]">{m.Precision.toFixed(4)}</td>
                  <td className="py-3 font-medium text-[#19153F]">{m.Recall.toFixed(4)}</td>
                  <td className="py-3 font-bold text-[#6045F5]">{m.F1.toFixed(4)}</td>
                  <td className="py-3 font-medium text-[#19153F]">{m['ROC-AUC'].toFixed(4)}</td>
                  <td className="py-3 text-[#77778D] font-mono">{m.latency} ms</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Visualizer & Champion Rationale */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        {/* Metric Comparison Chart */}
        <div className={`lg:col-span-7 bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card transition-all ${
          activeSubTab === 'visualizer' ? 'ring-2 ring-[#6045F5]/20' : ''
        }`}>
          <div className="flex items-center justify-between pb-3 border-b border-gray-100">
            <h3 className="text-[15px] font-bold text-[#19153F]">Metric Comparison Visualizer</h3>
            <div className="flex items-center gap-2">
              <span className="text-[11.5px] text-[#77778D] font-medium">Metric:</span>
              <select
                value={selectedMetric}
                onChange={(e) => setSelectedMetric(e.target.value as any)}
                className="bg-[#F4F4F8] border border-[#E6E6EF] rounded-lg px-2.5 py-1 text-[12px] font-semibold text-[#19153F] cursor-pointer"
              >
                <option value="F1">F1-Score (Spam Target)</option>
                <option value="Precision">Precision</option>
                <option value="Recall">Recall</option>
                <option value="ROC-AUC">ROC-AUC</option>
                <option value="Accuracy">Accuracy</option>
              </select>
            </div>
          </div>

          <div className="w-full h-[220px] mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={modelsData} margin={{ top: 15, right: 15, left: -15, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F0F0F5" />
                <XAxis dataKey="short" tick={{ fill: '#77778D', fontSize: 11 }} />
                <YAxis domain={[0.75, 1.0]} tick={{ fill: '#9E9EA7', fontSize: 11 }} />
                <Tooltip 
                  content={({ active, payload, label }) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="bg-[#19153F] text-white text-[11px] p-2 rounded-md shadow-md">
                          <div className="font-bold border-b border-white/20 pb-1">{label}</div>
                          <div className="text-purple-300 mt-1">{selectedMetric}: {payload[0]?.value}</div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Bar dataKey={selectedMetric} radius={[6, 6, 0, 0]}>
                  {modelsData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Champion Rationale Card */}
        <div className={`lg:col-span-5 bg-[#FAF9FD] rounded-[14px] p-5 border border-[#E6E6EF] shadow-card transition-all ${
          activeSubTab === 'rationale' ? 'ring-2 ring-[#6045F5]/20' : ''
        }`}>
          <div className="flex items-center gap-2 mb-3">
            <div className="w-8 h-8 rounded-xl bg-[#6045F5] text-white flex items-center justify-center shadow-xs">
              <Trophy size={16} />
            </div>
            <div>
              <h3 className="text-[14.5px] font-bold text-[#19153F]">Champion Selection Rationale</h3>
              <span className="text-[11px] text-[#6045F5] font-semibold">Logistic Regression (L2 Balanced)</span>
            </div>
          </div>

          <div className="space-y-3 text-[12px] text-[#47475A] leading-relaxed mt-3">
            <div className="p-2.5 bg-white rounded-xl border border-gray-100 shadow-2xs">
              <strong className="text-[#19153F] block mb-0.5">🏆 Highest F1-Score (0.9653):</strong>
              Maximizes spam detection while keeping false positive rate under 0.8% on legitimate ham messages.
            </div>

            <div className="p-2.5 bg-white rounded-xl border border-gray-100 shadow-2xs">
              <strong className="text-[#19153F] block mb-0.5">🔍 Mathematical Interpretability:</strong>
              Coefficients directly correspond to word-level odds ratios (exp(β)), enabling transparent human auditing.
            </div>

            <div className="p-2.5 bg-white rounded-xl border border-gray-100 shadow-2xs">
              <strong className="text-[#19153F] block mb-0.5">⚡ 160× Faster Than k-NN:</strong>
              Evaluates 1,000 predictions in just 1.18 milliseconds, making it suitable for live telecom gateway workloads.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
