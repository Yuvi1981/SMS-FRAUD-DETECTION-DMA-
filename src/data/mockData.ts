import { OrderItem, KpiData, MonthlyBarData, DistributionSegment, DailySalesPoint } from '../types';

export const KPI_DATA: KpiData[] = [
  {
    id: 'sales',
    label: 'Total sales',
    value: '$59,690',
    change: '13.4%',
    changePositive: true,
    colorType: 'blue',
    sparkline: [35, 42, 38, 55, 46, 68, 62, 75, 70, 85]
  },
  {
    id: 'orders',
    label: 'Total Orders',
    value: '4,865',
    change: '13.4%',
    changePositive: true,
    colorType: 'pink',
    sparkline: [30, 48, 36, 62, 45, 58, 52, 68, 60, 78]
  },
  {
    id: 'customers',
    label: 'Total Customers',
    value: '2,245',
    change: '13.4%',
    changePositive: true,
    colorType: 'mint',
    sparkline: [25, 38, 42, 36, 58, 50, 65, 59, 72, 80]
  }
];

export const SALES_REPORT_12M: MonthlyBarData[] = [
  { month: 'January', short: 'Jan', value: 24500 },
  { month: 'February', short: 'Feb', value: 29000 },
  { month: 'March', short: 'Mar', value: 37500 },
  { month: 'April', short: 'Apr', value: 32000 },
  { month: 'May', short: 'May', value: 52000 },
  { month: 'June', short: 'Jun', value: 28000 },
  { month: 'July', short: 'Jul', value: 43000 },
  { month: 'August', short: 'Aug', value: 36000 },
  { month: 'September', short: 'Sep', value: 47500, isHighlighted: true },
  { month: 'October', short: 'Oct', value: 34500 },
  { month: 'November', short: 'Nov', value: 38000 },
  { month: 'December', short: 'Dec', value: 42000 }
];

export const SALES_REPORT_6M: MonthlyBarData[] = [
  { month: 'July', short: 'Jul', value: 43000 },
  { month: 'August', short: 'Aug', value: 36000 },
  { month: 'September', short: 'Sep', value: 47500, isHighlighted: true },
  { month: 'October', short: 'Oct', value: 34500 },
  { month: 'November', short: 'Nov', value: 38000 },
  { month: 'December', short: 'Dec', value: 42000 }
];

export const SALES_REPORT_30D: MonthlyBarData[] = [
  { month: 'Week 1', short: 'W1', value: 38000 },
  { month: 'Week 2', short: 'W2', value: 42000 },
  { month: 'Week 3', short: 'W3', value: 47500, isHighlighted: true },
  { month: 'Week 4', short: 'W4', value: 39000 }
];

export const SALES_REPORT_7D: MonthlyBarData[] = [
  { month: 'Mon', short: 'Mon', value: 5400 },
  { month: 'Tue', short: 'Tue', value: 6200 },
  { month: 'Wed', short: 'Wed', value: 7100 },
  { month: 'Thu', short: 'Thu', value: 6800 },
  { month: 'Fri', short: 'Fri', value: 9200, isHighlighted: true },
  { month: 'Sat', short: 'Sat', value: 8100 },
  { month: 'Sun', short: 'Sun', value: 5900 }
];

export const ORDERS_DISTRIBUTION_DATA: DistributionSegment[] = [
  {
    name: 'January',
    p10: 5,
    p20: 7,
    p40: 6,
    p60: 5,
    p80: 4
  },
  {
    name: 'February',
    p10: 4,
    p20: 6,
    p40: 8,
    p60: 4,
    p80: 5
  }
];

export const ORDERS_TABLE_DATA: OrderItem[] = [
  {
    num: 1,
    customer: {
      name: 'John C.',
      avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80',
      initials: 'JC'
    },
    orderNumber: '#5845-12',
    cost: 97.50,
    dueDate: '7 Feb,2023',
    rating: 5,
    status: 'Completed'
  },
  {
    num: 2,
    customer: {
      name: 'Matthew K.',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80',
      initials: 'MK'
    },
    orderNumber: '#4734-01',
    cost: 79.90,
    dueDate: '6 Feb,2023',
    rating: 4,
    status: 'Pending'
  },
  {
    num: 3,
    customer: {
      name: 'Dontai G.',
      avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop&q=80',
      initials: 'DG'
    },
    orderNumber: '#6956-23',
    cost: 80.40,
    dueDate: '5 Feb,2023',
    rating: 5,
    status: 'Canceled'
  }
];

export const DAILY_SALES_DATA: DailySalesPoint[] = [
  { day: 1, sales: 36000 },
  { day: 2, sales: 38500 },
  { day: 3, sales: 37000 },
  { day: 4, sales: 42000 },
  { day: 5, sales: 40500 },
  { day: 6, sales: 43000 },
  { day: 7, sales: 41000 },
  { day: 8, sales: 44500 },
  { day: 9, sales: 47500, highlighted: true },
  { day: 10, sales: 43800 },
  { day: 11, sales: 46200 }
];
