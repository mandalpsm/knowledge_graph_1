import pandas as pd
import networkx as nx
from pyvis.network import Network

# ==========================
# Step 1: Load dataset
# ==========================
file_path = "Dataset.csv"   # replace with your file name
df = pd.read_csv(file_path, encoding="latin1")

# Drop extra unnamed column if exists
df = df.drop(columns=["Unnamed: 9"], errors="ignore")

# Use a subset for visualization (adjust size for your machine/browser)
sample_df = df.head(300)

# ==========================
# Step 2: Create Graph
# ==========================
G = nx.MultiDiGraph()

for _, row in sample_df.iterrows():
    # Journal
    if pd.notna(row.get("Journal", None)):
        journal = str(row["Journal"]).strip()
        if journal:
            G.add_node(journal, type="Journal", color="green", shape="diamond")

            # Place
            if pd.notna(row.get("Place", None)):
                place = str(row["Place"]).strip()
                if place:
                    G.add_node(place, type="Place", color="purple", shape="star")
                    G.add_edge(journal, place, relation="located_in")

            # Publisher
            if pd.notna(row.get("Publisher", None)):
                publisher = str(row["Publisher"]).strip()
                if publisher:
                    G.add_node(publisher, type="Publisher", color="orange", shape="triangle")
                    G.add_edge(journal, publisher, relation="owned_by")

# ==========================
# Step 3: Visualization
# ==========================
net = Network(height="750px", width="100%", directed=True, notebook=False)
net.from_nx(G)

net.write_html("knowledge_graph_jpp.html")
print("✅ Graph saved as knowledge_graph_jpp.html (Journal–Place–Publisher only)")
