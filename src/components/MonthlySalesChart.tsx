import React, { useState } from 'react';
import { ChevronDown, ArrowUpRight } from 'lucide-react';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  Tooltip, 
  ResponsiveContainer, 
  ReferenceLine 
} from 'recharts';
import { DAILY_SALES_DATA } from '../data/mockData';

export const MonthlySalesChart: React.FC = () => {
  const [selectedMonth, setSelectedMonth] = useState('January');
  const [activeDay, setActiveDay] = useState(9);
  const [showMonthMenu, setShowMonthMenu] = useState(false);

  const months = ['January', 'February', 'March', 'April', 'May', 'June'];

  const currentDayData = DAILY_SALES_DATA.find(d => d.day === activeDay);

  return (
    <div className="bg-[#F1F5FE] rounded-[14px] p-5 border border-[#DFE7FA] shadow-card flex flex-col justify-between relative overflow-hidden">
      {/* Top Header */}
      <div className="flex items-center justify-between pb-1">
        <h2 className="text-[16px] font-bold text-[#19153F]">Monthly Sales</h2>

        {/* Month Selector Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowMonthMenu(!showMonthMenu)}
            className="flex items-center gap-1.5 bg-white border border-[#E2E8F0] px-2.5 py-1 rounded-lg text-[11.5px] font-semibold text-[#19153F] shadow-xs hover:bg-gray-50 transition-colors"
          >
            <span>{selectedMonth}</span>
            <ChevronDown size={13} className="text-[#77778D]" />
          </button>

          {showMonthMenu && (
            <div className="absolute right-0 top-8 w-32 bg-white border border-[#E6E6EF] shadow-dropdown rounded-xl p-1 z-30 text-[12px] flex flex-col">
              {months.map(m => (
                <button
                  key={m}
                  onClick={() => { setSelectedMonth(m); setShowMonthMenu(false); }}
                  className={`px-2.5 py-1.5 rounded-lg text-left transition-colors ${
                    selectedMonth === m ? 'bg-[#EDE9FE] text-[#6045F5] font-semibold' : 'hover:bg-gray-50 text-[#19153F]'
                  }`}
                >
                  {m}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Main Stats */}
      <div className="mt-1 mb-2">
        <span className="text-[11px] font-medium text-[#77778D]">Total this month</span>
        <div className="flex items-center gap-2 mt-0.5">
          <span className="text-[24px] font-bold text-[#19153F] tracking-tight">$59,690</span>
          <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold bg-[#DCFCE7] text-[#15803D]">
            13.4%
            <ArrowUpRight size={10} className="ml-0.5" />
          </span>
        </div>
      </div>

      {/* Area Chart with Vertical Reference on activeDay */}
      <div className="w-full h-[120px] relative -mx-2">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart 
            data={DAILY_SALES_DATA} 
            margin={{ top: 22, right: 15, left: 15, bottom: 0 }}
          >
            <defs>
              <linearGradient id="salesGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#4C6EF5" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#4C6EF5" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <XAxis dataKey="day" hide domain={[1, 11]} />
            <YAxis hide domain={[30000, 52000]} />
            <Tooltip 
              cursor={false}
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="bg-[#19153F] text-white text-[10.5px] font-bold px-2 py-0.5 rounded shadow-md">
                      ${(payload[0].value as number).toLocaleString()}
                    </div>
                  );
                }
                return null;
              }}
            />
            {/* Vertical Line on activeDay */}
            <ReferenceLine 
              x={activeDay} 
              stroke="#4C6EF5" 
              strokeDasharray="3 3" 
              strokeWidth={1.5} 
            />
            <Area 
              type="monotone" 
              dataKey="sales" 
              stroke="#4C6EF5" 
              strokeWidth={2.2} 
              fillOpacity={1} 
              fill="url(#salesGradient)" 
            />
          </AreaChart>
        </ResponsiveContainer>

        {/* Floating Tooltip Pill over Active Day */}
        <div 
          className="absolute top-0 flex flex-col items-center pointer-events-none transition-all duration-200 z-10"
          style={{ 
            left: `${((activeDay - 1) / 10) * 88 + 6}%`,
            transform: 'translateX(-50%)'
          }}
        >
          <div className="bg-[#19153F] text-white text-[10px] font-bold px-2 py-0.5 rounded shadow-md">
            ${currentDayData ? currentDayData.sales.toLocaleString() : '47,500'}
          </div>
          <div className="w-1.5 h-1.5 rounded-full bg-[#19153F] mt-0.5"></div>
        </div>
      </div>

      {/* Days Selector Row (1 to 11) */}
      <div className="flex items-center justify-between pt-2 border-t border-[#DFE7FA]/80 px-1 text-[11px] font-medium text-[#77778D]">
        {DAILY_SALES_DATA.map((d) => {
          const isSelected = d.day === activeDay;
          return (
            <button
              key={d.day}
              onClick={() => setActiveDay(d.day)}
              className={`w-6 h-6 rounded-md flex items-center justify-center transition-all ${
                isSelected 
                  ? 'bg-[#19153F] text-white font-bold shadow-xs' 
                  : 'hover:text-[#19153F]'
              }`}
            >
              {d.day}
            </button>
          );
        })}
      </div>
    </div>
  );
};
