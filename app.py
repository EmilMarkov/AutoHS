import concurrent.futures

from hearthstone.enums import Step
from hslog.packets import Block
from Helpers.packets_helper import *

parser = LogParser()


def process_packet(packet):
    if type(packet) is Block:
        for sub_packet in get_packets_by_packet_item(packet):
            if (type(sub_packet) is not Block) and hasattr(sub_packet, "packet_id"):
                tags = get_tags_by_packet_id(parser, sub_packet.packet_id)
                if tags is not None:
                    for tag in tags:
                        if tag == GameTag.STEP:
                            print(tag)
                            return packet
    return None


def main():
    with open("/Applications/Hearthstone/Logs/Hearthstone_2024_04_04_19_29_05/Power.log") as f:
        parser.read(f)
    packet_tree = parser.games[0]

    # step_blocks = []
    #
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     results = [executor.submit(process_packet, packet) for packet in packet_tree.packets]
    #     for future in concurrent.futures.as_completed(results):
    #         step_block = future.result()
    #         if step_block is not None:
    #             step_blocks.append(step_block)
    #
    # print(step_blocks)

    cards = get_cards_by_step_end(parser, 3)

    packet_tree = get_packet_tree(parser)

    # for packet in packet_tree.packets:
    #     if hasattr(packet, "packets"):
    #         for sub_packet in packet.packets:
    #             if hasattr(sub_packet, "tag"):
    #                 if sub_packet.tag == GameTag.STEP and sub_packet.value == Step.MAIN_START:
    #                     print("main_start", sub_packet.tag)
    #     else:
    #         if hasattr(packet, "tag"):
    #             if packet.tag == GameTag.STEP and packet.value == Step.MAIN_START:
    #                 print("main_start", packet.value)

    for i in range(get_step_count(parser)):
        deck_begin = get_cards_by_step_begin(parser, i + 1)
        deck_end = get_cards_by_step_end(parser, i + 1)
        print("STEP:", i + 1, '\n')
        print("\tBEGIN:\n")
        print('\t', deck_begin)
        print("\tEND:\n")
        print('\t', deck_end, '\n')

    # trimmed = get_trimmed_packet_tree(parser, 486)
    # print(trimmed)


if __name__ == "__main__":
    main()
