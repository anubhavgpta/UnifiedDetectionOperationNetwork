import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Loading = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/dashboard");
    }, 2000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="min-h-screen bg-background flex items-center justify-center animate-fade-in">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-primary animate-[spin_3s_linear_infinite]"></div>
        <span className="text-primary font-bold text-4xl">UDON</span>
      </div>
    </div>
  );
};

export default Loading;
