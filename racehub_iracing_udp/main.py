import socket
import time
import racehub_iracing_udp.iracing_message_pb2 as iRacingMessage
from racehub_iracing_udp.config import config
from racehub_iracing_udp.constants import rad_to_deg
import irsdk
import logging

# Configure the logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IRacingUDPServer:
    def __init__(self):
        self.frequency = config.get("frequency", 60)
        self.address = config.get("address", "127.0.0.1")
        self.port = config.get("port", 20900)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ir = irsdk.IRSDK()
        self.state = self.State()

        logging.info(
            f"Starting Server at {self.address}:{self.port} with frequency {self.frequency} Hz"
        )

    class State:
        def __init__(self):
            self.ir_connected = False
            self.last_car_setup_tick = -1

    def check_iracing(self):
        """Check the connection status with iRacing and update the state accordingly."""
        if self.state.ir_connected and not (
            self.ir.is_initialized and self.ir.is_connected
        ):
            self.state.ir_connected = False
            self.state.last_car_setup_tick = -1
            self.ir.shutdown()
            logging.info("iRacing Disconnected")
        elif (
            not self.state.ir_connected
            and self.ir.startup()
            and self.ir.is_initialized
            and self.ir.is_connected
        ):
            self.state.ir_connected = True
            logging.info("iRacing Connected")

    def get_packet(self):
        """Retrieve the telemetry data and convert it to a protobuf packet."""
        self.ir.freeze_var_buffer_latest()
        packet = iRacingMessage.TelemetryPacket()

        if not self.ir["DriverInfo"]:
            return packet

        di = self.ir["DriverInfo"]
        num_cars = len(di["Drivers"])
        player_idx = self.ir["PlayerCarIdx"]

        cars = [packet.Cars.add() for _ in range(num_cars)]
        participants = [packet.Participants.add() for _ in range(num_cars)]

        for i, car in enumerate(cars):
            car.CarIdx = i
            car.Lap = self.ir["CarIdxLap"][i]
            car.LapDistancePct = self.ir["CarIdxLapDistPct"][i]
            car.Steer = self.ir["CarIdxSteer"][i] * rad_to_deg

            if player_idx == i:
                car.Brake = self.ir["Brake"] * 100
                car.Clutch = self.ir["Clutch"] * 100
                car.Gear = self.ir["Gear"]
                car.RPM = self.ir["RPM"]
                car.Speed = self.ir["Speed"]
                car.Throttle = self.ir["Throttle"] * 100
                car.LapTime = self.ir["LapCurrentLapTime"]

            participant = participants[i]
            participant.ParticipantIdx = i
            participant.DriverName = di["Drivers"][i]["UserName"]
            abbreviation = di["Drivers"][i]["AbbrevName"]
            participant.CarNumber = di["Drivers"][i]["CarNumberRaw"]
            participant.TeamName = di["Drivers"][i]["TeamName"]

            if abbreviation:
                participant.Abbreviation = abbreviation

        if not self.ir["WeekendInfo"]:
            return packet

        wi = self.ir["WeekendInfo"]
        session_info = packet.SessionInfo
        session_info.SessionID = wi["SessionID"]
        session_info.Category = wi["Category"]
        session_info.EventType = wi["EventType"]
        session_info.TrackName = wi["TrackDisplayName"]
        session_info.TrackLength = int(wi["TrackLength"].split(" ")[0]) * 1000
        session_info.AirDensity = self.ir["AirDensity"]
        session_info.AirPressure = self.ir["AirPressure"]
        session_info.AirTemperature = self.ir["AirTemp"]
        session_info.SessionTime = self.ir["SessionTime"]
        session_info.TrackTemperature = self.ir["TrackTempCrew"]
        session_info.TrackWetness = self.ir["TrackWetness"]

        return packet

    def send_udp_message(self, message):
        """Send the message to the configured address via UDP."""
        self.sock.sendto(message, (self.address, self.port))

    def run(self):
        """Run the main server loop, checking iRacing status and sending telemetry data."""
        try:
            while True:
                self.check_iracing()
                if self.state.ir_connected:
                    packet = self.get_packet()
                    msg = packet.SerializeToString()
                    self.send_udp_message(msg)
                time.sleep(1 / self.frequency)
        except KeyboardInterrupt:
            self.sock.close()


def main():
    server = IRacingUDPServer()
    server.run()


if __name__ == "__main__":
    main()
