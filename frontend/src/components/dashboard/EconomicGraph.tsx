'use client';

import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { apiClient, WorldState } from '@/lib/api';

export function EconomicGraph() {
  const [data, setData] = useState<Array<{ day: number; tick: number; value: number }>>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const state: WorldState = await apiClient.getState();
        
        // Calculate total economic value (sum of all agent inventories)
        const totalValue = state.agents.reduce((sum, agent) => {
          const inventoryValue = Object.values(agent.inventory || {}).reduce((invSum: number, amount: any) => invSum + (amount || 0), 0);
          return sum + inventoryValue;
        }, 0);

        setData((prev) => [
          ...prev,
          { day: state.current_day, tick: state.current_tick, value: totalValue },
        ]);
      } catch (error) {
        console.error('Failed to fetch state:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 3000); // Poll every 3 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="border rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-4">Total Economic Value Over Time</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="tick" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="value" stroke="#8884d8" name="Total Value" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

