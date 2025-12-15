import { create } from 'zustand';

interface SimulationState {
  isRunning: boolean;
  currentView: 'config' | 'dashboard';
  setRunning: (running: boolean) => void;
  setView: (view: 'config' | 'dashboard') => void;
}

export const useSimulationStore = create<SimulationState>((set) => ({
  isRunning: false,
  currentView: 'config',
  setRunning: (running: boolean) => set({ isRunning: running }),
  setView: (view: 'config' | 'dashboard') => set({ currentView: view }),
}));

