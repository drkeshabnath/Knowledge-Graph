import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# Set up page
st.set_page_config(page_title="Interactive Biomedical Knowledge Graph", layout="wide")
st.title("Drug–Disease–Biomarker Knowledge Graph")
st.markdown("Explore how **knowledge graphs** connect real-world medical concepts through drugs, diseases, and biomarkers.")

# Generate synthetic 100-row dataset
@st.cache_data
def load_data():
    drugs = ["Aspirin", "Metformin", "Atorvastatin", "Insulin", "Losartan", "Paracetamol", "Ibuprofen", "Omeprazole", "Amoxicillin", "Ciprofloxacin"]
    diseases = ["Heart Attack", "Type 2 Diabetes", "Stroke", "Hypertension", "PCOS", "Arthritis", "Acid Reflux", "Infection", "Asthma", "Migraine"]
    biomarkers = ["CRP", "HbA1c", "LDL", "Glucose", "BP", "Insulin", "ESR", "pH", "WBC Count", "Serotonin"]
    data = []
    for _ in range(100):
        data.append({
            "Drug": random.choice(drugs),
            "Disease": random.choice(diseases),
            "Biomarker": random.choice(biomarkers)
        })
    return pd.DataFrame(data)

df = load_data()

# Display dataset
st.subheader("📋 Dataset: 100 Drug–Disease–Biomarker Records")
st.dataframe(df)

# Build the graph
G = nx.Graph()
for row in df.itertuples(index=False):
    G.add_node(row.Drug, type='Drug')
    G.add_node(row.Disease, type='Disease')
    G.add_node(row.Biomarker, type='Biomarker')
    G.add_edge(row.Drug, row.Disease, relation='treats')
    G.add_edge(row.Disease, row.Biomarker, relation='indicated_by')

# Subgraph filter
st.subheader("Explore Subgraph by Selecting a Drug or Disease")
all_entities = sorted(set(df['Drug'].unique()).union(df['Disease'].unique()))
selected_entity = st.selectbox("Select a Drug or Disease:", all_entities)

H = nx.ego_graph(G, selected_entity, radius=1)
fig1, ax1 = plt.subplots(figsize=(10, 6))
pos1 = nx.spring_layout(H, seed=42)
node_colors = ['lightblue' if H.nodes[n]['type'] == 'Drug' else 'lightgreen' if H.nodes[n]['type'] == 'Disease' else 'salmon' for n in H.nodes]
nx.draw(H, pos1, with_labels=True, node_color=node_colors, node_size=1000, font_size=9, ax=ax1)
nx.draw_networkx_edge_labels(H, pos1, edge_labels=nx.get_edge_attributes(H, 'relation'), font_color='red', ax=ax1)
plt.axis('off')
st.pyplot(fig1)



# Show full graph (optional)
if st.checkbox("Show Full Knowledge Graph"):
    st.subheader("Full Knowledge Graph")
    fig2, ax2 = plt.subplots(figsize=(14, 10))
    pos2 = nx.spring_layout(G, seed=42)
    node_colors2 = ['lightblue' if G.nodes[n]['type'] == 'Drug' else 'lightgreen' if G.nodes[n]['type'] == 'Disease' else 'salmon' for n in G.nodes]
    nx.draw(G, pos2, with_labels=True, node_color=node_colors2, node_size=800, font_size=7, ax=ax2)
    nx.draw_networkx_edge_labels(G, pos2, edge_labels=nx.get_edge_attributes(G, 'relation'), font_color='red', font_size=6, ax=ax2)
    plt.axis('off')
    st.pyplot(fig2)


