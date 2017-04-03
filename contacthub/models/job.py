from copy import deepcopy, copy

from contacthub.api_manager.api_customer import CustomerAPIManager


class Job(object):
    """
    Job model
    """

    __attributes__ = ('attributes', 'customer','customer_api_manager','entity_name', 'parent_attr')

    def __init__(self, customer, parent_attr=None, **attributes):
        self.customer = customer
        self.attributes = attributes
        self.customer_api_manager = CustomerAPIManager(node=customer.node)
        self.entity_name = 'jobs'
        self.parent_attr = parent_attr

    @classmethod
    def from_dict(cls, customer, attributes=None, parent_attr=None):
        o = cls(customer=customer, parent_attr=parent_attr)
        if attributes is None:
            o.attributes = {}
        else:
            o.attributes = attributes
        return o

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple properties. Otherwise, if the
        element is datetime format, return a datetime object
        :param item: the key of the base properties dict
        :return: an element of the dictionary, or datetime object if element associated at the key contains a datetime format object
        """
        try:
            return self.attributes[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" %(type(self).__name__, e))

    def __setattr__(self, attr, val):
        if attr in self.__attributes__:
            return super(Job, self).__setattr__(attr, val)
        else:
            self.attributes[attr] = val
            if self.parent_attr:
                attr = self.parent_attr.split('.')[-1:][0]
                base_attr = self.parent_attr.split('.')[-2:][0]
                if base_attr not in self.customer.mute:
                    self.customer.mute[base_attr] = {}
                self.customer.mute[base_attr][attr] = self.customer.attributes[base_attr][attr]

    def to_dict(self):
        return deepcopy(self.attributes)

    def post(self):
        """
        Post this Education in the list of the Education for a Customer(specified in the constructor of the Education)
        :return: a Education object representing the posted Education
        """
        entity_attrs = self.customer_api_manager.post(body=self.attributes, urls_extra=self.customer.id + '/'
                                                                                   + self.entity_name)
        if 'base' not in self.customer.attributes:
            self.customer.attributes['base'] = {}
        if self.entity_name not in self.customer.attributes['base']:
            self.customer.attributes['base'][self.entity_name] = []
        self.customer.attributes['base'][self.entity_name] += [entity_attrs]

    def delete(self):
        """
        Remove this Education from the list of the Education for a Customer(specified in the constructor of
        the Education)
        :return: a Education object representing the deleted Education
        """
        self.customer_api_manager.delete(_id=self.customer.id, urls_extra=self.entity_name + '/' + self.attributes['id'])

    def put(self):
        """
        Put this Education in the list of the Education for a Customer(specified in the constructor of the Education)
        :return: a Education object representing the putted Education
        """
        try:
            find = False
            for job in self.customer.attributes['base'][self.entity_name]:
                if self.attributes['id'] == job['id']:
                    find = True
            if not find:
                raise ValueError("Job object doesn't exists in the specified customer")
        except KeyError as e:
            raise ValueError("Job object doesn't exists in the specified customer")

        entity_attrs = self.customer_api_manager.put(_id=self.customer.id, body=self.attributes,
                                                 urls_extra=self.entity_name + '/' + self.attributes['id'])
        for job in self.customer.attributes['base'][self.entity_name]:
            if job['id'] == entity_attrs['id']:
                index = self.customer.attributes['base'][self.entity_name].index(job)
                self.customer.attributes['base'][self.entity_name][index] = entity_attrs