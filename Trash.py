# IMPORTS ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# <1>
# from watchdog.events import PatternMatchingEventHandler
# <1>

# IMPORTS ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# CLASSES ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# <1>
# class MyHandler(PatternMatchingEventHandler):
#     patterns = ["*/Power.log"]
#     previous_lines = []
#
#     def on_modified(self, event):
#         with open(event.src_path, 'r') as file:
#             new_lines = file.readlines()
#             added_lines = [line for line in new_lines if line not in self.previous_lines]
#             self.previous_lines = new_lines
#             if added_lines:
#                 print(f"Файл {event.src_path} был изменен:")
#                 for line in added_lines:
#                     print(line.strip())
# <1>

# CLASSES ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# FUNCTIONS ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# FUNCTIONS ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ANY CODE ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# <1>
# path = '/Applications/Hearthstone/Logs/Hearthstone_2024_04_11_11_52_46'  # Директория, которую нужно отслеживать
# event_handler = MyHandler()
# observer = Observer()
# observer.schedule(event_handler, path, recursive=True)
# observer.start()
#
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     observer.stop()
#     observer.join()
# <1>

# <2>
# for i in range(get_step_count(parser)):
#     deck_begin = get_cards_by_step_begin(parser, i + 1)
#     deck_end = get_cards_by_step_end(parser, i + 1)
#     print("STEP:", i + 1, '\n')
#     print("\tBEGIN:\n")
#     print('\t', deck_begin)
#     print("\tEND:\n")
#     print('\t', deck_end, '\n')
# <2>

# <3>
# trimmed = get_trimmed_packet_tree(parser, 486)
# print(trimmed)
# <3>

# <4>
# step_packets_list = []
#
# for i in range(1, get_step_count(parser)):
#     step_packets = get_packets_by_step(parser, i)
#     step_packets_list.append(step_packets)
#
# print(len(step_packets_list))
# <4>

# ANY CODE ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
