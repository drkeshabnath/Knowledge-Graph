import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# Configure Streamlit page
st.set_page_config(page_title="Knowledge Graph Demo", layout="wide")
st.title("🧠 Drug–Disease–Biomarker Knowledge Graph")
st.markdown("Explore relationships in a biomedical knowledge graph built from a **100-row synthetic dataset**.")

# Create the fixed-size dataset (100 rows)
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

# Display the dataset
st.subheader("📋 Dataset: 100 Drug–Disease–Biomarker Triplets")
st.dataframe(df)

# Create the Knowledge Graph
G = nx.Graph()

for row in df.itertuples(index=False):
    G.add_node(row.Drug, type='Drug')
    G.add_node(row.Disease, type='Disease')
    G.add_node(row.Biomarker, type='Biomarker')

    G.add_edge(row.Drug, row.Disease, relation='treats')
    G.add_edge(row.Disease, row.Biomarker, relation='indicated_by')

# Graph Visualization
st.subheader("📌 Knowledge Graph Visualization")

fig, ax = plt.subplots(figsize=(14, 10))
pos = nx.spring_layout(G, seed=42)
node_colors = [
    'lightblue' if G.nodes[n]['type'] == 'Drug' else
    'lightgreen' if G.nodes[n]['type'] == 'Disease' else
    'salmon'
    for n in G.nodes
]

nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_size=8, ax=ax)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'relation'), font_color='red', font_size=7, ax=ax)

plt.axis('off')
st.pyplot(fig)

st.success("✅ Lightweight biomedical knowledge graph successfully rendered using 100 synthetic entries.")
