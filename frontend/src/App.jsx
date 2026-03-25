import React, { useState } from 'react';
import axios from 'axios';
import { Sparkles, MapPin, DollarSign, CalendarDays, Loader2, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import ReactMarkdown from 'react-markdown';

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8001";

function App() {
  const [destination, setDestination] = useState('');
  const [budget, setBudget] = useState('');
  const [days, setDays] = useState('');
  const [itinerary, setItinerary] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handlePlanTrip = async (e) => {
    e.preventDefault();
    if (!destination || !budget || !days) {
      setError('Please fill in all fields');
      return;
    }

    setLoading(true);
    setError('');
    setItinerary('');

    try {
      const response = await axios.post(`${API_URL}/plan-trip`, {
        destination,
        budget: parseFloat(budget),
        days: parseInt(days)
      });

      if (response.data.status === 'success') {
        setItinerary(response.data.itinerary);
      } else {
        // Show the actual itinerary/error message, not the reasoning logs
        setError(response.data.itinerary || response.data.reasoning_logs || 'Failed to generate itinerary');
      }
    } catch (err) {
      console.error(err);
      setError('Connection to backend failed. Make sure the server is running at ' + API_URL);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background pt-8 pb-12 px-4">
      <div className="max-w-2xl mx-auto">
        <header className="mb-6 text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Sparkles className="text-foreground size={18}" />
            <h1 className="text-3xl font-bold tracking-tight text-foreground m-0">Routewise</h1>
          </div>
          <p className="text-sm text-muted-foreground">AI-Powered Travel Planning for Your Next Adventure</p>
        </header>

        <main className="space-y-8">
          <Card className="shadow-sm border border-border border-t-2 border-t-zinc-400">
            <CardContent className="p-6">
              <form onSubmit={handlePlanTrip} className="space-y-4">
                <div className="space-y-1.5">
                  <Label htmlFor="destination">Destination</Label>
                  <div className="relative">
                    <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 size={16} text-muted-foreground" />
                    <Input
                      id="destination"
                      type="text"
                      placeholder="e.g. Paris"
                      value={destination}
                      onChange={(e) => setDestination(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="budget">Budget ($)</Label>
                  <div className="relative">
                    <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 size={16} text-muted-foreground" />
                    <Input
                      id="budget"
                      type="number"
                      placeholder="Total budget"
                      value={budget}
                      onChange={(e) => setBudget(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="days">Duration (Days)</Label>
                  <div className="relative">
                    <CalendarDays className="absolute left-3 top-1/2 transform -translate-y-1/2 size={16} text-muted-foreground" />
                    <Input
                      id="days"
                      type="number"
                      placeholder="Number of days"
                      value={days}
                      onChange={(e) => setDays(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>

                <Button 
                  type="submit" 
                  disabled={loading}
                  className="w-full transition-transform hover:scale-[1.01]"
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                      <Loader2 className="animate-spin size={16}" />
                      Agent is planning your trip...
                    </span>
                  ) : (
                    "Create Optimized Itinerary"
                  )}
                </Button>
              </form>

              {error && (
                <div className="mt-6 p-4 bg-destructive/10 border border-destructive text-destructive-foreground">
                  <div className="flex items-center gap-3 mb-2">
                    <AlertCircle className="size={16} flex-shrink-0" />
                    <span className="text-sm font-medium">Error</span>
                  </div>
                  <div className="prose prose-invert max-w-none">
                    <ReactMarkdown 
                      className="text-sm leading-relaxed"
                      components={{
                        h1: ({children, ...props}) => (
                          <h1 className="text-lg font-bold mb-2" {...props}>{children}</h1>
                        ),
                        h2: ({children, ...props}) => (
                          <h2 className="text-base font-semibold mb-2 mt-3" {...props}>{children}</h2>
                        ),
                        h3: ({children, ...props}) => (
                          <h3 className="text-sm font-medium mb-1 mt-2" {...props}>{children}</h3>
                        ),
                        ul: ({children, ...props}) => (
                          <ul className="list-disc list-inside space-y-1 ml-4 mb-3" {...props}>{children}</ul>
                        ),
                        li: ({children, ...props}) => (
                          <li className="text-sm leading-relaxed" {...props}>{children}</li>
                        ),
                        p: ({children, ...props}) => (
                          <p className="text-sm leading-relaxed mb-2" {...props}>{children}</p>
                        ),
                        strong: ({children, ...props}) => (
                          <strong className="font-medium" {...props}>{children}</strong>
                        ),
                        a: ({children, ...props}) => (
                          <a className="underline hover:no-underline" {...props}>{children}</a>
                        )
                      }}
                    >
                      {error}
                    </ReactMarkdown>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {itinerary && (
            <Card className="shadow-sm border border-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-foreground">
                  <Sparkles className="text-foreground size={18}" /> 
                  Your Personalized Itinerary
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="prose prose-invert max-w-none">
                  <ReactMarkdown 
                    className="text-sm text-muted-foreground leading-relaxed"
                    components={{
                      h1: ({children, ...props}) => (
                        <h1 className="text-2xl font-bold text-foreground mb-4" {...props}>{children}</h1>
                      ),
                      h2: ({children, ...props}) => (
                        <h2 className="text-xl font-semibold text-foreground mb-3 mt-6" {...props}>{children}</h2>
                      ),
                      h3: ({children, ...props}) => (
                        <h3 className="text-lg font-medium text-foreground mb-2 mt-4" {...props}>{children}</h3>
                      ),
                      ul: ({children, ...props}) => (
                        <ul className="list-disc list-inside space-y-1 ml-4 mb-4" {...props}>{children}</ul>
                      ),
                      li: ({children, ...props}) => (
                        <li className="text-sm text-muted-foreground leading-relaxed" {...props}>{children}</li>
                      ),
                      p: ({children, ...props}) => (
                        <p className="text-sm text-muted-foreground leading-relaxed mb-4" {...props}>{children}</p>
                      ),
                      strong: ({children, ...props}) => (
                        <strong className="font-semibold text-foreground" {...props}>{children}</strong>
                      ),
                      hr: ({...props}) => (
                        <Separator className="my-6" {...props} />
                      )
                    }}
                  >
                    {itinerary}
                  </ReactMarkdown>
                </div>
              </CardContent>
            </Card>
          )}
        </main>

        <footer className="mt-16 py-8 text-muted-foreground text-sm border-t border-border text-center">
          <p>© 2026 Routewise - Powered by CrewAI & OpenRouter</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
