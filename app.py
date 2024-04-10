from Helpers.packets_helper import *
from constants import *

parser = LogParser()


def main():
    with open(LAST_LOG_PATH) as f:
        parser.read(f)
    packet_tree = parser.games[0]

    cards = get_cards_by_step_end(parser, 3)

    packet_tree = get_packet_tree(parser)

    # for i in range(get_step_count(parser)):
    #     deck_begin = get_cards_by_step_begin(parser, i + 1)
    #     deck_end = get_cards_by_step_end(parser, i + 1)
    #     print("STEP:", i + 1, '\n')
    #     print("\tBEGIN:\n")
    #     print('\t', deck_begin)
    #     print("\tEND:\n")
    #     print('\t', deck_end, '\n')
    #

    # trimmed = get_trimmed_packet_tree(parser, 486)
    # print(trimmed)

    # step_packets_list = []
    #
    # for i in range(1, get_step_count(parser)):
    #     step_packets = get_packets_by_step(parser, i)
    #     step_packets_list.append(step_packets)
    #
    # print(len(step_packets_list))


if __name__ == "__main__":
    main()
