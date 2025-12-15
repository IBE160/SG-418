'use client';

import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { apiClient, WorldState } from '@/lib/api';

export function EconomicGraph() {
  const [data, setData] = useState<Array<{ index: number; day: number; tick: number; value: number }>>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const state: WorldState = await apiClient.getState();
        
        // Use market_history from backend if available, otherwise calculate from agents
        if (state.market_history && state.market_history.length > 0) {
          // Convert market_history to chart data format with sequential index
          const chartData = state.market_history.map((entry: any, index: number) => ({
            index: index,
            day: entry.day || state.current_day,
            tick: entry.tick || 0,
            value: entry.total_value || 0
          }));
          setData(chartData);
        } else {
          // Fallback: calculate total economic value (sum of all agent inventories)
          const totalValue = state.agents.reduce((sum, agent) => {
            const inventoryValue = Object.values(agent.inventory || {}).reduce((invSum: number, amount: any) => invSum + (amount || 0), 0);
            return sum + inventoryValue;
          }, 0);

          // Only add if tick changed to avoid duplicates
          setData((prev) => {
            const lastTick = prev.length > 0 ? prev[prev.length - 1].tick : -1;
            if (state.current_tick > lastTick) {
              return [...prev, { index: prev.length, day: state.current_day, tick: state.current_tick, value: totalValue }];
            }
            return prev;
          });
        }
      } catch (error) {
        console.error('Failed to fetch state:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 2000); // Poll every 2 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="border rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-4">Total Economic Value Over Time</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="index" 
            label={{ value: 'Time Point', position: 'insideBottom', offset: -5 }}
          />
          <YAxis />
          <Tooltip 
            formatter={(value: any) => [value, 'Total Value']}
            labelFormatter={(index: any) => {
              const point = data[Number(index)];
              return point ? `Day ${point.day}, Tick ${point.tick}` : `Point ${index}`;
            }}
          />
          <Legend />
          <Line type="monotone" dataKey="value" stroke="#8884d8" name="Total Value" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

