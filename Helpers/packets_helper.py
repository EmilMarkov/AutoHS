import copy

from hearthstone.enums import GameTag, Zone, CardType, Step
from hslog.export import EntityTreeExporter
from hslog.packets import PacketTree
from hslog.parser import LogParser
from hslog.packets import Packet


def get_packet_tree(_parser: LogParser) -> PacketTree:
    """
    Get a PacketTree
    :param _parser: LogParser instance
    :return: PacketTree instance
    """
    return _parser.games[0]


def get_packet_by_id(_parser: LogParser, packet_id: int) -> Packet | None:
    """
    Get a Packet by packet id
    :param _parser: LogParser instance
    :param packet_id: ID of the getting packet
    :return: Packet | None (if not found)
    """
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
    """
    Get list of cards at the end of PacketTree instance
    :param packet_tree: PacketTree instance
    :return: list[Card]
    """
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
    """
    Get trimmed PacketTree to a packet with the specified packet_id
    :param _parser: LogParser instance
    :param packet_id: ID of the getting packet
    :return: PacketTree instance
    """
    packet_tree = get_packet_tree(_parser)
    trimmed_packet_tree = PacketTree(ts=packet_tree.ts)

    def traverse_packets(packets, trimmed_packets):
        for packet in packets:
            if hasattr(packet, "packet_id") and packet.packet_id == packet_id:
                trimmed_packets.append(copy.copy(packet))
                return True
            elif hasattr(packet, "packets"):
                new_packet = copy.copy(packet)
                new_packet.packets = []
                if traverse_packets(packet.packets, new_packet.packets):
                    trimmed_packets.append(new_packet)
                    return True
                else:
                    trimmed_packets.append(new_packet)
            else:
                trimmed_packets.append(packet)
        return False

    traverse_packets(packet_tree.packets, trimmed_packet_tree.packets)
    return trimmed_packet_tree


def get_step_count(_parser: LogParser) -> int:
    """
    Get number of steps at the game
    :param _parser: LogParser instance
    :return: number of steps
    """
    packet_tree = get_packet_tree(_parser)
    count = 0

    for packet in packet_tree.packets:
        if hasattr(packet, "packets"):
            for sub_packet in packet.packets:
                if hasattr(sub_packet, "tag"):
                    if sub_packet.tag == GameTag.STEP and sub_packet.value == Step.MAIN_START:
                        count += 1
        else:
            if hasattr(packet, "tag"):
                if packet.tag == GameTag.STEP and packet.value == Step.MAIN_START:
                    count += 1

    return count


def get_begin_step_packet_id(_parser: LogParser, step_number: int) -> int:
    """
    Get a packet id that indicates beginning of a step
    :param _parser: LogParser instance
    :param step_number: number of the step
    :return: packet_id value
    """
    packet_tree = get_packet_tree(_parser)
    count = 0

    for packet in packet_tree.packets:
        if hasattr(packet, "tag") and hasattr(packet, "value"):
            if packet.tag == GameTag.STEP and packet.value == Step.MAIN_START:
                count += 1
                if count == step_number:
                    return packet.packet_id


def get_end_step_packet_id(_parser: LogParser, step_number: int) -> int:
    """
    Get a packet id that indicates ending of a step
    :param _parser: LogParser instance
    :param step_number: number of the step
    :return: packet_id value
    """
    packet_tree = get_packet_tree(_parser)
    count = 0

    for packet in packet_tree.packets:
        if hasattr(packet, "tag") and hasattr(packet, "value"):
            if packet.tag == GameTag.STEP and packet.value == Step.MAIN_END:
                count += 1
                if count == step_number:
                    return packet.packet_id


def get_cards_by_step_begin(_parser: LogParser, step_number: int) -> list:
    """
    Get cards at the beginning of the step
    :param _parser: LogParser instance
    :param step_number: number of the step
    :return: list of cards
    """
    step_packet_id = get_begin_step_packet_id(_parser, step_number)
    trimmed_packet_tree = get_trimmed_packet_tree(_parser, step_packet_id)

    return get_cards_by_tree(trimmed_packet_tree)


def get_cards_by_step_end(_parser: LogParser, step_number: int) -> list:
    """
    Get cards at the end of the step
    :param _parser: LogParser instance
    :param step_number: number of the step
    :return: list of cards
    """
    step_packet_id = get_end_step_packet_id(_parser, step_number)
    trimmed_packet_tree = get_trimmed_packet_tree(_parser, step_packet_id)

    return get_cards_by_tree(trimmed_packet_tree)


def get_packets_by_packet_id(_parser: LogParser, packet_id: int) -> list[Packet] | None:
    """
    Get all nested packets by packet_id
    :param _parser: LogParser instance
    :param packet_id: ID of the getting packet
    :return: list of packets
    """
    packet = get_packet_by_id(_parser, packet_id)

    if hasattr(packet, "packets"):
        return packet.packets

    return None


def get_packets_by_packet_item(packet: Packet) -> list[Packet] | None:
    """
    Get all nested packets by Packet instance
    :param packet: Packet instance
    :return: list of packets
    """
    if hasattr(packet, "packets"):
        return packet.packets

    return None


def get_tags_by_packet_id(_parser: LogParser, packet_id: int) -> list[GameTag] | None:
    """
    Get all tags by packet_id
    :param _parser: LogParser instance
    :param packet_id: ID of the getting packet
    :return: list of tags
    """
    packet = get_packet_by_id(_parser, packet_id)

    if hasattr(packet, "tags"):
        return packet.tags
    if hasattr(packet, "tag"):
        return [packet.tag]

    return None


def get_tags_by_packet_item(packet: Packet) -> list[GameTag] | None:
    """
    Get all tags by Packet instance
    :param packet: Packet instance
    :return: list of tags
    """
    if hasattr(packet, "tags"):
        return packet.tags
    if hasattr(packet, "tag"):
        return [packet.tag]

    return None


def get_packets_by_step(_parser: LogParser, step_number: int) -> list[Packet]:
    """
    Get all packets by step number
    :param _parser: LogParser instance
    :param step_number: nunmber of the step
    :return: list of packets
    """

    step_packets = []
    packet_tree = get_packet_tree(_parser)
    step_begin = get_begin_step_packet_id(_parser, step_number)
    step_end = get_end_step_packet_id(_parser, step_number)
    is_step = False

    for packet in packet_tree.packets:
        if hasattr(packet, "packet_id"):
            if packet.packet_id == step_begin:
                is_step = True
                continue
            if packet.packet_id == step_end:
                is_step = False
                continue
            if is_step:
                step_packets.append(packet)

    return step_packets
