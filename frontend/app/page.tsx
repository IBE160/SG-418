'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api';

export default function Home() {
  const [status, setStatus] = useState<'online' | 'offline' | 'checking'>('checking');

  useEffect(() => {
    const checkStatus = async () => {
      try {
        await apiClient.getHealth();
        setStatus('online');
      } catch (error) {
        setStatus('offline');
      }
    };

    checkStatus();
    // Check status every 5 seconds
    const interval = setInterval(checkStatus, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-center py-32 px-16 bg-white dark:bg-black">
        <div className="flex flex-col items-center gap-6 text-center">
          <h1 className="text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
            AIES - AI Economy Simulator
          </h1>
          <div className="flex items-center gap-3">
            <div
              className={`h-3 w-3 rounded-full ${
                status === 'online'
                  ? 'bg-green-500'
                  : status === 'offline'
                  ? 'bg-red-500'
                  : 'bg-yellow-500 animate-pulse'
              }`}
            />
            <p className="text-lg text-zinc-600 dark:text-zinc-400">
              System Status: {status === 'online' ? 'Online' : status === 'offline' ? 'Offline' : 'Checking...'}
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
