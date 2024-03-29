"""MAPIO leds controls."""

import logging
from pathlib import Path


class LED:
    """Defines a led object."""

    def __init__(self, number: int, color: str) -> None:
        """Initialise led object.

        Args:
            number (int): led number
            color (str): led color
        """
        self.logger = logging.getLogger(__name__)
        color = color.upper()
        self.number = number
        self.is_blinking = False

        if number in [1, 2, 3] and color in ["G", "R", "B"]:
            self.led_path = "/sys/class/leds/LED" + str(number) + "_" + color
        else:
            self.logger.warning("Wrong led parameters")

    def on(self) -> None:
        """Set a led to ON."""
        try:
            with Path.open(Path(f"{self.led_path}/brightness"), "w") as brightness:
                brightness.write("1")
        except OSError:
            self.logger.warning("Unknown led")

    def off(self) -> None:
        """Set a led to OFF."""
        try:
            with Path.open(Path(f"{self.led_path}/brightness"), "w") as brightness:
                brightness.write("0")
                self.is_blinking = False
        except OSError:
            self.logger.warning("Unknown led")

    def blink(self) -> bool:
        """Make a led blinking.

        Returns:
            bool: True if the led has started to blink
        """
        try:
            # Test if LED is already blinking
            with Path.open(Path(f"{self.led_path}/trigger")) as trigger:
                if "[timer]" in trigger.read():
                    # Nothing to do
                    return False
            with Path.open(Path(f"{self.led_path}/trigger"), "w") as trigger:
                trigger.write("timer")
                self.is_blinking = True
                return True

        except OSError:
            self.logger.warning("Unknown led")
            return False

    def reset(self, number: int) -> None:
        """Reset all color for a specific led."""
        try:
            for color in ["R", "G", "B"]:
                path = "/sys/class/leds/LED" + str(number) + "_" + color + "/brightness"
                with Path.open(Path(path), "w") as led:
                    led.write("0")
                path = "/sys/class/leds/LED" + str(number) + "_" + color + "/trigger"
                with Path.open(Path(path), "w") as led:
                    led.write("none")
                    self.is_blinking = False
        except OSError:
            self.logger.warning("Unknown led")
