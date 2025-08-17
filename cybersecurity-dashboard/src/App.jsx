import { useState, useEffect} from 'react'
import './App.css'

function App() {
  const [threats, setThreats] = useState([])

  useEffect(()=> {
    const eventSource = new EventSource('http://localhost:5001/events');
  eventSource.onmessage = (event) => {
    const threatData = JSON.parse(event.data);
    setThreats(prevThreats => [threatData, ...prevThreats]);
  };
  return () => eventSource.close();
  },[])
    
  return (
    <div className="dashboard">
      <div className='header'>
      <h1 className='dashboard-title'>Cybersecurity Dashboard</h1>
      <p className='dashboard-subtitle'>Network threat monitoring system</p>
      <div className="threat-container">
      {threats.map((threat) => (
      <div key={threat.ip + threat.time} className={`threat-box threat-${threat.threat_level.toLowerCase()}`}>
      <h3>{threat.threat_level == "CRITICAL" ? "🔴" : threat.threat_level == "HIGH" ? "⚠️" : threat.threat_level == "MEDIUM" ? "🟡" : "🟢"} {threat.threat_level} THREAT DETECTED</h3>
      <p>{threat.attack_type} Traffic detected from IP: {threat.ip}</p>
      <p>Time: {threat.time}</p>
      <p>Confidence: {threat.confidence * 100}%</p>

      </div>
    ))}
      </div>
    </div>
    </div>
  )
};

export default App