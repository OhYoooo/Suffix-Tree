from collections import defaultdict

class Node:

    def __init__(self):
        """
        Node of tree
        suffix_node: the index of a node with a matching suffix, -1 represents no suffix link
        """
        self.suffix_node = -1

    def __repr__(self):
        return "link: %d"%self.suffix_node

class Edge:

    def __init__(self, first_char_index: int, last_char_index: int, source_node_index: int, target_node_index: int):
        """
        Edge in the tree
        :type:
            first_char_index: int (index of the start of the string)
            last_char_index: int (index of the end of the string)
            source_node_index: int (index of the source node of the edge)
            target_node_index: int (index of the target node of the edge)
        :rtype: void
        """
        self.first_char_index = first_char_index
        self.last_char_index = last_char_index
        self.source_node_index = source_node_index
        self.target_node_index = target_node_index

    def size(self) -> int:
        """
        length of the edge
        :type: void
        :rtype: int
        """
        return self.last_char_index - self.first_char_index

    def __repr__(self):
        return 'Edge(%d, %d, %d, %d)'% (self.source_node_index, self.dest_node_index 
                                        ,self.first_char_index, self.last_char_index )


class Suffix:

    def __init__(self, source_node_index: int, first_char_index: int, last_char_index: int):
        """
        Suffix start from the first index to the last index of a source node
        :type:
            source_node_index: int
            first_char_index: int
            last_char_index: int
        :rtype: void
        """
        self.source_node_index = source_node_index
        self.first_char_index = first_char_index
        self.last_char_index = last_char_index

    def size(self):
        """
        The length of the suffix
        :type: void
        :rtype: int
        """
        return self.last_char_index - self.first_char_index

    def explicit(self) -> bool:
        """
        Suffix is explicit if it ends up in an existed node. Set first_char_index greater than last_char_index to indicate this circumstance
        :type: void
        :rtype: bool
        """
        return self.first_char_index > self.last_char_index

    def implicit(self) -> bool:
        """
        Suffix is implicit if
        :type: void
        :rtype: bool
        """
        return self.last_char_index >= self.first_char_index

class SuffixTree:

    def __init__(self, text: str):
        self.text = text
        self.size = len(text) - 1
        self.nodes = [Node()]
        self.edges = {}
        self.active = Suffix(0, 0, -1)
        for i in range(len(text)):
            self._add_prefix(i)

    def _add_prefix(self, last_char_index: int):
        last_parent_node = -1
        while True:
            parent_node = self.active.source_node_index
            if self.active.explicit():
                if (self.active.source_node_index, self.text[last_char_index]) in self.edges:
                    # prefix already exist in the tree
                    break
            else:
                e = self.edges[self.active.source_node_index, self.text[self.active.first_char_index]]
                if self.text[e.first_char_index + self.active.size + 1] = self.text[last_char_index]:
                    # prefix already exist in the tree
                    break
                parent_node = self._splite_dge(e, self.active)
            
            self.nodes.append(Node())
            e = Edge(last_char_index, self.size, parent_node, len(self.nodes) - 1)
            self._insert_edge(e)

            if last_parent_node > 0:
                self.nodes[last_parent_node].suffix_node = parent_node
            last_parent_node = parent_node

            if self.active.source_node_index == 0:
                self.active.first_char_index += 1
            else:
                self.active.source_node_index = self.nodes[self.active.source_node_index].suffix_node
            self._canonize_suffix(self.active)
        
        if last_parent_node > 0:
            self.nodes[last_parent_node].suffix_node = parent_node
        self.active.last_char_index += 1
        self._canonize_suffix(self.active)


    def _inserte_dge(self, edge: Edge):
        self.edges[(edge.source_node_index, self.text[edge.first_char_index])] = edge

    def _remove_edge(self, edge: Edge):
        self.edges.pop((edge.source_node_index, self.text[edge.first_char_index]))

    def _split_edge(self, edge: Edge, suffix: Suffix) -> int:
        self.nodes.append(Node())
        e = Edge(edge.first_char_index, edge.first_char_index + suffix.size, suffix.source_node_index, len(self.nodes) - 1)
        self._remove_edge(edge)
        self._insert_edge(e)
        self.nodes[e.target_node_index].suffix_node = suffix.source_node_index
        edge.first_char_index = edge.first_char_index + suffix.size + 1
        edge.source_node_index = e.target_node_index
        self._insert_edge(edge)
        return e.target_node_index

    def _canonize_suffix(self, suffix: Suffix):
        if not suffix.explicit():
            e = self.edges[suffix.source_node_index, self.text[suffix.first_char_index]]
            if e.size <= suffix.size:
                suffix.first_char_index += e.size + 1
                suffix.source_node_index = e.target_node_index
                self._canonize_suffix(suffix)
        