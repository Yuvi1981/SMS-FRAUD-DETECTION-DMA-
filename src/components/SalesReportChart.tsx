import React, { useState } from 'react';
import { Download, MoreHorizontal, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  ResponsiveContainer, 
  ReferenceLine, 
  Cell 
} from 'recharts';
import { 
  SALES_REPORT_12M, 
  SALES_REPORT_6M, 
  SALES_REPORT_30D, 
  SALES_REPORT_7D 
} from '../data/mockData';
import { MonthlyBarData } from '../types';

export const SalesReportChart: React.FC = () => {
  const [period, setPeriod] = useState<'12M' | '6M' | '30D' | '7D'>('12M');
  const [activeMenu, setActiveMenu] = useState(false);

  const dataMap: Record<string, MonthlyBarData[]> = {
    '12M': SALES_REPORT_12M,
    '6M': SALES_REPORT_6M,
    '30D': SALES_REPORT_30D,
    '7D': SALES_REPORT_7D
  };

  const currentData = dataMap[period];

  const handleDownloadCSV = () => {
    const csvContent = "data:text/csv;charset=utf-8," 
      + ["Month,Sales"].concat(currentData.map(d => `${d.month},${d.value}`)).join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `sales_report_${period}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card flex flex-col justify-between">
      {/* Card Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3">
        <h2 className="text-[16px] font-bold text-[#19153F]">Sales Report</h2>

        <div className="flex items-center gap-2">
          {/* Time Filter Pills */}
          <div className="flex items-center bg-[#F4F4F8] p-1 rounded-lg text-[11px] font-medium text-[#77778D]">
            {(['12M', '6M', '30D', '7D'] as const).map((p) => {
              const labelMap = { '12M': '12 Months', '6M': '6 Months', '30D': '30 Days', '7D': '7 Days' };
              const isActive = period === p;
              return (
                <button
                  key={p}
                  onClick={() => setPeriod(p)}
                  className={`px-2.5 py-1 rounded-md transition-all ${
                    isActive 
                      ? 'bg-white text-[#19153F] font-semibold shadow-xs' 
                      : 'hover:text-[#19153F]'
                  }`}
                >
                  {labelMap[p]}
                </button>
              );
            })}
          </div>

          {/* Action Icons */}
          <div className="flex items-center gap-1 text-[#77778D] relative">
            <button 
              onClick={handleDownloadCSV}
              className="p-1.5 hover:bg-gray-100 rounded-lg transition-colors"
              title="Download Report CSV"
            >
              <Download size={15} />
            </button>
            <button 
              onClick={() => setActiveMenu(!activeMenu)}
              className="p-1.5 hover:bg-gray-100 rounded-lg transition-colors"
              title="More options"
            >
              <MoreHorizontal size={15} />
            </button>

            {/* Quick Context Menu */}
            {activeMenu && (
              <div className="absolute right-0 top-8 w-40 bg-white border border-[#E6E6EF] shadow-dropdown rounded-xl p-1.5 z-30 text-[12px] flex flex-col">
                <button 
                  onClick={() => { handleDownloadCSV(); setActiveMenu(false); }}
                  className="px-2.5 py-1.5 hover:bg-gray-50 rounded-lg text-left text-[#19153F]"
                >
                  Export as CSV
                </button>
                <button 
                  onClick={() => { window.print(); setActiveMenu(false); }}
                  className="px-2.5 py-1.5 hover:bg-gray-50 rounded-lg text-left text-[#19153F]"
                >
                  Print Report
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main Statistics Row */}
      <div className="flex flex-col mt-1 mb-3">
        <span className="text-[11px] font-medium text-[#77778D]">Avg. per month</span>
        <div className="flex items-center gap-2 mt-0.5">
          <span className="text-[24px] font-bold text-[#19153F] tracking-tight">$38,500</span>
          <div className="flex items-center">
            <span className="w-0 h-0 border-l-[4px] border-l-transparent border-r-[4px] border-r-transparent border-b-[6px] border-b-[#10B981] mr-1"></span>
            <span className="w-0 h-0 border-l-[4px] border-l-transparent border-r-[4px] border-r-transparent border-t-[6px] border-t-[#EF4444]"></span>
          </div>
        </div>

        {/* Median Reference Label directly under stats matching reference */}
        <div className="flex items-center gap-1.5 text-[11px] font-medium text-[#77778D] mt-2">
          <span className="w-1.5 h-1.5 rounded-full bg-[#EF4444]"></span>
          <span>Median $45,000</span>
        </div>
      </div>

      {/* Bar Chart Container */}
      <div className="w-full h-[180px] relative">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart 
            data={currentData} 
            margin={{ top: 28, right: 10, left: 0, bottom: 0 }}
            barSize={currentData.length > 7 ? 22 : 32}
          >
            <XAxis 
              dataKey="short" 
              axisLine={false} 
              tickLine={false} 
              interval={0}
              tick={({ x, y, payload }) => {
                const isSep = payload.value === 'Sep';
                return (
                  <g transform={`translate(${x},${y + 4})`}>
                    {isSep ? (
                      <>
                        <rect x="-14" y="2" width="28" height="18" rx="5" fill="#19153F" />
                        <text x="0" y="15" textAnchor="middle" fill="#FFFFFF" fontSize="10" fontWeight="600">
                          {payload.value}
                        </text>
                      </>
                    ) : (
                      <text x="0" y="14" textAnchor="middle" fill="#77778D" fontSize="11" fontWeight="500">
                        {payload.value}
                      </text>
                    )}
                  </g>
                );
              }}
            />
            <YAxis hide domain={[0, 60000]} />
            <Tooltip 
              cursor={{ fill: 'rgba(96, 69, 245, 0.04)' }}
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="bg-[#19153F] text-white text-[11px] font-semibold px-2.5 py-1 rounded-md shadow-md">
                      ${(payload[0].value as number).toLocaleString()}
                    </div>
                  );
                }
                return null;
              }}
            />
            
            {/* Dashed Median Line */}
            <ReferenceLine 
              y={45000} 
              stroke="#F87171" 
              strokeDasharray="4 4" 
              strokeWidth={1.5} 
            />

            <Bar 
              dataKey="value" 
              radius={[6, 6, 0, 0]}
            >
              {currentData.map((entry, index) => {
                const isHighlight = entry.isHighlighted || entry.short === 'Sep';
                return (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={isHighlight ? '#5A43F5' : '#DDE1FA'} 
                  />
                );
              })}
            </Bar>
          </BarChart>
        </ResponsiveContainer>

        {/* Callout Tooltip Pin permanently positioned above September in 12M view */}
        {period === '12M' && (
          <div className="absolute top-0 left-[70.8%] -translate-x-1/2 flex flex-col items-center pointer-events-none z-10">
            <div className="bg-[#19153F] text-white text-[10px] font-bold px-2 py-0.5 rounded shadow-md">
              $47,500
            </div>
            {/* Pin pointer & ring */}
            <div className="w-[1.5px] h-2.5 bg-[#19153F]"></div>
            <div className="w-2 h-2 rounded-full border-[1.5px] border-[#19153F] bg-white -mt-0.5"></div>
          </div>
        )}
      </div>
    </div>
  );
};
