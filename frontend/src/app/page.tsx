import { AlertTriangle, Truck, PackageX, TrendingUp, LineChart } from 'lucide-react';

export default function Dashboard() {
  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      
      {/* Urgent Alerts Section */}
      <div>
        <h2 className="text-xl font-semibold mb-4">What needs my attention right now?</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          
          {/* Alert Card 1 */}
          <div className="bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900 p-4 rounded-xl flex flex-col items-center text-center">
            <AlertTriangle className="text-red-500 dark:text-red-400 mb-2 h-8 w-8" />
            <span className="text-2xl font-bold text-red-600 dark:text-red-400">7</span>
            <span className="text-sm font-medium text-red-800 dark:text-red-200 mt-1">Products Approaching Stockout</span>
          </div>

          {/* Alert Card 2 */}
          <div className="bg-orange-50 dark:bg-orange-950/20 border border-orange-200 dark:border-orange-900 p-4 rounded-xl flex flex-col items-center text-center">
            <Truck className="text-orange-500 dark:text-orange-400 mb-2 h-8 w-8" />
            <span className="text-2xl font-bold text-orange-600 dark:text-orange-400">3</span>
            <span className="text-sm font-medium text-orange-800 dark:text-orange-200 mt-1">Suppliers with High Delay Risk</span>
          </div>

          {/* Alert Card 3 */}
          <div className="bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 p-4 rounded-xl flex flex-col items-center text-center">
            <PackageX className="text-gray-400 dark:text-zinc-500 mb-2 h-8 w-8" />
            <span className="text-2xl font-bold">12</span>
            <span className="text-sm font-medium text-gray-500 dark:text-zinc-400 mt-1">Dead Stock Items Detected</span>
          </div>

          {/* Alert Card 4 */}
          <div className="bg-green-50 dark:bg-green-950/20 border border-green-200 dark:border-green-900 p-4 rounded-xl flex flex-col items-center text-center">
            <TrendingUp className="text-green-500 dark:text-green-400 mb-2 h-8 w-8" />
            <span className="text-2xl font-bold text-green-600 dark:text-green-400">92%</span>
            <span className="text-sm font-medium text-green-800 dark:text-green-200 mt-1">30-Day Forecast Accuracy</span>
          </div>

        </div>
      </div>

      {/* Main Content Split */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Chart Placeholder */}
        <div className="bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 rounded-xl p-6 shadow-sm">
          <h3 className="font-semibold text-lg mb-2">Demand Forecast (30 Days)</h3>
          <p className="text-sm text-gray-500 dark:text-zinc-400 mb-4">XGBoost regression overlaying historical data.</p>
          <div className="h-64 bg-gray-50 dark:bg-zinc-950/50 border border-gray-200 dark:border-zinc-800 rounded flex flex-col items-center justify-center border-dashed">
             <LineChart className="text-gray-400 dark:text-zinc-600 mb-2 h-8 w-8" />
             <span className="text-gray-500 dark:text-zinc-500 text-sm font-medium">Interactive Chart Engine</span>
          </div>
        </div>

        {/* Inventory Health */}
        <div className="bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 rounded-xl p-6 shadow-sm">
          <h3 className="font-semibold text-lg mb-2">ABC Distribution</h3>
          <p className="text-sm text-gray-500 dark:text-zinc-400 mb-4">Annual consumption value clustering.</p>
          <div className="h-64 flex items-end gap-2 px-8 pt-8 border-b border-gray-100 dark:border-zinc-800 pb-2">
              <div className="w-1/3 bg-blue-600 dark:bg-blue-700 rounded-t h-[80%] flex items-center justify-center text-white font-bold text-lg shadow-sm">A (80%)</div>
              <div className="w-1/3 bg-blue-400 dark:bg-blue-600 rounded-t h-[15%] flex items-center justify-center text-white font-bold text-sm shadow-sm">B (15%)</div>
              <div className="w-1/3 bg-blue-300 dark:bg-blue-500 rounded-t h-[5%] flex items-center justify-center text-white font-bold text-xs shadow-sm">C (5%)</div>
          </div>
          <div className="flex justify-between px-8 mt-2 text-xs font-medium text-gray-400 dark:text-zinc-500">
            <span className="w-1/3 text-center">Top Performers</span>
            <span className="w-1/3 text-center">Mid-Tier</span>
            <span className="w-1/3 text-center">Long Tail</span>
          </div>
        </div>
      </div>

    </div>
  )
}
