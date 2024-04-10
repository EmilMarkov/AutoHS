from hslog import LogParser
from hsreplay.document import HSReplayDocument
import xml.etree.ElementTree as ET


def save_xml_to_file(xml_content, file_path):
    """
    Save XML content to a file.

    Args:
    xml_content (str): XML content to be saved.
    file_path (str): File path where XML will be saved.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(xml_content)
        print(f"XML content successfully saved to {file_path}")
    except Exception as e:
        print(f"Error occurred while saving XML to {file_path}: {e}")


parser = LogParser()

with open("/Applications/Hearthstone/Logs/Hearthstone_2024_04_04_19_29_05/Power.log") as f:
    parser.read(f)

xml = HSReplayDocument.from_parser(parser, build=None).to_xml(pretty=True)
save_xml_to_file(xml, "./log.xml")
