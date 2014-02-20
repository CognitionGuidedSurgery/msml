import msml.model as M
import msml.xml as X

if __name__=='__main__':
  alphabet = X.load_alphabet("../alphabet")

  print alphabet._xsd()

