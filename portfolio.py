import xml.etree.ElementTree as ET

class Portfolio:
    
    file_name = 'PruebaPortfolio.xml'

    initial_capital = {}
    total_capital = {}
    invested_capital = {}
    not_invested_capital = {}
    performance = {}
    portfolio = []

    def __init__(self,file_name):
        self.file_name = file_name
        self.init_portfolio(file_name)

    @staticmethod
    def get_xml_float_value(tree,field_text):
        """Search for an element in a xml tree and return a dictionary with
        the text of the xml tag as a float with the key 'value'

        Args:
            tree: ElementTree object
            field_text: string which the text to find

        Returns:
            A dict with the key 'value' and all attributes of xml tag
        """
        output_dict = {}
        element = tree.find(field_text)
        if element is not None:
            output_dict['value'] = float(element.text)
            output_dict.update(element.attrib)
        return output_dict

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
        """ initial_capital """
        self.initial_capital = self.get_xml_float_value(tree,'initial_capital')
        """ total_capital """
        self.total_capital = self.get_xml_float_value(tree,'total_capital')
        """ invested_capital """
        self.invested_capital = self.get_xml_float_value(tree, \
                'invested_capital')
        """ not_invested_capital """
        self.not_invested_capital = self.get_xml_float_value(tree, \
                'not_invested_capital')
        """ performance """
        self.performance = self.get_xml_float_value(tree,'performance')
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
            keys: 'asset_id', 'Symbol', 'Name', used to find the asset.
        purchase_price_dict: Dictionary containing the 'value' and 'currency'
            (price), and 'datetime' of the purchase of the asset.
        units: number of units bought at purchase_price_dict

        Returns:
        Update the selected portfolio asset with the new number of units and 
        purchase price. In case the asset could not be found, it
        returns an error message.
        """
        if asset_id_dict and purchase_price and units > 0:
            for asset in self.portfolio:
                asset_found = True
                while k in asset_id_dict:
                    if k not in asset:
                        asset_found = False
                        output_message.append('{} key not found in portfolio keys'.format(k)')


                for k in asset_id_dict:
                    if k in asset and 
            
        for asset in self.portfolio:
            # find asset

        

