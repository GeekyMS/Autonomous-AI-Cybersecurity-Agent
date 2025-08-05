import time

class flowData:
    def __init__(self):
        self.packets = 0
        self.total_bytes = 0
        self.start_time = None
        self.last_packet_time = None
    
    def add_packet(self,packet):
        if self.start_time is None:
            self.start_time = time.time()
        self.last_packet_time = time.time()
        self.packets += 1
        self.total_bytes += len(packet)
    
    def get_current_features(self):
        if self.start_time is None:
            return None
        
        duration = self.last_packet_time - self.start_time

        duration = max(duration, 0.001)

        return {'flow_duration': duration,
                'total_packets': self.packets,
                'total_bytes': self.total_bytes,
                'packets_per_second': self.packets / duration,
                'bytes_per_second': self.total_bytes / duration
                }

class flowTracker:
    def __init__(self):
        self.flows = {}
        self.max_flows = 1000

    def get_flow_key(self, packet):
        try:
            if packet.haslayer('IP'):
                src_ip = packet['IP'].src
                dest_ip = packet['IP'].dst
                protocol = packet['IP'].proto
                
                if packet.haslayer('TCP'):
                    src_port = packet['TCP'].sport
                    dest_port = packet['TCP'].dport
                    return (src_ip, dest_ip, src_port, dest_port, protocol)
                elif packet.haslayer('UDP'):
                    src_port = packet['UDP'].sport
                    dest_port = packet['UDP'].dport
                    return (src_ip, dest_ip, src_port, dest_port, protocol)
                else:
                    return None
            else:
                return None
        except Exception as e:
            print((f"Packet parsing error: {e}"))
            return None

    def extract_features(self,packet):
        flow_key = self.get_flow_key(packet)

        if flow_key is None:
            return None
        
        if flow_key not in self.flows:
            if len(self.flows) >= self.max_flows:
                self.cleanup()
            self.flows[flow_key] = flowData()

        self.flows[flow_key].add_packet(packet)
        
        return self.flows[flow_key].get_current_features()

    def cleanup(self):
        if len(self.flows) < self.max_flows:
            return
        
        sorted_flows = sorted(self.flows.items(), key=lambda x: x[1].last_packet_time)

        flows_to_remove = len(self.flows)//4

        for i in range(flows_to_remove):
            del self.flows[sorted_flows[i][0]]
            