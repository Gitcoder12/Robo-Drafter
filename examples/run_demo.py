from robo_drafter import AdaptiveAgent

if __name__ == "__main__":
    agent = AdaptiveAgent("config/default.yaml")
    agent.run_workflow(["pick_and_place", "navigate", "pick_and_place"])
    agent.save_policy("config/learned_policy.yaml")
