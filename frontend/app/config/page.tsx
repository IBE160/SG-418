'use client';

import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { apiClient } from '@/lib/api';
import { useState } from 'react';
import { useSimulationStore } from '../store/simulation';
import { useRouter } from 'next/navigation';

const jobSchema = z.object({
  job_name: z.string().min(1, 'Job name is required'),
  resource_produced: z.string().min(1, 'Resource name is required'),
});

const agentConfigSchema = z.object({
  job: z.string().min(1, 'Job selection is required'),
  count: z.coerce.number().int().positive('Count must be a positive integer'),
  culture: z.string().default('Neutral'),
  needs: z.string().default('{}'), // JSON string for needs dict
  wants: z.string().default('{}'), // JSON string for wants dict
  income: z.coerce.number().int().positive('Income must be a positive integer'),
});

const configSchema = z.object({
  day_length_seconds: z.coerce.number().int().positive('Day length must be a positive integer'),
  max_days: z.coerce.number().int().positive('Max days must be a positive integer'),
  jobs: z.array(jobSchema).min(1, 'At least one job is required'),
  agents: z.array(agentConfigSchema).min(1, 'At least one agent configuration is required'),
}).refine((data) => {
  const totalAgents = data.agents.reduce((sum, agent) => sum + agent.count, 0);
  return totalAgents > 1;
}, {
  message: 'Total agent count must be greater than 1',
  path: ['agents'],
});

type ConfigFormValues = z.infer<typeof configSchema>;

export default function ConfigPage() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const setView = useSimulationStore((state) => state.setView);
  const router = useRouter();
  
  const form = useForm({
    resolver: zodResolver(configSchema),
    defaultValues: {
      day_length_seconds: 60,
      max_days: 5,
      jobs: [{ job_name: 'Woodcutter', resource_produced: 'Wood' }],
      agents: [{ job: 'Woodcutter', count: 2, culture: 'Neutral', needs: '{"food": 10}', wants: '{}', income: 100 }],
    },
  });

  const { fields: jobFields, append: appendJob, remove: removeJob } = useFieldArray({
    control: form.control,
    name: 'jobs',
  });

  const { fields: agentFields, append: appendAgent, remove: removeAgent } = useFieldArray({
    control: form.control,
    name: 'agents',
  });

  const jobs = form.watch('jobs');

  const onSubmit = async (data: ConfigFormValues) => {
    setIsSubmitting(true);
    setSubmitError(null);
    
    try {
      await apiClient.setConfig(data);
      // Start simulation and navigate to dashboard
      await apiClient.startSimulation();
      setView('dashboard');
      router.push('/dashboard');
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'Failed to submit configuration');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container mx-auto py-10 px-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Simulation Configuration</h1>
        
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="day_length_seconds"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Day Length (seconds)</FormLabel>
                  <FormControl>
                    <Input 
                      type="number" 
                      {...field} 
                      value={String(field.value ?? '')}
                      onChange={(e) => field.onChange(parseInt(e.target.value) || 0)}
                    />
                  </FormControl>
                  <FormDescription>
                    Duration of a simulation day in real-time seconds
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="max_days"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Maximum Days</FormLabel>
                  <FormControl>
                    <Input 
                      type="number" 
                      {...field} 
                      value={String(field.value ?? '')}
                      onChange={(e) => field.onChange(parseInt(e.target.value) || 0)}
                    />
                  </FormControl>
                  <FormDescription>
                    The total number of days the simulation will run
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <Label>Jobs & Resources</Label>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => appendJob({ job_name: '', resource_produced: '' })}
                >
                  Add Job
                </Button>
              </div>

              {jobFields.map((field, index) => (
                <div key={field.id} className="flex gap-2 items-start">
                  <FormField
                    control={form.control}
                    name={`jobs.${index}.job_name`}
                    render={({ field }) => (
                      <FormItem className="flex-1">
                        <FormLabel>Job Name</FormLabel>
                        <FormControl>
                          <Input placeholder="e.g., Woodcutter" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name={`jobs.${index}.resource_produced`}
                    render={({ field }) => (
                      <FormItem className="flex-1">
                        <FormLabel>Resource Produced</FormLabel>
                        <FormControl>
                          <Input placeholder="e.g., Wood" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <Button
                    type="button"
                    variant="destructive"
                    onClick={() => removeJob(index)}
                    className="mt-8"
                  >
                    Remove
                  </Button>
                </div>
              ))}
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <Label>Agent Configuration</Label>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => appendAgent({ 
                    job: jobs[0]?.job_name || '', 
                    count: 1, 
                    culture: 'Neutral', 
                    needs: '{}', 
                    wants: '{}', 
                    income: 100 
                  })}
                >
                  Add Agent Config
                </Button>
              </div>

              {agentFields.map((field, index) => (
                <div key={field.id} className="border p-4 rounded-lg space-y-4">
                  <div className="flex gap-2">
                    <FormField
                      control={form.control}
                      name={`agents.${index}.job`}
                      render={({ field }) => (
                        <FormItem className="flex-1">
                          <FormLabel>Job</FormLabel>
                          <FormControl>
                            <select {...field} className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
                              {jobs.map((job) => (
                                <option key={job.job_name} value={job.job_name}>
                                  {job.job_name}
                                </option>
                              ))}
                            </select>
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name={`agents.${index}.count`}
                      render={({ field }) => (
                        <FormItem className="flex-1">
                          <FormLabel>Count</FormLabel>
                          <FormControl>
                            <Input 
                              type="number" 
                              {...field} 
                              value={String(field.value ?? '')}
                              onChange={(e) => field.onChange(parseInt(e.target.value) || 0)}
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name={`agents.${index}.income`}
                      render={({ field }) => (
                        <FormItem className="flex-1">
                          <FormLabel>Income</FormLabel>
                          <FormControl>
                            <Input 
                              type="number" 
                              {...field} 
                              value={String(field.value ?? '')}
                              onChange={(e) => field.onChange(parseInt(e.target.value) || 0)}
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                  <FormField
                    control={form.control}
                    name={`agents.${index}.culture`}
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Culture</FormLabel>
                        <FormControl>
                          <Input placeholder="e.g., Cooperative, Aggressive" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <div className="grid grid-cols-2 gap-2">
                    <FormField
                      control={form.control}
                      name={`agents.${index}.needs`}
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Needs (JSON)</FormLabel>
                          <FormControl>
                            <Input placeholder='{"food": 10, "water": 10}' {...field} />
                          </FormControl>
                          <FormDescription>Essential resources as JSON</FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name={`agents.${index}.wants`}
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Wants (JSON)</FormLabel>
                          <FormControl>
                            <Input placeholder='{"tools": 5}' {...field} />
                          </FormControl>
                          <FormDescription>Desirable resources as JSON</FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                  <Button
                    type="button"
                    variant="destructive"
                    onClick={() => removeAgent(index)}
                  >
                    Remove
                  </Button>
                </div>
              ))}
            </div>

            {submitError && (
              <div className="text-red-500 text-sm">{submitError}</div>
            )}
            
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Submitting...' : 'Continue'}
            </Button>
          </form>
        </Form>
      </div>
    </div>
  );
}

