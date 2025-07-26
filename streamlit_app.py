import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pykeen.datasets import Hetionet
from pykeen.pipeline import pipeline

# Set wide layout for Streamlit
st.set_page_config(layout="wide")

st.title("🧠 Hetionet Knowledge Graph Explorer")
st.markdown("""
Explore real-world biomedical knowledge from **Hetionet** — a large-scale drug–gene–disease graph.
You can view relationships, visualize a subgraph, and even predict new connections using machine learning.
""")

# Load Hetionet triples
@st.cache_data
def load_hetionet():
    return Hetionet().to_triples()

triples = load_hetionet()
df = pd.DataFrame(triples, columns=["head", "relation", "tail"])

# Show sample data
st.subheader("📊 Sample Triplets from Hetionet")
st.dataframe(df.sample(300, random_state=42))

# Filter compound–disease edges
df_cd = df[df['relation'] == "treats"].sample(100, random_state=1)
st.subheader("💊 Compound → Disease Relationships (treats)")
st.dataframe(df_cd)

# Build knowledge graph using NetworkX
st.subheader("📌 Graph Visualization (Subset)")

G = nx.Graph()
for h, r, t in df_cd.itertuples(index=False):
    G.add_node(h, type="Compound")
    G.add_node(t, type="Disease")
    G.add_edge(h, t, relation=r)

fig, ax = plt.subplots(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
node_colors = ['lightblue' if G.nodes[n]['type'] == "Compound" else 'lightgreen' for n in G.nodes]
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_size=8, ax=ax)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'relation'), font_color='red', ax=ax)
plt.axis('off')
st.pyplot(fig)

# Link prediction section
st.subheader("🔮 Predict New Disease Targets for a Drug")

if st.button("Run Embedding & Predict"):
    st.info("Training TransE model on Hetionet... (may take a few minutes)")
    result = pipeline(
        dataset="Hetionet",
        model="TransE",
        training_loop="slcwa",
        epochs=10,
        random_seed=42,
    )
    predictions = result.model.predict_relations(["Compound:aspirin"], target_types=["Disease"])
    st.success("Top predicted disease targets for aspirin:")
    st.dataframe(predictions.head(10))
