__author__ = 'Alexander Weigl'

import msml.frontend

MSML = "msml"
hasOperator = "hasOperator"

from  msml.generators import IdentifierGenerator

metaGenerator = IdentifierGenerator("meta")
slotIdGen = IdentifierGenerator("slot")


def get_triples(operator):
    """
    :param operator:
    :type operator: msml.model.base.Operator
    :return:
    """

    def generateMeta(top, meta):
        metaId = metaGenerator()
        return [(metaId, "has" + str(k).title(), v)
                for k, v in operator.meta.items()
                if len(v) <= 25
                if k.isalpha()
               ] + ([(top, 'hasMeta', metaId)] if meta else [])

    def slots(slots, rel):
        def typename(x):
            if x:
                return x.__name__
            else:
                return "None"
        result = []
        for slot in slots:
            slotId = slotIdGen()
            meta = generateMeta(slotId, slot.meta)
            result += [   (operator.name, rel, slotId),
                       (slotId, 'hasName', slot.name),
                       (slotId, 'hasDefault', slot.default),
                       (slotId, 'hasLogicalType' , typename(slot.sort.logical)),
                       (slotId, 'hasPhysicalType',typename(slot.sort.physical)),
                       (slotId, 'isRequired', slot.required)] + meta
        return result


    triples = [(MSML, hasOperator, operator.name)] + generateMeta(operator.name, operator.meta)
    triples += slots(operator.input.values(), 'hasInput')
    triples += slots(operator.parameters.values(), 'hasParameter')
    triples += slots(operator.output.values(), 'hasOutput')

    return triples


def triple_of_operators_in_alphabet():
    alphabet = msml.frontend.App(novalidate=True).alphabet
    operators = alphabet.operators.values()

    triple_store = []
    for o in operators:
        triple_store += get_triples(o)
    return triple_store

def todot(triples):
    s = """
    digraph G {
    """

    def clean(*args):
        return tuple( map(lambda string: string.replace('"',"'"), args) )

    for a,b,c in triples:
        s+= '"%s" -> "%s" [label="%s"]; ' % (a,c,b)

    s += "}"

    return s;

if __name__ == "__main__":
    import pprint
    t = triple_of_operators_in_alphabet()
    pprint.pprint(t)

    with open('test.dot','w') as fp:
        fp.write(todot(t))


