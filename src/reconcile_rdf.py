import RDF


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
        print sub_predicates.difference(super_predicates)
        return False
