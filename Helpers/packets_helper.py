import copy

from hearthstone.enums import GameTag, Zone, CardType
from hslog.export import EntityTreeExporter
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


def get_cards_by_tree(packet_tree: PacketTree) -> list:
    exporter = EntityTreeExporter(packet_tree)
    export = exporter.export()
    player = export.game.players[0]

    minions = []
    for e in player.entities:
        if e.tags[GameTag.CONTROLLER] == player.tags[GameTag.CONTROLLER] and e.zone == Zone.PLAY:
            if GameTag.CARDTYPE in e.tags.keys() and e.tags[GameTag.CARDTYPE] == CardType.MINION:
                minions.append(e)
    return minions


def get_trimmed_packet_tree(_parser: LogParser, packet_id: int) -> PacketTree:
    packet_tree = get_packet_tree(_parser)
    trimmed_packet_tree = PacketTree(ts=packet_tree.ts)

    for packet in packet_tree.packets:
        if hasattr(packet, "packet_id"):
            if packet.packet_id == packet_id:
                trimmed_packet_tree.packets.append(copy.copy(packet))
                return trimmed_packet_tree
        if hasattr(packet, "packets"):
            new_packet = copy.copy(packet)
            new_packet.packets = []
            for sub_packet in packet.packets:
                if hasattr(sub_packet, "packet_id"):
                    if sub_packet.packet_id == packet_id:
                        new_packet.packets.append(copy.copy(sub_packet))
                        trimmed_packet_tree.packets.append(new_packet)
                        return trimmed_packet_tree
                    else:
                        new_packet.packets.append(sub_packet)
            trimmed_packet_tree.packets.append(new_packet)
        else:
            trimmed_packet_tree.packets.append(packet)


def get_step_packet_id(_parser: LogParser, turn_number: int) -> int:
    packet_tree = get_packet_tree(_parser)
    count = 0

    for packet in packet_tree.packets:
        if hasattr(packet, "packets"):
            for sub_packet in packet.packets:
                if hasattr(sub_packet, "tag"):
                    if sub_packet.tag == GameTag.STEP:
                        count += 1
                        if count == turn_number:
                            return sub_packet.packet_id


def get_cards_by_turn(_parser: LogParser, turn_number: int) -> list:
    step_packet_id = get_step_packet_id(_parser, turn_number)
    trimmed_packet_tree = get_trimmed_packet_tree(_parser, step_packet_id)

    return get_cards_by_tree(trimmed_packet_tree)


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
