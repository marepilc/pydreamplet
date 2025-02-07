from lxml import etree


def set_attrs(element: etree.Element, attrs: dict) -> None:
    for k, v in attrs.items():
        element.set(k, v)
