import React from 'react';
import { ArrowUpRight } from 'lucide-react';
import { KpiData } from '../types';

interface KpiCardProps {
  data: KpiData;
}

export const KpiCard: React.FC<KpiCardProps> = ({ data }) => {
  // Styles based on colorType
  const colorMap = {
    blue: {
      bg: 'bg-[#DDE6FF]',
      stroke: '#4C6EF5',
      badgeBg: 'bg-white/80',
      badgeText: 'text-[#4C6EF5]'
    },
    pink: {
      bg: 'bg-[#F9E1E4]',
      stroke: '#F06595',
      badgeBg: 'bg-white/80',
      badgeText: 'text-[#E03131]'
    },
    mint: {
      bg: 'bg-[#DCEFEB]',
      stroke: '#20C997',
      badgeBg: 'bg-white/80',
      badgeText: 'text-[#0CA678]'
    }
  };

  const style = colorMap[data.colorType];

  // Generate SVG path for sparkline
  const width = 80;
  const height = 36;
  const min = Math.min(...data.sparkline);
  const max = Math.max(...data.sparkline);
  const range = max - min || 1;

  const points = data.sparkline.map((val, idx) => {
    const x = (idx / (data.sparkline.length - 1)) * width;
    const y = height - ((val - min) / range) * (height - 8) - 4;
    return `${x},${y}`;
  }).join(' ');

  return (
    <div className={`${style.bg} rounded-[14px] p-4 flex flex-col justify-between h-[120px] transition-transform duration-200 hover:-translate-y-0.5 shadow-sm relative overflow-hidden group`}>
      {/* Top Header: Label & Sparkline */}
      <div className="flex items-start justify-between">
        <span className="text-[12px] font-medium text-[#77778D]">{data.label}</span>
        
        {/* SVG Sparkline */}
        <div className="w-20 h-9 shrink-0 flex items-center justify-end">
          <svg width={width} height={height} className="overflow-visible">
            <polyline
              fill="none"
              stroke={style.stroke}
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              points={points}
              className="opacity-80 group-hover:opacity-100 transition-opacity"
            />
          </svg>
        </div>
      </div>

      {/* Main Metric Value */}
      <div className="text-[24px] font-bold text-[#19153F] tracking-tight leading-none mt-1">
        {data.value}
      </div>

      {/* Comparison Text */}
      <div className="flex items-center gap-1.5 text-[11px] text-[#77778D] font-medium">
        <span>Since last week</span>
        <span className={`inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold ${style.badgeBg} ${style.badgeText} shadow-xs`}>
          {data.change}
          <ArrowUpRight size={10} className="ml-0.5" />
        </span>
      </div>
    </div>
  );
};
