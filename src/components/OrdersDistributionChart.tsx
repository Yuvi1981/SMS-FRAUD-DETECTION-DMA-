import React, { useState } from 'react';
import { Download, MoreHorizontal } from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  ResponsiveContainer, 
  CartesianGrid 
} from 'recharts';
import { ORDERS_DISTRIBUTION_DATA } from '../data/mockData';

export const OrdersDistributionChart: React.FC = () => {
  const [activeMenu, setActiveMenu] = useState(false);

  // Purple gradient shades matching reference image
  const segments = [
    { key: 'p10', color: '#5A43F5', label: '10%' },
    { key: 'p20', color: '#7E6CF7', label: '20%' },
    { key: 'p40', color: '#A092F9', label: '40%' },
    { key: 'p60', color: '#C5BCFB', label: '60%' },
    { key: 'p80', color: '#E4E0FD', label: '80%' },
  ];

  const handleDownload = () => {
    const csvContent = "data:text/csv;charset=utf-8,Month,10%,20%,40%,60%,80%\n" 
      + ORDERS_DISTRIBUTION_DATA.map(d => `${d.name},${d.p10},${d.p20},${d.p40},${d.p60},${d.p80}`).join("\n");
    const link = document.createElement("a");
    link.href = encodeURI(csvContent);
    link.download = "orders_distribution.csv";
    link.click();
  };

  return (
    <div className="bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card flex flex-col justify-between">
      {/* Header */}
      <div className="flex items-center justify-between pb-2">
        <h2 className="text-[16px] font-bold text-[#19153F]">Orders List</h2>
        
        <div className="flex items-center gap-1 text-[#77778D] relative">
          <button 
            onClick={handleDownload}
            className="p-1.5 hover:bg-gray-100 rounded-lg transition-colors"
            title="Download CSV"
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

          {activeMenu && (
            <div className="absolute right-0 top-8 w-36 bg-white border border-[#E6E6EF] shadow-dropdown rounded-xl p-1.5 z-30 text-[12px] flex flex-col">
              <button 
                onClick={() => { handleDownload(); setActiveMenu(false); }}
                className="px-2.5 py-1.5 hover:bg-gray-50 rounded-lg text-left text-[#19153F]"
              >
                Export CSV
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Stacked Bar Chart */}
      <div className="w-full h-[180px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={ORDERS_DISTRIBUTION_DATA}
            margin={{ top: 15, right: 15, left: -20, bottom: 0 }}
            barSize={40}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F0F0F5" />
            <XAxis 
              dataKey="name" 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#77778D', fontSize: 11, fontWeight: 500 }}
            />
            <YAxis 
              axisLine={false} 
              tickLine={false} 
              ticks={[0, 5, 15, 25, 30]}
              domain={[0, 32]}
              tick={{ fill: '#9E9EA7', fontSize: 10 }}
            />
            <Tooltip 
              cursor={{ fill: 'rgba(96, 69, 245, 0.04)' }}
              content={({ active, payload, label }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="bg-[#19153F] text-white text-[11px] p-2.5 rounded-lg shadow-md space-y-1">
                      <div className="font-semibold border-b border-white/20 pb-1">{label} Distribution</div>
                      {payload.map((entry, idx) => (
                        <div key={idx} className="flex items-center justify-between gap-3 text-[10px]">
                          <span className="flex items-center gap-1.5">
                            <span className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }}></span>
                            <span>{segments[idx]?.label} tier:</span>
                          </span>
                          <span className="font-bold">{entry.value}k orders</span>
                        </div>
                      ))}
                    </div>
                  );
                }
                return null;
              }}
            />
            {/* Stacked Segments */}
            {segments.map((seg, idx) => (
              <Bar 
                key={seg.key} 
                dataKey={seg.key} 
                stackId="ordersStack" 
                fill={seg.color}
                radius={idx === segments.length - 1 ? [4, 4, 0, 0] : [0, 0, 0, 0]}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Legend underneath */}
      <div className="flex items-center justify-center gap-3.5 pt-2 border-t border-gray-50 text-[11px] text-[#77778D] font-medium">
        {segments.map((seg) => (
          <div key={seg.key} className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: seg.color }}></span>
            <span>{seg.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
