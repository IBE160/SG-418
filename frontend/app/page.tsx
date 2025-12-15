'use client';

import Link from 'next/link';
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

  const isOnline = status === 'online';

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

          <div className="mt-4 flex flex-col items-center gap-2">
            <p className="text-sm text-zinc-500 dark:text-zinc-400">
              Configure a simulation to open the interactive dashboard.
            </p>
            <Link
              href="/config"
              className={`inline-flex items-center rounded-md px-4 py-2 text-sm font-medium text-white transition ${
                isOnline
                  ? 'bg-black hover:bg-zinc-800 dark:bg-zinc-100 dark:text-black dark:hover:bg-white'
                  : 'bg-zinc-400 cursor-not-allowed'
              }`}
              aria-disabled={!isOnline}
              onClick={(e) => {
                if (!isOnline) {
                  e.preventDefault();
                }
              }}
            >
              {isOnline ? 'Get started' : 'Waiting for backend...'}
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
