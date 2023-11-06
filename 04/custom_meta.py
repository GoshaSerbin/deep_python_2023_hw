class CustomMeta(type):
    def __new__(mcs, name, bases, classdict):
        custom_classdict = {}
        for k, v in classdict.items():
            if k.startswith("__") and k.endswith("__"):
                custom_classdict[k] = v
            else:
                custom_classdict["custom_" + k] = v
        classdict = custom_classdict
        cls = super().__new__(mcs, name, bases, classdict)
        return cls

    def __setattr__(cls, name, value):
        if not (name.startswith("__") and name.endswith("__")):
            name = "custom_" + name
        super().__setattr__(name, value)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        custom_dict = {}
        for k, v in instance.__dict__.items():
            if k.startswith("__") and k.endswith("__"):
                custom_dict[k] = v
            else:
                custom_dict["custom_" + k] = v
        instance.__dict__ = custom_dict

        def custom_setattr(self, name, value):
            if not (name.startswith("__") and name.endswith("__")):
                name = "custom_" + name
            super(self.__class__, self).__setattr__(name, value)

        cls.__setattr__ = custom_setattr

        return instance
