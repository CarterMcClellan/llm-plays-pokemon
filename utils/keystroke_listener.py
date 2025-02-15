import Quartz
from AppKit import NSEvent
import time
from collections import defaultdict
import subprocess
import contextlib
from typing import TypedDict, Callable

class ModernKeyController:
    def __init__(self):
        # Common modifier masks
        self.modifier_masks = {
            'shift': Quartz.kCGEventFlagMaskShift,
            'caps': Quartz.kCGEventFlagMaskAlphaShift,
            'alt': Quartz.kCGEventFlagMaskAlternate,
            'ctrl': Quartz.kCGEventFlagMaskControl,
            'cmd': Quartz.kCGEventFlagMaskCommand
        }
        
        # Track modifier states
        self.current_modifiers = {
            "shift": False,
            "caps": False,
            "alt": False,
            "ctrl": False,
            "cmd": False,
        }

        self.keycode_map = {
            # Letters
            0x00: 'a',
            0x01: 's',
            0x02: 'd',
            0x03: 'f',
            0x04: 'h',
            0x05: 'g',
            0x06: 'z',
            0x07: 'x',
            0x08: 'c',
            0x09: 'v',
            0x0B: 'b',
            0x0C: 'q',
            0x0D: 'w',
            0x0E: 'e',
            0x0F: 'r',
            0x10: 'y',
            0x11: 't',
            0x12: '1',
            0x13: '2',
            0x14: '3',
            0x15: '4',
            0x16: '6',
            0x17: '5',
            0x18: '=',
            0x19: '9',
            0x1A: '7',
            0x1B: '-',
            0x1C: '8',
            0x1D: '0',
            0x1E: ']',
            0x1F: 'o',
            0x20: 'u',
            0x21: '[',
            0x22: 'i',
            0x23: 'p',
            0x24: 'return',
            0x25: 'l',
            0x26: 'j',
            0x27: "'",
            0x28: 'k',
            0x29: ';',
            0x2A: '\\',
            0x2B: ',',
            0x2C: '/',
            0x2D: 'n',
            0x2E: 'm',
            0x2F: '.',
            0x30: 'tab',
            0x31: 'space',
            0x32: '`',
            0x33: 'delete',
            0x35: 'escape',
            
            # Modifier keys
            0x37: 'command',
            0x38: 'shift',
            0x39: 'capslock',
            0x3A: 'option',
            0x3B: 'control',
            0x3C: 'right shift',
            0x3D: 'right option',
            0x3E: 'right control',
            0x3F: 'function',
            
            # Function keys
            0x7A: 'f1',
            0x78: 'f2',
            0x63: 'f3',
            0x76: 'f4',
            0x60: 'f5',
            0x61: 'f6',
            0x62: 'f7',
            0x64: 'f8',
            0x65: 'f9',
            0x6D: 'f10',
            0x67: 'f11',
            0x6F: 'f12',
            0x69: 'f13',
            0x6B: 'f14',
            0x71: 'f15',
            0x6A: 'f16',
            0x40: 'f17',
            0x4F: 'f18',
            0x50: 'f19',
            0x5A: 'f20',
            
            # Arrow keys
            0x7B: 'left',
            0x7C: 'right',
            0x7D: 'down',
            0x7E: 'up',
            
            # Special keys
            0x72: 'help',
            0x73: 'home',
            0x74: 'page_up',
            0x75: 'forward_delete',
            0x77: 'end',
            0x79: 'page_down',
            
            # Keypad keys
            0x41: 'keypad_decimal',
            0x43: 'keypad_multiply',
            0x45: 'keypad_plus',
            0x47: 'keypad_clear',
            0x4B: 'keypad_divide',
            0x4C: 'keypad_enter',
            0x4E: 'keypad_minus',
            0x51: 'keypad_equals',
            0x52: 'keypad_0',
            0x53: 'keypad_1',
            0x54: 'keypad_2',
            0x55: 'keypad_3',
            0x56: 'keypad_4',
            0x57: 'keypad_5',
            0x58: 'keypad_6',
            0x59: 'keypad_7',
            0x5B: 'keypad_8',
            0x5C: 'keypad_9',
        }

    def press(self, keycode):
        """Send a keydown event"""
        # Update modifier state if it's a modifier key
        self._update_modifier_state(keycode, True)
        
        # Create and post the event
        event = Quartz.CGEventCreateKeyboardEvent(None, keycode, True)
        self._apply_current_modifiers(event)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
        time.sleep(0.01)

    def release(self, keycode):
        """Send a keyup event"""
        # Update modifier state if it's a modifier key
        self._update_modifier_state(keycode, False)
        
        # Create and post the event
        event = Quartz.CGEventCreateKeyboardEvent(None, keycode, False)
        self._apply_current_modifiers(event)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
        time.sleep(0.01)

    def _update_modifier_state(self, keycode, is_press):
        """Update internal modifier state based on key events"""
        if keycode == 0x37:  # cmd
            self.current_modifiers["cmd"] = is_press
        elif keycode in (0x38, 0x3C):  # shift or right shift
            self.current_modifiers["shift"] = is_press
        elif keycode == 0x39:  # caps lock
            self.current_modifiers["caps"] = is_press
        elif keycode == 0x3A:  # alt
            self.current_modifiers["alt"] = is_press
        elif keycode == 0x3B:  # ctrl
            self.current_modifiers["ctrl"] = is_press

    def _apply_current_modifiers(self, event):
        """Apply current modifier states to an event"""
        flags = 0
        for mod, active in self.current_modifiers.items():
            if active and mod in self.modifier_masks:
                flags |= self.modifier_masks[mod]
        Quartz.CGEventSetFlags(event, flags)

    def get_key_name(self, keycode):
        """Convert keycode to key name"""
        return self.keycode_map.get(keycode, f"unknown_{keycode}")

class KeyEvent(TypedDict):
    type: str  # "up" or "down"
    keycode: int
    name: str
    flags: int

class ModernKeyboardListener:
    def __init__(self, callback: Callable[[KeyEvent], None], blocking=False):
        self.callback = callback
        self.blocking = blocking
        self.listening = True
        self.controller = ModernKeyController()
        
    def run(self):
        """Start listening for keyboard events"""
        def handler(proxy, type_, event, refcon):
            if not self.listening:
                return None
                
            keycode = Quartz.CGEventGetIntegerValueField(
                event,
                Quartz.kCGKeyboardEventKeycode
            )
            
            flags = Quartz.CGEventGetFlags(event)
            
            if type_ == Quartz.kCGEventKeyDown:
                event_type = "down"
            elif type_ == Quartz.kCGEventKeyUp:
                event_type = "up"
            else:
                return event if not self.blocking else None
                
            # Create event object (you can customize this based on your needs)
            key_event = {
                'type': event_type,
                'keycode': keycode,
                'name': self.controller.get_key_name(keycode),
                'flags': flags
            }
            
            self.callback(key_event)
            return None if self.blocking else event

        # Create event tap
        tap = Quartz.CGEventTapCreate(
            Quartz.kCGSessionEventTap,
            Quartz.kCGHeadInsertEventTap,
            Quartz.kCGEventTapOptionDefault,
            Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown) |
            Quartz.CGEventMaskBit(Quartz.kCGEventKeyUp),
            handler,
            None
        )

        if tap is None:
            raise Exception("Failed to create event tap")

        # Create and add to run loop
        run_loop_source = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
        loop = Quartz.CFRunLoopGetCurrent()
        Quartz.CFRunLoopAddSource(loop, run_loop_source, Quartz.kCFRunLoopDefaultMode)
        Quartz.CGEventTapEnable(tap, True)

        while self.listening:
            Quartz.CFRunLoopRunInMode(Quartz.kCFRunLoopDefaultMode, 5, False)

    def stop(self):
        """Stop listening for events"""
        self.listening = False


def echooff():
    subprocess.run(['stty', '-echo'], check=True)
def echoon():
    subprocess.run(['stty', 'echo'], check=True)

@contextlib.contextmanager
def echo_disabled():
    try:
        echooff()
        yield
    finally:
        echoon()

def example_usage():
    # Example callback function
    def print_event(event):
        print(f"Key {event['type']}: {event['name']} (keycode: {event['keycode']})")

    # Create and start listener
    listener = ModernKeyboardListener(print_event)

    with echo_disabled():
        try:
            print("Listening for keyboard events... Press Ctrl+C to stop")
            listener.run()
        except KeyboardInterrupt:
            listener.stop()
            print("\nStopped listening for keyboard events")

if __name__ == "__main__":
    example_usage()