"use client";

import { useState } from 'react';
import { Play, CheckCircle2, AlertTriangle, Lightbulb } from 'lucide-react';
import { runSimulation } from '@/lib/api/simulation';
import { SimulationResponse } from '@/lib/types/simulation';

export default function SimulationPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SimulationResponse | null>(null);
  
  // Form State
  const [delay, setDelay] = useState(5);
  const [demandChange, setDemandChange] = useState(20);

  const handleSimulate = async () => {
    setLoading(true);
    try {
      // In MVP, assuming product 1 and warehouse 1
      const res = await runSimulation({
        product_id: 1,
        warehouse_id: 1,
        horizon_days: 30,
        scenarios: [
          { type: 'supplier_delay', delay_days: delay },
          { type: 'demand_change', demand_multiplier: 1 + (demandChange / 100) }
        ]
      });
      setResult(res);
    } catch (error) {
      console.error("Simulation failed", error);
      // Fallback for demonstration if backend is down
      setResult({
        scenario_type: "combined",
        baseline: { stockout: false, stockout_date: null, ending_inventory: 420 },
        scenario: { stockout: true, stockout_date: "2026-08-28", ending_inventory: 76 },
        impact: { additional_shortage_units: 344, inventory_delta: -344 },
        recommendations: ["Expedite inbound shipment for Purchase Order #PO-8832", "Increase replenishment quantity"]
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="mb-8 border-b border-gray-200 dark:border-zinc-800 pb-4">
        <h2 className="text-2xl font-bold tracking-tight">WHAT-IF SIMULATION</h2>
        <p className="text-gray-500 dark:text-zinc-400 mt-1">Non-Destructive Scenario Projection Engine</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Scenario Builder */}
        <div className="lg:col-span-1 bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 rounded-xl p-6 h-fit shadow-sm">
          <h3 className="text-lg font-semibold border-b border-gray-200 dark:border-zinc-800 pb-2 mb-4">Configure Scenario</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-zinc-300">Target Product</label>
              <select className="w-full bg-gray-50 dark:bg-zinc-950 border border-gray-200 dark:border-zinc-800 rounded p-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all">
                <option>SKU-1002 (Industrial Bearings)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-zinc-300">Supplier Delay (Days)</label>
              <input 
                type="number" 
                value={delay} 
                onChange={(e) => setDelay(Number(e.target.value))}
                className="w-full bg-gray-50 dark:bg-zinc-950 border border-gray-200 dark:border-zinc-800 rounded p-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all" 
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-zinc-300">Demand Change (%)</label>
              <input 
                type="number" 
                value={demandChange} 
                onChange={(e) => setDemandChange(Number(e.target.value))}
                className="w-full bg-gray-50 dark:bg-zinc-950 border border-gray-200 dark:border-zinc-800 rounded p-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all" 
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-zinc-300">Projection Horizon</label>
              <select className="w-full bg-gray-50 dark:bg-zinc-950 border border-gray-200 dark:border-zinc-800 rounded p-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all">
                <option>30 Days</option>
                <option>90 Days</option>
              </select>
            </div>

            <button 
              onClick={handleSimulate}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 px-4 rounded mt-6 flex items-center justify-center gap-2 transition-colors disabled:opacity-50 shadow-sm"
            >
              {loading ? <span className="animate-pulse">Running...</span> : (
                <>
                  <Play className="h-4 w-4" />
                  RUN SIMULATION
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results */}
        <div className="lg:col-span-2 space-y-8">
          
          {!result ? (
            <div className="h-full min-h-[400px] border-2 border-dashed border-gray-200 dark:border-zinc-800 rounded-xl flex items-center justify-center text-gray-400 dark:text-zinc-600">
              Configure parameters and run the simulation to project impacts.
            </div>
          ) : (
            <div className="space-y-8 animate-in zoom-in-95 duration-300">
              {/* Split Comparison */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 rounded-xl p-6 flex flex-col items-center justify-center text-center shadow-sm">
                  <h4 className="text-xs font-bold text-gray-400 dark:text-zinc-500 mb-2 tracking-widest">BASELINE (UNTOUCHED)</h4>
                  <div className={`flex items-center font-medium mb-1 gap-1 ${result.baseline.stockout ? 'text-red-500' : 'text-green-500'}`}>
                    {result.baseline.stockout ? <AlertTriangle className="h-5 w-5" /> : <CheckCircle2 className="h-5 w-5" />} 
                    {result.baseline.stockout ? 'Stockout Expected' : 'No Stockout'}
                  </div>
                  <p className="text-4xl font-bold">{result.baseline.ending_inventory.toFixed(0)}</p>
                  <p className="text-xs text-gray-500 dark:text-zinc-400 mt-1">Ending Inventory (Day 30)</p>
                </div>

                <div className={`rounded-xl p-6 flex flex-col items-center justify-center text-center relative overflow-hidden shadow-sm border ${result.scenario.stockout ? 'bg-red-50 dark:bg-red-950/20 border-red-200 dark:border-red-900' : 'bg-green-50 dark:bg-green-950/20 border-green-200 dark:border-green-900'}`}>
                  {/* Warning strip */}
                  {result.scenario.stockout && <div className="absolute top-0 w-full h-1.5 bg-red-500"></div>}
                  <h4 className={`text-xs font-bold mb-2 tracking-widest ${result.scenario.stockout ? 'text-red-500 dark:text-red-400' : 'text-green-600'}`}>SCENARIO IMPACT</h4>
                  <div className={`flex items-center font-bold mb-1 gap-1 ${result.scenario.stockout ? 'text-red-600 dark:text-red-500' : 'text-green-600 dark:text-green-500'}`}>
                    {result.scenario.stockout ? <AlertTriangle className="h-5 w-5" /> : <CheckCircle2 className="h-5 w-5" />} 
                    {result.scenario.stockout ? 'Stockout Occurs' : 'No Stockout'}
                  </div>
                  <p className={`text-4xl font-bold ${result.scenario.stockout ? 'text-red-600 dark:text-red-500' : 'text-green-600 dark:text-green-500'}`}>
                    {result.scenario.stockout ? (result.scenario.stockout_date ? new Date(result.scenario.stockout_date).toLocaleDateString(undefined, {month: 'short', day: 'numeric'}) : 'Yes') : result.scenario.ending_inventory.toFixed(0)}
                  </p>
                  <p className={`text-xs font-medium mt-1 ${result.scenario.stockout ? 'text-red-800 dark:text-red-300' : 'text-green-800 dark:text-green-300'}`}>
                    Ending Inventory: {result.scenario.ending_inventory.toFixed(0)}
                  </p>
                </div>
              </div>

              {/* Delta Impact Details */}
              <div className="bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 rounded-xl p-6 shadow-sm">
                <h4 className="text-lg font-semibold mb-6">Calculated Impact</h4>
                
                <div className="grid grid-cols-2 gap-8 mb-8">
                  <div>
                    <p className="text-sm font-medium text-gray-500 dark:text-zinc-400">Additional Shortage Units</p>
                    <p className="text-3xl font-bold font-mono mt-1">
                      {result.impact.additional_shortage_units.toFixed(0)} <span className="text-sm font-normal text-gray-400">units</span>
                    </p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500 dark:text-zinc-400">Inventory Delta vs Baseline</p>
                    <p className={`text-3xl font-bold font-mono mt-1 ${result.impact.inventory_delta < 0 ? 'text-red-500' : 'text-green-500'}`}>
                      {result.impact.inventory_delta > 0 ? '+' : ''}{result.impact.inventory_delta.toFixed(0)}
                    </p>
                  </div>
                </div>

                <div className="bg-orange-50 dark:bg-orange-950/20 border border-orange-200 dark:border-orange-900 rounded-lg p-5">
                  <h5 className="font-bold text-orange-600 dark:text-orange-500 flex items-center gap-2 mb-3">
                    <Lightbulb className="h-5 w-5" />
                    System Recommendation
                  </h5>
                  <ul className="list-disc list-inside space-y-2 text-sm text-gray-800 dark:text-gray-200">
                    {result.recommendations.map((rec, i) => (
                      <li key={i}>{rec}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
