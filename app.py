import concurrent.futures
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

    step_blocks = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(process_packet, packet) for packet in packet_tree.packets]
        for future in concurrent.futures.as_completed(results):
            step_block = future.result()
            if step_block is not None:
                step_blocks.append(step_block)

    print(step_blocks)


if __name__ == "__main__":
    main()
