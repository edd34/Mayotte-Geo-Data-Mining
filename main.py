import lxml.etree
tree = lxml.etree.parse('mayotte.xml')

list_amenity = []
set_amenity = set()

for tag in tree.findall('.//tag/..')[10:]:
    for child in tag.xpath("./tag"):
        if child.get("k") == "amenity":
            set_amenity.add(child.get("v"))

print(set_amenity)
