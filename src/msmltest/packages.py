__author__ = 'weigl'

from unittest import TestCase

from path import path

import msml.package as P

TEST_DATA = path(__file__).dirname() / "../../share/testdata/package"


class PackageTest(TestCase):
    def test_from_file(self):
        package_file = TEST_DATA / "r1.xml"
        p = P.Package.from_file(package_file)

        self.assertEquals(p.information.maintainer.name, "N")
        self.assertEquals(p.information.maintainer.email, "E")
        self.assertEquals(p.information.documentation.content,
                          'A\n            B\n            C\n            D\n            E\n            F\n\n            G')
        self.assertEquals(p.information.repository.type, "git")

        self.assertListEqual(p.alphabet_dir, ['R1A'])
        self.assertListEqual(p.python_dir, ['R1P'])
        self.assertListEqual(p.binary_dir, ['R1B'])


class RepositoryTest(TestCase):
    def test_read_from_file(self):
        r = P.Repository.from_file(TEST_DATA / "repo-p.xml")

        self.assertEquals(r.base_path, TEST_DATA)
        self.assertEquals(r.active, True)
        self.assertEquals(r.msml_version, "1.0")

    def test_resolve(self):
        r = P.Repository.from_file(TEST_DATA / "repo-p.xml")
        packs = r.resolve_packages()
        names = map(lambda x: x.name, packs)
        self.assertListEqual(names, ['P1', 'P2', 'Q1', 'Q2', 'P3', 'P4', 'S1'])

        a, b, c = P.get_concrete_paths(packs)

        print repr(a)
        print repr(c)
        print repr(b)

        self.assertListEqual(a, [(u'/homes/students/weigl/workspace1/msml/share/testdata/package/P1A'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/P2A'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/Q1A'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/Q2A'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/P3A'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/P4A'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/S1A')])
        self.assertListEqual(c, [(u'/homes/students/weigl/workspace1/msml/share/testdata/package/P1P'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/P2P'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/Q1P'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/Q2P'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/P3P'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/P4P'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/S1P')])
        self.assertListEqual(b, [(u'/homes/students/weigl/workspace1/msml/share/testdata/package/P1B'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/P2B'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/Q1B'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/Q2B'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/P3B'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/P4B'),
                                 (u'/homes/students/weigl/workspace1/msml/share/testdata/package/S1B')])

        map(lambda x: x.validate(), packs)

        P.clean_paths(a)