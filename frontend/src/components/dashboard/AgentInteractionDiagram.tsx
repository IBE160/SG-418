'use client';

import { useEffect, useState } from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { apiClient, WorldState } from '@/lib/api';

interface AgentInteractionDiagramProps {
  onAgentClick?: (agentId: string) => void;
}

export function AgentInteractionDiagram({ onAgentClick }: AgentInteractionDiagramProps) {
  const [nodes, setNodes] = useState<Array<{ x: number; y: number; id: string; name: string }>>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const state: WorldState = await apiClient.getState();
        
        // Create nodes from agents
        const agentNodes = state.agents.map((agent: any, index: number) => ({
          x: Math.cos((index * 2 * Math.PI) / state.agents.length) * 100 + 200,
          y: Math.sin((index * 2 * Math.PI) / state.agents.length) * 100 + 200,
          id: agent.id || `agent-${index}`,
          name: agent.id || `Agent ${index + 1}`,
        }));

        setNodes(agentNodes);
      } catch (error) {
        console.error('Failed to fetch state:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="border rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-4">Agent Interaction Diagram</h2>
      <ResponsiveContainer width="100%" height={300}>
        <ScatterChart>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" dataKey="x" hide />
          <YAxis type="number" dataKey="y" hide />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} content={({ active, payload }) => {
            if (active && payload && payload[0]) {
              return (
                <div className="bg-background border rounded p-2">
                  <p>{payload[0].payload.name}</p>
                </div>
              );
            }
            return null;
          }} />
          <Scatter name="Agents" data={nodes} fill="#8884d8" onClick={(data) => {
            if (onAgentClick && data) {
              onAgentClick(data.id);
            }
          }}>
            {nodes.map((entry, index) => (
              <Cell key={`cell-${index}`} fill="#8884d8" style={{ cursor: 'pointer' }} />
            ))}
          </Scatter>
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}

