class FieldNode:
    """Utility functions for GraphQLResolveInfo"""

    def __init__(self, field_dict:dict) -> None:
        self.field_name = field_dict.get('name').get('value')
        self.sub_fields = []

        if field_dict.get('selection_set') == None: return
        
        for sub_field_dict in field_dict.get('selection_set').get('selections', []):
            self.sub_fields.append(FieldNode(sub_field_dict))
    

    def has_field(self, field:str) -> bool:
       """Verify wheter a field is selected or not"""

       return field in (self.sub_fields) 
    

    def has_fields(self, *fields:list[str]) -> bool:
        """Verify wheter a on field of a list of fields is selected or not"""

        for field in fields:
            if self.has_field(field): return True

        return False


    def get_query(self) -> str:
        """Get the query string"""

        sub_fields = ", ".join(map(str, self.sub_fields))
        sub_fields = f"({sub_fields})" if sub_fields else sub_fields

        return(f"{self.field_name}{sub_fields}")
    

    def __str__(self) -> str:
        return self.get_query()
    

    def __eq__(self, __o: object) -> bool:
        if (isinstance(__o, FieldNode)):
            return self.field_name == __o.field_name
    
        return self.field_name == str(__o)
    

def buildFieldNodeFromInfo(info) -> FieldNode:
    """Build field node from GraphQLResolveInfo"""
    if len(info.field_nodes) != 1: return None

    return FieldNode(info.field_nodes[0].to_dict())            