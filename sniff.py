from scapy.all import sniff
import threading
import time
from queue import Queue

class PacketSniffer:
    def __init__(self):
        self.is_running = False
        self.packet_queue = Queue()
        self.sniffer_thread = None
    
    def start_sniffing(self):
        if not self.is_running:
            self.is_running = True
            self.sniffer_thread = threading.Thread(target=self.sniffing_loop)
            self.sniffer_thread.start()
            print("Packet Sniffing started")
    def stop_sniffing(self):
        self.is_running = False
        if self.sniffer_thread:
            self.sniffer_thread.join()
        print("Packet Sniffing stopped")
    def sniffing_loop(self):
        while self.is_running:
            packets = sniff(count = 5, timeout = 2, iface = "lo")
            for packet in packets:
                if self.is_running:
                    features = packet.extract_features(packet)
                    self.packet_queue.put(features)
    def get_latest_packets(self):
        packets = []
        while not self.packet_queue.empty():
            packets.append(self.packet_queue.get())
        return packets