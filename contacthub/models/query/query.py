import json

from contacthub.DeclarativeAPIManager.declarative_api_customer import CustomerDeclarativeApiManager
from contacthub.models.customer import Customer
from contacthub.models.query.criterion import Criterion
from copy import deepcopy


class Query(object):
    """
    Query object for applying the specified query in the APIs.

    Use this class for interact with the DeclarativeAPIManager Layer or APIManagerLevel and return the queried as object or
    json format variables
    """
    def __init__(self, node, entity, previous_query=None):
        """
        :param node: the node for applying for fetching data
        :param query: a JSON API-like object for querying data
        :param entity: the entity on which apply the query
        """
        self.node = node
        self.entity = entity
        self.condition = None
        self.inner_query = None
        if previous_query:
            self.inner_query = previous_query
            if previous_query['type'] == 'simple':
                self.condition = previous_query['are']['condition']

    @staticmethod
    def _combine_query(query1, query2, operation):
        if query2.inner_query['type'] == 'combined' and query2.inner_query['conjunction'] == operation:
            query_ret = deepcopy(query2.inner_query)
            query_ret['queries'].append(query1.inner_query)
        else:
            if query1.inner_query['type'] == 'combined' and query1.inner_query['conjunction'] == operation:
                query_ret = deepcopy(query1.inner_query)
                query_ret['queries'].append(query2.inner_query)
            else:
                query_ret = {'type': 'combined', 'name': 'query', 'conjunction': operation,
                             'queries': [query1.inner_query, query2.inner_query]}
        return query_ret

    def __and__(self, other):
        return Query(node=self.node, entity=self.entity,
                     previous_query=self._combine_query(query1=self,query2=other, operation='INTERSECT'))

    def __or__(self, other):
        return Query(node=self.node, entity=self.entity,
                     previous_query=self._combine_query(query1=self, query2=other, operation='UNION'))

    def all(self):
        """
        Get all queried data of an entity from the API
        :return: a list of Entity object
        """
        complete_query = {'name': 'query', 'query': self.inner_query}
        if self.entity is Customer:
            return CustomerDeclarativeApiManager(self.node).get_all(query=complete_query)

    def filter(self, criterion):
        """
        Create a new API Like query for ContactHub APIs (JSON Format)
        :param criterion: the Criterion object for fields for query data
        :return: a Query object containing the JSON object representing a query for the APIs
        """
        if self.inner_query and self.inner_query['type'] == 'combined':
            raise Exception('Operation not permitted')
        query_ret = {'type': 'simple', 'name': 'query', 'are': {}}
        new_query = {}
        if self.condition is None:
            new_query = self._filter(criterion)
        elif self.condition['type'] == 'atomic':
            new_query = self._and_query(deepcopy(self.condition), self._filter(criterion=criterion))
        else:
            if self.condition['conjunction'] == Criterion.COMPLEX_OPERATORS.AND:
                new_query = deepcopy(self.condition)
                new_query['conditions'].append(self._filter(criterion=criterion))
            elif self.condition['conjunction'] == Criterion.COMPLEX_OPERATORS.OR:
                new_query = self._and_query(deepcopy(self.condition), self._filter(criterion=criterion))
        query_ret['are']['condition'] = new_query
        return Query(node=self.node, entity=self.entity, previous_query=query_ret)

    @staticmethod
    def _and_query(query1, query2):
        query_ret = {}
        query_ret['type'] = 'composite'
        query_ret['conditions'] = []
        query_ret['conditions'].append(query1)
        query_ret['conditions'].append(query2)
        query_ret['conjunction'] = 'and'
        return query_ret

    def _filter(self, criterion):
        """
        Private function for creating atomic or composite subqueries found in major query.
        :param criterion: the Criterion object for fields for query data
        :return: a JSON object containing a subquery for creating the query for the APIs
        """
        if criterion.operator in Criterion.SIMPLE_OPERATORS.OPERATORS:
            atomic_query = {'type': 'atomic'}
            entity_field = criterion.first_element
            fields = [entity_field.field]

            while not type(entity_field.entity) is type(self.entity):
                entity_field = entity_field.entity
                fields.append(entity_field.field)

            attribute = ''
            for field in reversed(fields):
                attribute += field
                attribute += '.'

            attribute = attribute[:-1]

            atomic_query['attribute'] = attribute
            atomic_query['operator'] = criterion.operator
            if criterion.second_element:
                atomic_query['value'] = criterion.second_element
            return atomic_query

        else:
            if criterion.operator in Criterion.COMPLEX_OPERATORS.OPERATORS:
                composite_query = {'type': 'composite', 'conditions': []}
                composite_query['conjunction'] = criterion.operator
                first_element = self._filter(criterion.first_element)
                second_element = self._filter(criterion.second_element)
                composite_query['conditions'].append(first_element)
                composite_query['conditions'].append(second_element)
                return composite_query




