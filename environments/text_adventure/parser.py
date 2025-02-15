import re
from typing import Optional
from .actions import TextAdventureGameAction

class ResponseParser:
    @staticmethod
    def _brute_parse(answer: str) -> Optional[str]:
        answer = re.sub(r'<think>(.*?)</think>', '', answer)
        answer = answer.strip().lower()

        action_counts = {
            "up": answer.count("up"),
            "down": answer.count("down"),
            "left": answer.count("left"),
            "right": answer.count("right")
        }

        if sum(action_counts.values()) == 0:
            return None

        return max(action_counts, key=action_counts.get)
                
    @staticmethod
    def parse_answer(answer: Optional[str]) -> TextAdventureGameAction:
        if answer:
            tag_match = re.search(r'<answer>(.*?)</answer>', answer)
            box_match = re.search(r'\\boxed{\\text{(.*?)}}', answer)
            brute_match = ResponseParser._brute_parse(answer)
            
            action = None
            if tag_match:
                action = tag_match.group(1).strip().lower()
            elif box_match:
                action = box_match.group(1).strip().lower()
            elif brute_match:
                action = brute_match
            
            if action:
                if action == "up":
                    return TextAdventureGameAction.UP
                elif action == "down":
                    return TextAdventureGameAction.DOWN
                elif action == "left":
                    return TextAdventureGameAction.LEFT
                elif action == "right":
                    return TextAdventureGameAction.RIGHT

        return TextAdventureGameAction.UP