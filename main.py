# main.py
# Streamlit app for the Mystery Solver

import streamlit as st
import pandas as pd
from pgmpy.inference import VariableElimination
from supports.mystery_solver import build_bayesian_network, create_graphviz_plot
from supports.scenario_loader import load_case, list_available_cases

# Set up the page
st.set_page_config(page_title="Mystery Solver", layout="wide")
st.title("🕵️‍♀️ Mystery Solver: Bayesian Inference App")

# Load available cases
case_options = list_available_cases()
case_id_to_title = {case['case_id']: case['title'] for case in case_options}
selected_case_id = st.sidebar.selectbox("Select a Mystery Case", options=list(case_id_to_title.keys()), format_func=lambda x: case_id_to_title[x])

# Load selected case data
case_data = load_case(selected_case_id)
st.subheader(case_data['title'])
st.markdown(f"**Case Description:** {case_data['description']}")

# Build and visualize the model
model = build_bayesian_network()
inference = VariableElimination(model)

graph_viz = create_graphviz_plot(model)
if graph_viz:
    st.graphviz_chart(graph_viz)

# Sidebar: Clue Inputs
st.sidebar.header("Input Clues")
evidence_dict = {}

for clue in case_data['evidence']:
    node = clue['node']
    label = clue['label']
    if node == 'FingerprintMatch':
        options = ['Unknown', 'None', 'A', 'B', 'C', 'D', 'E']
        selected = st.sidebar.selectbox(label, options=options, index=0)
        if selected != 'Unknown':
            evidence_dict[node] = selected
    elif node == 'WeaponUsed':
        options = ['Unknown', 'CuttingTool', 'HackingDevice', 'AcidSpray', 'None']
        selected = st.sidebar.selectbox(label, options=options, index=0)
        if selected != 'Unknown':
            evidence_dict[node] = selected
    else:
        selected = st.sidebar.radio(label, options=['Unknown', 'Yes', 'No'], index=0, horizontal=True)
        if selected != 'Unknown':
            evidence_dict[node] = selected

# Run inference
st.markdown("---")
st.header("🔍 Inference Results")
if st.button("Solve Case"):
    st.subheader("Evidence Entered:")
    st.json(evidence_dict)

    try:
        result = inference.query(variables=['GuiltyParty'], evidence=evidence_dict)
        df = pd.DataFrame({
            'Suspect': result.state_names['GuiltyParty'],
            'Probability': result.values
        })
        df = df.sort_values(by='Probability', ascending=False)
        df['% Probability'] = df['Probability'].map(lambda x: f"{x:.2%}")

        st.subheader("Posterior Probability of Guilt:")
        st.dataframe(df[['Suspect', '% Probability']], use_container_width=True)

        chart_data = pd.DataFrame(df['Probability'].values, index=df['Suspect'].values, columns=['Probability'])
        st.bar_chart(chart_data)

    except Exception as e:
        st.error(f"Inference failed: {e}")
else:
    st.info("Enter clues on the left and click 'Solve Case'.")
