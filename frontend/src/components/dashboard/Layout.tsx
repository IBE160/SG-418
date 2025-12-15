'use client';

import { ReactNode } from 'react';
import { Button } from '@/components/ui/button';
import { useSimulationStore } from '@/app/store/simulation';
import { apiClient } from '@/lib/api';

interface DashboardLayoutProps {
  children: ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const isRunning = useSimulationStore((state) => state.isRunning);
  const setRunning = useSimulationStore((state) => state.setRunning);

  const handleStart = async () => {
    try {
      await apiClient.startSimulation();
      setRunning(true);
    } catch (error) {
      console.error('Failed to start simulation:', error);
    }
  };

  const handleStop = async () => {
    try {
      await apiClient.stopSimulation();
      setRunning(false);
    } catch (error) {
      console.error('Failed to stop simulation:', error);
    }
  };

  const handleExport = async () => {
    try {
      const blob = await apiClient.exportEventLog();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'event-log.csv';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Failed to export:', error);
    }
  };

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <aside className="w-64 border-r bg-muted/40 p-4 flex flex-col gap-4">
        <h2 className="text-lg font-semibold">Controls</h2>
        <div className="flex flex-col gap-2">
          {!isRunning ? (
            <Button onClick={handleStart} className="w-full">Start Simulation</Button>
          ) : (
            <Button onClick={handleStop} variant="destructive" className="w-full">Stop Simulation</Button>
          )}
          <Button onClick={handleExport} variant="outline" className="w-full">Export Data</Button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto p-6">
        {children}
      </main>
    </div>
  );
}

