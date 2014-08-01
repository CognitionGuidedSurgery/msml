s = """

    LIBRARY_API std::string CoarseSurfaceMeshPython(std::string infile, std::string outfile,int numberOfElements);

    LIBRARY_API bool CoarseSurfaceMesh(const char* infile,const char* outfile,unsigned int numberOfElements);
"""


for l in s.split("\n"):
    if l == "": continue
    if l.startswith("//"): continue

    a = l.index('(')
    b = l.index(')')

    p = l[a+1:b]
    params = p.split(",")
    P = "\n".join(map(
        lambda x: "    :params %s:" % x.strip().replace("<", r"\<"), params
    ))
    print """

.. cpp:function: %s

%s

    :returns:
    :rtype:

""" % (l.replace(";", "").replace("<", r"\<").replace("LIBRARY_API", "").strip(), P)

