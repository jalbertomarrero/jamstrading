import xml.etree.ElementTree as ET

class MyPortfolio:
    
    file_name = 'PruebaPortfolio.xml'

    """ Class variables """
    initial_capital = {'currency':'','value':0.0}
    total_capital = {'currency':'','value':0.0}
    invested_capital = {'currency':'','value':0.0}
    not_invested_capital = {'currency':'','value':0.0}
    performance = {'units':'%','value':0.0}
    portfolio = []
    """
    {
    'asset_id':(int),
    'name':(string),
    'market':(string),
    'symbol':(string),
    'currency':(string),
    'units':(int),
    'purchase_price':{'datetime':(datetime), 'value':(float)},
    'previous_close':{'datetime':(datetime), 'value':(float)},
    'maximum_close':{'datetime':(datetime), 'value':(float)},
    'minimum_close':{'datetime':(datetime), 'value':(float)},
    'stop_price':(float),
    'add_units_price':(float)
    }
    """

    def __init__(self,file_name):
        self.file_name = file_name
        self.init_portfolio(file_name)

    @staticmethod
    def get_xml_portfolio_element(element):
        """Return a dictionary"""
        output_dict = {}
        if element is not None:
            output_dict['asset_id'] = int(element.attrib['id'])
            for child in element:
                if not child.attrib:
                    output_dict[child.tag] = child.text
                else:
                    output_dict[child.tag] = dict(value=child.text)
                    output_dict[child.tag].update(child.attrib)
        return output_dict
    
    def init_portfolio(self,file_name):
        tree = ET.parse(file_name)
        # PENDIENTE!!: Dar un error en caso que devuelva un diccionario vacío
        """ initial_capital """
        self.initial_capital = get_xml_capital_value(tree,'initial_capital')
        """ total_capital """
        self.total_capital = get_xml_capital_value(tree,'total_capital')
        """ invested_capital """
        self.invested_capital = get_xml_capital_value(tree,'invested_capital')
        """ not_invested_capital """
        self.not_invested_capital = get_xml_capital_value(tree,
                'not_invested_capital')
        """ performance """
        self.performance = get_xml_performance_value(tree,'performance')
        """ portfolio list """
        element = tree.find('portfolio')
        if element is not None:
            for asset in element:
                self.portfolio.append(self.get_xml_portfolio_element(asset))

    def increase_capital(self,new_capital):
        """ Increase portfolio capital for investment from an exteral account.

        Args:
        new_capital: amount of new capital to the portfolio account
        """
        self.initial_capital['value'] += new_capital
        # pending: what should it return? a message?
        return print(self.initial_capital)

    def withdraw_capital(self,remove_capital):
        """ Reduce portfolio capital for investment.

        Args:
        remove_capital: amount of capital to be withdrawn from the portfolio
            account
        """
        if remove_capital <= self.not_invested_capital['value']:
            self.initial_capital['value'] -= remove_capital
        else:
            print("ERROR: Not enough not invested capital to be remove.")
            print("Please reduce the quantity to be withdrawn or increase not invested capital")
        # pending: what should it return? a message?
        return print(self.not_invested_capital)

    def add_units(self,asset_id_dict,purchase_price_dict,units):
        """ Increase number of units of an asset already in the portfolio.

        Args:
        asset_id_dict: Dictionary containing at least one of the following
            keys: 'asset_id', 'symbol', 'name', used to find the asset.
        purchase_price_dict: Dictionary containing the 'value' and 'currency'
            (price), and 'datetime' of the purchase of the asset.
        units: number of units bought at purchase_price_dict

        Returns:
        Update the selected portfolio asset with the new number of units and 
        purchase price. In case the asset could not be found, it
        returns an error message.
        """
        # Buffer with messages to return
        output_message = []
        if not asset_id_dict:
            output_message.append = 'Empty search dictionary'
        elif not purchase_price_dict:
            output_message.append = 'Not purchase price given'
        elif units <= 0:
            output_message.append = 'Number of units lower or equal 0'
        else:
            asset_found = False
            for index, asset in enumerate(self.portfolio):
                asset_found = True
                for k in asset_id_dict:
                    if k not in asset:
                        # key no se encuentra en el asset
                        asset_found = False
                    elif asset_id_dict[k] != asset[k]:
                        # valor de la key no coincide
                        asset_found = False

                if asset_found:
                    # encontrado asset, paro bucle
                    break

            if asset_found:
                if purchase_price_dict['currency'] != (self.portfolio[index]
                        ['purchase_price']['currency']):
                    output_message.append = 'Wrong purchase price currency'
                elif purchase_price_dict.keys() != \
                        self.portfolio[index]['purchase_price'].keys():
                    output_message.append = ('Some incompatible key in the 
                            purchase dictionary')
                else:
                    # incremento unidades
                    self.portfolio[index]['units'] += units
                    # actualizo purchase_price
                    self.portfolio[index]['purchase_price'] = \
                            purchase_price_dict
                    output_message.append = 'Units added to the asset'
            else:
                output_message.append = 'Asset not found'

        return output_message

def get_xml_capital_value(tree,field_text):
    """Search for an capital entry (currency+value) in a xml tree and return a
    dictionary with the following keys: {'currency':(string),'value':(float)}

    Args:
        tree: ElementTree object
        field_text: string which the tag to find

    Returns:
        dictionary {'currency':(string),'value':(float)}
        or empty dictionary in case entry not found or not capital type
    """
    output_dict = {}
    element = tree.find(field_text)
    if element is not None and 'currency' in element.attrib.keys():
        output_dict['value'] = float(element.text)
        output_dict.update(element.attrib)
    return output_dict

def get_xml_performance_value(tree,field_text):
    """Search for an performance entry (units+value) in a xml tree and return a
    dictionary with the following keys: {'units':(string),'value':(float)}

    Args:
        tree: ElementTree object
        field_text: string which the tag to find

    Returns:
        dictionary {'units':(string),'value':(float)}
        or empty dictionary in case entry not found or not capital type
    """
    output_dict = {}
    element = tree.find(field_text)
    if element is not None and 'units' in element.attrib.keys():
        output_dict['value'] = float(element.text)
        output_dict.update(element.attrib)
    return output_dict

def get_xml_portfolio_element(element):
    """Given a portfolio element, it returns a portfolio dictionary with
    following structure:
    {
    'asset_id':(int),
    'name':(string),
    'market':(string),
    'symbol':(string),
    'currency':(string),
    'units':(int),
    'purchase_price':{'datetime':(datetime), 'value':(float)},
    'previous_close':{'datetime':(datetime), 'value':(float)},
    'maximum_close':{'datetime':(datetime), 'value':(float)},
    'minimum_close':{'datetime':(datetime), 'value':(float)},
    'stop_price':(float),
    'add_units_price':(float)
    }

    Args:
        element: ElementTree object with the portfolio childrens

    Returns:
        portfolio dictionary
    """
    output_dict = {'asset_id':1,'name':'','market':'','symbol':'',
            'currency':'','units':0,
            'purchase_price':{'datetime':'','value':0.0},
            'previous_close':{'datetime':'','value':0.0},
            'maximum_close':{'datetime':'','value':0.0},
            'minimum_close':{'datetime':'','value':0.0},
            'stop_price':0.0,'add_units_price':0.0}
    temp_dict = {}
    
    bSomeKeyMissing = False
    if element is not None:
        # asset_id
        child = element.attrib['id']
        if not child:
            output_dict['asset_id'] = int(child.attrib['id'])
        else:
            bSomeKeyMissing = True
        # name
        child = element.find('name')
        if not child:
            output_dict['name'] = child.text
        else:
            bSomeKeyMissing = True
        # market
        child = element.find('market')
        if not child:
            output_dict['market'] = child.text
        else:
            bSomeKeyMissing = True
        # symbol
        child = element.find('symbol')
        if not child:
            output_dict['symbol'] = child.text
        else:
            bSomeKeyMissing = True
        # currency
        child = element.find('currency')
        if not child:
            output_dict['currency'] = child.text
        else:
            bSomeKeyMissing = True
        # units
        child = element.find('units')
        if not child:
            output_dict['units'] = int(child.text)
        else:
            bSomeKeyMissing = True
        # purchase_price
        child = element.find('purchase_price')
        if not child and 'datetime' in child.attrib.keys():
            # PENDIENTE!!: poner tipo datetime 
            output_dict['purchase_price']['datetime'] = (
                    child.attrib['datetime'])
            output_dict['purchase_price']['value'] = float(child.text)
        else
            bSomeKeyMissing = True
        # previous_close
        child = element.find('previous_close')
        if not child and 'datetime' in child.attrib.keys():
            # PENDIENTE!!: poner tipo datetime 
            output_dict['previous_price']['datetime'] = (
                    child.attrib['datetime'])
            output_dict['previous_price']['value'] = float(child.text)
        else
            bSomeKeyMissing = True
        # maximum_close
        child = element.find('maximum_close')
        if not child and 'datetime' in child.attrib.keys():
            # PENDIENTE!!: poner tipo datetime 
            output_dict['maximum_price']['datetime'] = child.attrib['datetime']
            output_dict['maximum_price']['value'] = float(child.text)
        else
            bSomeKeyMissing = True
        # minimum_close
        child = element.find('minimum_close')
        if not child and 'datetime' in child.attrib.keys():
            # PENDIENTE!!: poner tipo datetime 
            output_dict['minimum_price']['datetime'] = child.attrib['datetime']
            output_dict['minimum_price']['value'] = float(child.text)
        else
            bSomeKeyMissing = True
        # stop_price
        child = element.find('stop_price')
        if not child:
            output_dict['stop_price'] = float(child.text)
        else:
            bSomeKeyMissing = True
        # add_units_price
        child = element.find('add_units_price')
        if not child:
            output_dict['stop_price'] = float(child.text)
        else:
            bSomeKeyMissing = True





        for key in output_dict.keys():
            if not element.find(key):
                # key not found, returns empty dictionary
                output_dict = {}
                break
            else:
    if element is not None:
        temp_dict['asset_id'] = int(element.attrib['id'])
         for child in element:
            if not child.attrib:
               output_dict[child.tag] = child.text
            else:
                output_dict[child.tag] = dict(value=child.text)
                output_dict[child.tag].update(child.attrib)
    return output_dict
