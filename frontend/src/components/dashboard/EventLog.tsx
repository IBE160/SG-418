'use client';

import { useEffect, useState, useRef } from 'react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { apiClient, WorldState } from '@/lib/api';

export function EventLog() {
  const [events, setEvents] = useState<Array<{ day: number; tick: number; description: string }>>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const state: WorldState = await apiClient.getState();
        
        // Convert event log to display format
        const formattedEvents = (state.event_log || []).map((event: any) => {
          // Format description from event fields
          let description = '';
          if (event.details) {
            description = event.details;
          } else if (event.action) {
            description = `${event.action}${event.agent_id ? ` (Agent: ${event.agent_id})` : ''}${event.result ? ` - ${event.result}` : ''}`;
          } else {
            description = JSON.stringify(event);
          }
          
          return {
            day: event.day || state.current_day,
            tick: event.tick || state.current_tick,
            description: description,
          };
        });

        setEvents(formattedEvents);
      } catch (error) {
        console.error('Failed to fetch state:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 2000); // Poll every 2 seconds

    return () => clearInterval(interval);
  }, []);

  // Auto-scroll to bottom when new events arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [events]);

  return (
    <div className="border rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-4">Event Log</h2>
      <ScrollArea className="h-[300px]">
        <div className="space-y-2" ref={scrollRef}>
          {events.length === 0 ? (
            <p className="text-muted-foreground">No events yet...</p>
          ) : (
            events.map((event, index) => (
              <div key={index} className="text-sm">
                <span className="font-mono text-muted-foreground">
                  Day {event.day}, Tick {event.tick}:
                </span>{' '}
                {event.description}
              </div>
            ))
          )}
        </div>
      </ScrollArea>
    </div>
  );
}

