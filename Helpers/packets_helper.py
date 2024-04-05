from hearthstone.enums import GameTag
from hslog.packets import PacketTree
from hslog.parser import LogParser
from hslog.packets import Packet


def get_packet_tree(_parser: LogParser) -> PacketTree:
    return _parser.games[0]


def get_packet_by_id(_parser: LogParser, packet_id: int) -> Packet | None:
    def find_packet(packets):
        for packet in packets:
            if hasattr(packet, "packet_id"):
                if packet.packet_id == packet_id:
                    return packet
                elif hasattr(packet, "packets"):
                    sub_packet = find_packet(packet.packets)
                    if sub_packet:
                        return sub_packet
        return None

    packet_tree = get_packet_tree(_parser)
    return find_packet(packet_tree.packets)


def get_packets_by_step_number(_parser: LogParser, turn_number: int) -> list[Packet]:
    pass


def get_packets_by_packet_id(_parser: LogParser, packet_id: int) -> list[Packet] | None:
    packet = get_packet_by_id(_parser, packet_id)

    if hasattr(packet, "packets"):
        return packet.packets

    return None


def get_packets_by_packet_item(packet: Packet) -> list[Packet] | None:
    if hasattr(packet, "packets"):
        return packet.packets

    return None


def get_tags_by_packet_id(_parser: LogParser, packet_id: int) -> list[GameTag] | None:
    packet = get_packet_by_id(_parser, packet_id)

    if hasattr(packet, "tags"):
        return packet.tags
    if hasattr(packet, "tag"):
        return [packet.tag]

    return None


def get_tags_by_packet_item(packet: Packet) -> list[GameTag] | None:
    if hasattr(packet, "tags"):
        return packet.tags
    if hasattr(packet, "tag"):
        return [packet.tag]

    return None
