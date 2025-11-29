import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { Input } from "@/components/ui/input";
import {
  startCapture,
  stopCapture,
  getLatestPackets,
  resetCapture,
} from "../api/packetApi";

interface Packet {
  id: number;
  source: string;
  destination: string;
  protocol: string;
  length: number;
  risk: "LOW" | "MEDIUM" | "HIGH";
  timestamp: string;
}
interface PacketResponse {
  count?: number;
  packets?: Packet[];
}

const Dashboard = () => {
  const navigate = useNavigate();
  const [packets, setPackets] = useState<Packet[]>([]);
  const [allPackets, setAllPackets] = useState<Packet[]>([]);
  const [isActive, setIsActive] = useState(false);
  const [activeSection, setActiveSection] = useState("DASHBOARD");
  const [searchQuery, setSearchQuery] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleStartSession = async () => {
    try {
      await startCapture();
      setIsActive(true);
      setError(null);
    } catch (err) {
      setError("Failed to start capture session.");
    }
  };

  const handleStopSession = async () => {
    try {
      await stopCapture();
      setIsActive(false);
      setError(null);
    } catch (err) {
      setError("Failed to stop capture session.");
    }
  };

  const handleResetSession = async () => {
    try {
      await resetCapture();
      setPackets([]);
      setAllPackets([]);
      setError(null);
      setIsActive(false);
    } catch (err) {
      setError("Failed to reset capture session.");
    }
  };

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    const fetchPackets = async () => {
      try {
        const data: PacketResponse | Packet[] = await getLatestPackets();
        let newPackets: Packet[] = [];

        if (typeof data === "object" && data !== null && "packets" in data) {
          newPackets = (data as PacketResponse).packets ?? [];
        } else if (Array.isArray(data)) {
          newPackets = data;
        } else {
          console.warn("Unexpected backend response:", data);
          setError("Unexpected backend response format.");
          return;
        }

        setAllPackets((prevPackets) => {
          const merged = [...prevPackets, ...newPackets];
          const unique = Array.from(new Map(merged.map((p) => [p.id, p])).values());
          return unique;
        });

        setPackets((prev) => {
          const combined = [...prev, ...newPackets];
          const unique = Array.from(new Map(combined.map((p) => [p.id, p])).values());
          return unique.slice(-10);
        });

        setError(null);
      } catch (err) {
        console.error("Error fetching packets:", err);
        setError("Error fetching packets from backend.");
      }
    };

    if (isActive) {
      fetchPackets();
      interval = setInterval(fetchPackets, 2000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isActive]);

  const filteredPackets = allPackets.filter((packet) => {
  const query = searchQuery.trim().toLowerCase();
  if (!query) return true;

  const searchable = [
    packet.id,
    packet.source,
    packet.destination,
    packet.protocol,
    packet.length,
    packet.risk,
  ]
    .map((val) => String(val ?? "").toLowerCase())
    .join(" ");

  return searchable.includes(query);
});


  const getRiskColor = (risk: string) => {
    switch (risk) {
      case "HIGH":
        return "bg-red-500 text-white";
      case "MEDIUM":
        return "bg-yellow-500 text-black";
      default:
        return "bg-green-500 text-white";
    }
  };

  const renderContent = () => {
    switch (activeSection) {
      case "ANALYSIS":
        return (
          <div className="p-6">
            <h2 className="text-3xl font-bold text-primary mb-8">TRAFFIC ANALYSIS</h2>
            <div className="grid grid-cols-2 gap-6 mb-8">
              <div className="border-2 border-primary p-6">
                <h3 className="text-xl text-primary mb-4">PACKET STATISTICS</h3>
                <div className="space-y-2 text-primary">
                  <div className="flex justify-between">
                    <span>TOTAL PACKETS:</span>
                    <span>{allPackets.length}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>HIGH RISK:</span>
                    <span className="text-destructive">
                      {allPackets.filter((p) => p.risk === "HIGH").length}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>MEDIUM RISK:</span>
                    <span className="text-yellow-500">
                      {allPackets.filter((p) => p.risk === "MEDIUM").length}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>LOW RISK:</span>
                    <span>
                      {allPackets.filter((p) => p.risk === "LOW").length}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="border-2 border-primary p-6">
              <h3 className="text-xl text-primary mb-4">THREAT ASSESSMENT</h3>
              <div className="space-y-3 text-primary">
                {[
                  { label: "LOW", color: "bg-green-500" },
                  { label: "MEDIUM", color: "bg-yellow-500" },
                  { label: "HIGH", color: "bg-red-500" },
                ].map(({ label, color }) => (
                  <div key={label} className="flex items-center gap-4">
                    <div className="w-full bg-muted h-8 relative">
                      <div
                        className={`${color} h-full`}
                        style={{
                          width: `${
                            allPackets.length > 0
                              ? (allPackets.filter((p) => p.risk === label).length /
                                  allPackets.length) *
                                100
                              : 0
                          }%`,
                        }}
                      />
                    </div>
                    <span>{label} RISK</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      case "ALARMS":
        const highRiskPackets = allPackets.filter((p) => p.risk === "HIGH");
        return (
          <div className="p-6">
            <h2 className="text-3xl font-bold text-primary mb-8">SECURITY ALARMS</h2>
            {highRiskPackets.length === 0 ? (
              <div className="border-2 border-primary p-8 text-center">
                <p className="text-primary text-xl">NO ACTIVE ALARMS</p>
                <p className="text-primary mt-2">SYSTEM MONITORING NORMAL</p>
              </div>
            ) : (
              <div className="space-y-4">
                {highRiskPackets.slice(0, 20).map((packet) => (
                  <div key={packet.id} className="border-2 border-destructive p-6">
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-destructive text-xl font-bold">
                        HIGH RISK DETECTED
                      </span>
                      <span className="text-primary">{packet.timestamp}</span>
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-primary">
                      <div>
                        <span className="text-muted-foreground">SOURCE: </span>
                        <span>{packet.source}</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">DESTINATION: </span>
                        <span>{packet.destination}</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">PROTOCOL: </span>
                        <span>{packet.protocol}</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">LENGTH: </span>
                        <span>{packet.length} bytes</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        );

      case "LOGS":
        return (
          <div className="p-6">
            <h2 className="text-3xl font-bold text-primary mb-8">LOG ANALYSIS</h2>
            <div className="mb-6">
              <Input
                type="text"
                placeholder="SEARCH LOGS (SOURCE, DESTINATION, PROTOCOL, RISK)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-background text-primary border-2 border-primary placeholder:text-muted-foreground"
              />
            </div>
            {allPackets.length === 0 ? (
              <div className="border-2 border-primary p-8 text-center">
                <p className="text-primary text-xl">NO LOGS AVAILABLE</p>
                <p className="text-primary mt-2">START A SESSION TO BEGIN LOGGING</p>
              </div>
            ) : (
              <div className="border-2 border-primary">
                <div className="overflow-auto max-h-[600px]">
                  <table className="w-full text-primary">
                    <thead className="sticky top-0 bg-background">
                      <tr className="border-b-2 border-primary">
                        <th className="text-left p-3 font-normal">#</th>
                        <th className="text-left p-3 font-normal">TIME</th>
                        <th className="text-left p-3 font-normal">SOURCE</th>
                        <th className="text-left p-3 font-normal">DESTINATION</th>
                        <th className="text-left p-3 font-normal">PROTOCOL</th>
                        <th className="text-left p-3 font-normal">LENGTH</th>
                        <th className="text-left p-3 font-normal">RISK</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredPackets.map((packet) => (
                        <tr key={packet.id} className="border-b border-primary/30">
                          <td className="p-3">{packet.id}</td>
                          <td className="p-3">{packet.timestamp}</td>
                          <td className="p-3">{packet.source}</td>
                          <td className="p-3">{packet.destination}</td>
                          <td className="p-3">{packet.protocol}</td>
                          <td className="p-3">{packet.length}</td>
                          <td className="p-3">
                            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getRiskColor(packet.risk)}`}>
                              {packet.risk}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <div className="p-3 border-t-2 border-primary text-primary">
                  TOTAL ENTRIES: {filteredPackets.length} {searchQuery && `(FILTERED FROM ${allPackets.length})`}
                </div>
              </div>
            )}
          </div>
        );

      default:
        return (
          <div className="flex-1 overflow-auto p-6">
            {packets.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <span className="text-primary font-bold text-4xl">UDON</span>
              </div>
            ) : (
              <>
                <div className="mb-4 text-primary text-sm">
                  SHOWING LAST 10 PACKETS (TOTAL CAPTURED: {allPackets.length})
                </div>
                <table className="w-full text-primary">
                  <thead>
                    <tr className="border-b-2 border-primary">
                      <th className="text-left p-3 font-normal">#</th>
                      <th className="text-left p-3 font-normal">SOURCE</th>
                      <th className="text-left p-3 font-normal">DESTINATION</th>
                      <th className="text-left p-3 font-normal">PROTOCOL</th>
                      <th className="text-left p-3 font-normal">LENGTH</th>
                      <th className="text-left p-3 font-normal">RISK</th>
                    </tr>
                  </thead>
                  <tbody>
                    {packets.map((packet) => (
                      <tr key={packet.id} className="border-b border-primary/30">
                        <td className="p-3">{packet.id}</td>
                        <td className="p-3">{packet.source}</td>
                        <td className="p-3">{packet.destination}</td>
                        <td className="p-3">{packet.protocol}</td>
                        <td className="p-3">{packet.length}</td>
                        <td className="p-3">
                          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getRiskColor(packet.risk)}`}>
                            {packet.risk}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </>
            )}
          </div>
        );
    }
  };

  return (
    <div className="flex h-screen bg-background animate-fade-in">
      <aside className="w-48 bg-primary flex flex-col border-2 border-primary m-4">
        <div className="p-4 flex items-center gap-2">
          <div className="w-4 h-4 bg-background"></div>
          <span className="text-background font-bold">UDON</span>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          {["DASHBOARD", "ANALYSIS", "ALARMS", "LOGS"].map((item) => (
            <button
              key={item}
              onClick={() => setActiveSection(item)}
              className={`w-full text-left px-3 py-2 text-background ${
                activeSection === item
                  ? "bg-background/20 border-b-2 border-background"
                  : "hover:bg-background/10"
              }`}
            >
              {item}
            </button>
          ))}
        </nav>

        <div className="p-4">
          <button
            onClick={() => navigate("/")}
            className="w-full text-left px-3 py-2 text-background hover:bg-background/10"
          >
            HOME
          </button>
        </div>
      </aside>

      <main className="flex-1 flex flex-col">
        <header className="p-4 flex items-center justify-end gap-4">
          {isActive && (
            <div className="flex items-center gap-2 border-2 border-primary px-4 py-2">
              <div className="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
              <span className="text-primary">SYSTEM ACTIVE</span>
            </div>
          )}

          <Button
            onClick={isActive ? handleStopSession : handleStartSession}
            className={`${
              isActive
                ? "bg-background text-primary hover:bg-muted border-2 border-primary"
                : "bg-primary text-background hover:bg-primary/90 border-2 border-primary"
            }`}
          >
            {isActive ? "STOP SESSION" : "START SESSION"}
          </Button>

          <Button
            onClick={handleResetSession}
            className="bg-background text-destructive hover:bg-muted border-2 border-destructive"
          >
            RESET SESSION
          </Button>
        </header>

        {error && <div className="text-center text-destructive mb-2">{error}</div>}

        {renderContent()}
      </main>
    </div>
  );
};

export default Dashboard;