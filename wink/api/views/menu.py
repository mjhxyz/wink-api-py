from wink.models.menu import WinkMenu


class WinkMenuView:
    def __init__(self, menu: WinkMenu):
        self.id = menu.id
        self.code = menu.code
        self.name = menu.name
        self.type = menu.type
        self.weight = menu.weight
        self.parent_id = menu.parent_id
        self.setting = menu.setting
        self.status = menu.status
        self.children = []

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'type': self.type,
            'weight': self.weight,
            'parent_id': self.parent_id,
            'setting': self.setting,
            'status': self.status,
            'children': self.children,
        }
