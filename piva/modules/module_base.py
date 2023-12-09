class ModuleBase:
    @staticmethod
    def get_module_name():
        return None

    @staticmethod
    def get_dependencies():
        return []

    def get_class_name(self):
        return self.__class__.__name__

    def process(self, *args, **kwargs):
        pass
