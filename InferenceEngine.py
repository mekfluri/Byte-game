class InferenceEngine:
    def __init__(self):
        self.rules = []

    def add_rule(self, condition, action):
        rule = Rule(condition, action)
        self.rules.append(rule)

    def infer(self, facts):
        for rule in self.rules:
            if rule.condition(facts):
                rule.action(facts)


class Rule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action
