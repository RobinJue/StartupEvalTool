import os
import graphviz

# Define the root directory
root_dir = "/Users/robinjuengerich/Library/Mobile Documents/com~apple~CloudDocs/Documents/Studies/CAU/24-25 WS/Thesis/code"

# Ensure the directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError(f"Directory not found: {root_dir}")

# Create a Graphviz Digraph
dot = graphviz.Digraph(format='png')
dot.attr(rankdir='TB')  # Top to bottom layout

# Function to recursively add files and folders to Graphviz
def add_nodes_edges(directory, parent=None):
    folder_name = os.path.basename(directory)

    # Ignore .git and __pycache__ folders
    if folder_name in [".git", "__pycache__"]:
        return  

    node_id = directory.replace("/", "_")  # Unique ID for Graphviz nodes

    # Add folder node
    dot.node(node_id, folder_name, shape='box', style='filled', fillcolor='lightblue')

    if parent:
        dot.edge(parent, node_id)

    # Process files and subdirectories
    for item in sorted(os.listdir(directory)):
        item_path = os.path.join(directory, item)
        item_id = item_path.replace("/", "_")  # Unique ID for files/folders

        if os.path.isdir(item_path):
            add_nodes_edges(item_path, node_id)  # Recurse for subdirectory
        elif (item.endswith(".py") or item.endswith(".sh")) and item != "__init__.py":  # Only include .py and .sh (ignore __init__.py)
            dot.node(item_id, item, shape='ellipse', style='filled', fillcolor='lightgray')  # File as ellipse
            dot.edge(node_id, item_id)

# Build the Graphviz tree
add_nodes_edges(root_dir)

# Render and display
output_path = "file_structure"
dot.render(output_path)
print(f"Visualization saved as {output_path}.png")
