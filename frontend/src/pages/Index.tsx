import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background flex flex-col animate-fade-in">
      {/* Header */}
      <header className="border-b-2 border-primary p-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-primary"></div>
          <span className="text-primary font-bold">UDON</span>
        </div>
        <div className="flex gap-4">
          <Button
            variant="outline"
            className="bg-background text-primary hover:bg-primary hover:text-background border-2 border-primary"
          >
            ABOUT
          </Button>
          <Button
            onClick={() => navigate("/loading")}
            className="bg-primary text-background hover:bg-primary/90 border-2 border-primary"
          >
            START SESSION
          </Button>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-start justify-center px-16 py-20">
        <h1 className="text-8xl font-bold text-primary leading-tight mb-8">
          ML TRAINED,
          <br />
          INTRUSION
          <br />
          DETECTION
          <br />
          SYSTEM
        </h1>
        
        <p className="text-primary text-xl mb-16 max-w-3xl leading-relaxed">
          Real-time network packet analysis powered by machine learning algorithms.
          <br />
          Detect anomalies, monitor traffic patterns, and protect your infrastructure
          <br />
          from sophisticated cyber threats with advanced behavioral detection.
        </p>

        <div className="flex gap-6">
          <Button
            variant="outline"
            className="bg-background text-primary hover:bg-primary hover:text-background border-2 border-primary text-lg px-8 py-6"
          >
            ABOUT
          </Button>
          <Button
            onClick={() => navigate("/loading")}
            className="bg-primary text-background hover:bg-primary/90 border-2 border-primary text-lg px-8 py-6"
          >
            START SESSION
          </Button>
        </div>
      </main>
    </div>
  );
};

export default Index;
