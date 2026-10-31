import React, { useState } from 'react';
import { Filter, Download, MoreHorizontal, Star } from 'lucide-react';
import { ORDERS_TABLE_DATA } from '../data/mockData';
import { OrderItem } from '../types';

interface OrdersTableProps {
  searchQuery?: string;
}

export const OrdersTable: React.FC<OrdersTableProps> = ({ searchQuery = '' }) => {
  const [statusFilter, setStatusFilter] = useState<'All' | 'Completed' | 'Pending' | 'Canceled'>('All');
  const [showFilterMenu, setShowFilterMenu] = useState(false);
  const [showMoreMenu, setShowMoreMenu] = useState(false);

  // Filter items based on search and status
  const filteredOrders = ORDERS_TABLE_DATA.filter((order) => {
    const matchesStatus = statusFilter === 'All' || order.status === statusFilter;
    const matchesSearch = !searchQuery.trim() || 
      order.customer.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      order.orderNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
      order.dueDate.toLowerCase().includes(searchQuery.toLowerCase()) ||
      order.status.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  const handleExportCSV = () => {
    const headers = ["Num,Customer,Order Number,Cost,Due Date,Rating,Status"];
    const rows = filteredOrders.map(o => 
      `${o.num},"${o.customer.name}",${o.orderNumber},${o.cost},"${o.dueDate}",${o.rating},${o.status}`
    );
    const csvString = "data:text/csv;charset=utf-8," + headers.concat(rows).join("\n");
    const link = document.createElement("a");
    link.href = encodeURI(csvString);
    link.download = `orders_list_${new Date().toISOString().slice(0,10)}.csv`;
    link.click();
  };

  const getStatusBadge = (status: OrderItem['status']) => {
    switch (status) {
      case 'Completed':
        return (
          <span className="inline-flex items-center gap-1.5 text-[11.5px] font-semibold text-[#10B981]">
            <span className="w-1.5 h-1.5 rounded-full bg-[#10B981]"></span>
            <span>Completed</span>
          </span>
        );
      case 'Pending':
        return (
          <span className="inline-flex items-center gap-1.5 text-[11.5px] font-semibold text-[#F59E0B]">
            <span className="w-1.5 h-1.5 rounded-full bg-[#F59E0B]"></span>
            <span>Pending</span>
          </span>
        );
      case 'Canceled':
        return (
          <span className="inline-flex items-center gap-1.5 text-[11.5px] font-semibold text-[#EF4444]">
            <span className="w-1.5 h-1.5 rounded-full bg-[#EF4444]"></span>
            <span>Canceled</span>
          </span>
        );
    }
  };

  return (
    <div className="bg-white rounded-[14px] p-5 border border-[#E6E6EF] shadow-card">
      {/* Header */}
      <div className="flex items-center justify-between pb-3">
        <div className="flex items-center gap-2">
          <h2 className="text-[16px] font-bold text-[#19153F]">Orders List</h2>
          {statusFilter !== 'All' && (
            <span className="text-[10px] font-semibold bg-[#EDE9FE] text-[#6045F5] px-2 py-0.5 rounded-full">
              Filtered: {statusFilter}
            </span>
          )}
        </div>

        <div className="flex items-center gap-1 text-[#77778D] relative">
          {/* Filter Popover */}
          <div className="relative">
            <button 
              onClick={() => setShowFilterMenu(!showFilterMenu)}
              className={`p-1.5 rounded-lg transition-colors ${
                showFilterMenu || statusFilter !== 'All' ? 'bg-[#EDE9FE] text-[#6045F5]' : 'hover:bg-gray-100'
              }`}
              title="Filter by status"
            >
              <Filter size={15} />
            </button>

            {showFilterMenu && (
              <div className="absolute right-0 top-8 w-36 bg-white border border-[#E6E6EF] shadow-dropdown rounded-xl p-1.5 z-30 text-[12px] flex flex-col">
                <span className="text-[10px] font-bold text-[#77778D] px-2 py-1 uppercase tracking-wider">Status</span>
                {(['All', 'Completed', 'Pending', 'Canceled'] as const).map(st => (
                  <button
                    key={st}
                    onClick={() => { setStatusFilter(st); setShowFilterMenu(false); }}
                    className={`px-2.5 py-1.5 rounded-lg text-left transition-colors flex items-center justify-between ${
                      statusFilter === st ? 'bg-[#F4F2FF] text-[#6045F5] font-semibold' : 'hover:bg-gray-50 text-[#19153F]'
                    }`}
                  >
                    <span>{st}</span>
                    {statusFilter === st && <span className="w-1.5 h-1.5 rounded-full bg-[#6045F5]"></span>}
                  </button>
                ))}
              </div>
            )}
          </div>

          <button 
            onClick={handleExportCSV}
            className="p-1.5 hover:bg-gray-100 rounded-lg transition-colors"
            title="Download table CSV"
          >
            <Download size={15} />
          </button>

          <button 
            onClick={() => setShowMoreMenu(!showMoreMenu)}
            className="p-1.5 hover:bg-gray-100 rounded-lg transition-colors"
            title="More table actions"
          >
            <MoreHorizontal size={15} />
          </button>

          {showMoreMenu && (
            <div className="absolute right-0 top-8 w-40 bg-white border border-[#E6E6EF] shadow-dropdown rounded-xl p-1.5 z-30 text-[12px] flex flex-col">
              <button 
                onClick={() => { handleExportCSV(); setShowMoreMenu(false); }}
                className="px-2.5 py-1.5 hover:bg-gray-50 rounded-lg text-left text-[#19153F]"
              >
                Export all as CSV
              </button>
              <button 
                onClick={() => { setStatusFilter('All'); setShowMoreMenu(false); }}
                className="px-2.5 py-1.5 hover:bg-gray-50 rounded-lg text-left text-[#19153F]"
              >
                Reset filters
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Table Container */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-[12.5px] border-collapse">
          <thead>
            <tr className="border-b border-[#F0F0F5] text-[#77778D] font-medium text-[11px]">
              <th className="pb-2.5 pt-1 font-medium w-12 text-center">Num</th>
              <th className="pb-2.5 pt-1 font-medium">Customer</th>
              <th className="pb-2.5 pt-1 font-medium">Order</th>
              <th className="pb-2.5 pt-1 font-medium">Cost</th>
              <th className="pb-2.5 pt-1 font-medium">Due Date</th>
              <th className="pb-2.5 pt-1 font-medium">Rating</th>
              <th className="pb-2.5 pt-1 font-medium">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#F4F4F8]">
            {filteredOrders.length > 0 ? (
              filteredOrders.map((order) => (
                <tr key={order.num} className="hover:bg-[#FAF9FD] transition-colors group">
                  {/* Number Circle */}
                  <td className="py-2.5 text-center">
                    <span className="w-5 h-5 rounded-full border border-[#E2E2EA] text-[#77778D] inline-flex items-center justify-center text-[10.5px] font-medium group-hover:border-[#6045F5] group-hover:text-[#6045F5] transition-colors">
                      {order.num}
                    </span>
                  </td>

                  {/* Customer Avatar & Name */}
                  <td className="py-2.5">
                    <div className="flex items-center gap-2.5">
                      <img 
                        src={order.customer.avatar} 
                        alt={order.customer.name}
                        className="w-6 h-6 rounded-full object-cover border border-gray-100"
                        onError={(e) => {
                          // Fallback to initials
                          (e.target as HTMLElement).style.display = 'none';
                        }}
                      />
                      <span className="font-semibold text-[#19153F]">{order.customer.name}</span>
                    </div>
                  </td>

                  {/* Order Number Tag */}
                  <td className="py-2.5">
                    <span className="inline-block bg-[#F0EEFF] text-[#6045F5] text-[11px] font-semibold px-2 py-0.5 rounded-md">
                      {order.orderNumber}
                    </span>
                  </td>

                  {/* Cost */}
                  <td className="py-2.5 font-semibold text-[#19153F]">
                    ${order.cost.toFixed(2)}
                  </td>

                  {/* Due Date */}
                  <td className="py-2.5 text-[#77778D] font-medium text-[11.5px]">
                    {order.dueDate}
                  </td>

                  {/* Rating Stars */}
                  <td className="py-2.5">
                    <div className="flex items-center gap-0.5 text-[#F59E0B]">
                      {Array.from({ length: 5 }).map((_, i) => (
                        <Star 
                          key={i} 
                          size={11} 
                          fill={i < order.rating ? '#F59E0B' : '#E5E7EB'} 
                          stroke="none"
                        />
                      ))}
                    </div>
                  </td>

                  {/* Status */}
                  <td className="py-2.5">
                    {getStatusBadge(order.status)}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={7} className="text-center py-6 text-gray-400 text-xs">
                  No orders match your filter criteria.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
