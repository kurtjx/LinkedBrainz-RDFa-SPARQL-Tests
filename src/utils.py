import RDF
from settings import endpoint_uri
from urllib import quote
from SPARQLWrapper import SPARQLWrapper2

def load_rdfa_model(uri):
    ''' loads RDFa from URI '''
    rdfa_parser = RDF.Parser(name='rdfa')
    model = RDF.Model()
    def rdfa_error_handler(code, level, facility, message, line, column, byte, file, uri):
        ''' error handler needed to deal with HTML5 stuff '''
        print message
    rdfa_parser.parse_into_model(model, uri, handler=rdfa_error_handler)
    return model

DESCRIBE_QUERY = '''
 CONSTRUCT {
  <%(uri)s> ?p ?o .
  }
 WHERE {
  <%(uri)s> ?p ?o . 
 }
'''

def load_rdf_model(uri):
    p = RDF.Parser()
    model = RDF.Model()
    p.parse_into_model(model, endpoint_uri+'?query='+quote(DESCRIBE_QUERY%locals()))
    return model

def model_is_subset(model_sub, model_super, subject=None):
    '''test that model_sub is a subset of model_super'''
    if subject is None:
        query = RDF.SPARQLQuery('select distinct * where { ?s ?p ?o . }')
    else:
        query = RDF.SPARQLQuery('select distinct * where { <%s> ?p ?o . }' % subject)
    sub_predicates = set()
    for predicate in query.execute(model_sub):
        sub_predicates.add( ( str(predicate['p']), str(predicate['o']) ) )

    super_predicates = set()
    for predicate in query.execute(model_super):
        super_predicates.add( ( str(predicate['p']), str(predicate['o']) ) )


    if sub_predicates.issubset(super_predicates):
        return True
    else:
        print 'additional predicates for %s:' % subject
        for p in sub_predicates.difference(super_predicates):
            print '%s %s;' % p
        return False

ASK = """ASK { %s . }"""
                   
def ask_each_triple(rdfa_model, endpoint):
    "docstring for ask_each_triple"
    nts = RDF.NTriplesSerializer()
    nt_lines = nts.serialize_model_to_string(rdfa_model).split('\n')
    sparql = SPARQLWrapper2(endpoint)
    missing_triples = False
    for t in nt_lines:
        sparql.setQuery(ASK % t)
        if not sparql.query().convert()['boolean']:
            print 'missing triple:'
            print t
            missing_triples = True
    return missing_triples
            
    
