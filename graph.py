from enum import Enum

def normalize_edge_name(edge_name):
    return edge_name.replace(" ", "_").replace(".", "_").replace(":", "")


def normalize_node_name(node_name):
    return node_name.replace(" ", "_").replace(".", "_").replace(":", "").replace("$", "")


class NodeTypeStyle(Enum):
    SRC = "shape=ellipse"
    OUT = "shape=ellipse, style=filled, fillcolor=black, fontcolor=white"
    IM = "shape=rectangle"
    IM_PROG = "shape=circle, style=filled, width=0.05, fixedsize=true"
    NULL = "shape=none"

class Programs:
    def __init__(self):
        self.edges = {}
        self.nodes = {}
        self.node_counter = 0
        self.edge_counter = 0

    def add_prog(self, prog_name, inputs, outputs, line=None):
        edge_label = prog_name
        if line is not None:
            edge_label += f" :{line}"
        edge_name = normalize_edge_name(edge_label)

        input_nodes = []
        output_nodes = []

        for node in inputs:
            node_name = normalize_node_name(node)
            if node_name not in self.nodes:
                self.nodes[node_name] = {"label": node}
            input_nodes.append(node_name)

        for node in outputs:
            node_name = normalize_node_name(node)
            if node_name not in self.nodes:
                self.nodes[node_name] = {"label": node}
            output_nodes.append(node_name)

        if len(input_nodes) == 1 and len(output_nodes) == 1:
            self.edges[edge_name] = {"from": input_nodes[0], "to": output_nodes[0], "label": edge_label, "arrow": True}
            return

        im_node = f"im_node_{edge_name}_{self.node_counter}"
        self.node_counter += 1
        self.nodes[im_node] = {"type": NodeTypeStyle.IM_PROG, "label": edge_label}

        for node in input_nodes:
            self.edges[f"{edge_name}_in_{self.edge_counter}"] = {"from": node, "to": im_node, "arrow": False}
            self.edge_counter += 1

        for node in output_nodes:
            self.edges[f"{edge_name}_in_{self.edge_counter}"] = {"from": im_node, "to": node, "arrow": True}
            self.edge_counter += 1

    def get_node_type(self):
        node_deg = {node: {"in": 0, "out": 0} for node in self.nodes}
        for edge in self.edges.values():
            node_deg[edge["from"]]["out"] += 1
            node_deg[edge["to"]]["in"] += 1
        for node in node_deg:
            if self.nodes[node].get("type") == NodeTypeStyle.IM_PROG:
                continue
            if node_deg[node]["in"] == 0 and node_deg[node]["out"] == 0:
                self.nodes[node]["type"] = NodeTypeStyle.NULL
            elif node_deg[node]["in"] == 0:
                self.nodes[node]["type"] = NodeTypeStyle.SRC
            elif node_deg[node]["out"] == 0:
                self.nodes[node]["type"] = NodeTypeStyle.OUT
            else:
                self.nodes[node]["type"] = NodeTypeStyle.IM

    @staticmethod
    def get_style(node):
        if node.get("type"):
            return node["type"].value
        return "shape=none"

    def write_to(self, filename):
        self.get_node_type()
        __import__('pprint').pprint(self.nodes)
        with open(filename, "w") as f:
            f.write("digraph f {\n")
            for nodename, node in self.nodes.items():
                f.write(f"\t{nodename} [{self.get_style(node)}, label=\"{node.get('label', ' ')}\"];\n")
            for edge in self.edges.values():
                if not edge.get("arrow"):
                    style = " dir=none"
                else:
                    style = ""
                f.write(f"\t{edge['from']} -> {edge['to']} [label=\"{edge.get('label', ' ')}\"{style}];\n")
            f.write("}\n")


if __name__ == "__main__":
    prog = Programs()
    prog.add_prog("tr", ["$PLIST_NAME"], ["dict.plist"], 120)
    prog.add_prog("xsltproc", ["extract_property.xsl", "dict.plist"], ["dict_prop_list.txt"], 123)
    prog.add_prog("generate_dict_template.sh", ["dict_prop_list.txt"], ["customized_template.plist"], 129)
    prog.add_prog("tr", ["$SRC_FILE"], ["dict.xml"], 136)
    prog.add_prog("sed", ["dict.xml"], ["dict_mod.xml"], 148)
    prog.add_prog("make_line.pl", ["dict_mod.xml"], ["dict.formattedSource.xml"], 140)
    prog.add_prog("make_body.pl", ["dict.formattedSource.xml"], ["dict.body", "dict.offsets"], 142)
    prog.add_prog("extract_index.pl", ["dict.formattedSource.xml"], ["key_entry_list.txt"], 147)
    prog.add_prog("extract_referred_id.pl", ["dict.formattedSource.xml"], ["referred_id_list.txt"], 148)
    prog.add_prog("extract_front_matter_id.pl", ["$PLIST_NAME"], ["referred_id_list.txt"], 149)
    prog.add_prog("make_dict_package", ["customized_template.plist"], ["dict.dictionary"], 156)
    prog.add_prog("add_body_record", ["dict.dictionary", "dict.offsets", "dict.body"], ["entry_body_list.txt", "$BODY_DATA_NAME"], 161)
    prog.add_prog("replace_entryid_bodyid.pl", ["entry_body_list.txt", "key_entry_list.txt"], ["key_body_list.txt"], 167)
    prog.add_prog("normalize_key_text", ["key_body_list.txt"], ["normalized_key_body_list_1.txt"], 172)
    prog.add_prog("add_supplementary_key", ["normalized_key_body_list_1.txt"], ["normalized_key_body_list_2.txt"], 176)
    prog.add_prog("remove_duplicate_key.pl", ["normalized_key_body_list_2.txt"], ["normalized_key_body_list.txt"], 182)
    prog.add_prog("build_key_index", ["dict.dictionary", "normalized_key_body_list.txt"], ["$KEY_TEXT_INDEX_NAME"], 187)
    prog.add_prog("pick_referred_entry_id.pl", ["entry_body_list.txt", "referred_id_list.txt"], ["referred_entry_body_list.txt"], 196)
    prog.add_prog("build_reference_index", ["referred_entry_body_list.txt", "dict.dictionary"], ["$ENTRY_ID_INDEX_NAME"], 197)

    prog.write_to("graph.dot")