import json

question_bank = {
    'basics': [
        "Tell me about yourself.",
        "Can you share your biography or professional background?"
    ],
    'project': [
        "Describe one of your projects in detail, including the challenges you faced and how you overcame them."
    ],
    'hobbies': [
        "What are your hobbies and how do they contribute to your personal development?"
    ],
    'logical_thinking': [
        "If you have 8 balls, one of which is heavier than the others, how can you find the heavy ball using a balance scale in just 2 weighings?",
        "You have 12 coins, one of which is counterfeit (either heavier or lighter). Using a balance scale, how can you identify the counterfeit coin and determine if it's heavier or lighter in 3 weighings?",
        "A lily pad doubles in size every day. If it takes 30 days to cover the entire pond, on which day does it cover half the pond?",
        "You have three boxes, one with two gold coins, one with two silver coins, and one with one gold and one silver. Labels are wrong. Pick one coin from the box labeled 'mixed' - if gold, that box is gold; if silver, the other unlabeled is gold."
    ]
}

with open('questions.json', 'w') as f:
    json.dump(question_bank, f, indent=4)
