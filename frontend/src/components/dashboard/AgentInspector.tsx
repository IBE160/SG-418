'use client';

import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle } from '@/components/ui/sheet';
import { useEffect, useState } from 'react';
import { apiClient, WorldState } from '@/lib/api';

interface AgentInspectorProps {
  agentId: string | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function AgentInspector({ agentId, open, onOpenChange }: AgentInspectorProps) {
  const [agent, setAgent] = useState<any>(null);

  useEffect(() => {
    if (!agentId || !open) return;

    const fetchAgent = async () => {
      try {
        const state: WorldState = await apiClient.getState();
        const foundAgent = state.agents.find((a: any) => a.id === agentId);
        setAgent(foundAgent || null);
      } catch (error) {
        console.error('Failed to fetch agent:', error);
      }
    };

    fetchAgent();
    const interval = setInterval(fetchAgent, 2000); // Poll every 2 seconds

    return () => clearInterval(interval);
  }, [agentId, open]);

  if (!agent) return null;

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>Agent Details: {agent.id}</SheetTitle>
          <SheetDescription>Detailed information about this agent</SheetDescription>
        </SheetHeader>
        <div className="mt-6 space-y-4">
          <div>
            <h3 className="font-semibold">Job</h3>
            <p>{agent.job || 'N/A'}</p>
          </div>
          <div>
            <h3 className="font-semibold">Culture</h3>
            <p>{agent.culture || 'N/A'}</p>
          </div>
          <div>
            <h3 className="font-semibold">Inventory</h3>
            <pre className="bg-muted p-2 rounded text-sm">
              {JSON.stringify(agent.inventory || {}, null, 2)}
            </pre>
          </div>
          <div>
            <h3 className="font-semibold">Needs</h3>
            <pre className="bg-muted p-2 rounded text-sm">
              {JSON.stringify(agent.needs || {}, null, 2)}
            </pre>
          </div>
          <div>
            <h3 className="font-semibold">Wants</h3>
            <pre className="bg-muted p-2 rounded text-sm">
              {JSON.stringify(agent.wants || {}, null, 2)}
            </pre>
          </div>
          <div>
            <h3 className="font-semibold">Income</h3>
            <p>{agent.income || 0}</p>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}

