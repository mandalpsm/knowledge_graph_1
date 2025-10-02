import pandas as pd
import networkx as nx
from pyvis.network import Network

# Load dataset
file_path = "Dataset.csv"
df = pd.read_csv(file_path, encoding="latin1")

# Drop empty column
df = df.drop(columns=["Unnamed: 9"], errors="ignore")

# Use only a sample for visualization (avoid crash)
sample_df = df.head(300)  # try 300 papers, increase if browser handles it

# Create Graph
G = nx.MultiDiGraph()

for _, row in sample_df.iterrows():
    paper_id = row["DOI"]

    # Paper node
    G.add_node(paper_id, label=row["Title"], type="Paper", color="red", shape="square")
    
    # Authors
    if pd.notna(row["Author"]):
        for author in row["Author"].split(","):
            author = author.strip()
            G.add_node(author, type="Author", color="blue", shape="dot")
            G.add_edge(author, paper_id, relation="wrote")
    
    # Journal
    if pd.notna(row["Journal"]):
        G.add_node(row["Journal"], type="Journal", color="green", shape="diamond")
        G.add_edge(paper_id, row["Journal"], relation="published_in")
    
    # Publisher
    if pd.notna(row["Publisher"]):
        G.add_node(row["Publisher"], type="Publisher", color="orange", shape="triangle")
        G.add_edge(row["Journal"], row["Publisher"], relation="owned_by")
    
    # Place
    if pd.notna(row["Place"]):
        G.add_node(row["Place"], type="Place", color="purple", shape="star")
        G.add_edge(paper_id, row["Place"], relation="from")

# Visualization
net = Network(height="750px", width="100%", directed=True, notebook=False)
net.from_nx(G)

net.write_html("knowledge_graph_no_keywords.html")
print("✅ Graph saved as knowledge_graph_no_keywords.html (without keywords)")
