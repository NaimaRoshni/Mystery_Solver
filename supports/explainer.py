# explainer.py
# Generates a natural-language explanation for the inference results

def explain_top_suspect(case_data, evidence, inference_result):
    """
    Generates a basic explanation for the top suspect using evidence and probability.

    Args:
        case_data (dict): Loaded scenario with suspect descriptions.
        evidence (dict): Clues provided by the user.
        inference_result (pgmpy inference result): Result of inference.query()

    Returns:
        str: A narrative explanation string
    """
    try:
        suspects = inference_result.state_names['GuiltyParty']
        probs = inference_result.values

        top_index = probs.argmax()
        top_suspect = suspects[top_index]
        top_prob = probs[top_index]

        name = case_data['suspects'][top_suspect]['name']
        description = case_data['suspects'][top_suspect]['description']

        clues = []
        for clue_key, clue_value in evidence.items():
            if top_suspect in clue_value or clue_key in ['Motive', 'WitnessStatement']:
                clues.append(f"**{clue_key}** = {clue_value}")

        if not clues:
            clues.append("limited supporting evidence")

        return (
            f"🕵️‍♂️ **Verdict:** {name} is the most likely suspect with a probability of {top_prob:.2%}.\n"
            f"\n> {description}\n"
            f"\nBased on clues like: {', '.join(clues)}."
        )

    except Exception as e:
        return f"❌ Unable to generate explanation: {e}"
