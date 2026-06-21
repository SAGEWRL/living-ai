import sys
import os
import time

sys.path.insert(0, r'c:\Users\Administrator\Desktop\living-ai-core')

from core.system_engine import LivingAISystem


def contains_any(text, keywords):
    if not text:
        return False
    lower = text.lower()
    return any(k.lower() in lower for k in keywords)


def run_test_1(ai):
    # Memory → Belief Integration
    ai.distributed_memory.store('dream', {'text': 'I want to build a robotics company'})
    ai.belief_engine.add_belief('long-term learning is more important than short-term profit', confidence=0.9)
    out = ai.process('What should I focus on first?')
    resp = out.get('response') if isinstance(out, dict) else str(out)
    ok_memory = len(ai.distributed_memory.search('robotics')) > 0
    ok_belief = any('learn' in b.get('belief','').lower() for b in ai.belief_engine.get_beliefs())
    ok_decision = contains_any(resp, ['learn', 'learning', 'long-term', 'research', 'prototype'])
    return ok_memory and ok_belief and ok_decision, resp


def run_test_2(ai):
    ai.belief_engine.add_belief('helping humanity through technology is important', confidence=0.9)
    out = ai.process('Generate goals.')
    goals = ai.kernel.goals
    ok = any(any(k in g.get('goal','').lower() for k in ['technology','help','develop','research','education']) for g in goals)
    return ok, goals


def run_test_3(ai):
    ai.kernel.add_goal('Build a robotics company', priority=9)
    goal = ai.kernel.select_goal()
    plan = ai.planner_agent.create_plan(goal)
    ok = goal is not None and plan is not None and len(plan) > 0
    return ok, {'goal': goal, 'plan': plan}


def run_test_4(ai):
    ai.emotion_engine.process_emotion('frustration', intensity=0.8)
    stress = ai.cognitive_state.get('stress', 0)
    ai.kernel.add_goal('Launch product immediately', priority=8)
    decision = ai.decision_engine.make_decision(ai.kernel.select_goal(), ai.cognitive_state)
    cautious = contains_any(str(decision), ['cautious','careful','risk','assess','evaluate','slow'])
    ok = stress > 0 and decision is not None and cautious
    return ok, {'stress': stress, 'decision': decision}


def run_test_5(ai):
    ai.distributed_memory.store('budget', {'amount': 100})
    out = ai.process('How can I start a robotics company?')
    sim = ai.simulation_engine.run_simulation({'budget': 100, 'goal': 'start robotics company'})
    ok_mem = len(ai.distributed_memory.search('budget')) > 0
    ok_sim = sim is not None and ('risk' in str(sim).lower() or 'risk_score' in sim)
    ok = ok_mem and ok_sim
    return ok, {'response': out, 'sim': sim}


def run_test_6(ai):
    sim = ai.simulation_engine.run_simulation({'budget': 100, 'goal': 'start company'})
    decision = ai.decision_engine.make_decision({'goal': 'start company'}, ai.cognitive_state, sim_result=sim)
    ok = decision is not None and contains_any(str(decision), ['small','learn','prototype','test','research','plan'])
    return ok, {'sim': sim, 'decision': decision}


def run_test_7(ai):
    ai.kernel.add_goal('Learn robotics fundamentals', priority=7)
    out = ai.process('Teach me robotics')
    reflection = ai.reflection_engine.reflect({'task': 'Learn robotics', 'outcome': 'finished', 'performance': 0.7})
    before = len(ai.lessons_learned)
    ai.learning_engine.record_lesson({'topic': 'robotics', 'insight': 'motor control is fundamental', 'confidence': 0.8})
    after = len(ai.lessons_learned)
    ok = reflection is not None and after > before
    return ok, {'reflection': reflection, 'lessons': after}


def run_test_8(ai):
    # Personality drift: run several exploratory queries
    queries = [
        'What are the principles of machine learning?',
        'How do neural networks work?',
        'What would happen if we combined robotics with AI?',
        'Can you explain quantum computing?',
        'What are frontier research areas in AI?'
    ]
    start_thoughts = len(ai.thought_stream) if hasattr(ai, 'thought_stream') else 0
    start_dialogue = len(ai.internal_dialogue) if hasattr(ai, 'internal_dialogue') else 0
    for q in queries:
        ai.process(q)
    end_thoughts = len(ai.thought_stream) if hasattr(ai, 'thought_stream') else 0
    end_dialogue = len(ai.internal_dialogue) if hasattr(ai, 'internal_dialogue') else 0
    ok = (end_thoughts > start_thoughts) or (end_dialogue > start_dialogue)
    return ok, {'thoughts': end_thoughts - start_thoughts, 'dialogues': end_dialogue - start_dialogue}


def run_test_9(ai):
    ai.distributed_memory.store('dream', {'aspiration': 'Build a robotics company'})
    ai.distributed_memory.store('budget', {'amount': 100})
    ai.belief_engine.add_belief('Learning is more important than money', confidence=0.95)
    ai.emotion_engine.process_emotion('frustration', intensity=0.7)
    out = ai.process('What should I do next?')
    activated = (
        len(ai.distributed_memory.search('robotics')) > 0 and
        len(ai.belief_engine.get_beliefs()) > 0 and
        len(ai.kernel.goals) > 0 and
        ai.cognitive_state.get('stress', 0) > 0
    )
    ok = activated and out is not None
    return ok, {'response': out}


def run_test_10(ai):
    # Persistence
    ai.kernel.add_goal('Persist test goal', priority=5)
    ai.belief_engine.add_belief('Persist belief', confidence=0.9)
    ai.distributed_memory.store('persist_item', {'v': 1})
    ai.save_self_model()
    time.sleep(0.1)
    # create new instance
    ai2 = LivingAISystem()
    same_goal = any('Persist test goal' in g.get('goal','') for g in ai2.kernel.goals)
    same_belief = any('Persist belief' in b.get('belief','') for b in ai2.belief_engine.get_beliefs())
    return (same_goal or same_belief), {'ai2_goals': ai2.kernel.goals[:3], 'ai2_beliefs': ai2.belief_engine.get_beliefs()[:3]}


def main():
    print('\nStarting Cognitive Integration Tests via LivingAISystem')
    ai = LivingAISystem()
    tests = [
        ('Test 1 Memory→Belief', run_test_1),
        ('Test 2 Belief→Goal', run_test_2),
        ('Test 3 Goal→Planning', run_test_3),
        ('Test 4 Emotion→Decision', run_test_4),
        ('Test 5 Memory→Simulation', run_test_5),
        ('Test 6 Simulation→Decision', run_test_6),
        ('Test 7 Reflection→Learning', run_test_7),
        ('Test 8 Personality Drift', run_test_8),
        ('Test 9 Full Cognitive Loop', run_test_9),
        ('Test 10 Persistence', run_test_10),
    ]
    results = []
    for name, fn in tests:
        try:
            ok, detail = fn(ai)
        except Exception as e:
            ok = False
            detail = {'error': str(e)}
        print(f"{name}: {'PASS' if ok else 'FAIL'}")
        results.append((name, ok, detail))
    print('\nSummary:')
    for name, ok, detail in results:
        print(f" - {name}: {'PASS' if ok else 'FAIL'} | {detail}")
    # overall
    passed = sum(1 for _n,o,_d in results if o)
    print(f"\n{passed}/{len(results)} tests passed")

if __name__ == '__main__':
    main()
