from tempfile import NamedTemporaryFile, TemporaryDirectory, mkdtemp

import pytest

from gseapy.enrichr import enrichr
from gseapy.gsea import gsea, prerank, replot, ssgsea


@pytest.fixture
def edbDIR():
    return "tests/data"


@pytest.fixture
def genelist():
    return "tests/data/gene_list.txt"


@pytest.fixture
def gseaGCT():
    return "tests/data/P53_resampling_data.txt"


@pytest.fixture
def gseaCLS():
    return "tests/data/P53.cls"


@pytest.fixture
def prernk():
    return "tests/data/edb/gsea_data.gsea_data.rnk"


@pytest.fixture
def geneGMT():
    return "tests/data/genes.gmt"


@pytest.fixture
def ssGMT():
    return "tests/data/randomSets.gmt"


@pytest.fixture
def ssGCT():
    return "tests/data/testSet_rand1200.gct"


def test_gsea(gseaGCT, gseaCLS, geneGMT):
    # Only tests of the command runs successfully,
    # doesnt't check the image
    tmpdir = TemporaryDirectory(dir="tests")
    gs_res = gsea(
        data=gseaGCT,
        gene_sets=geneGMT,
        cls=gseaCLS,
        method="t_test",
        outdir=tmpdir.name,
        permutation_type="phenotype",
        permutation_num=47,
    )
    tmpdir.cleanup()

def test_fdr_gsea(gseaGCT, gseaCLS, geneGMT):
    # Runs and verifies a reasonable result for pval
    # when method="t_test" and permutation_type="gene_set"
    tmpdir = TemporaryDirectory(dir="tests")
    gs_res = gsea(
        data=gseaGCT,
        gene_sets=geneGMT,
        cls=gseaCLS,
        method="t_test",
        outdir=tmpdir.name,
        permutation_type="gene_set",
        permutation_num=47,
        seed=7,
    )
    assert gs_res.res2d['pval'].max() > 0.0
    tmpdir.cleanup()

def test_prerank(prernk, geneGMT):
    # Only tests of the command runs successfully,
    # doesnt't check the image
    tmpdir = TemporaryDirectory(dir="tests")
    prerank(prernk, geneGMT, tmpdir.name, permutation_num=10)
    tmpdir.cleanup()
    prerank(prernk, geneGMT, None, permutation_num=99)


def test_ssgsea1(ssGCT, geneGMT):
    # Only tests of the command runs successfully,
    # doesnt't check the image
    tmpdir = TemporaryDirectory(dir="tests")
    ssgsea(ssGCT, geneGMT, tmpdir.name, permutation_num=100)
    tmpdir.cleanup()


def test_ssgsea2(ssGCT, geneGMT):
    # Only tests of the command runs successfully,
    # doesnt't check the image
    tmpdir = TemporaryDirectory(dir="tests")
    ssgsea(ssGCT, geneGMT, tmpdir.name, permutation_num=0)
    tmpdir.cleanup()
    ssgsea(ssGCT, geneGMT, None, permutation_num=0)


def test_enrichr(genelist, geneGMT):
    # Only tests of the command runs successfully,
    # doesnt't check the image
    tmpdir = TemporaryDirectory(dir="tests")
    enrichr(
        genelist, gene_sets=["KEGG_2016", geneGMT], outdir=tmpdir.name, verbose=True
    )
    # tmpdir.cleanup()
    tmpdir = TemporaryDirectory(dir="tests")
    enrichr(genelist, organism="Fly", gene_sets="KEGG_2019", outdir=tmpdir.name)
    # tmpdir.cleanup()


def test_replot(edbDIR):
    # Only tests of the command runs successfully,
    # doesnt't check the image
    tmpdir = TemporaryDirectory(dir="tests")
    replot(edbDIR, tmpdir.name)
    tmpdir.cleanup()
