import re

from textnode import TextNode, TextType

def split_nodes_delimiter(
        old_nodes: list[TextNode],  
        delimiter: str, 
        text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Uneven number of delimiters in text")
        split_node_text = node.text.split(delimiter)
        for i in range(len(split_node_text)):
            if split_node_text[i] != "":
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_node_text[i], TextType.PLAIN))
                else:
                    new_nodes.append(TextNode(split_node_text[i], text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        # Précautions d'usage : pas de texte vide ajouté, et on ajoute le node tel quel s'il n'y a pas d'image.
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        if node.text == "":
            continue
        if not extract_markdown_images(node.text):
            new_nodes.append(node)
            continue

        # On récupère les textes links:
        images = extract_markdown_images(node.text)
        # Pour chaque texte LINK, on split le texte du node. On ajoute la première partie du split dans new_nodes, et on refait la meme chose sur la 2ème partie.
        # new_text_split = []
        new_node_text = node.text
        for i in range(len(images)):
            temp_split = new_node_text.split(f"![{images[i][0]}]({images[i][1]})", 1)
            if temp_split[0] != "":
                new_nodes.append(TextNode(temp_split[0], TextType.PLAIN))
            new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
            new_node_text = temp_split[1]
        # Comme on split en fonction du nombre d'LINK, il reste forcément une chaine de caractères. Si elle n'est pas vide, on l'ajoute.
        if new_node_text != "":
            new_nodes.append(TextNode(new_node_text), TextType.PLAIN)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        # Précautions d'usage : pas de texte vide ajouté, et on ajoute le node tel quel s'il n'y a pas de lien.
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        if node.text == "":
            continue
        if not extract_markdown_links(node.text):
            new_nodes.append(node)
            continue
        # On récupère les textes liens:
        links = extract_markdown_links(node.text)
        # Pour chaque texte lien, on split le texte du node. On ajoute la première partie du split dans new_nodes, et on refait la meme chose sur la 2ème partie.
        new_node_text = node.text
        for i in range(len(links)):
            temp_split = new_node_text.split(f"[{links[i][0]}]({links[i][1]})", 1)
            if temp_split[0] != "":
                new_nodes.append(TextNode(temp_split[0], TextType.PLAIN))
            new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
            new_node_text = temp_split[1]
        # Comme on split en fonction du nombre de liens, il reste forcément une chaine de caractères. Si elle n'est pas vide, on l'ajoute.
        if new_node_text != "":
            new_nodes.append(TextNode(new_node_text), TextType.PLAIN)
    return new_nodes

