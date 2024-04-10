from enum import Enum
from hslog.packets import Packet


class ActionType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    ACTIVATE = "ACTIVATE"
    CHANGE_ZONE = "CHANGE_ZONE"


class Action:
    """
    Represents an action object constructed from a set of packets.

    Attributes:
        packets (list): A list of packets that constitute the action.
        action_type (ActionType): The type of action performed.
        details (dict): Additional details or metadata associated with the action.

    Methods:
        add_packet(packet): Adds a packet to the action.
        get_action_type(): Returns the type of action performed.
        get_details(): Returns the additional details or metadata associated with the action.
        to_dict(): Converts the Action object to a dictionary.
    """

    def __init__(self, packets: list[Packet], action_type: ActionType):
        self.packets = []
        self.action_type = action_type
        self.details = {}

    def get_action_type(self):
        """
        Returns the type of action performed.

        Returns:
            ActionType: The type of action performed.
        """
        return self.action_type

    def get_details(self):
        """
        Returns the additional details or metadata associated with the action.

        Returns:
            dict: Additional details or metadata associated with the action.
        """
        return self.details

    def to_dict(self):
        """
        Converts the Action object to a dictionary.

        Returns:
            dict: A dictionary representation of the Action object.
        """
        return {
            "action_type": self.action_type.value,
            "details": self.details,
            "packets": [packet.to_dict() for packet in self.packets]
        }