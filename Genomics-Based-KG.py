import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# Streamlit page setup
st.set_page_config(page_title="Precision Medicine Knowledge Graph", layout="wide")
st.title("🧬 Genomics-Based Precision Medicine Knowledge Graph")
st.markdown("Explore the connections between **genes, variants, diseases, drugs, pathways,** and **populations** in a synthetic biomedical dataset.")

# Generate synthetic dataset
@st.cache_data
def generate_data():
    genes = ["BRCA1", "TP53", "EGFR", "KRAS", "APOE", "ALK", "PTEN", "BRAF", "HER2", "PIK3CA"]
    variants = ["V600E", "R175H", "G12D", "E746_A750del", "L858R", "T790M", "R132H", "H1047R", "N501Y", "R273H"]
    diseases = ["Breast Cancer", "Lung Cancer", "Glioblastoma", "Alzheimer's", "Colon Cancer", "Melanoma", "Pancreatic Cancer", "Prostate Cancer", "Ovarian Cancer", "Thyroid Cancer"]
    drugs = ["Olaparib", "Gefitinib", "Erlotinib", "Trastuzumab", "Bevacizumab", "Temozolomide", "Crizotinib", "Sorafenib", "Tamoxifen", "Pembrolizumab"]
    pathways = ["DNA Repair", "Cell Cycle", "Apoptosis", "MAPK", "PI3K/AKT", "RTK", "mTOR", "Notch", "WNT", "JAK/STAT"]
    populations = ["Ashkenazi Jews", "East Asians", "African Americans", "Hispanics", "South Asians", "Europeans", "Native Americans", "Pacific Islanders", "Caucasians", "Mediterranean"]

    rows = []
    for _ in range(100):
        rows.append({
            "Gene": random.choice(genes),
            "Variant": random.choice(variants),
            "Disease": random.choice(diseases),
            "Drug": random.choice(drugs),
            "Pathway": random.choice(pathways),
            "Population": random.choice(populations),
        })
    return pd.DataFrame(rows)

df = generate_data()
st.subheader("📋 Synthetic Dataset (100 rows)")
st.dataframe(df)

# Build the Knowledge Graph
G = nx.Graph()
for row in df.itertuples(index=False):
    G.add_node(row.Gene, type="Gene")
    G.add_node(row.Variant, type="Variant")
    G.add_node(row.Disease, type="Disease")
    G.add_node(row.Drug, type="Drug")
    G.add_node(row.Pathway, type="Pathway")
    G.add_node(row.Population, type="Population")

    G.add_edge(row.Gene, row.Variant, relation="has_variant")
    G.add_edge(row.Variant, row.Disease, relation="associated_with")
    G.add_edge(row.Disease, row.Drug, relation="treated_by")
    G.add_edge(row.Gene, row.Pathway, relation="part_of_pathway")
    G.add_edge(row.Variant, row.Population, relation="prevalent_in")

# Filter node selection
st.subheader("🔍 Select an Entity to Explore Its Subgraph")
entity_options = sorted(set(df["Gene"].unique()) | set(df["Disease"].unique()) | set(df["Drug"].unique()))
selected_node = st.selectbox("Choose a Gene, Disease or Drug:", entity_options)

# Subgraph visualization
H = nx.ego_graph(G, selected_node, radius=1)
fig, ax = plt.subplots(figsize=(12, 8))
pos = nx.spring_layout(H, seed=42)
node_colors = [
    'skyblue' if H.nodes[n]['type'] == 'Gene' else
    'lightgreen' if H.nodes[n]['type'] == 'Disease' else
    'lightcoral' if H.nodes[n]['type'] == 'Drug' else
    'violet' if H.nodes[n]['type'] == 'Variant' else
    'orange' if H.nodes[n]['type'] == 'Population' else
    'gold'
    for n in H.nodes
]
nx.draw(H, pos, with_labels=True, node_color=node_colors, node_size=1000, font_size=9, ax=ax)
nx.draw_networkx_edge_labels(H, pos, edge_labels=nx.get_edge_attributes(H, 'relation'), font_color='red', font_size=8, ax=ax)
plt.axis('off')
st.pyplot(fig)

# Narrative explanation
st.subheader("🧠 Natural Language Explanation (if available)")
explained = False
for node in H.nodes:
    if node != selected_node and nx.has_path(H, selected_node, node):
        path = nx.shortest_path(H, selected_node, node)
        if len(path) == 3:
            rel1 = G.edges[path[0], path[1]]['relation']
            rel2 = G.edges[path[1], path[2]]['relation']
            st.markdown(f"**Explanation**: `{path[0]}` → *{rel1}* → `{path[1]}` → *{rel2}* → `{path[2]}`")
            explained = True
            break
if not explained:
    st.info("No 2-step explanation found from the selected node.")

# Full graph toggle
if st.checkbox("🌐 Show Full Knowledge Graph"):
    st.subheader("Complete Knowledge Graph")
    fig2, ax2 = plt.subplots(figsize=(14, 12))
    pos2 = nx.spring_layout(G, seed=42)
    all_node_colors = [
        'skyblue' if G.nodes[n]['type'] == 'Gene' else
        'lightgreen' if G.nodes[n]['type'] == 'Disease' else
        'lightcoral' if G.nodes[n]['type'] == 'Drug' else
        'violet' if G.nodes[n]['type'] == 'Variant' else
        'orange' if G.nodes[n]['type'] == 'Population' else
        'gold'
        for n in G.nodes
    ]
    nx.draw(G, pos2, with_labels=True, node_color=all_node_colors, node_size=800, font_size=7, ax=ax2)
    nx.draw_networkx_edge_labels(G, pos2, edge_labels=nx.get_edge_attributes(G, 'relation'), font_color='red', font_size=6, ax=ax2)
    plt.axis('off')
    st.pyplot(fig2)

st.success("✅ This app demonstrates how knowledge graphs can support personalized medicine and genomic diagnostics.")
