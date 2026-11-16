"""Scripted user messages (3 sessions x 2 messages per person) for the demo and sample buttons."""
SCRIPTS = {
    "p01": [
        ["Hi, I'm Aarav. I want to sleep better because I feel tired every afternoon. I work at a desk all day and I prefer morning workouts.",
         "I think the main problem is I scroll on my phone in bed until very late."],
        ["Hey, I tried going to bed earlier most nights this week. It was hard but I managed it.",
         "I also skipped my morning workout twice because I was busy."],
        ["Hi again! Work was stressful this week but I'm feeling a bit more rested.",
         "Can you suggest something simple I can do at my desk?"]],
    "p02": [
        ["Hello, I'm Meera. I want to lose weight and be more active. I have knee pain so I can't run or jump. I prefer evening activities.",
         "I mostly sit at a computer all day, so I rarely walk."],
        ["I didn't manage the walks this week. I was too busy and tired after work.",
         "Honestly I forget unless I have a reminder."],
        ["I tried the new routine and it fit better into my day.",
         "My knee felt okay during walking, which is a relief."]],
    "p03": [
        ["Hi, I'm Rohan. I want to improve my fitness and lower my resting heart rate. I enjoy cycling and prefer morning exercise. I sleep badly during exam stress.",
         "I usually go to bed around 1 am because of studying."],
        ["I did my cycling but I still went to bed late most nights.",
         "Exams are making me anxious."],
        ["I managed to stick to a fixed bedtime a few nights this week.",
         "I feel better in the mornings now."]],
}


def get_scripts_for_user(uid, name="User", goal="health"):
    if uid in SCRIPTS:
        return SCRIPTS[uid]
    return [
        [
            f"Hi! I'm {name}. I want to focus on {goal}. Can you assess my baseline and ask me what you need to know?",
            "I sit at a desk most of the day, have no major injuries, and prefer evening routines."
        ],
        [
            "Hey coach! I tried following the advice from last session. How are my stats looking?",
            "I had a couple of busy days where it was tough to keep up, but I stuck with the plan mostly."
        ],
        [
            "Hi again! I feel like the routine is becoming a natural habit now.",
            "What should be our next progression or milestone from here?"
        ]
    ]

