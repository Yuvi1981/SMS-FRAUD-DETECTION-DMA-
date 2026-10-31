import React from 'react';
import { Star } from 'lucide-react';

export const TotalOrdersSummary: React.FC = () => {
  const avatars = [
    'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80',
    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80',
    'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&auto=format&fit=crop&q=80'
  ];

  return (
    <div className="bg-[#DDE6FF] rounded-[14px] p-4 flex items-center justify-between shadow-sm transition-transform duration-200 hover:-translate-y-0.5">
      {/* Left: Star Icon & Titles */}
      <div className="flex items-center gap-3">
        {/* White Rounded Square Icon Box */}
        <div className="w-10 h-10 rounded-xl bg-white flex items-center justify-center text-[#4C6EF5] shadow-xs shrink-0">
          <Star size={18} fill="#4C6EF5" stroke="none" />
        </div>

        <div className="flex flex-col">
          <span className="text-[14px] font-bold text-[#19153F] leading-tight">Total Orders</span>
          <span className="text-[11px] text-[#77778D] font-medium mt-0.5">Sep 01 to Oct 01, 2023</span>
        </div>
      </div>

      {/* Right: Overlapping Avatars */}
      <div className="flex items-center -space-x-2 shrink-0 pr-1">
        {avatars.map((url, idx) => (
          <img
            key={idx}
            src={url}
            alt="Customer avatar"
            className="w-7 h-7 rounded-full object-cover border-2 border-[#DDE6FF] shadow-xs"
          />
        ))}
      </div>
    </div>
  );
};
