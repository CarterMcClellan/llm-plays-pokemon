from agents.lcpp_agent import LlamaCppAgent

if __name__ == "__main__":
    agent = LlamaCppAgent({"debug": False})
    response = agent.get_action_raw("What is 1+1?")
    print(response)