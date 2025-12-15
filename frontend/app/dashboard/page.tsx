'use client';

import { useState } from 'react';
import { DashboardLayout } from '@/src/components/dashboard/Layout';
import { EconomicGraph } from '@/src/components/dashboard/EconomicGraph';
import { EventLog } from '@/src/components/dashboard/EventLog';
import { AgentInteractionDiagram } from '@/src/components/dashboard/AgentInteractionDiagram';
import { AgentInspector } from '@/src/components/dashboard/AgentInspector';

export default function DashboardPage() {
  const [selectedAgentId, setSelectedAgentId] = useState<string | null>(null);
  const [inspectorOpen, setInspectorOpen] = useState(false);

  const handleAgentClick = (agentId: string) => {
    setSelectedAgentId(agentId);
    setInspectorOpen(true);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold">Simulation Dashboard</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="lg:col-span-2">
            <EconomicGraph />
          </div>
          
          <div>
            <AgentInteractionDiagram onAgentClick={handleAgentClick} />
          </div>
          
          <div>
            <EventLog />
          </div>
        </div>
      </div>
      
      <AgentInspector 
        agentId={selectedAgentId} 
        open={inspectorOpen} 
        onOpenChange={setInspectorOpen} 
      />
    </DashboardLayout>
  );
}

