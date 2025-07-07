# mystery_solver.py
# Custom version: Midnight Gala Heist with 5 suspects and extended evidence

import graphviz
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD

def build_bayesian_network():
    """
    Builds a Bayesian Network for the "Midnight Gala Heist" mystery.
    Includes 5 suspects and multiple types of evidence.
    """
    model = DiscreteBayesianNetwork([
        ('GuiltyParty', 'AlibiA'),
        ('GuiltyParty', 'AlibiB'),
        ('GuiltyParty', 'AlibiC'),
        ('GuiltyParty', 'AlibiD'),
        ('GuiltyParty', 'AlibiE'),
        ('GuiltyParty', 'Motive'),
        ('GuiltyParty', 'WitnessStatement'),
        ('GuiltyParty', 'FingerprintMatch'),
        ('GuiltyParty', 'ForcedEntry'),
        ('GuiltyParty', 'SecurityFootage'),
        ('GuiltyParty', 'WeaponUsed')
    ])

    # P(GuiltyParty) - Prior
    cpd_gp = TabularCPD(
        variable='GuiltyParty', variable_card=5,
        values=[[1/5], [1/5], [1/5], [1/5], [1/5]],
        state_names={'GuiltyParty': ['A', 'B', 'C', 'D', 'E']}
    )

    def binary_cpd(name, probs_yes):
        return TabularCPD(
            variable=name, variable_card=2,
            values=[probs_yes, [1 - p for p in probs_yes]],
            evidence=['GuiltyParty'], evidence_card=[5],
            state_names={name: ['Yes', 'No'], 'GuiltyParty': ['A', 'B', 'C', 'D', 'E']}
        )

    # Alibis
    cpd_alibia = binary_cpd('AlibiA', [0.2, 0.9, 0.9, 0.8, 0.95])
    cpd_alibib = binary_cpd('AlibiB', [0.85, 0.3, 0.85, 0.9, 0.95])
    cpd_alibic = binary_cpd('AlibiC', [0.9, 0.9, 0.4, 0.85, 0.95])
    cpd_alibid = binary_cpd('AlibiD', [0.75, 0.8, 0.8, 0.2, 0.9])
    cpd_alibie = binary_cpd('AlibiE', [0.95, 0.95, 0.95, 0.9, 0.3])

    # Motive & Witness
    cpd_motive = binary_cpd('Motive', [0.7, 0.6, 0.5, 0.3, 0.2])
    cpd_witness = binary_cpd('WitnessStatement', [0.6, 0.4, 0.3, 0.5, 0.2])

    # Other Binary Clues
    cpd_forced = binary_cpd('ForcedEntry', [0.1, 0.2, 0.4, 0.7, 0.1])
    cpd_footage = binary_cpd('SecurityFootage', [0.2, 0.3, 0.5, 0.6, 0.4])

    cpd_fingerprint = TabularCPD(
    variable='FingerprintMatch', variable_card=6,
    values=[
        [0.4, 0.4, 0.3, 0.3, 0.2],   # None
        [0.4, 0.1, 0.2, 0.2, 0.2],   # Match A
        [0.05, 0.4, 0.1, 0.1, 0.1],  # Match B
        [0.05, 0.05, 0.2, 0.1, 0.1], # Match C
        [0.05, 0.05, 0.1, 0.2, 0.1], # Match D
        [0.05, 0.0, 0.1, 0.1, 0.3]   # Match E
    ],
    evidence=['GuiltyParty'], evidence_card=[5],
    state_names={'FingerprintMatch': ['None', 'A', 'B', 'C', 'D', 'E'],
                 'GuiltyParty': ['A', 'B', 'C', 'D', 'E']}
    )


    # WeaponUsed (multi-category)
    cpd_weapon = TabularCPD(
        variable='WeaponUsed', variable_card=4,
        values=[
            [0.1, 0.1, 0.2, 0.6, 0.1],  # CuttingTool
            [0.2, 0.5, 0.1, 0.1, 0.1],  # HackingDevice
            [0.1, 0.1, 0.6, 0.2, 0.1],  # AcidSpray
            [0.6, 0.3, 0.1, 0.1, 0.7]   # None
        ],
        evidence=['GuiltyParty'], evidence_card=[5],
        state_names={'WeaponUsed': ['CuttingTool', 'HackingDevice', 'AcidSpray', 'None'],
                     'GuiltyParty': ['A', 'B', 'C', 'D', 'E']}
    )

    # Add all CPDs to the model
    model.add_cpds(
        cpd_gp, cpd_alibia, cpd_alibib, cpd_alibic, cpd_alibid, cpd_alibie,
        cpd_motive, cpd_witness, cpd_forced, cpd_footage,
        cpd_fingerprint, cpd_weapon
    )

    # Validate structure
    if not model.check_model():
        raise ValueError("Model definition is invalid. Check CPDs and structure.")

    return model

def create_graphviz_plot(model):
    """
    Creates a graphviz Digraph object representing the BN structure.
    """
    if not graphviz:
        print("Warning: Graphviz not available.")
        return None

    dot = graphviz.Digraph(comment='Bayesian Network Structure', graph_attr={'rankdir': 'TB'})
    for node in model.nodes():
        dot.node(node, node)
    for edge in model.edges():
        dot.edge(*edge)
    return dot
