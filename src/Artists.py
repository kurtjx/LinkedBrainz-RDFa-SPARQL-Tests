import unittest
import RDF
from settings import uri_base, endpoint_uri
from utils import load_rdf_model, load_rdfa_model, model_is_subset, ask_each_triple

class ArtistTest(unittest.TestCase):
    jamesbrown = 'artist/20ff3303-4fe2-4a47-a1b6-291e26aa3438'
    suffix = '#_'
    
    def setUp(self):
        self.artist_uri = uri_base + self.jamesbrown + self.suffix
        self.rdf = load_rdf_model(self.artist_uri)

    def test_exhaustive(self):
        "docstring for exhaustive_test"
        rdfa = load_rdfa_model(self.artist_uri)
        self.assertTrue(ask_each_triple(rdfa, endpoint_uri), 'missing some triples')
        
    # def test_rdfa_subset_rdf(self):
    #     rdfa = load_rdfa_model(self.artist_uri)
    #     self.assertTrue(model_is_subset(rdfa, self.rdf, self.artist_uri),
    #                     'RDFa model should be a subset  of RDF model.')


    # def test_rdfa_subset_rdf_releases(self):
    #     rdfa = load_rdfa_model(uri_base+self.jamesbrown+'/releases')
    #     self.assertTrue(model_is_subset(rdfa, self.rdf, self.artist_uri),
    #                     'RDFa model should be a subset  of RDF model.')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
