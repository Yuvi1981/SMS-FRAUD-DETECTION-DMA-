export interface OrderItem {
  num: number;
  customer: {
    name: string;
    avatar: string;
    initials: string;
  };
  orderNumber: string;
  cost: number;
  dueDate: string;
  rating: number;
  status: 'Completed' | 'Pending' | 'Canceled';
}

export interface KpiData {
  id: string;
  label: string;
  value: string;
  change: string;
  changePositive: boolean;
  colorType: 'blue' | 'pink' | 'mint';
  sparkline: number[];
}

export interface MonthlyBarData {
  month: string;
  short: string;
  value: number;
  isHighlighted?: boolean;
}

export interface DistributionSegment {
  name: string;
  p10: number;
  p20: number;
  p40: number;
  p60: number;
  p80: number;
}

export interface DailySalesPoint {
  day: number;
  sales: number;
  highlighted?: boolean;
}
